from KivyWidgets.KivyButtonBackend import CustomButtonWidget
from Widgets.Button import ButtonStyle 
from KivyWidgets.KivyHelper import KivyHelper

from Widgets.Brick import BrickBackend , CalendarBrickData
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty , StringProperty , BooleanProperty
from kivy.core.window import Window

class BrickWidget( CustomButtonWidget, BoxLayout):
   
      info_text = StringProperty()
      title_text = StringProperty()
      has_note = BooleanProperty(False)
     
     
class KivyBrickBackend(KivyHelper , BrickBackend):
  

    def __init__(self, parent=None):
        self.parent = parent
        self.widget = None
        self._on_enter = None
        self._on_leave = None

    def create(self, data: CalendarBrickData, style: ButtonStyle, on_click: callable):

        self.widget = BrickWidget(text=data.title)
        self.widget.style = style
        self.widget.has_note = data.has_note
        self.widget.bind(on_release=lambda instance: on_click())
        self.bind_hover()
        return self.widget
    
    

    def bind_hover(self ,on_enter: callable, on_leave: callable):
        pass
  