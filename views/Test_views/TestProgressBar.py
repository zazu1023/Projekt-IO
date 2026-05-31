from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from progressBar import ProgressBar, ProgressBarStyle
from kivyProgressBarBackend import KivyProgressBarBackend


class TestProgressApp(App):

    def build(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        style = ProgressBarStyle(
            bg_color="white",
            fill_color="blue",
            text_color="black"
        )

        backend = KivyProgressBarBackend()

        self.progress = ProgressBar(
            value=30,
            max_value=100,
            backend=backend,
            style=style
        )

        progress_widget = self.progress.render()

        button = Button(text="Add progress")

        button.bind(on_press=self.addProgress)

        layout.add_widget(progress_widget)
        layout.add_widget(button)

        return layout

    def addProgress(self, instance):

        new_value = self.progress.value + 10

        self.progress.updateValue(new_value)


TestProgressApp().run()