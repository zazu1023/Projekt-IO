from KivyWidgets.KivyButtonBackend import CustomButtonWidget
from Widgets.Button import ButtonStyle 
from KivyWidgets.KivyHelper import KivyHelper

from Widgets.Brick import CalendarBrickData
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty , StringProperty , BooleanProperty
from kivy.core.window import Window


     
class DashboardBrick( CustomButtonWidget, BoxLayout ):
    style = ObjectProperty()
    subject_obj = ObjectProperty(None)
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)

class BrickWidget(CustomButtonWidget, BoxLayout):
    info_text = StringProperty()
    title_text = StringProperty()
    has_note = BooleanProperty(False)
