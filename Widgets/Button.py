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
