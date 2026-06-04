from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock  # <--- To jest kluczowe
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
    def on_pre_enter(self):
        self.populate_cards()
        

    def populate_cards(self):
        self.ids.rules_container.clear_widgets()
        app = App.get_running_app()
        
        style = ProgressBarStyle(
            bg_color=get_color_from_hex("#3b3232"),
            fill_color=(1, 1, 1, 1), 
            text_color=(1, 1, 1, 1)
        )

        try:
            subjects = app.repo.get_all_subjects()

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
                
                # Używamy Clock.schedule_once, aby dodać ProgressBar z lekkim opóźnieniem,
                # gdy karta będzie już w pełni "narysowana" i będzie miała wymiary.
                def add_progress_bar(dt, card=card, curr=curr, mx=mx, style=style):
                    backend = KivyProgressBarBackend()
                    pb_logic = ProgressBar(curr, mx, backend, style)
                    card.ids.progress_container.add_widget(pb_logic.render())

                Clock.schedule_once(add_progress_bar, 0.1) # 0.1s powinno wystarczyć
                
                self.ids.rules_container.add_widget(card)
        except Exception as e:
            print(f"Błąd przy wyświetlaniu: {e}")