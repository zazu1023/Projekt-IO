from abc import ABC , abstractmethod
from enum import Enum, auto
from dataclasses import dataclass


from kivy.uix.button import Button as KivyButton
from kivy.uix.label import Label as KivyLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


from KivyHelper import KivyHelper

class ButtonState(Enum):
    NORMAL = auto()
    HOVER = auto()
    PRESSED = auto()
    DISABLED = auto()
    LOADING = auto()

class Shapes(Enum):
    RECTANGLE = auto()
    ROUNDED = auto()
    CIRCLE = auto()

@dataclass(frozen=True)
class ButtonStyle():
    bg_color: str
    text_color: str

    hover_bg_color: str
    hover_text_color: str

    border_radius: int
    border_color: str
    border_width: int

    shape: Shapes


class ButtonBackend(ABC):

    @abstractmethod
    def create(self, label: str , onclick: callable , style: ButtonStyle):
        # Tworzenie przycisku
        pass

    @abstractmethod
    def set_label(self , label: str ):
        # zmiana podpisu
        pass

    @abstractmethod
    def apply_state(self, state: ButtonState, style: ButtonStyle):
        # zmiana stanu
        pass

    @abstractmethod
    def update_style(self, style: ButtonStyle):
        pass

    @abstractmethod
    def bind_hover(self, on_enter: callable, on_leave: callable):
        pass

class Button:

    def __init__(self , label: str, backend: ButtonBackend , style: ButtonStyle, action:callable = None ):
        self.label = label
        self.style = style
        self._backend = backend
        self.action = action

        self._state = ButtonState.NORMAL

    def render(self):
        widget = self._backend.create(label=self.label , onclick=self.action , style=self.style)
        return widget
    
    def update_label(self, new_text: str):
        self.label = new_text
        self._backend.set_label(new_text)

    def update_style(self, new_style: ButtonStyle):
        self.style = new_style
        self._backend.update_style(self.style)

    def set_state(self, new_state:ButtonState):
        if self._state == new_state:
            return
        self._state = new_state
        self._backend.apply_state(self._state, self.style)

    def _handle_click(self):

        if self._status != ButtonState.NORMAL:
            return
        if self.action:
            self.action()
 

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
