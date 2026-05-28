import os
import sys

# Automatycznie znajdujemy główny folder projektu
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.factory import Factory 
from kivy.clock import Clock 
from kivy.metrics import dp 
from kivy.uix.popup import Popup 
from kivy.uix.label import Label

from KivyWidgets.KivyButtonBackend import CustomButtonWidget 
import database as db 

# ==============================================================
# INICJALIZACJA I DANE TESTOWE
# ==============================================================
db.init_db()

# --- TEN BLOK BĘDZIESZ MÓGŁ USUNĄĆ, GDY POWSTANIE ZAKŁADKA PRZEDMIOTÓW ---
db_test = db.get_connection()
if db_test.execute("SELECT COUNT(*) FROM subjects").fetchone()[0] == 0:
    print("Baza pusta! Wstrzykuję testowe kafelki i wydarzenia...")
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Matematyka", "Dr Jan Kowalski"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Fizyka", "Prof. Anna Nowak"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("IO", "Prof. Adam Roman"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Sieci", "Dr Edward Szczypka"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Sieci", "Dr Edward Szczypka"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Sieci", "Dr Edward Szczypka"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Sieci", "Dr Edward Szczypka"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Sieci", "Dr Edward Szczypka"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Sieci", "Dr Edward Szczypka"))
    db_test.execute("INSERT INTO subjects (name, teacher) VALUES (?, ?)", ("Sieci", "Dr Edward Szczypka"))
    
    db_test.commit()
# -------------------------------------------------------------------------

# Rejestrujemy klasę z pliku Twojego kolegi w globalnej fabryce Kivy
Factory.register('CustomButtonWidget', cls=CustomButtonWidget)

# Dynamicznie ładujemy plik .kv
kv_path = os.path.join(parent_dir, 'kv', 'egzaminy_i_kolokwia.kv')
Builder.load_file(kv_path)


class ExamsAndColloquiumsScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_subject_btn = None 
        self.selected_subject_id = None
        Clock.schedule_once(self.load_subjects, 0)
        Clock.schedule_once(self.load_events, 0)

    def load_subjects(self, dt):
        grid = self.ids.subjects_grid
        grid.clear_widgets() 
        
        db_connection = db.get_connection()
        fetched_subjects = db_connection.execute("SELECT id, name, teacher FROM subjects").fetchall()

        for subject_record in fetched_subjects:
            btn = Factory.PrimaryButton()
            btn.size_hint_y = None
            btn.height = dp(85) 
            btn.markup = True
            btn.halign = 'center'
            btn.valign = 'middle'
            btn.shorten = True
            btn.shorten_from = 'right'
            
            subject_id = subject_record['id']
            subject_name = subject_record['name']
            teacher_name = subject_record['teacher']
            
            btn.text = f"{subject_name}\n[size=12sp]{teacher_name}[/size]"
            btn.bind(on_release=lambda instance, s_id=subject_id, s_name=subject_name: self.select_subject(instance, s_id, s_name))
            
            grid.add_widget(btn)

    def select_subject(self, instance, subject_id, subject_name):
        if self.selected_subject_btn:
            self.selected_subject_btn.is_selected = False
            
        self.selected_subject_btn = instance
        self.selected_subject_btn.is_selected = True
        self.selected_subject_id = subject_id
        
        self.ids.label_selected_subject.text = f"Wybrany przedmiot: {subject_name}"
        self.load_events()

    def load_events(self, dt=None):
        container = self.ids.events_container
        container.clear_widgets() 
        
        db_connection = db.get_connection()
        
        query = """
            SELECT events.id, events.title, events.date_time, subjects.name AS subject_name 
            FROM events 
            JOIN subjects ON events.subject_id = subjects.id 
            ORDER BY events.date_time ASC
        """
        fetched_events = db_connection.execute(query).fetchall()

        for event_record in fetched_events:
            card = Factory.EventCard()
            card.date_text = event_record['date_time']
            card.title_text = event_record['title']
            
            card.subject_text = event_record['subject_name'] 
            
            event_id = event_record['id']
            card.ids.btn_delete.bind(on_release=lambda instance, e_id=event_id, e_title=event_record['title']: self.show_delete_popup(e_id, e_title))
            
            container.add_widget(card)

    def submit_event(self):
        if not self.selected_subject_id:
            return 
            
        event_title = self.ids.input_event_title.text
        event_date = self.ids.input_event_date.text
        event_time = self.ids.input_event_time.text
        full_event_start = f"{event_date} {event_time}".strip()
        
        if event_title and full_event_start:
            db_connection = db.get_connection()
            db_connection.execute(
                "INSERT INTO events (subject_id, type, title, date_time) VALUES (?, ?, ?, ?)", 
                (self.selected_subject_id, 'Exam', event_title, full_event_start)
            )
            db_connection.commit()
            
            self.load_events()
            
            self.ids.input_event_title.text = ""
            self.ids.input_event_date.text = ""
            self.ids.input_event_time.text = ""

    def show_delete_popup(self, event_id, event_title):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        message = Label(
            text=f"Czy na pewno chcesz usunąć to wydarzenie:\n[b]{event_title}[/b]?", 
            markup=True, halign='center'
        )
        content.add_widget(message)

        buttons = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        btn_cancel = Factory.PrimaryButton()
        btn_cancel.text = "Anuluj"
        btn_confirm = Factory.DangerButton()
        btn_confirm.text = "Usuń"

        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_confirm)
        content.add_widget(buttons)

        popup = Popup(
            title="Potwierdzenie usunięcia", 
            content=content, 
            size_hint=(None, None), size=(dp(400), dp(200)), 
            auto_dismiss=False
        )

        btn_cancel.bind(on_release=popup.dismiss)
        btn_confirm.bind(on_release=lambda instance: self.delete_event(event_id, popup))
        popup.open()

    def delete_event(self, event_id, popup):
        db_connection = db.get_connection()
        db_connection.execute("DELETE FROM events WHERE id = ?", (event_id,))
        db_connection.commit()
        
        popup.dismiss()
        self.load_events()

    def open_calendar(self):
        pass


class ExamsAndColloquiumsApp(App):
    def build(self):
        return ExamsAndColloquiumsScreen()


if __name__ == "__main__":
    Window.clearcolor = (0.08, 0.12, 0.18, 1)
    ExamsAndColloquiumsApp().run()