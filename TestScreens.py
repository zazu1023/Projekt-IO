from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.lang import Builder
from kivy.app import App

from Button import CustomButtonWidget
from Brick import BrickWidget

class TestApp(App):
    def build(self):
       
       Builder.load_file('styles.kv')
       root_widget = Builder.load_file('test_screens.kv')

       return root_widget




if __name__ == "__main__":
    TestApp().run()