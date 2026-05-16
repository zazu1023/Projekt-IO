from datetime import date
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from datePicker import DatePicker, DatePickerStyle
from kivyDatePickerBackend import KivyDatePickerBackend


class TestApp(App):
    def build(self):
        layout = BoxLayout(padding=20)

        style = DatePickerStyle(
            bg_color="white",
            selected_color="blue",
            today_color="green",
            text_color="black"
        )

        backend = KivyDatePickerBackend()

        picker = DatePicker(
            selected_date=date(2026, 5, 16),
            backend=backend,
            style=style
        )

        layout.add_widget(picker.render())

        return layout


TestApp().run()