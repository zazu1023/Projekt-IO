from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from Widgets.progressBar import ProgressBar, ProgressBarStyle
from KivyWidgets.kivyProgressBarBackend import KivyProgressBarBackend

class SubjectCard(BoxLayout):
    title = StringProperty('')
    teacher = StringProperty('')
    status = StringProperty('')
    rules = StringProperty('')
    absences = StringProperty('')

class RepozytoriumZasadScreen(Screen):
    repo = ObjectProperty(None)
    app = ObjectProperty(None)

    def on_pre_enter(self):
        self.populate_cards()
        

    def populate_cards(self):
        self.ids.rules_container.clear_widgets()
        
        style = ProgressBarStyle(
            bg_color=get_color_from_hex("#3b3232"),
            fill_color=(1, 1, 1, 1), 
            text_color=(1, 1, 1, 1)
        )

        try:
            subjects = self.repo.get_all_subjects()

            for s in subjects:
                curr = s.get('current_absences', 0)
                raw_mx = s.get('max_absences', 0)
                mx = raw_mx if raw_mx > 0 else 1
                
                card = SubjectCard(
                    title=str(s.get('name', 'Brak')),
                    teacher=str(s.get('teacher', 'Brak')),
                    status=str(s.get('status', 'Brak')),
                    absences=f"{curr} / {mx}",
                    rules=str(s.get('grading_rules', 'Brak zasad'))
                )
                
                def add_progress_bar(dt, card=card, curr=curr, mx=mx, style=style):
                    backend = KivyProgressBarBackend()
                    pb_logic = ProgressBar(curr, mx, backend, style)
                    card.ids.progress_container.add_widget(pb_logic.render())

                Clock.schedule_once(add_progress_bar, 0.1)
                
                self.ids.rules_container.add_widget(card)
        except Exception as e:
            print(f"Błąd przy wyświetlaniu: {e}")
