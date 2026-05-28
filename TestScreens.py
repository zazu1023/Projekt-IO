from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.lang import Builder
from kivy.app import App

from KivyWidgets.KivyButtonBackend import KivyButton
from KivyWidgets.KivyBrickBackend import BrickWidget
from kivy.uix.screenmanager import ScreenManager, Screen

from views.mojePrzedmioty import MojePrzedmiotyScreen , SzczegolyPrzedmiotuScreen , SubjectData
from views.startKalendarz import StartKalendarz

import json
from kivy.event import EventDispatcher
from kivy.properties import StringProperty , NumericProperty




# Tworzymy przykładowe dane przedmiotu
testowe_dane = SubjectData(
    title="Algebra Liniowa",
    teacher="prof. dr hab. Jan Kowalski",
    note="Pamiętać o powtórzeniu macierzy i wyznaczników przed kolokwium!",
    max_absences = 5
)

# Pakujemy dane w "kafelek"



class TestApp(App):
    
    def build(self):
       
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

         self.change_screen('mySubjects' , selectedSubject=testowe_dane)
         return root_widget
      
    def translate(self, text:str):
        return self.translations[self.language].get(text)
    
    def change_screen(self, target_screen , **kwargs):
        if not self.sm.has_screen(target_screen):
         
            screens = {
                'mySubjects': {'class': MojePrzedmiotyScreen, 'kv': 'kv/mojePrzedmioty.kv'},
                'subjectDetails': {'class': SzczegolyPrzedmiotuScreen, 'kv': 'kv/szczegolyPrzedmiotu.kv'},
                'calendar' : {'class':StartKalendarz, 'kv': 'kv/calendar.kv'}
            }
            
            config = screens.get(target_screen)
            
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

    def get_subjects_from_db(self):
    
        return [
            SubjectData(title="Algebra", teacher="Jan Kowalski", status="completed" , note=""),
            SubjectData(title="ASD", teacher="JŚW", status="completed", note=""),
            SubjectData(title="Bazy Danych", teacher="Anna Nowak", status="completed", note="")
        ]
    
if __name__ == "__main__":
    TestApp().run()