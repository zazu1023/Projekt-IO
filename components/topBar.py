import json

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class TopBarButton(Button):
    pass


class TopBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.language = "pl"

        with open("translation.json", "r", encoding="utf-8") as file:
            self.translations = json.load(file)

    def translate(self, key):
        return self.translations[self.language][key]

    def change_language(self, button):
        if self.language == "pl":
            self.language = "en"
        else:
            self.language = "pl"

        self.ids.nearest_label.text = self.translate("nearest_text")
        self.ids.language_button.text = self.translate("language_button")

    def show_notifications(self):
        print("Kliknięto powiadomienia")