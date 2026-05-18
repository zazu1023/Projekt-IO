from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass
from datetime import datetime

from kivy.clock import Clock
from kivy.uix.label import Label as KivyLabel
from kivy.properties import ObjectProperty

from KivyWidgets.KivyHelper import KivyHelper



class TimerState(Enum):
    RUNNING = auto()
    STOPPED = auto()
    PAUSED = auto()


@dataclass(frozen=True)
class TimerStyle:
    text_color: str
    font_size: int
    bold: bool = False


class CountdownBackend(ABC):

    @abstractmethod
    def create(self, target_date: datetime, style: TimerStyle):
        pass

    @abstractmethod
    def update_text(self, text: str):
        pass

    @abstractmethod
    def update_style(self, style: TimerStyle):
        pass


class CountdownWidget:

    def __init__(
        self,
        target_date: datetime,
        backend: CountdownBackend,
        style: TimerStyle
    ):
        self.target_date = target_date
        self.style = style
        self._backend = backend

        self._state = TimerState.STOPPED
        self._event = None

    def render(self):
        widget = self._backend.create(
            target_date=self.target_date,
            style=self.style
        )

        self.start()

        return widget

    def start(self):
        if self._state == TimerState.RUNNING:
            return

        self._state = TimerState.RUNNING
        self._event = Clock.schedule_interval(self._update, 1)

    def stop(self):
        if self._event:
            self._event.cancel()

        self._state = TimerState.STOPPED

    def pause(self):
        if self._event:
            self._event.cancel()

        self._state = TimerState.PAUSED

    def update_style(self, new_style: TimerStyle):
        self.style = new_style
        self._backend.update_style(self.style)

    def _update(self, dt):
        now = datetime.now()

        delta = self.target_date - now

        total_seconds = int(delta.total_seconds())

        if total_seconds <= 0:
            self._backend.update_text("00:00:00")
            self.stop()
            return

        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        text = f"{days}d {hours:02}:{minutes:02}:{seconds:02}"

        self._backend.update_text(text)


class CustomCountdownWidget(KivyLabel):
    style = ObjectProperty(None)


class KivyCountdownBackend(KivyHelper, CountdownBackend):

    def __init__(self, parent=None):
        self.parent = parent
        self.widget = None

    def create(self, target_date: datetime, style: TimerStyle):

        self.widget = CustomCountdownWidget(
            text="Loading..."
        )

        self.update_style(style)

        return self.widget

    def update_text(self, text: str):

        if self.widget:
            self.widget.text = text

    def update_style(self, style: TimerStyle):

        if self.widget:
            self.widget.color = self._parse_color(style.text_color)
            self.widget.font_size = style.font_size
            self.widget.bold = style.bold
