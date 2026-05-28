import json

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager

import Style.stylesMain as styles

from views.startKalendarz import StartKalendarz
from components.topBar import TopBar
from components.sideBar import SideBar
from components.calendarWidget import CalendarWidget

from kivy.core.window import Window
Window.maximize()


class StudentPlannerApp(App):
    language = StringProperty("pl")

    def build(self):
        self.styles = styles

        with open("translation.json", "r", encoding="utf-8") as file:
            self.translations = json.load(file)

        Builder.load_file("Style/styles.kv")
        Builder.load_file("kv/topbar.kv")
        Builder.load_file("kv/sidebar.kv")
        Builder.load_file("kv/calendar.kv")
        Builder.load_file("kv/home.kv")

        screen_manager = ScreenManager()
        screen_manager.add_widget(StartKalendarz(name="start"))

        return screen_manager

    def translate(self, key):
        return self.translations[self.language][key]

    def change_language(self):
        if self.language == "pl":
            self.language = "en"
        else:
            self.language = "pl"

        print("Zmieniono język na:", self.language)