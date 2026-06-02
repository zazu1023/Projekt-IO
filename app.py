import json
import Widgets.notifications

from Database.database_sqllite import SqliteAppRepository

from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '600')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty

from datetime import datetime
from Widgets.countdown import CountdownWidget, CountdownStyle, KivyCountdownBackend

from tests.create_default_values import DatabaseStarter

from screenHandler import *

class StudentPlannerApp(App):

    language = StringProperty("pl")

    def __init__(self, repository, **kwargs):
        super().__init__(**kwargs)
        self.repo = repository

    def build(self):

        self.screens = SCREENS # wczytanie screenow z screenHandler

        with open('translation.json' , 'r' , encoding='utf-8') as file:
            data = json.load(file)
        
        self.translations = data

        Builder.load_file('Style/styles.kv')
        Builder.load_file('views/Kalendarz/calendar.kv')

        root_widget = Builder.load_file('views/main.kv')

        self.sesja_countdown = CountdownWidget(
            target_date=datetime(2026, 6, 22, 0, 0),
            backend=KivyCountdownBackend(),
            style=CountdownStyle(bg_color=(0, 0, 0, 0), text_color=(1, 1, 1, 1))
        )

        self.sm = root_widget.ids.sm
        self.change_screen(target_screen='mySubjects')
        return root_widget


    def translate(self, text:str, langtrigger ):
                return self.translations[self.language].get(text)

    def change_screen(self, target_screen , **kwargs):
        if not self.sm.has_screen(target_screen):
            
            
            
            config = self.screens.get(target_screen)
            
            if config:
                
                Builder.load_file(config['kv'])
                new_screen = config['class'](name=target_screen)
                self.sm.add_widget(new_screen)
            else:
                print(f"Error invaild scren name {target_screen}")
                return
            
        new_screen = self.sm.get_screen(target_screen)

        for klucz, wartosc in kwargs.items():
            setattr(new_screen, klucz, wartosc)

        self.sm.current = target_screen

    def change_language(self):
        if self.language == "pl":
            self.language = "en"
        else:
            self.language = "pl"

        print("Zmieniono język na:", self.language)


if __name__ == "__main__":

    # inicjalizacja bazy
    repo = SqliteAppRepository(db_connection=None)
    repo.init_db()
    
    # init_db()

    # 2. TYMCZASOWE WYPEŁNIENIE BAZY DO TESTÓW KALENDARZA
    # To rozwiązuje błąd FOREIGN KEY. Dodajemy przedmioty z ID 1, 2, 3
    # conn = get_connection()
    # conn.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (1, 'IO')")
    # conn.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (2, 'SK')")
    # conn.execute("INSERT OR IGNORE INTO subjects (id, name) VALUES (3, 'RPiS')")
    # conn.commit()
    # repo.get_db_connection().execute("Delete from subjects")

    # repo.add_subject(data={'title':'WDI' , 'teacher': "Rafal Kawa" , 'status': "atrisk"})

    DS = DatabaseStarter(repo)

    DS.remove_all_subjects()
    DS.add_test_subjects()

    StudentPlannerApp(repository=repo).run()