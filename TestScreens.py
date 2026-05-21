from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.lang import Builder
from kivy.app import App

from KivyWidgets.KivyButtonBackend import KivyButton
from KivyWidgets.KivyBrickBackend import BrickWidget
from kivy.uix.screenmanager import ScreenManager, Screen

from views.mojePrzedmioty import MojePrzedmiotyScreen , SzczegolyPrzedmiotuScreen

import json
from kivy.event import EventDispatcher
from kivy.properties import StringProperty , NumericProperty

# 1. Upewnij się, że masz klasę danych (dziedziczącą po EventDispatcher, żeby UI reagowało na zmiany)
class SubjectData(EventDispatcher):
    title = StringProperty("")
    teacher = StringProperty("")
    note = StringProperty("")
    
    # NOWE POLA Z DOCELOWEGO EKRANU:
    status = StringProperty("Zaliczony")
    absences = NumericProperty(1)
    max_absences = NumericProperty(2)
    conditions = StringProperty("bleble")
    max_pluses = NumericProperty(10.0)
    
    def __init__(self, title, teacher, note, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.teacher = teacher
        self.note = note
# 2. Klasa udająca Twój kafelek (zawiera w sobie pole 'data')
class MockBrick:
    def __init__(self, data):
        self.data = data

# ==========================================
# 3. TWORZENIE OBIEKTU TESTOWEGO W PRAKTYCE
# ==========================================

# Tworzymy przykładowe dane przedmiotu
testowe_dane = SubjectData(
    title="Algebra Liniowa",
    teacher="prof. dr hab. Jan Kowalski",
    note="Pamiętać o powtórzeniu macierzy i wyznaczników przed kolokwium!"
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