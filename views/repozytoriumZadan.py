from abc import ABC, abstractmethod
from typing import Dict

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView


class TileStyle:

    def __init__(
        self,
        bg_color,
        text_color,
        note_bg_color,
        progress_color
    ):

        self.bg_color = bg_color
        self.text_color = text_color

        self.note_bg_color = note_bg_color
        self.progress_color = progress_color




class StatusBadge:

    COLORS = {
        "green": (0, 0.7, 0, 1),
        "yellow": (0.9, 0.7, 0, 1),
        "red": (0.8, 0, 0, 1),
        "white":(0.7,0.7,0.7,1)
    }

    def __init__(
        self,
        text,
        
            

        color_name="green"
    ):

        self.text = text
        self.color = self.COLORS.get(
            color_name,
            (0.5, 0.5, 0.5, 1)
        )




class TileData:

    def __init__(
        self,
        title,
        subtitle,
        status,
        progress_value,
        progress_max,
        progress_label,
        note_title,
        note_text
    ):

        self.title = title
        self.subtitle = subtitle

        self.status = status

        self.progress_value = progress_value
        self.progress_max = progress_max
        self.progress_label = progress_label

        self.note_title = note_title
        self.note_text = note_text




class TileBackend(ABC):

    @abstractmethod
    def create(
        self,
        tiles,
        style
    ):
        pass




class KivyTileBackend(TileBackend):

    def __init__(self):

        self.layout = None

    def create(
    self,
    tiles,
    style
    ):

    

        root_scroll = ScrollView(

            do_scroll_x=False,

            do_scroll_y=True
        )

    

        self.layout = BoxLayout(

            orientation="vertical",

            spacing=15,

            padding=20,

            size_hint_y=None
        )

    

        self.layout.bind(

            minimum_height=self.layout.setter(
            "height"
            )
        )

    

        for tile in tiles:

            tile_widget = self._create_tile(
            tile,
            style
            )

            self.layout.add_widget(
            tile_widget
            )

    

        root_scroll.add_widget(
            self.layout
        )

    

        return root_scroll

    

    def _create_tile(
        self,
        tile,
        style
    ):

        container = BoxLayout(

            orientation="vertical",

            spacing=10,

            padding=10,

            size_hint_y=None
        )

        container.bind(

            minimum_height=container.setter(
                "height"
            )
        )

        

        with container.canvas.before:

            Color(*style.bg_color)

            rect = Rectangle(
                pos=container.pos,
                size=container.size
            )

        container.bind(
            pos=lambda instance, value:
            self._update_rect(instance, rect),

            size=lambda instance, value:
            self._update_rect(instance, rect)
        )

        

        top_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50
        )

        

        left_side = BoxLayout(
            orientation="vertical"
        )

        title = Label(
            text=tile.title,
            color=style.text_color,
            halign="left",
            valign="middle"
        )

        subtitle = Label(
            text=tile.subtitle,
            color=style.text_color,
            halign="left",
            valign="middle"
        )

        title.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        subtitle.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        left_side.add_widget(title)
        left_side.add_widget(subtitle)

        

        status_box = BoxLayout(
            size_hint=(None, None),
            width=90,
            height=40,
            padding=5
        )

        with status_box.canvas.before:

            Color(*tile.status.color)

            status_rect = Rectangle(
                pos=status_box.pos,
                size=status_box.size
            )

        status_box.bind(
            pos=lambda instance, value:
            self._update_rect(instance, status_rect),

            size=lambda instance, value:
            self._update_rect(instance, status_rect)
        )

        status_label = Label(
            text=tile.status.text,
            color=(1, 1, 1, 1)
        )

        status_box.add_widget(status_label)

        

        top_row.add_widget(left_side)
        top_row.add_widget(status_box)

        container.add_widget(top_row)

        

        progress_label = Label(
            text=tile.progress_label,
            color=style.text_color,
            size_hint_y=None,
            height=25,
            halign="left",
            valign="middle"
        )

        progress_label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        container.add_widget(progress_label)

        

        progress = ProgressBar(
            max=tile.progress_max,
            value=tile.progress_value,
            size_hint_y=None,
            height=25
        )

        container.add_widget(progress)

        

        progress_info = Label(
            text=f"{tile.progress_value}/{tile.progress_max}",
            color=style.text_color,
            size_hint_y=None,
            height=25
        )

        container.add_widget(progress_info)

        

        note_box = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=5
        )

        with note_box.canvas.before:

            Color(*style.note_bg_color)

            note_rect = Rectangle(
                pos=note_box.pos,
                size=note_box.size
            )

        note_box.bind(
            pos=lambda instance, value:
            self._update_rect(instance, note_rect),

            size=lambda instance, value:
            self._update_rect(instance, note_rect)
        )

        

        note_title = Label(
            text=tile.note_title,
            bold=True,
            color=style.text_color,
            size_hint_y=None,
            height=30,
            halign="left",
            valign="middle"
        )

        note_title.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        

        note_text = Label(

            text=tile.note_text,

            color=style.text_color,

            halign="left",

            valign="top",

            size_hint_y=None
        )

        note_text.bind(

            width=lambda instance, value:
            setattr(
                instance,
                "text_size",
                (value, None)
            )
        )

        note_text.bind(

            texture_size=lambda instance, value:
            setattr(
                instance,
                "height",
                value[1]
            )
        )
        note_box.size_hint_y = None

        note_box.bind(

            minimum_height=note_box.setter(
        "height"
            )
        )
        note_box.add_widget(note_title)
        note_box.add_widget(note_text)

        container.add_widget(note_box)

        return container

    

    def _update_rect(
        self,
        widget,
        rect
    ):

        rect.pos = widget.pos
        rect.size = widget.size




