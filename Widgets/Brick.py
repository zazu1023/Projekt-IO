from abc import abstractmethod
from dataclasses import dataclass

from typing import Optional

from Button import ButtonStyle , ButtonBackend , Button

from kivy.uix.button import Button as KivyButton
from KivyHelper import KivyHelper
from kivy.properties import ObjectProperty


@dataclass(frozen=True)
class LessonNote:
    id: str                # ID z bazy danych
    content: str           # Treść notatki
    last_modified: str     # Timestamp


@dataclass(frozen=True)
class CalendarBrickData:
    id: str
    title: str        
    start_time: str    
    end_time: str
    category_id: str
    note: Optional[LessonNote] = None

    @property
    def has_note(self) -> bool:
        return self.note is not None

class BrickBackend(ButtonBackend):
 
    @abstractmethod
    def create_brick(self, data: CalendarBrickData, style: ButtonStyle, on_click: callable):
        pass

    @abstractmethod
    def update_content(self, data: CalendarBrickData):
        pass



class Brick(Button):
   
    def __init__(self, data: CalendarBrickData, backend: BrickBackend, style: ButtonStyle):
        super().__init__(label=data.title, backend=backend, style=style)
        
        self.data = data
        self._brick_backend = backend

    def render(self):
      
        # Delegujemy tworzenie kafelka do backendu
        widget = self._brick_backend.create_brick(
            data=self.data, 
            style=self.style, 
            on_click=self._handle_click
        )
        
        self._backend.bind_hover(self._on_mouseenter, self._on_mouseleave)
        
        return widget
    def _handle_click(self, event_id):
        if self._on_click_callback:
            self._on_click_callback(self.event)

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