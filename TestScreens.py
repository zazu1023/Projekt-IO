from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.lang import Builder
from kivy.app import App

from KivyWidgets.KivyButtonBackend import KivyButton
from KivyWidgets.KivyBrickBackend import BrickWidget
from kivy.uix.screenmanager import ScreenManager, Screen

from views.mojePrzedmioty import MojePrzedmiotyScreen , SzczegolyPrzedmiotuScreen , SubjectData

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
         Builder.load_file('kv/mojePrzedmioty.kv')
         Builder.load_file('kv/szczegolyPrzedmiotu.kv')

         self.sm = ScreenManager()

        #  screen_mojePrzedmioty = MojePrzedmiotyScreen(name='moje_przedmioty_screen')
         screen_mojePrzedmioty = SzczegolyPrzedmiotuScreen(name='moje_przedmioty_screen')
         screen_mojePrzedmioty.selectedSubject = testowe_dane
         self.sm.add_widget(screen_mojePrzedmioty)
         return self.sm
      
    def translate(self, text:str):
        return self.translations[self.language].get(text)
    
    def change_screen(self, target_screen):
        # logika ladowania by oszczedzic czas i pamiec
        # wczytuj pojedynczo ekrany, tylko wtedy gdy sa konieczne
        if not self.sm.has_screen(target_screen):

            screens = {
                'mySubjects': MojePrzedmiotyScreen,
                'subjectDetails': SzczegolyPrzedmiotuScreen,
            }
            
            screen = screens.get(target_screen)
            
            if screen:
                new_screen = screen(name=target_screen)
                self.sm.add_widget(new_screen)
            else:
                print(f"Error invaild scren name {target_screen}")
                return

        self.sm.current = target_screen
        def open_details(self, clicked_brick_logic):
            if not self.sm.has_screen('subjectDetails'):
                self.sm.add_widget(SzczegolyPrzedmiotuScreen(name='subjectDetails'))
      
            ekran_detali = self.sm.get_screen('subjectDetails')

            ekran_detali.selectedSubject = clicked_brick_logic

            self.sm.current = 'subjectDetails'

if __name__ == "__main__":
    TestApp().run()