import sqlite3
import pytest
import re
import database as db

# ==============================================================
# KONFIGURACJA ŚRODOWISKA TESTOWEGO (FIXTURES)
# ==============================================================

@pytest.fixture(autouse=True)
def isolate_database(monkeypatch):
    """
    izolacja bazy danych w pamieci RAM przed kazdym testem
    """
    monkeypatch.setattr(db, 'DB_NAME', ':memory:')
    monkeypatch.setattr(db, 'db_connection', None)
    db.init_db()
    yield
    db.close_connection()

# ==============================================================
# TESTY INTEGRACYJNE BAZY DANYCH
# ==============================================================

def test_tables_creation():
    conn = db.get_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    table_names = [row['name'] for row in tables]
    
    assert 'subjects' in table_names
    assert 'schedule' in table_names
    assert 'daily_notes' in table_names
    assert 'events' in table_names
    assert 'app_settings' in table_names

def test_language_settings():
    assert db.get_language() == 'pl'
    db.set_language('en')
    assert db.get_language() == 'en'

def test_get_all_subjects():
    conn = db.get_connection()
    conn.execute("INSERT INTO subjects (name) VALUES ('Physics')")
    conn.execute("INSERT INTO subjects (name) VALUES ('Computer Science')")
    conn.commit()
    
    fetched_subjects = db.get_all_subjects()
    assert len(fetched_subjects) == 2
    assert fetched_subjects[0]['name'] == 'Physics'
    assert fetched_subjects[1]['name'] == 'Computer Science'


# --- ANALIZA WARTOŚCI GRANICZNYCH: DODAWANIE NIEOBECNOŚCI ---
def test_add_and_subtract_absences():
    conn = db.get_connection()
    conn.execute("INSERT INTO subjects (name) VALUES ('Mathematics')")
    conn.commit()
    
    subject_id = conn.execute("SELECT id FROM subjects WHERE name='Mathematics'").fetchone()['id']
    
    # symulacja: użytkownik klika PLUS dwa razy (+2)
    db.add_absence(subject_id, 2)
    result = conn.execute("SELECT current_absences FROM subjects WHERE id=?", (subject_id,)).fetchone()
    assert result['current_absences'] == 2
    
    # symulacja: użytkownik klika MINUS raz (-1), oczekujemy wyniku 1
    db.add_absence(subject_id, -1)
    result = conn.execute("SELECT current_absences FROM subjects WHERE id=?", (subject_id,)).fetchone()
    assert result['current_absences'] == 1
    
    # symulacja błędu: użytkownik klika MINUS pięć razy (-5), mimo że ma tylko 1 nieobecność
    db.add_absence(subject_id, -5)
    
    # oczekujemy, że system zatrzyma się na 0
    result = conn.execute("SELECT current_absences FROM subjects WHERE id=?", (subject_id,)).fetchone()
    assert result['current_absences'] == 0


# ==============================================================
# TESTY JEDNOSTKOWE WALIDACJI (KLASY RÓWNOWAŻNOŚCI I GRANICE)
# ==============================================================

# --- ANALIZA WARTOŚCI GRANICZNYCH: WALIDACJA DATY (YYYY-MM-DD) ---
@pytest.mark.parametrize("test_date, is_valid", [
    # klasa wartości poprawnych (wewnątrz granic)
    ("2026-05-28", True),
    ("2000-01-01", True),
    
    # wartości graniczne i błędy strukturalne (tuż poza krawędzią)
    ("2026-05-32", False),
    ("2026-13-10", False),
    ("2026-00-15", False),
    ("2026-05-00", False),
    
    # skrajne wartości niepoprawne (ujemne / za długie / zły format)
    ("-026-05-10", False),
    ("20261-05-10", False),
    ("abc-de-fg", False),
    ("", False),
])
def test_date_regex_boundaries(test_date, is_valid):

    date_pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    result = re.match(date_pattern, test_date)
    
    if is_valid:
        assert result is not None
    else:
        assert result is None


# --- ANALIZA WARTOŚCI GRANICZNYCH: WALIDACJA GODZINY (HH:MM) ---
@pytest.mark.parametrize("test_time, is_valid", [
    # klasa wartości poprawnych (wewnątrz i na krawędziach)
    ("14:30", True),
    ("00:00", True),
    ("23:59", True),
    
    # wartości tuż poza krawędzią (graniczne niepoprawne)
    ("24:00", False),
    ("23:60", False),
    ("12:61", False),
    ("25:00", False),
    ("00:60", False),
    ("08:60", False),
    
    # skrajne wartości niepoprawne (ujemne / ucięte)
    ("-1:30", False),
    ("14:-5", False),
    ("9:05", False),
    ("14:3", False),
    ("23:59:59", False),
    ("01:01:01", False),
])
def test_time_regex_boundaries(test_time, is_valid):
    time_pattern = r"^([01]\d|2[0-3]):([0-5]\d)$"
    result = re.match(time_pattern, test_time)
        
    if is_valid:
        assert result is not None
    else:
        assert result is None
        
# ==============================================================
# TESTY USUWANIA KASKADOWEGO I BRAKU MOZLIWOSCI DODANIA DWOCH NOTATEK DO JEDNEGO PRZEDMIOTU JEDNEGO DNIA
# ==============================================================

def test_foreign_key_cascade_delete():
    conn = db.get_connection()
    
    # tworzymy przedmiot
    conn.execute("INSERT INTO subjects (name) VALUES ('Physics')")
    conn.commit()
    subject_id = conn.execute("SELECT id FROM subjects WHERE name='Physics'").fetchone()['id']
    
    # dodajemy do niego wydarzenie i notatkę
    conn.execute("INSERT INTO events (subject_id, type, title) VALUES (?, ?, ?)", (subject_id, 'Exam', 'Final'))
    conn.execute("INSERT INTO daily_notes (subject_id, note_date, content) VALUES (?, ?, ?)", (subject_id, '2026-05-29', 'Study chapter 1'))
    conn.commit()
    
    # usuwamy SAM przedmiot
    conn.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
    conn.commit()
    
    # sprawdzamy, czy baza kaskadowo usunęła powiązane dane (powinno być 0)
    event_count = conn.execute("SELECT COUNT(*) as count FROM events").fetchone()['count']
    note_count = conn.execute("SELECT COUNT(*) as count FROM daily_notes").fetchone()['count']
    
    assert event_count == 0
    assert note_count == 0

def test_unique_daily_note_constraint():
    conn = db.get_connection()
    
    conn.execute("INSERT INTO subjects (name) VALUES ('Chemistry')")
    conn.commit()
    subject_id = conn.execute("SELECT id FROM subjects WHERE name='Chemistry'").fetchone()['id']
    
    # dodajemy pierwszą notatkę (powinno przejść)
    conn.execute("INSERT INTO daily_notes (subject_id, note_date, content) VALUES (?, ?, ?)", (subject_id, '2026-05-29', 'First note'))
    conn.commit()
    
    # próbujemy dodać drugą notatkę w tym samym dniu dla tego samego przedmiotu
    # oczekujemy, że baza danych zablokuje tę operację błędem IntegrityError
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO daily_notes (subject_id, note_date, content) VALUES (?, ?, ?)", (subject_id, '2026-05-29', 'Second note'))
        conn.commit()