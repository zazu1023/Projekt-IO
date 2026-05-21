from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from Widgets.form import FormStyle, FormField, FormWidget, KivyFormBackend

class ExamsAndColloquiumsApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=[30, 20, 30, 20], spacing=20)
        
        # === NAGŁÓWEK STRONY ===
        header_label = Label(
            text="Egzaminy i kolokwia", 
            font_size='32sp', 
            bold=True, 
            size_hint=(1, None), 
            height=60,
            halign='left',
            valign='middle'
        )
        header_label.bind(size=header_label.setter('text_size'))
        root.add_widget(header_label)

        content_layout = BoxLayout(orientation='horizontal', spacing=40)

        # ================= LEWA KOLUMNA (Formularz i Przedmioty) =================
        left_column = BoxLayout(orientation='vertical', spacing=20, size_hint_x=0.65)
        
        subjects_label = Label(
            text="Przedmioty", 
            bold=True, 
            size_hint=(1, None), 
            height=30, 
            halign='left'
        )
        subjects_label.bind(size=subjects_label.setter('text_size'))
        left_column.add_widget(subjects_label)

        tiles_grid = GridLayout(cols=4, spacing=15, size_hint_y=None, height=100)
        
        subjects = [
            ("3referfd", "#fefedfef"), ("ASD", "/JŚW"), 
            ("IO", "IOx"), ("SK", "ES")
        ]
        for sub, code in subjects:
            btn = Button(
                text=f"[b]{sub}[/b]\n{code}", 
                markup=True,
                background_normal='',
                background_color=(0.25, 0.45, 0.7, 1),
                halign='center'
            )
            tiles_grid.add_widget(btn)
        
        left_column.add_widget(tiles_grid)
        
        selected_info = Label(
            text="Wybrany przedmiot: 3referfd", 
            size_hint_y=None, height=40, 
            halign='left'
        )
        selected_info.bind(size=selected_info.setter('text_size'))
        left_column.add_widget(selected_info)

        # === FORMULARZ ===
        style = FormStyle(
            bg_color=(0, 0, 0, 0),
            text_color=(1, 1, 1, 1),
            button_color=(0.10, 0.25, 0.45, 1),
            field_background_color=(0.85, 0.85, 0.84, 1),
            field_text_color=(0, 0, 0, 1)
        )

        fields = [
            FormField(name="Tytuł wydarzenia", width=800),
            FormField(name="Start (YYYY-MM-DD HH:MM)", width=300, use_calendar=True)
        ]

        form = FormWidget(
            fields=fields, 
            backend=KivyFormBackend(), 
            style=style
        )
        
        form_render = form.render()
        left_column.add_widget(form_render)
        
        left_column.add_widget(BoxLayout())

        # ================= PRAWA KOLUMNA =================
        right_column = BoxLayout(orientation='vertical', spacing=15, size_hint_x=0.35)
        
        events_label = Label(
            text="Zapisane wydarzenia", 
            bold=True, 
            size_hint=(1, None), 
            height=30,
            halign='left'
        )
        events_label.bind(size=events_label.setter('text_size'))
        right_column.add_widget(events_label)

        event_card = Button(
            text="[size=14sp]2027-04-04 12:30[/size]\n[b]dsdsfdsf[/b]", 
            markup=True,
            size_hint=(1, None),
            height=100,
            background_normal='',
            background_color=(0.15, 0.3, 0.5, 1),
            halign='left',
            padding=(20, 10)
        )
        event_card.bind(size=event_card.setter('text_size'))
        
        right_column.add_widget(event_card)
        right_column.add_widget(BoxLayout())

        content_layout.add_widget(left_column)
        content_layout.add_widget(right_column)
        
        root.add_widget(content_layout)
        
        return root

if __name__ == "__main__":
    Window.clearcolor = (0.08, 0.12, 0.18, 1)
    ExamsAndColloquiumsApp().run()