class TileWidget:

    def __init__(
        self,
        tiles,
        backend,
        style
    ):

        self.tiles = tiles
        self.backend = backend
        self.style = style

    def render(self):

        return self.backend.create(
            self.tiles,
            self.style
        )




if __name__ == "__main__":

    from kivy.app import App



    class Repozytorum_zasad(App):

        def build(self):

            style = TileStyle(

                bg_color=(0.18, 0.34, 0.55, 1),

                text_color=(1, 1, 1, 1),

                note_bg_color=(0.45, 0.45, 0.45, 1),

                progress_color=(0, 0.7, 1, 1)
            )

            

            tiles = [

                TileData(

                    title="hhdad",

                    subtitle="jjhank",

                    status=StatusBadge(
                        "Zaliczony",
                        "green"
                    ),

                    progress_value=8,

                    progress_max=15,

                    progress_label="nieobecności",

                    note_title="Warunki zaliczenia",

                    note_text=(
                        "vgbhnjmcvbhnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjudabbvbfgnhmjjjjjjjjjjjjjjjjdsadadsabbbhbhawbdvagvdahbhdvayv"
                        
                        
                    )
                ),

                

                TileData(

                    title="Programowanie 1",

                    subtitle="Kawa",

                    status=StatusBadge(
                       "W trakcie",
                        
                        "white"
                    ),

                    progress_value=1,

                    progress_max=10,

                    progress_label="nieobecności",

                    note_title="Warunki Zaliczenia",

                    note_text=(
                        "Dostać wystarczająco punktów w maszynie losującej zwanej kawowym kolokwium"
                        
                    )
                ),

                

                TileData(

                    title="lkjhgfd",

                    subtitle="uubhubhubu",

                    status=StatusBadge(
                        "Zagrożony",
                        "red"
                    ),

                    progress_value=2,

                    progress_max=10,

                    progress_label="nieobecności",

                    note_title="Warunki zaliczenia",

                    note_text=(
                        "Należy poprawić "
                        "ostatnie kolokwium."
                    )
                )
            ]

            

            backend = KivyTileBackend()

            

            widget = TileWidget(

                tiles=tiles,

                backend=backend,

                style=style
            )

            

            return widget.render()



    Repozytorum_zasad().run()
