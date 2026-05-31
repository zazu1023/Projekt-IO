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
            raise e #

    return wrapper


class SqliteAppRepository(IAppRepository):
    def __init__(self , db_connection) -> None:
        self.conn = db_connection

   
    def get_db_connection(self):
        if self.conn is None:
            db_connection = sqlite3.connect(DB_NAME)
            db_connection.row_factory = sqlite3.Row
            db_connection.execute("PRAGMA foreign_keys = ON;")
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


    def get_all_subjects(self) -> list[dict]:
        pass


    def add_absence(self, subject_id: int, amount: int = 1):
        pass


    def add_subject(self, data:dict) -> None:
        pass


    def remove_subject(self, id:int) -> None:
        pass

    """
    Notes
    """


    def get_daily_note(self, id:int , date:str) -> dict:
        pass

    def set_daily_note(self, id:int , date:str) -> None:
        pass
