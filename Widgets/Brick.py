from abc import abstractmethod
from dataclasses import dataclass

from typing import Optional

from Widgets.Button import ButtonStyle

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
