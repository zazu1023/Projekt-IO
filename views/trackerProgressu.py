from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

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
    
    def __init__(self, title, max_points, pluses, exam, **kwargs):
        super().__init__(**kwargs)
        self.title_text = title
        self.max_points = max_points
        self.pluses_val = pluses
        self.exam_val = exam
        
        style = ProgressBarStyle(bg_color=(1,1,1,1), fill_color=(0,0,0,1), text_color=(0,0,0,1))
        
        self.pb = ProgressBar(
            value=self.get_total(), 
            max_value=self.max_points, 
            backend=KivyProgressBarBackend(), 
            style=style
        )
        self.ids.progress_container.add_widget(self.pb.render())
        self.update_texts()

    def get_total(self):
        return self.pluses_val + self.exam_val

    def change_pluses(self, amount):
        new_val = self.pluses_val + amount
        # ZMIANA: Pozwalamy rosnąć punktom do woli, byle nie zeszły poniżej 0
        if new_val >= 0:
            self.pluses_val = new_val
            self.update_ui()

    def change_exam(self, amount):
        new_val = self.exam_val + amount
        # ZMIANA: Tutaj również usunięto blokadę powyżej max_points
        if new_val >= 0:
            self.exam_val = new_val
            self.update_ui()

    def update_ui(self):
        # Wasza klasa ProgressBar domyślnie "przycina" wartość do maksa 
        # (w pliku progressBar.py masz _validate_values), więc suwak sam się zablokuje na końcu.
        self.pb.updateValue(self.get_total()) 
        self.update_texts()

    def update_texts(self):
        total = self.get_total()
        
        # Zabezpieczamy procenty na karcie głównej, żeby zatrzymały się na 100%
        capped_total = min(total, self.max_points)
        percentage = round((capped_total / self.max_points) * 100, 1) if self.max_points > 0 else 0.0
        
        # Nawet jak zdobędziesz 35/30, pokaże "Zdobyto 35 z 30 punktów (100.0%)"
        self.points_text = f"Zdobyto {total} z {self.max_points} punktów ({percentage}%)"

class TrackerProgresuScreen(Screen):
    def on_enter(self, *args):
        self.load_cards()

    def load_cards(self):
        self.ids.cards_container.clear_widgets()
        
        subjects = [
            {"title": "3referfd (efefedfef)", "max": 5.0, "pluses": 3, "exam": 0},
            {"title": "ASD (JŚW)", "max": 30.0, "pluses": 10, "exam": 17},
            {"title": "IO (xjsx)", "max": 11.0, "pluses": 6, "exam": 1},
        ]
        
        for s in subjects:
            card = ProgressCard(title=s["title"], max_points=s["max"], pluses=s["pluses"], exam=s["exam"])
            self.ids.cards_container.add_widget(card)