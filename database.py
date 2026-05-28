import sqlite3

DB_NAME = "student_planner.db" # zmienna globalna trzymajaca jedno otwarte polaczenie, rozwiazuje problem z zacinaniem sie aplikacji przy czestym odpytywaniu bazy
db_connection = None 

def get_connection(): # zwraca aktywne polaczenie, jesli nie istnieje, tworzy je i konfiguruje raz
    global db_connection
    if db_connection is None:
        db_connection = sqlite3.connect(DB_NAME)
        db_connection.row_factory = sqlite3.Row
        db_connection.execute("PRAGMA foreign_keys = ON;")
    return db_connection

def close_connection():# te funkcję wywolywac dopiero przy zamykaniu calej aplikacji
    global db_connection
    if db_connection:
        db_connection.close()
        db_connection = None

def init_db(): # inicjalizuje strukture bazy danych
    conn = get_connection()
    cursor = conn.cursor()

    # TABELA 1: PRZEDMIOTY (glowna konfiguracja + sledzenie postepow)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            teacher TEXT,
            status TEXT DEFAULT 'W trakcie', 
            grading_rules TEXT,              
            max_absences INTEGER DEFAULT 0,
            current_absences INTEGER DEFAULT 0,  -- sledzenie biezacych nieobecnosci
            max_activity_points REAL DEFAULT 0,
            current_activity_points REAL DEFAULT 0, -- aktualnie zdobyte punkty z aktywnosci
            max_colloquium_points REAL DEFAULT 0,
            current_colloquium_points REAL DEFAULT 0, -- aktualnie zdobyte punkty z kolokwiow
            term_start TEXT,                 
            term_end TEXT                    
        )
    ''')

    # TABELA 2: HARMONOGRAM
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            day_of_week INTEGER, -- w INTEGER (0=Pon, 6=Niedz)
            start_time TEXT,                 
            duration_minutes INTEGER, -- czas trwania zajec
            FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
        )
    ''')

    # TABELA 3: NOTATKI
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            note_date TEXT NOT NULL,         
            content TEXT,
            UNIQUE(subject_id, note_date), -- brak mozliwosci stworzenia dwoch roznych notatek dla tego samego przedmiotu w tym samym dniu
            FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
        )
    ''')

    # TABELA 4: WYDARZENIA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            type TEXT,                       
            title TEXT,
            date_time TEXT,                  
            FOREIGN KEY (subject_id) REFERENCES subjects (id) ON DELETE CASCADE
        )
    ''')

    # TABELA 5: USTAWIENIA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO app_settings (key, value) VALUES ('language', 'pl')")

    conn.commit()
    
    # po utworzeniu tabel nalezy uruchomic weryfikacje struktury
    run_migrations()
    print("Baza danych gotowa do pracy!")

def run_migrations(): # bezpiecznie aktualizuje plik bazy, jesli dodamy nowe kolumny w przyszlosci
    conn = get_connection()
    cursor = conn.cursor()

    # lista nowych kolumn do potencjalnego dodania
    new_columns = [
        ("current_absences", "INTEGER DEFAULT 0"),
        ("current_activity_points", "REAL DEFAULT 0"),
        ("current_colloquium_points", "REAL DEFAULT 0")
    ]

    for column_name, column_type in new_columns:
        try: # probuje dokleic kolumne do istniejacej tabeli
            cursor.execute(f"ALTER TABLE subjects ADD COLUMN {column_name} {column_type}")
        except sqlite3.OperationalError: # blad oznacza, ze kolumna juz tam jest, ignoruje to
            pass
            
    conn.commit()


# FUNKCJE

def get_all_subjects():
    conn = get_connection()
    return conn.execute("SELECT * FROM subjects").fetchall()

def add_absence(subject_id, amount=1): #licznik, ktory dopisuje nieobecnosci do przedmiotu w bazie danych
    conn = get_connection()
    conn.execute('''
        UPDATE subjects 
        SET current_absences = current_absences + ? 
        WHERE id = ?
    ''', (amount, subject_id))
    conn.commit()

def set_language(lang): #funkcja sprawia, ze preferencje użytkownika nie znikaja po zamknieciu okna programu
    conn = get_connection()
    conn.execute("INSERT OR REPLACE INTO app_settings (key, value) VALUES ('language', ?)", (lang,))
    conn.commit()

def get_language():
    conn = get_connection()
    row = conn.execute("SELECT value FROM app_settings WHERE key = 'language'").fetchone()
    return row['value'] if row else 'pl'

def save_daily_note(subject_id, note_date, content):
    conn = get_connection()
    conn.execute('''
        INSERT INTO daily_notes (subject_id, note_date, content)
        VALUES (?, ?, ?)
        ON CONFLICT(subject_id, note_date) DO UPDATE SET content = excluded.content
    ''', (subject_id, note_date, content))
    conn.commit()

def get_daily_note(subject_id, note_date):
    conn = get_connection()
    row = conn.execute('''
        SELECT content FROM daily_notes 
        WHERE subject_id = ? AND note_date = ?
    ''', (subject_id, note_date)).fetchone()
    
    return row['content'] if row else ""

if __name__ == "__main__":
    init_db()
    # close_connection() zawsze na koniec dzialania programu