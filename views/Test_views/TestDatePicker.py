from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from Widgets.datePicker import DatePicker, DatePickerStyle
from KivyWidgets.kivyDatePickerBackend import KivyDatePickerBackend


class TestDatePickerApp(App):
    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        style = DatePickerStyle(
            bg_color=(0.1, 0.1, 0.1, 1),
            selected_color=(1, 0.4, 0.1, 1),
            today_color=(0.2, 0.6, 1, 1),
            text_color=(1, 1, 1, 1)
        )

        backend = KivyDatePickerBackend()

        self.date_picker = DatePicker(
            selected_date=None,
            backend=backend,
            style=style
        )

        root.add_widget(self.date_picker.render())

        return root


if __name__ == "__main__":
    TestDatePickerApp().run()