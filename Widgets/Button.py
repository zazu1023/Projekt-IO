from abc import ABC , abstractmethod
from enum import Enum, auto
from dataclasses import dataclass

from typing import Optional ,Union,List


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
    shape: Shapes = Shapes.ROUNDED
 
    border_radius: Union[int, List[int]] = 10 
    border_color: Optional[str] = "#FFFFFF"
    border_width: int = 0

    bg_color: Optional[str] = "#FFFFFF"
    text_color: Optional[str] = "#FFFFFF" # Domyślnie biały tekst
    

    hover_bg_color: Optional[str] = "#FFFFFF"
    hover_text_color: Optional[str] ="#FFFFFF"


    pressed_bg_color: Optional[str] = "#FFFFFF"
    pressed_text_color: Optional[str] = "#FFFFFF"

    disabled_bg_color: Optional[str] = "#555555" # Standardowy szary dla zablokowanych
    disabled_text_color: Optional[str] = "#888888"

    font_size: str = "14sp"
    font_name: str = "Roboto"
    bold: bool = False
    
    icon_source: Optional[str] = None # Ścieżka do obrazka, jeśli przycisk ma ikonę

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
        if self._state in (ButtonState.DISABLED, ButtonState.LOADING):
            return
            
        if self.action:
            self.action()
 
