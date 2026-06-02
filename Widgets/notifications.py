from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from kivy.metrics import dp

class NotificationPopup(Popup):
    def on_open(self):
        self.ids.events_container.clear_widgets()
        
        app = App.get_running_app()
        upcoming_events = app.repo.get_upcoming_events()

        if not upcoming_events:
            empty_text = app.translations[app.language]["no_upcoming_events"]
            
            empty_label = Label(
                text=empty_text, 
                size_hint_y=None, 
                height=dp(40)
            )
            self.ids.events_container.add_widget(empty_label)
            return

        for event_data in upcoming_events:
            event_text = f"{event_data['date_time']} | {event_data['title']}"
            
            event_label = Label(
                text=event_text,
                size_hint_y=None,
                height=dp(40),
                halign='left',
                valign='middle'
            )
            event_label.bind(size=event_label.setter('text_size'))
            
            self.ids.events_container.add_widget(event_label)