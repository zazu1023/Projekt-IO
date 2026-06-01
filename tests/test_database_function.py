import sqlite3
import pytest
from Database.database_sqllite import SqliteAppRepository

@pytest.fixture
def db_repo():
# ==========================================
#   konfiguracja środowiska testowego
#   tworzy nowa, czysta baze danych w pamieci RAM przed kazdym testem
# ==========================================
    connection = sqlite3.connect(':memory:')
    connection.row_factory = sqlite3.Row
    # obluga kluczy obcych dla testow kaskadowego usuwania
    connection.execute("PRAGMA foreign_keys = ON;") 
    
    repo = SqliteAppRepository(connection)
    repo.init_db()
    
    yield repo
    
    connection.close()

# ==========================================
# TESTY INICJALIZACJI
# ==========================================

def test_init_db_creates_all_tables(db_repo):
    connection = db_repo.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row['name'] for row in cursor.fetchall()]
    
    assert 'subjects' in tables
    assert 'schedule' in tables
    assert 'daily_notes' in tables
    assert 'events' in tables
    assert 'app_settings' in tables

# ==========================================
# TESTY USTAWIEN (SETTINGS)
# ==========================================

def test_language_settings(db_repo):

    assert db_repo.get_language('dummy_arg') == 'pl'
    
    # zmiana jezyka
    db_repo.set_language('en')
    assert db_repo.get_language('dummy_arg') == 'en'

# ==========================================
# TESTY PRZEDMIOTOW (SUBJECTS)
# ==========================================

def test_add_and_get_subjects(db_repo):
    subject_data = {
        'title': 'Mathematics',
        'teacher': 'Dr. Smith',
        'status': 'inprogress',
        'conditions': 'Final exam 50%',
        'max_absences': 3,
        'max_pluses': 10.0
    }
    
    db_repo.add_subject(subject_data)
    fetched_subjects = db_repo.get_all_subjects()
    
    assert len(fetched_subjects) == 1
    assert fetched_subjects[0]['name'] == 'Mathematics'
    assert fetched_subjects[0]['teacher'] == 'Dr. Smith'
    assert fetched_subjects[0]['current_absences'] == 0

def test_update_subject(db_repo):
    db_repo.add_subject({'title': 'Physics'})
    subject_id = db_repo.get_all_subjects()[0]['id']
    
    update_data = {
        'title': 'Advanced Physics',
        'teacher': 'Prof. Johnson',
        'conditions': 'Project',
        'max_colloquium_pluses': 20.0,
        'note': 'Hard subject'
    }
    
    db_repo.update_subject(subject_id, update_data)
    updated_subject = db_repo.get_all_subjects()[0]
    
    assert updated_subject['name'] == 'Advanced Physics'
    assert updated_subject['note'] == 'Hard subject'
    assert updated_subject['max_colloquium_points'] == 20.0

def test_remove_subject(db_repo):
    db_repo.add_subject({'title': 'Chemistry'})
    db_repo.add_subject({'title': 'Biology'})
    
    subjects_before = db_repo.get_all_subjects()
    assert len(subjects_before) == 2
    
    subject_id_to_remove = subjects_before[0]['id']
    db_repo.remove_subject(subject_id_to_remove)
    
    subjects_after = db_repo.get_all_subjects()
    assert len(subjects_after) == 1
    assert subjects_after[0]['name'] == 'Biology'

def test_set_status(db_repo):
    db_repo.add_subject({'title': 'History', 'status': 'inprogress'})
    subject_id = db_repo.get_all_subjects()[0]['id']
    
    db_repo.set_status(subject_id, 'completed')
    
    updated_subject = db_repo.get_all_subjects()[0]
    assert updated_subject['status'] == 'completed'

# ==========================================
# TESTY NIEOBECNOŚCI (LOGIKA BIZNESOWA)
# ==========================================

def test_add_absence_logic(db_repo):
    db_repo.add_subject({'title': 'Art'})
    subject_id = db_repo.get_all_subjects()[0]['id']
    
    # didaje 2 nieobecnosci
    current = db_repo.add_absence(subject_id, 2)
    assert current == 2
    
    # odejmuje 1 nieobecnosc
    current = db_repo.add_absence(subject_id, -1)
    assert current == 1
    
    # odejmuje 5 nieobecnosci - system powinien zatrzymac sie na 0 (MAX(0, ...))
    current = db_repo.add_absence(subject_id, -5)
    assert current == 0

# ==========================================
# TESTY NOTATEK DZIENNYCH (DAILY NOTES)
# ==========================================

def test_set_and_get_daily_note(db_repo):
    db_repo.add_subject({'title': 'Programming'})
    subject_id = db_repo.get_all_subjects()[0]['id']
    test_date = '2026-06-01'
    
    # tworzymy nowa notatke
    db_repo.set_daily_note(subject_id, test_date, 'Learn Python decorators')
    note_content = db_repo.get_daily_note(subject_id, test_date)
    assert note_content == 'Learn Python decorators'
    
    # testujemy mechanizm nadpisywania
    db_repo.set_daily_note(subject_id, test_date, 'Updated note content')
    updated_content = db_repo.get_daily_note(subject_id, test_date)
    assert updated_content == 'Updated note content'

def test_get_nonexistent_daily_note_returns_empty_string(db_repo):
    db_repo.add_subject({'title': 'Database Systems'})
    subject_id = db_repo.get_all_subjects()[0]['id']
    
    note_content = db_repo.get_daily_note(subject_id, '2099-01-01')
    assert note_content == ""

