from KivyWidgets.KivyButtonBackend import CustomButtonWidget
from Widgets.Button import ButtonStyle 

from Widgets.Brick import CalendarBrickData
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty , StringProperty , BooleanProperty
from kivy.core.window import Window

class DashboardBrick2( CustomButtonWidget, BoxLayout ):
    subject_obj = ObjectProperty(None)
     
class DashboardBrick( CustomButtonWidget, BoxLayout ):
    subject_obj = ObjectProperty(None)

class BrickWidget(CustomButtonWidget, BoxLayout):
    info_text = StringProperty()
    title_text = StringProperty()
    has_note = BooleanProperty(False)
class BlueBrick(BrickWidget):
    pass
