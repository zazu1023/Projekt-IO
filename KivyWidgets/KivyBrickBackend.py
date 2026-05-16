from KivyWidgets.KivyButtonBackend import KivyButton
from Widgets.Button import ButtonStyle 
from KivyWidgets.KivyHelper import KivyHelper

from Widgets.Brick import BrickBackend , CalendarBrickData


from kivy.properties import ObjectProperty

class BrickWidget(KivyButton):
      style = ObjectProperty(None)

class KivyBrickBackend(KivyHelper , BrickBackend):
  

    def __init__(self, parent=None):
        self.parent = parent
        self.widget = None

    def create_brick(self, data: CalendarBrickData, style: ButtonStyle, on_click: callable):

        self.widget = BrickWidget(text=data.title)
        self.widget.style = style
        self.widget.bind(on_release=lambda instance: on_click())

        return self.widget