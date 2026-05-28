from app import StudentPlannerApp
from database import init_db, get_connection # Importujemy narzędzia z bazy

init_db()

# 2. TYMCZASOWE WYPEŁNIENIE BAZY DO TESTÓW KALENDARZA
# To rozwiązuje błąd FOREIGN KEY. Dodajemy przedmioty z ID 1, 2, 3
conn = get_connection()
conn.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (1, 'IO')")
conn.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (2, 'SK')")
conn.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (3, 'RPiS')")
conn.commit()

StudentPlannerApp().run()