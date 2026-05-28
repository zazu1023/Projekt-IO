from datetime import date, timedelta
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty

from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from Widgets.Brick import CalendarBrickData, LessonNote
from Widgets.notePopup import NotePopup
from KivyWidgets.kivyNotePopupBackend import KivyNotePopupBackend
from KivyWidgets.KivyBrickBackend import BrickWidget , BlueBrick

# Przykładowe importy Twojego modułu (dostosuj ścieżki do swoich folderów)
from Widgets.datePicker import DatePicker, DatePickerStyle
from KivyWidgets.kivyDatePickerBackend import KivyDatePickerBackend

from Widgets.Brick import CalendarBrickData
from Widgets.Button import ButtonStyle
from KivyWidgets.KivyCalendarBrickAdapter import SafeKivyBrickBackend

from database import save_daily_note, get_daily_note

DAY_NAMES = {
    'pl': {0: "Pon", 1: "Wt", 2: "Śr", 3: "Czw", 4: "Pt", 5: "Sob", 6: "Ndz"},
    'en': {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
}

class CalendarWidget(BoxLayout):
    week_label = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_week_start = self.get_monday(date.today())

        self.events = [
            {
                "date": date(2026, 5, 12),
                "data": CalendarBrickData(
                    id="1",
                    title="IO",
                    start_time="10:30",
                    end_time="1.5 h",
                    category_id="IO"
                )
            },
            {
                "date": date(2026, 5, 12),
                "data": CalendarBrickData(
                    id="2",
                    title="ASD",
                    start_time="14:30",
                    end_time="1.5 h",
                    category_id="ASD"
                )
            },
            {
                "date": date(2026, 5, 12),
                "data": CalendarBrickData(
                    id="3",
                    title="ASD",
                    start_time="15:30",
                    end_time="1.5 h",
                    category_id="ASD"
                )
            },
            {
                "date": date(2026, 5, 12),
                "data": CalendarBrickData(
                    id="4",
                    title="ASD",
                    start_time="18:30",
                    end_time="1.5 h",
                    category_id="ASD"
                )
            },
            {
                "date": date(2026, 5, 13),
                "data": CalendarBrickData(
                    id="5",
                    title="SK",
                    start_time="08:00",
                    end_time="1.5 h",
                    category_id="IO"
                )
            },
            {
                "date": date(2026, 5, 14),
                "data": CalendarBrickData(
                    id="6",
                    title="RPiS",
                    start_time="08:00",
                    end_time="1.5 h",
                    category_id="IO"
                )
            },
            {
                "date": date(2026, 5, 12), # Upewnij się, że masz tu datę pasującą do wyświetlanego tygodnia!
                "data": CalendarBrickData(
                    id="7",
                    title="SK",
                    start_time="10:30",
                    end_time="1.5 h",
                    category_id="IO",
                    # DODAJEMY TESTOWĄ NOTATKĘ TUTAJ:
                    note=LessonNote(id="n1", content="To jest moja pierwsza próbna notatka!", last_modified="2026-05-28")
                )
            },
        ]

    def get_monday(self, selected_date):
        return selected_date - timedelta(days=selected_date.weekday())

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()
        if self.app:
            self.app.bind(language=self._on_language_change)
        self.refresh_calendar()
        
    def _on_language_change(self, instance, value):
        self.refresh_calendar()

    def refresh_calendar(self):
        week_end = self.current_week_start + timedelta(days=6)
        self.week_label = f"{self.current_week_start} - {week_end}"

        self.ids.days_box.clear_widgets()

        for i in range(7):
            day_date = self.current_week_start + timedelta(days=i)
            day_column = self.create_day_column(day_date)
            self.ids.days_box.add_widget(day_column)

    def create_day_column(self, day_date):
        # Główna kolumna dla całego dnia (Nagłówek + ScrollView)
        column = BoxLayout(
            orientation="vertical",
            padding=2,
            spacing=4
        )
        lang = self.app.language if self.app else 'pl'
        day_str = DAY_NAMES[lang][day_date.weekday()]

        # Nagłówek dnia (zostaje na samej górze, nie będzie się scrollował)
        header = Label(
            text=f"{day_str}\n{day_date.strftime('%m-%d')}",
            size_hint_y=None,
            height=45,
            color=(1, 1, 1, 1),
            bold=True,
            halign="center",
            valign="middle"
        )
        header.bind(size=lambda instance, value: setattr(instance, "text_size", instance.size))
        column.add_widget(header)

        # Tworzymy widżet umożliwiający przewijanie
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False, # Blokujemy przewijanie na boki
            do_scroll_y=True   # Pozwalamy na przewijanie góra/dół
        )

        # Kontener na KAFELKI wewnątrz ScrollView
        # To tutaj ustawiamy "marginesy" (spacing i padding)
        events_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,  # Musi być None, żeby ScrollView wiedziało, że ma przewijać!
            spacing=12,        # MARGINES MIĘDZY kafelkami (pionowy)
            padding=[5, 10, 5, 10] # MARGINES ZEWNĘTRZNY (lewo, góra, prawo, dół)
        )
        # Bardzo ważne: Kontener musi dynamicznie rosnąć w dół wraz z dodawaniem kafelków
        events_layout.bind(minimum_height=events_layout.setter('height'))

        events_for_day = self.get_events_for_day(day_date)
        
        if not events_for_day:
            
            empty = Label(
                text="-",
                size_hint_y=None,
                height=35,
                color=(1, 1, 1, 0.5)
            )
            events_layout.add_widget(empty)
        else:
            for event in events_for_day:
                
                brick = self.create_brick(event, day_date)
                brick.size_hint_x = 1 
                events_layout.add_widget(brick)

        # Pakujemy wszystko do siebie jak rosyjską matrioszkę
        scroll_view.add_widget(events_layout)
        column.add_widget(scroll_view)

        return column
    def get_events_for_day(self, day_date):
        result = []
        
        for event in self.events:
            if event["date"] == day_date:
                result.append(event["data"])

        return result

    # 1. TUTAJ DODAJEMY day_date W NAWIASIE
    def create_brick(self, event_data, day_date): 
        style = ButtonStyle(
            bg_color="e3e3e2",
            hover_bg_color="e3e3e2",
            text_color=(0, 0, 0, 1),
            border_radius=25
        )

        brick = BlueBrick()
        brick.style = style
        brick.data = event_data

        brick.title_text = event_data.title
        # Łączymy czas rozpoczęcia i czas trwania, żeby uzyskać np. "10:30 | 1.5 h"
        brick.info_text = f"{event_data.start_time} | {event_data.end_time}"

        return brick

    def on_event_click(self, event_data, day_date):  # <--- DODAJ ", day_date"
        # 1. Zmieniamy datę na tekst w formacie YYYY-MM-DD
        date_str = str(day_date)
        
        # 2. Pobieramy notatkę korzystając z PRAWIDŁOWEJ daty i ID
        existing_text = get_daily_note(event_data.id, date_str)
        
        backend = KivyNotePopupBackend()
        popup = NotePopup(
            subject_id=event_data.id, 
            subject_name=event_data.title,
            note_date=date_str, 
            backend=backend,
            existing_text=existing_text, 
            on_save=self.save_note_to_db 
        )
        popup.open()
    def save_note_to_db(self, subject_id, note_date, content):
        # 3. ZAPIS DO PRAWDZIWEJ BAZY DANYCH!
        save_daily_note(subject_id, note_date, content)
        print(f"Baza zaktualizowana: {subject_id} na dzień {note_date}")
        
        # Opcjonalnie: odświeżamy kalendarz po zapisie, 
        # żeby aplikacja na nowo przemieliła kropki (jeśli zajdzie taka potrzeba)
        self.refresh_calendar()

    def previous_week(self):
        self.current_week_start -= timedelta(days=7)
        self.refresh_calendar()

    def next_week(self):
        self.current_week_start += timedelta(days=7)
        self.refresh_calendar()

    def current_week(self):
        self.current_week_start = self.get_monday(date.today())
        self.refresh_calendar()
    def choose_week(self):
        dp_style = DatePickerStyle(
            bg_color=(1, 1, 1, 1),
            selected_color=(45/255, 88/255, 140/255, 1),
            today_color=(0.8, 0.8, 0.8, 1),
            text_color=(1, 1, 1, 1)
        )
        backend = KivyDatePickerBackend()
        picker = DatePicker(
            selected_date=date.today(),
            backend=backend,
            style=dp_style
        )
        picker_ui = picker.render()
        popup = Popup(
            title="Wybierz datę",
            content=picker_ui,
            size_hint=(None, None),
            size=(400, 450)
        )

        def on_confirm(instance):
            chosen_date = backend.selected_date
            self.current_week_start = self.get_monday(chosen_date)
            self.refresh_calendar()
            popup.dismiss()

        backend.confirm_button.bind(on_release=on_confirm)

        popup.open()