
from kivy.uix.button import Button as KivyButton
from Widgets.Button import ButtonBackend , ButtonStyle , ButtonState
from KivyWidgets.KivyHelper import KivyHelper

from kivy.properties import ObjectProperty , BooleanProperty
from kivy.core.window import Window

class CustomButtonWidget(KivyButton):
    style = ObjectProperty(None)
    hovered = BooleanProperty(False)
    btn_state = ObjectProperty(ButtonState.NORMAL)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):

        if not self.get_root_window():
            return

        local_pos = self.to_widget(*pos)

        inside = self.collide_point(*local_pos)

        if self.hovered != inside:
            self.hovered = inside
     
     
class KivyButtonBackend(KivyHelper,ButtonBackend):

    def __init__(self , parent = None):
       self.parent = parent
       self.widget = None

    def create(self, label: str , onclick: callable , style: ButtonStyle):
        self.widget = CustomButtonWidget(text=label)
        self.widget.bind(on_release=lambda x: onclick())

        self.apply_state(ButtonState.NORMAL, style)

        return self.widget

    def set_label(self , label: str ):
        if self.widget:
            self.widget.text = label

    def apply_state(self, state: ButtonState, style: ButtonStyle):
        if self.widget:
            pass
   
    def update_style(self, style: ButtonStyle):
        if self.widget:
            self.widget.bg_color = self._parse_color(style.bg_color)
            self.widget.text_color = self._parse_color(style.text_color)

   
    def bind_hover(self, on_enter: callable, on_leave: callable):
        pass
