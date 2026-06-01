import os
import sys
import re
from datetime import datetime, date

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.factory import Factory
from KivyWidgets.KivyButtonBackend import CustomButtonWidget

from Widgets.datePicker import DatePicker, DatePickerStyle
from KivyWidgets.kivyDatePickerBackend import KivyDatePickerBackend

kv_path = os.path.join(parent_dir, 'kv', 'dodaj_przedmiot.kv')

class AddSubjectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_date_field = None  # przechowuje informacje, które pole daty aktualizujemy

    def open_calendar(self, field_id):
        """Otwiera własny DatePicker zamiast MDDatePicker."""
        app = App.get_running_app()
        self.active_date_field = field_id

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
            title=app.translate("popup_choose_date", app.language),
            content=picker_ui,
            size_hint=(None, None),
            size=(400, 450)
        )

        def on_confirm(instance):
            chosen_date = backend.selected_date
            date_str = str(chosen_date)
            
            if self.active_date_field == 'start':
                self.ids.input_start_date.text = date_str
            elif self.active_date_field == 'end':
                self.ids.input_end_date.text = date_str
            
            popup.dismiss()

        backend.confirm_button.bind(on_release=on_confirm)
        popup.open()

    def save_subject(self):
        app = App.get_running_app()
        # 1. POBIERANIE DANYCH
        subject_name = self.ids.input_name.text.strip()
        teacher_name = self.ids.input_teacher.text.strip()
        pass_conditions = self.ids.input_conditions.text.strip()
        start_time = self.ids.input_time.text.strip()
        start_date = self.ids.input_start_date.text.strip()
        end_date = self.ids.input_end_date.text.strip()

        # 2. WALIDACJA TEKSTÓW
        if not subject_name:
            self.show_error_popup(app.translate("err_subject_req", app.language))
            return
        if not teacher_name:
            self.show_error_popup(app.translate("err_teacher_req", app.language))
            return

        # 3. WALIDACJA DAT
        try:
            d_start = datetime.strptime(start_date, '%Y-%m-%d')
            d_end = datetime.strptime(end_date, '%Y-%m-%d')
            if d_end < d_start:
                self.show_error_popup(app.translate("err_end_before_start", app.language))
                return
        except ValueError:
            self.show_error_popup(app.translate("err_invalid_dates", app.language))
            return

        # 4. KONWERSJA I WALIDACJA LICZB
        try:
            def parse_float(val):
                return float(val.strip().replace(',', '.'))

            absences_text = self.ids.input_absences.text.strip() or "0"
            try:
                absences = int(absences_text)
            except ValueError:
                self.show_error_popup(app.translate("err_absences_int", app.language))
                return

            pluses = parse_float(self.ids.input_pluses.text.strip() or "0.0")
            max_points = parse_float(self.ids.input_points.text.strip() or "0.0")
            duration_hours = parse_float(self.ids.input_duration.text.strip() or "0.0")

            if absences < 0 or pluses < 0 or max_points < 0 or duration_hours <= 0:
                self.show_error_popup(app.translate("err_num_positive", app.language))
                return

            duration_minutes = int(duration_hours * 60)
        except ValueError:
            self.show_error_popup(app.translate("err_num_only", app.language))
            return

        # 5. WALIDACJA GODZINY
        if not re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", start_time):
            self.show_error_popup(app.translate("err_start_time", app.language))
            return

        # 6. DNI TYGODNIA
        day_mapping = {self.ids.chk_mon: 0, self.ids.chk_tue: 1, self.ids.chk_wed: 2, 
                       self.ids.chk_thu: 3, self.ids.chk_fri: 4, self.ids.chk_sat: 5, self.ids.chk_sun: 6}
        selected_days = [val for chk, val in day_mapping.items() if chk.active]
        
        if not selected_days:
            self.show_error_popup(app.translate("err_select_day", app.language))
            return

        # 7. ZAPIS DO BAZY
        db_connection = db.get_connection()
        cursor = db_connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO subjects (name, teacher, grading_rules, max_absences, max_activity_points, max_colloquium_points, term_start, term_end) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (subject_name, teacher_name, pass_conditions, absences, pluses, max_points, start_date, end_date))
            
            new_subject_id = cursor.lastrowid 
            for day_int in selected_days:
                cursor.execute("INSERT INTO schedule (subject_id, day_of_week, start_time, duration_minutes) VALUES (?, ?, ?, ?)", 
                               (new_subject_id, day_int, start_time, duration_minutes))
            db_connection.commit()
            self.clear_form()
            print(f"SUKCES! Zapisano przedmiot '{subject_name}' oraz jego harmonogram do bazy danych.")
        except Exception as e:
            db_connection.rollback()
            error_prefix = app.translate("err_db_save", app.language)
            self.show_error_popup(f"{error_prefix}{str(e)}")
    
    def clear_form(self):
        self.ids.input_name.text = ""
        self.ids.input_teacher.text = ""
        self.ids.input_conditions.text = ""
        self.ids.input_absences.text = ""
        self.ids.input_pluses.text = ""
        self.ids.input_points.text = ""
        self.ids.input_time.text = ""
        self.ids.input_duration.text = ""
        self.ids.input_start_date.text = ""
        self.ids.input_end_date.text = ""
        
        for checkbox in [self.ids.chk_mon, self.ids.chk_tue, self.ids.chk_wed, 
                         self.ids.chk_thu, self.ids.chk_fri, self.ids.chk_sat, self.ids.chk_sun]:
            checkbox.active = False

    def show_error_popup(self, error_message):
        app = App.get_running_app()
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        label = Label(text=error_message, halign='center', valign='middle')
        label.bind(size=label.setter('text_size'))
        content.add_widget(label)

        btn_ok = Factory.DangerButton()
        btn_ok.text = app.translate("btn_will_fix", app.language)
        btn_ok.size_hint_y = None
        btn_ok.height = dp(40)
        content.add_widget(btn_ok)

        popup = Popup(
            title=app.translate("popup_error_form_title", app.language), 
            content=content, 
            size_hint=(None, None), size=(dp(400), dp(200)), 
            auto_dismiss=True
        )
        btn_ok.bind(on_release=popup.dismiss)
        popup.open()

'''
class AddSubjectTestApp(App):
    def build(self):
        Factory.register('CustomButtonWidget', cls=CustomButtonWidget)
        Builder.load_file(kv_path)
        return AddSubjectScreen()


if __name__ == "__main__":
    from kivy.core.window import Window
    Window.clearcolor = (0.08, 0.12, 0.18, 1)
    Window.minimum_width = 1000
    Window.minimum_height = 700
    
    db.init_db()
    AddSubjectTestApp().run()
'''