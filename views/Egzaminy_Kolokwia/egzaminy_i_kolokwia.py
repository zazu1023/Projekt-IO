import os
import sys
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.factory import Factory 
from kivy.clock import Clock 
from kivy.metrics import dp 
from kivy.uix.popup import Popup 
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from Widgets.datePicker import DatePicker, DatePickerStyle
from KivyWidgets.kivyDatePickerBackend import KivyDatePickerBackend
from datetime import date
from KivyWidgets.KivyButtonBackend import CustomButtonWidget 

# ==============================================================
# INICJALIZACJA I DANE TESTOWE
# ==============================================================

class ExamsAndColloquiumsScreen(Screen):
    repo = ObjectProperty(None)
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_subject_btn = None 
        self.selected_subject_id = None
        Clock.schedule_once(self.load_subjects, 0)
        Clock.schedule_once(self.load_events, 0)

    def load_subjects(self, dt):
        grid = self.ids.subjects_grid
        grid.clear_widgets() 
        
        db_connection = self.repo.get_db_connection()
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
        
        lbl_text = self.app.translate("lbl_selected_subject", self.app.language)
        self.ids.label_selected_subject.text = f"{lbl_text}{subject_name}"
        self.load_events()

    def load_events(self, dt=None):
        container = self.ids.events_container
        container.clear_widgets() 
        
        try:
            db_connection = self.repo.get_db_connection()
            cursor = db_connection.cursor()
            query = """
                SELECT events.id, events.title, events.date_time, subjects.name AS subject_name 
                FROM events 
                JOIN subjects ON events.subject_id = subjects.id 
                ORDER BY events.date_time ASC
            """
            fetched_events = cursor.execute(query).fetchall()

            for event_record in fetched_events:
                card = Factory.EventCard()
                card.date_text = str(event_record['date_time'])
                card.title_text = str(event_record['title'])
                card.subject_text = str(event_record['subject_name']) 
                
                event_id = event_record['id']
                event_title = str(event_record['title'])
                
                card.ids.btn_delete.bind(
                    on_release=lambda instance, e_id=event_id, e_title=event_title: self.show_delete_popup(e_id, e_title)
                )
                
                container.add_widget(card)
        except Exception as e:
            print(f"CRITICAL ERROR (load_events): {e}")

    def submit_event(self):

        # 1. WALIDACJA: Czy wybrano przedmiot
        if not self.selected_subject_id:
            self.show_error_popup(self.app.translate("err_select_subject", self.app.language))
            return 
            
        event_title = self.ids.input_event_title.text.strip()
        event_date = self.ids.input_event_date.text.strip()
        event_time = self.ids.input_event_time.text.strip()
        event_type = self.ids.input_event_type.text 
        
        if event_type == self.app.translate("type_placeholder", self.app.language):
            self.show_error_popup(self.app.translate("err_empty_event_type", self.app.language))
            return
        if not event_title:
            self.show_error_popup(self.app.translate("err_empty_event_title", self.app.language))
            return
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", event_date):
            self.show_error_popup(self.app.translate("err_invalid_date_format", self.app.language))
            return
        if not re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", event_time):
            self.show_error_popup(self.app.translate("err_invalid_time_format", self.app.language))
            return

        full_event_start = f"{event_date} {event_time}"
        
        db_connection = self.repo.get_db_connection()
        db_connection.execute(
            "INSERT INTO events (subject_id, type, title, date_time) VALUES (?, ?, ?, ?)", 
            (self.selected_subject_id, event_type, event_title, full_event_start)
        )
        db_connection.commit()
        
        self.load_events()
        self.ids.input_event_title.text = ""
        self.ids.input_event_date.text = ""
        self.ids.input_event_time.text = ""
        self.ids.input_event_type.text = self.app.translate("type_placeholder", self.app.language)

    def show_error_popup(self, error_message):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        label = Label(text=error_message, halign='center', valign='middle')
        label.bind(size=label.setter('text_size'))
        content.add_widget(label)

        btn_ok = Factory.DangerButton()
        btn_ok.text = self.app.translate("btn_will_fix", self.app.language)
        btn_ok.size_hint_y = None
        btn_ok.height = dp(40)
        content.add_widget(btn_ok)

        popup = Popup(
            title=self.app.translate("popup_error_input_title", self.app.language), 
            content=content, 
            size_hint=(None, None), size=(dp(400), dp(200)), 
            auto_dismiss=True
        )
        btn_ok.bind(on_release=popup.dismiss)
        popup.open()

    def show_delete_popup(self, event_id, event_title):
        try:
            content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
            
            safe_title = event_title.replace('[', '').replace(']', '')
            
            base_msg = self.app.translate("popup_delete_msg", self.app.language)
            message = Label(
                text=base_msg.format(safe_title), 
                markup=True, halign='center'
            )
            content.add_widget(message)

            buttons = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
            btn_cancel = Factory.PrimaryButton()
            btn_cancel.text = self.app.translate("btn_cancel", self.app.language)
            btn_confirm = Factory.DangerButton()
            btn_confirm.text = self.app.translate("btn_delete", self.app.language)
            
            buttons.add_widget(btn_cancel)
            buttons.add_widget(btn_confirm)
            content.add_widget(buttons)

            popup = Popup(
                title=self.app.translate("popup_delete_title", self.app.language), 
                content=content, 
                size_hint=(None, None), size=(dp(400), dp(200)), 
                auto_dismiss=False
            )

            btn_cancel.bind(on_release=popup.dismiss)
            btn_confirm.bind(on_release=lambda instance: self.delete_event(event_id, popup))
            
            popup.open()
        except Exception as e:
            print(f"CRITICAL ERROR (show_delete_popup): {e}")

    def delete_event(self, event_id, popup):
        db_connection = self.repo.get_db_connection()
        try:
            cursor = db_connection.cursor()
            cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
            db_connection.commit()
            
            popup.dismiss()
            self.load_events()
            
        except Exception as e:
            db_connection.rollback()
            popup.dismiss()
            error_prefix = self.app.translate("err_db_delete", self.app.language)
            self.show_error_popup(f"{error_prefix}{str(e)}")

    def open_calendar(self):
        dp_style = DatePickerStyle(
            bg_color=(0.15, 0.15, 0.15, 1), 
            selected_color=(0.2, 0.5, 0.8, 1), 
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
            title=self.app.translate("popup_choose_exam_date", self.app.language),
            content=picker_ui,
            size_hint=(None, None),
            size=(400, 450)
        )

        def on_confirm(instance):
            chosen_date = backend.selected_date 
            self.ids.input_event_date.text = str(chosen_date)
            popup.dismiss()

        backend.confirm_button.bind(on_release=on_confirm)
        
        popup.open()

class ExamsAndColloquiumsApp(App):
    def build(self):

        return ExamsAndColloquiumsScreen()

'''
if __name__ == "__main__":
    Window.clearcolor = (0.08, 0.12, 0.18, 1)
    Window.minimum_width = 1000
    Window.minimum_height = 700
    ExamsAndColloquiumsApp().run()
'''