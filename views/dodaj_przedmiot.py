import os
import re
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.factory import Factory
from kivymd.uix.pickers import MDDatePicker
from kivymd.app import MDApp
from KivyWidgets.KivyButtonBackend import CustomButtonWidget
import database as db

# Ścieżka do pliku .kv
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
kv_path = os.path.join(parent_dir, 'kv', 'dodaj_przedmiot.kv')

class AddSubjectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_date_field = None  # przechowuje informację, które pole daty aktualizujemy

    def open_calendar(self, field_id):
        """Otwiera kalendarz i zapamiętuje, do którego pola wpisać wynik."""
        self.active_date_field = field_id
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        """Wstawia wybraną datę do odpowiedniego pola."""
        if self.active_date_field == 'start':
            self.ids.input_start_date.text = str(value)
        elif self.active_date_field == 'end':
            self.ids.input_end_date.text = str(value)

    def save_subject(self):
        """Zbiera dane, waliduje, formatuje i zapisuje do relacyjnej bazy danych."""
        # 1. POBIERANIE TEKSTÓW Z UI
        subject_name = self.ids.input_name.text.strip()
        teacher_name = self.ids.input_teacher.text.strip()
        pass_conditions = self.ids.input_conditions.text.strip()
        
        # 2. POBIERANIE I KONWERSJA LICZB (puste pole = 0)
        try:
            absences = int(self.ids.input_absences.text.strip() or 0)
            pluses = float(self.ids.input_pluses.text.strip() or 0.0)
            max_points = float(self.ids.input_points.text.strip() or 0.0)
            
            duration_hours = float(self.ids.input_duration.text.strip() or 1.5)
            duration_minutes = int(duration_hours * 60) # baza oczekuje minut
        except ValueError:
            self.show_error_popup("Pola liczbowe mogą zawierać tylko cyfry\n(np. 1.5 dla półtorej godziny).")
            return
        
        # 3. POBIERANIE DAT I CZASU
        start_time = self.ids.input_time.text.strip()
        term_start = self.ids.input_start_date.text.strip()
        term_end = self.ids.input_end_date.text.strip()

        # 4. WALIDACJA FORMULARZA
        if not subject_name:
            self.show_error_popup("Nazwa przedmiotu jest wymagana!")
            return

        if not re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", start_time):
            self.show_error_popup("Godzina startu musi być w formacie HH:MM\n(np. 08:00)")
            return

        # 5. MAPOWANIE DNI TYGODNIA NA LICZBY (Zgodnie z bazą: 0=Pon, 6=Niedz)
        day_mapping = {
            self.ids.chk_mon: 0,
            self.ids.chk_tue: 1,
            self.ids.chk_wed: 2,
            self.ids.chk_thu: 3,
            self.ids.chk_fri: 4,
            self.ids.chk_sat: 5,
            self.ids.chk_sun: 6
        }
        
        selected_days = []
        for checkbox, day_int in day_mapping.items():
            if checkbox.active:
                selected_days.append(day_int)
                
        if not selected_days:
            self.show_error_popup("Zaznacz co najmniej jeden dzień zajęć!")
            return

        # ==============================================================
        # 6. ZAPIS DO RELACYJNEJ BAZY DANYCH
        # ==============================================================
        db_connection = db.get_connection()
        cursor = db_connection.cursor()
        
        try:
            query_subject = """
                INSERT INTO subjects 
                (name, teacher, grading_rules, max_absences, max_activity_points, max_colloquium_points, term_start, term_end) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_subject, (
                subject_name, teacher_name, pass_conditions, 
                absences, pluses, max_points, term_start, term_end
            ))
            
            new_subject_id = cursor.lastrowid 
            query_schedule = """
                INSERT INTO schedule 
                (subject_id, day_of_week, start_time, duration_minutes)
                VALUES (?, ?, ?, ?)
            """
            for day_int in selected_days:
                cursor.execute(query_schedule, (new_subject_id, day_int, start_time, duration_minutes))

            db_connection.commit()
            
            self.clear_form()
            print(f"SUKCES! Zapisano przedmiot '{subject_name}' oraz jego harmonogram do bazy danych.")

        except Exception as e:
            db_connection.rollback()
            self.show_error_popup(f"Wystąpił błąd podczas zapisu do bazy:\n{str(e)}")
    
    def clear_form(self):
        """Czyści formularz po pomyślnym dodaniu przedmiotu."""
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
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        label = Label(text=error_message, halign='center', valign='middle')
        label.bind(size=label.setter('text_size'))
        content.add_widget(label)

        btn_ok = Factory.DangerButton()
        btn_ok.text = "Poprawię"
        btn_ok.size_hint_y = None
        btn_ok.height = dp(40)
        content.add_widget(btn_ok)

        popup = Popup(
            title="Błąd formularza", 
            content=content, 
            size_hint=(None, None), size=(dp(400), dp(200)), 
            auto_dismiss=True
        )
        btn_ok.bind(on_release=popup.dismiss)
        popup.open()

# ==============================================================
# BLOK TESTOWY - DO URUCHAMIANIA WIDOKU SAMODZIELNIE
# (Usuń lub zakomentuj ten blok przed integracją z main.py)
# ==============================================================
class AddSubjectTestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        # Rejestrujemy CustomButtonWidget (wymagane dla przycisków)
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