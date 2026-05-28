import json

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager

import Style.stylesMain as styles

from screenHandler import ScreenHandler

class StudentPlannerApp(App):


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

        self.change_screen('mySubjects')
        return root_widget
        # Builder.load_file("Style/styles.kv")
        # Builder.load_file("kv/topbar.kv")
        # Builder.load_file("kv/sidebar.kv")
        # Builder.load_file("kv/calendar.kv")
        # Builder.load_file("kv/home.kv")
        # Builder.load_file("kv/rightPanel.kv")

        # screen_manager = ScreenManager()
        # screen_manager.add_widget(StartKalendarz(name="start"))


    def translate(self, key):
        return ScreenHandler.translate(key)
    
    def change_screen(self, target_screen , **kwargs):
        ScreenHandler.change_screen(target_screen , **kwargs)

    def change_language(self):
        if self.language == "pl":
            self.language = "en"
        else:
            self.language = "pl"

        print("Zmieniono język na:", self.language)