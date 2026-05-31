from datetime import datetime
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from Widgets.countdown import CountdownWidget, CountdownStyle, KivyCountdownBackend

class SessionPanel(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_timer, 0.1)

    def add_timer(self, dt):
        self.countdown = CountdownWidget(
            target_date=datetime(2026, 6, 22, 0, 0),
            backend=KivyCountdownBackend(),
            style=CountdownStyle(
                bg_color=(0, 0, 0, 0), 
                text_color=(1, 1, 1, 1)
            )
        )
        self.add_widget(self.countdown.render())