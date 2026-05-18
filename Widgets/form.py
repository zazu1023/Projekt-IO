from abc import ABC, abstractmethod
from typing import Dict

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button




class FormStyle:

    def __init__(
        self,
        bg_color,
        text_color,
        button_color
    ):

        self.bg_color = bg_color
        self.text_color = text_color
        self.button_color = button_color




class FormBackend(ABC):

    @abstractmethod
    def create(
        self,
        fields: list,
        style: FormStyle,
        submit_callback
    ):
        pass

    @abstractmethod
    def getValues(self) -> Dict[str, str]:
        pass




class KivyFormBackend(FormBackend):

    def __init__(self):

        self.layout = None
        self.inputs = {}

    def create(
        self,
        fields: list,
        style: FormStyle,
        submit_callback
    ):

        self.layout = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        for field in fields:

            label = Label(
                text=field,
                size_hint_y=None,
                height=30,
                color=style.text_color
            )

            text_input = TextInput(
                multiline=False,
                size_hint_y=None,
                height=40
            )

            self.inputs[field] = text_input

            self.layout.add_widget(label)
            self.layout.add_widget(text_input)

        submit_button = Button(
            text="Submit",
            size_hint_y=None,
            height=50,
            background_color=style.button_color
        )

        submit_button.bind(
            on_press=lambda instance: submit_callback(
                self.getValues()
            )
        )

        self.layout.add_widget(submit_button)

        return self.layout

    def getValues(self):

        values = {}

        for field, text_input in self.inputs.items():

            values[field] = text_input.text

        return values




class FormWidget:

    def __init__(
        self,
        fields: list,
        backend: FormBackend,
        style: FormStyle
    ):

        self.fields = fields
        self._backend = backend
        self.style = style

    def render(self):

        return self._backend.create(
            self.fields,
            self.style,
            self._on_submit
        )

    def _on_submit(self, values):

        print("Wysłane dane:")

        for key, value in values.items():

            print(f"{key}: {value}")