def test_add_subject_minimum_data(db_repo):
    db_repo.add_subject({'title': 'Matematyka'})

    subject = db_repo.get_all_subjects()[0]

    assert subject['name'] == 'Matematyka'
    assert subject['teacher'] == ''
    assert subject['status'] == 'inprogress'
    assert subject['current_absences'] == 0


def test_add_multiple_subjects(db_repo):
    for i in range(10):
        db_repo.add_subject({'title': f'Przedmiot {i}'})

    subjects = db_repo.get_all_subjects()

    assert len(subjects) == 10


def test_update_nonexistent_subject(db_repo):
    db_repo.update_subject(9999,{'title': 'Nieistniejący'})

    assert db_repo.get_all_subjects() == []


def test_remove_nonexistent_subject(db_repo):
    db_repo.remove_subject(9999)

    assert db_repo.get_all_subjects() == []


def test_remove_all_subjects(db_repo):
    db_repo.add_subject({'title': 'A'})
    db_repo.add_subject({'title': 'B'})
    db_repo.add_subject({'title': 'C'})

    assert len(db_repo.get_all_subjects()) == 3

    db_repo.remove_all_subjects()

    assert db_repo.get_all_subjects() == []


def test_absences_cannot_go_below_zero(db_repo):
    db_repo.add_subject({'title': 'Matma'})
    subject_id = db_repo.get_all_subjects()[0]['id']

    current = db_repo.add_absence(subject_id, -999)

    assert current == 0


def test_add_absence_nonexistent_subject(db_repo):
    current = db_repo.add_absence(9999, 1)

    assert current == 0


def test_large_absence_increment(db_repo):
    db_repo.add_subject({'title': 'Historia'})
    subject_id = db_repo.get_all_subjects()[0]['id']

    current = db_repo.add_absence(subject_id, 1000)

    assert current == 1000


def test_multiple_status_changes(db_repo):
    db_repo.add_subject({'title': 'Matma'})
    subject_id = db_repo.get_all_subjects()[0]['id']

    db_repo.set_status(subject_id, 'atrisk')
    db_repo.set_status(subject_id, 'failed')
    db_repo.set_status(subject_id, 'completed')

    subject = db_repo.get_all_subjects()[0]

    assert subject['status'] == 'completed'


def test_set_status_nonexistent_subject(db_repo):
    db_repo.set_status(9999, 'completed')

    assert db_repo.get_all_subjects() == []


def test_set_empty_daily_note(db_repo):
    db_repo.add_subject({'title': 'Programowanie'})
    subject_id = db_repo.get_all_subjects()[0]['id']

    db_repo.set_daily_note(subject_id,'2026-06-01','')

    note = db_repo.get_daily_note(subject_id,'2026-06-01')

    assert note == ''


def test_very_long_daily_note(db_repo):
    db_repo.add_subject({'title': 'Programowanie'})
    subject_id = db_repo.get_all_subjects()[0]['id']

    long_note = "A" * 10000

    db_repo.set_daily_note(subject_id,'2026-06-01',long_note)

    note = db_repo.get_daily_note(subject_id,'2026-06-01')

    assert note == long_note


def test_multiple_daily_notes_for_same_subject(db_repo):
    db_repo.add_subject({'title': 'Programowanie'})
    subject_id = db_repo.get_all_subjects()[0]['id']

    db_repo.set_daily_note(subject_id,'2026-06-01','Notatka 1')

    db_repo.set_daily_note(subject_id,'2026-06-02','Notatka 2')

    assert db_repo.get_daily_note(subject_id,'2026-06-01') == 'Notatka 1'

    assert db_repo.get_daily_note(subject_id,'2026-06-02') == 'Notatka 2'


def test_polish_characters(db_repo):
    db_repo.add_subject({'title': 'Programowanie Obiektowe','teacher': 'Łukasz Żółć'})

    subject = db_repo.get_all_subjects()[0]

    assert subject['teacher'] == 'Łukasz Żółć'


def test_unicode_subject_name(db_repo):
    db_repo.add_subject({'title': '📚 Matematyka 🚀'})

    subject = db_repo.get_all_subjects()[0]

    assert subject['name'] == '📚 Matematyka 🚀'


def test_default_language_exists(db_repo):
    assert db_repo.get_language(None) == 'pl'


def test_language_multiple_changes(db_repo):
    db_repo.set_language('en')
    db_repo.set_language('de')
    db_repo.set_language('pl')

    assert db_repo.get_language(None) == 'pl'


def test_cascade_delete_daily_notes(db_repo):
    db_repo.add_subject({'title': 'Programowanie'})

    subject_id = db_repo.get_all_subjects()[0]['id']

    db_repo.set_daily_note(subject_id,'2026-06-01','Testowa notatka')

    db_repo.remove_subject(subject_id)

    connection = db_repo.get_db_connection()

    count = connection.execute("SELECT COUNT(*) AS cnt FROM daily_notes").fetchone()['cnt']
    assert count == 0


def test_subject_ids_are_unique(db_repo):
    db_repo.add_subject({'title': 'A'})
    db_repo.add_subject({'title': 'B'})

    subjects = db_repo.get_all_subjects()

    ids = [s['id'] for s in subjects]
    assert len(ids) == len(set(ids))


def test_empty_teacher_is_allowed(db_repo):
    db_repo.add_subject({'title': 'Matematyka','teacher': ''})

    subject = db_repo.get_all_subjects()[0]
    assert subject['teacher'] == ''


def test_empty_conditions_are_allowed(db_repo):
    db_repo.add_subject({'title': 'Matematyka', 'conditions': ''})

    subject = db_repo.get_all_subjects()[0]
    assert subject['grading_rules'] == ''