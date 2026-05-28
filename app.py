import json
from database import init_db, get_connection


from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')



from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager

import Style.stylesMain as styles

from screenHandler import *

class StudentPlannerApp(App):


    def build(self):

        self.screens = SCREENS # wczytanie screenow z screenHandler

        with open('translation.json' , 'r' , encoding='utf-8') as file:
            data = json.load(file)
        
        self.translations = data
        self.language = 'pl'

        Builder.load_file('Style/styles.kv')

        root_widget = Builder.load_file('Style/main.kv')

        self.sm = root_widget.ids.sm

        #  Builder.load_file('kv/mojePrzedmioty.kv')
        #  Builder.load_file('kv/szczegolyPrzedmiotu.kv')


        #  screen_mojePrzedmioty = MojePrzedmiotyScreen(name='moje_przedmioty_screen')

        self.change_screen(target_screen='mySubjects')
        return root_widget
        # Builder.load_file("Style/styles.kv")
        # Builder.load_file("kv/topbar.kv")
        # Builder.load_file("kv/sidebar.kv")
        # Builder.load_file("kv/calendar.kv")
        # Builder.load_file("kv/home.kv")
        # Builder.load_file("kv/rightPanel.kv")

        # screen_manager = ScreenManager()
        # screen_manager.add_widget(StartKalendarz(name="start"))


    def translate(self, text:str):
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
    
    def get_subjects_from_db(self):
    
        return [
            SubjectData(title="Algebra", teacher="Jan Kowalski", status="completed" , note=""),
            SubjectData(title="ASD", teacher="JŚW", status="completed", note=""),
            SubjectData(title="Bazy Danych", teacher="Anna Nowak", status="completed", note="")
        ]
    


if __name__ == "__main__":
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