from datetime import datetime

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from Widgets.countdown import CountdownWidget, CountdownStyle, KivyCountdownBackend


class SideBar(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self.add_countdown, 0)

    def add_countdown(self, dt):
        countdown = CountdownWidget(
            target_date=datetime(2026, 6, 22, 0, 0),
            backend=KivyCountdownBackend(),
            style=CountdownStyle(
                bg_color=(0, 0, 0, 0),
                text_color=(1, 1, 1, 1)
            )
        )

        self.ids.countdown_content.add_widget(countdown.render())