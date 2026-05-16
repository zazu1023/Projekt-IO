
from kivy.uix.button import Button as KivyButton
from Widgets.Button import ButtonBackend , ButtonStyle , ButtonState
from KivyWidgets.KivyHelper import KivyHelper

from kivy.properties import ObjectProperty

class CustomButtonWidget(KivyButton):
    style = ObjectProperty(None)

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
