from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.lang import Builder
from kivy.app import App

from KivyWidgets.KivyButtonBackend import KivyButton
from KivyWidgets.KivyBrickBackend import BrickWidget

import json

class TestApp(App):
    
    def build(self):
       
       with open('translation.json' , 'r') as file:
            data = json.load(file)
       
       self.translations = data
       self.language = 'pl'
       Builder.load_file('Style/styles.kv')
    #    root_widget = Builder.load_file('Style/test_screens.kv')
       root_widget = Builder.load_file('kv/mojePrzedmioty.kv')
       return root_widget
       
    def translate(self, text:str):
        return self.translations[self.language].get(text)



if __name__ == "__main__":
    TestApp().run()