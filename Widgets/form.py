from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from kivy.uix.textinput import TextInput as KivyTextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label as KivyLabel
from kivy.properties import ObjectProperty




@dataclass(frozen=True)
class InputStyle:
    background_color: str
    text_color: str
    hint_text_color: str

    font_size: int

    border_radius: int = 0


@dataclass(frozen=True)
class FormField:
    name: str
    hint: str = ""
    multiline: bool = False
    password: bool = False


@dataclass
class FormData:
    values: dict = field(default_factory=dict)


class FormBackend(ABC):

    @abstractmethod
    def create(
        self,
        fields: List[FormField],
        style: InputStyle
    ):
        pass

    @abstractmethod
    def get_values(self) -> dict:
        pass

    @abstractmethod
    def set_value(self, field_name: str, value: str):
        pass

    @abstractmethod
    def update_style(self, style: InputStyle):
        pass


class Form:

    def __init__(
        self,
        fields: List[FormField],
        backend: FormBackend,
        style: InputStyle
    ):
        self.fields = fields
        self.style = style
        self._backend = backend

    def render(self):
        return self._backend.create(
            fields=self.fields,
            style=self.style
        )

    def get_data(self) -> FormData:
        return FormData(
            values=self._backend.get_values()
        )

    def set_value(self, field_name: str, value: str):
        self._backend.set_value(field_name, value)

    def update_style(self, new_style: InputStyle):
        self.style = new_style
        self._backend.update_style(self.style)


class CustomInputWidget(KivyTextInput):
    style = ObjectProperty(None)


class KivyFormBackend(KivyHelper, FormBackend):

    def __init__(self, parent=None):

        self.parent = parent
        self.widget = None

        self.inputs = {}

    def create(
        self,
        fields: List[FormField],
        style: InputStyle
    ):

        self.widget = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )

        for field in fields:

            label = KivyLabel(
                text=field.name,
                size_hint_y=None,
                height=30
            )

            input_widget = CustomInputWidget(
                hint_text=field.hint,
                multiline=field.multiline,
                password=field.password,
                size_hint_y=None,
                height=40
            )

            self._apply_input_style(
                input_widget,
                style
            )

            self.inputs[field.name] = input_widget

            self.widget.add_widget(label)
            self.widget.add_widget(input_widget)

        return self.widget

    def get_values(self) -> dict:

        result = {}

        for field_name, widget in self.inputs.items():
            result[field_name] = widget.text

        return result

    def set_value(self, field_name: str, value: str):

        if field_name in self.inputs:
            self.inputs[field_name].text = value

    def update_style(self, style: InputStyle):

        for widget in self.inputs.values():
            self._apply_input_style(widget, style)

    def _apply_input_style(
        self,
        widget: KivyTextInput,
        style: InputStyle
    ):

        widget.background_color = self._parse_color(
            style.background_color
        )

        widget.foreground_color = self._parse_color(
            style.text_color
        )

        widget.hint_text_color = self._parse_color(
            style.hint_text_color
        )

        widget.font_size = style.font_size
