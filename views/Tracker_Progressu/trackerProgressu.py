from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.factory import Factory
from kivy.utils import get_color_from_hex

from Widgets.progressBar import ProgressBar, ProgressBarStyle
from KivyWidgets.kivyProgressBarBackend import KivyProgressBarBackend

class PointControlRow(BoxLayout):
    label_text = StringProperty("")
    value_text = StringProperty("0")
    
    action_minus = ObjectProperty(None)
    action_plus = ObjectProperty(None)

    def on_minus(self):
        if self.action_minus:
            self.action_minus()

    def on_plus(self):
        if self.action_plus:
            self.action_plus()

class ProgressCard(BoxLayout):
    title_text = StringProperty("")
    points_text = StringProperty("")
    
    pluses_val = NumericProperty(0)
    exam_val = NumericProperty(0)
    
    def __init__(self, subject_id, name, teacher, max_activity, current_activity, max_colloquium, current_colloquium, repo=None, app=None, **kwargs):
        super().__init__(**kwargs)
        self.subject_id = subject_id
        self.repo = repo
        self.app = app
        
        if teacher:
            self.title_text = f"{name} ({teacher})"
        else:
            self.title_text = name
            
        self.pluses_val = int(current_activity) if current_activity else 0
        self.exam_val = int(current_colloquium) if current_colloquium else 0
        
        max_act = max_activity if max_activity else 0
        max_col = max_colloquium if max_colloquium else 0
        self.max_points = max_act + max_col
        
        if self.max_points <= 0:
            self.max_points = 100
            
        style = ProgressBarStyle(
            bg_color=get_color_from_hex("#c4c4c4"),
            fill_color=get_color_from_hex("#1c4271"),
            text_color=(1, 1, 1, 1)
        )
        self.pb = ProgressBar(
            value=self.get_total(), 
            max_value=self.max_points, 
            backend=KivyProgressBarBackend(), 
            style=style
        )
        self.ids.progress_container.add_widget(self.pb.render())
        
        if self.app:
            self.app.bind(language=self.on_language_change)
        
        self.update_texts()

    def on_language_change(self, instance, lang):
        self.update_texts()

    def get_total(self):
        return self.pluses_val + self.exam_val

    def save_to_db(self):
        conn = self.repo.get_db_connection()
        conn.execute('''
            UPDATE subjects 
            SET current_activity_points = ?, current_colloquium_points = ? 
            WHERE id = ?
        ''', (self.pluses_val, self.exam_val, self.subject_id))
        conn.commit()

    def change_pluses(self, amount):
        new_val = self.pluses_val + amount
        if new_val >= 0:
            self.pluses_val = new_val
            self.save_to_db() 
            self.update_ui()

    def change_exam(self, amount):
        new_val = self.exam_val + amount
        if new_val >= 0:
            self.exam_val = new_val
            self.save_to_db() 
            self.update_ui()

    def update_ui(self):
        self.pb.updateValue(self.get_total()) 
        self.update_texts()

    def update_texts(self):
        total = self.get_total()
        capped_total = min(total, self.max_points)
        percentage = round((capped_total / self.max_points) * 100, 1) if self.max_points > 0 else 0.0
        
        template = self.app.translate("scored_points", self.app.language)
        if not template:
            template = "Zdobyto {total} z {max} punktów ({percent}%)"
            
        self.points_text = template.format(total=total, max=self.max_points, percent=percentage)

class TrackerProgresuScreen(Screen):
    repo = ObjectProperty(None)
    app = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.load_cards()

    def load_cards(self):
        self.ids.cards_container.clear_widgets()
        
        conn = self.repo.get_db_connection()
        
        cursor = conn.execute('''
            SELECT id, name, teacher, 
                   max_activity_points, current_activity_points, 
                   max_colloquium_points, current_colloquium_points 
            FROM subjects
        ''')
        rows = cursor.fetchall()
        
        needs_reload = False
        for row in rows:
            if (row['max_activity_points'] == 0 or row['max_activity_points'] is None) and \
               (row['max_colloquium_points'] == 0 or row['max_colloquium_points'] is None):
                
                conn.execute('''
                    UPDATE subjects 
                    SET max_activity_points = 10, max_colloquium_points = 30,
                        current_activity_points = 3, current_colloquium_points = 17
                    WHERE id = ?
                ''', (row['id'],))
                needs_reload = True
                
        if needs_reload:
            conn.commit()
            cursor = conn.execute('''
                SELECT id, name, teacher, 
                       max_activity_points, current_activity_points, 
                       max_colloquium_points, current_colloquium_points 
                FROM subjects
            ''')
            rows = cursor.fetchall()

        for row in rows:
            card = ProgressCard(
                subject_id=row['id'],
                name=row['name'],
                teacher=row['teacher'],
                max_activity=row['max_activity_points'],
                current_activity=row['current_activity_points'],
                max_colloquium=row['max_colloquium_points'],
                current_colloquium=row['current_colloquium_points'],
                repo=self.repo,
                app=self.app,
            )
            self.ids.cards_container.add_widget(card)
