from abc import ABC, abstractmethod
from typing import Dict

import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.graphics import RoundedRectangle
from kivy.core.window import Window


class TranslationManager:

    def __init__(

        self,

        language="pl",

        translation_file="translation.json"
    ):

        self.language = language

        

        with open(

            translation_file,

            "r",

            encoding="utf-8"
        ) as file:

            self.translations = json.load(
                file
            )

    

    def get(

        self,

        key
    ):

        return self.translations[
            self.language
        ].get(
            key,
            key
        )

    

    def set_language(

        self,

        language
    ):

        self.language = language

class TileStyle:

    def __init__(
        self,
        bg_color,
        text_color,
        note_bg_color,
        progress_color,

        screen_bg_color,

        header_text_color
    ):

        self.bg_color = bg_color

        self.text_color = text_color

        self.note_bg_color = note_bg_color

        self.progress_color = progress_color

        self.screen_bg_color = screen_bg_color

        self.header_text_color = header_text_color



class StatusBadge:

    COLORS = {
        "green": (0.179, 0.796, 0.441, 1),
        "yellow": (0.941, 0.765, 0.058, 1),
        "red": (0.902, 0.296, 0.234, 1),
        "white":(0.7,0.7,0.7,1)
    }

    def __init__(

        self,

        translation_key,

        color_name="green"
    ):

        self.translation_key = translation_key
    
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
    style,
    language_manager
    ):
        self.language_manager = language_manager
    

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

            rect = RoundedRectangle(

                pos=container.pos,

                size=container.size,

                radius=[15]
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

            status_rect = RoundedRectangle(

                pos=status_box.pos,

                size=status_box.size,

                radius=[10]
            )

        status_box.bind(
            pos=lambda instance, value:
            self._update_rect(instance, status_rect),

            size=lambda instance, value:
            self._update_rect(instance, status_rect)
        )

        status_label = Label(
            text=self.language_manager.get(
                tile.status.translation_key
            ),
            color=(1, 1, 1, 1)
        )

        status_box.add_widget(status_label)

        

        top_row.add_widget(left_side)
        top_row.add_widget(status_box)

        container.add_widget(top_row)

        

        progress_label = Label(
            text=self.language_manager.get(
                "absences"
            ),
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

            note_rect = RoundedRectangle(

                pos=note_box.pos,

                size=note_box.size,

                radius=[12]
            )

        note_box.bind(
            pos=lambda instance, value:
            self._update_rect(instance, note_rect),

            size=lambda instance, value:
            self._update_rect(instance, note_rect)
        )

        

        note_title = Label(
            text=self.language_manager.get(
                "passing_conditions"
            ),
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

    style,

    language_manager,

    screen_title=None
    ):
        self.language_manager = language_manager
        self.tiles = tiles

        self.backend = backend

        self.style = style

        self.screen_title = screen_title

        if screen_title is None:

            self.screen_title = Label(
                text=self.language_manager.get(
                    "rules_repository"
                ),
            )
        
        else:

            self.screen_title = screen_title

    def _update_screen_bg(
        self,
        instance,
        value
    ):

        self.screen_rect.pos = instance.pos

        self.screen_rect.size = instance.size

    def render(self):

    

        root = BoxLayout(

            orientation="vertical"
        )
        root.padding = 0
        root.spacing = 0
    

        with root.canvas.before:

            self.bg_color = Color(
                *self.style.screen_bg_color
            )

            self.screen_rect = RoundedRectangle(

                pos=root.pos,
                
                size=root.size,

                radius=[0]
            )

    

        root.bind(

            pos=self._update_screen_bg,

            size=self._update_screen_bg
        )

    

        header = Label(

        text=self.language_manager.get(
            "rules_repository"
        ),

        size_hint_y=None,

        height=70,

        font_size=28,

        bold=True,

        color=self.style.header_text_color,

        halign="left",

        valign="middle",

        padding=(20, 0)
    )

        header.bind(

            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

    

        root.add_widget(header)

    

        content = self.backend.create(

            self.tiles,

            self.style,

            self.language_manager
        )

    

        root.add_widget(content)

    

        return root




if __name__ == "__main__":

    from kivy.app import App



    class Repozytorum_zasad(App):

        def build(self):
            Window.clearcolor = (0.196, 0.176, 0.176, 1)
            style = TileStyle(

            bg_color=(0.18, 0.34, 0.55, 1),

            text_color=(1, 1, 1, 1),

            note_bg_color=(0.196, 0.176, 0.176, 1),

            progress_color=(0, 0.7, 1, 1),

            screen_bg_color=(0.196, 0.176, 0.176, 1),

            header_text_color=(1, 1, 1, 1)
        )

            

            tiles = [

                TileData(

                    title="hhdad",

                    subtitle="jjhank",

                    status=StatusBadge(

                        translation_key="my_subject_completed",

                        color_name="green"
                    ),

                    progress_value=8,

                    progress_max=15,

                    progress_label="",

                    note_title="",

                    note_text=(
                        "vgbhnjmcvbhnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjnbhyjgjknbytvrcexcrvtbynubytvrcvtbynubynuybvtrtgbhudabbvbfgnhmjjjjjjjjjjjjjudabbvbfgnhmjjjjjjjjjjjjjjjjdsadadsabbbhbhawbdvagvdahbhdvayv"
                        
                        
                    )
                ),

                

                TileData(

                    title="Programowanie 1",

                    subtitle="Kawa",

                    status=StatusBadge(
                       translation_key="my_subject_inprogress",

                        color_name="yellow"
                        
                        
                    ),

                    progress_value=1,

                    progress_max=10,

                    progress_label="",

                    note_title="",

                    note_text=(
                        "Dostać wystarczająco punktów w maszynie losującej zwanej kawowym kolokwium"
                        
                    )
                ),

                

                TileData(

                    title="lkjhgfd",

                    subtitle="uubhubhubu",

                    status=StatusBadge(
                        translation_key="my_subject_atrisk",

                        color_name="red"
                        
                    ),

                    progress_value=2,

                    progress_max=10,

                    progress_label="",

                    note_title="",

                    note_text=(
                        "Należy poprawić "
                        "ostatnie kolokwium."
                    )
                )
            ]

            

            backend = KivyTileBackend()

            language = TranslationManager(
            language="en"
            )

            widget = TileWidget(

                tiles=tiles,

                backend=backend,

                style=style,

                screen_title="",
                language_manager=language
                )
                

            

            return widget.render()



    Repozytorum_zasad().run()


