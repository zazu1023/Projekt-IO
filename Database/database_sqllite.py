import sqlite3

from Database.database_interface import IAppRepository


DB_NAME = "student_planner.db" 


from functools import wraps

def db_transaction(func):
    """
    Dekorator bazy danych. Automatycznie zatwierdza (commit) zmiany po funkcji 
    i wycofuje je (rollback) w przypadku błędu.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
  
        conn = self.get_db_connection()

        try:
        
            result = func(self, *args, **kwargs)
            conn.commit()

            return result
        except sqlite3.Error as e:
           
            conn.rollback()
            print(f"Błąd SQL w metodzie {func.__name__}: {e}")
            # raise e #

    return wrapper


class SqliteAppRepository(IAppRepository):
    def __init__(self , db_connection) -> None:
        self.conn = db_connection

    def init_db(self) -> None:
       
        cursor = self.get_db_connection().cursor()

        # TABELA 1: PRZEDMIOTY (glowna konfiguracja + sledzenie postepow)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                teacher TEXT,
                status TEXT DEFAULT 'inprogress' CHECK(status IN ('inprogress', 'completed', 'atrisk', 'failed')),
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

        self.get_db_connection().commit()
        
        print("Baza danych gotowa do pracy!")
   

    def get_db_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(DB_NAME)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON;")
        return self.conn
    
    """
    Settings
    """

    @db_transaction
    def set_language(self,lang) -> None:
        self.get_db_connection().execute(
            "INSERT OR REPLACE INTO app_settings (key, value) VALUES ('language', ?)", 
            (lang,)
        )

    @db_transaction
    def get_language(self,lang) -> str:
        row = self.get_db_connection().execute("SELECT value FROM app_settings WHERE key = 'language'").fetchone()
        return row['value'] if row else 'pl'

    """
    Subjects
    """

    @db_transaction
    def get_all_subjects(self) -> list[dict]:
        rows = self.get_db_connection().execute("SELECT * FROM subjects").fetchall()
        return [dict(row) for row in rows]


    @db_transaction
    def add_absence(self, subject_id: int, amount: int = 1) -> int:
        row = self.get_db_connection().execute(
            '''
            UPDATE subjects 
            SET current_absences = MAX(0, current_absences + ?)
            WHERE id = ?
            RETURNING current_absences
            ''', 
            (amount, subject_id)
        ).fetchone()
  
        return row['current_absences'] if row else 0

    @db_transaction
    def set_status(self, subject_id:int , new_status:str):
        self.get_db_connection().execute(
            '''
            UPDATE subjects 
            SET status = ?
            WHERE id = ?
            ''', 
            (new_status, subject_id)
        )
    

    @db_transaction
    def add_subject(self, data:dict) -> None:
        name = data.get('title')
        teacher = data.get('teacher', '')
        status = data.get('status', 'inprogress')
        grading_rules = data.get('conditions', '')
        max_absences = data.get('max_absences', 0)
        max_activity_points = data.get('max_pluses', 0.0)

        self.get_db_connection().execute(
            '''
            INSERT INTO subjects (
                name, teacher, status, grading_rules, max_absences, max_activity_points
            ) VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (name, teacher, status, grading_rules, max_absences, max_activity_points)
        )

    @db_transaction
    def remove_subject(self, subject_id:int) -> None:
        self.get_db_connection().execute(
            "DELETE FROM subjects WHERE id = ?", 
            (subject_id,)
        )

    @db_transaction
    def remove_all_subjects(self) -> None:
        self.get_db_connection().execute(
            "DELETE FROM subjects"
            )
        
        
        

    """
    Notes
    """

    @db_transaction
    def get_daily_note(self, subject_id:int , date:str) -> dict:

        row = self.get_db_connection().execute(
            '''
            SELECT content FROM daily_notes 
            WHERE subject_id = ? AND note_date = ?
            ''', 
            (subject_id, date)
        ).fetchone()
          
        return row['content'] if row else ""
    
    @db_transaction
    def set_daily_note(self, subject_id:int , date:str, content:str) -> None:
        self.get_db_connection().execute(
            '''
            INSERT INTO daily_notes (subject_id, note_date, content)
            VALUES (?, ?, ?)
            ON CONFLICT(subject_id, note_date) DO UPDATE SET content = excluded.content
            ''',
            (subject_id, date, content)
        )
