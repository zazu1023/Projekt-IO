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
    border_color: Optional[str] = None
    border_width: int = 0

    bg_color: Optional[str] = None
    text_color: Optional[str] = "#FFFFFF" # Domyślnie biały tekst
    

    hover_bg_color: Optional[str] = None
    hover_text_color: Optional[str] =None


    pressed_bg_color: Optional[str] = None
    pressed_text_color: Optional[str] = None

    disabled_bg_color: Optional[str] = None # Standardowy szary dla zablokowanych
    disabled_text_color: Optional[str] = None

    font_size: str = "14sp"
    font_name: str = "Roboto"
    bold: bool = False
