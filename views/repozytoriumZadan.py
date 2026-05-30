from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
from kivy.properties import StringProperty , NumericProperty
from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from KivyWidgets.KivyBrickBackend import DashboardBrick2

class SubjectDatarep(EventDispatcher):
    title = StringProperty("")
    teacher = StringProperty("")
    note = StringProperty("")

    status = StringProperty("completed")
    absences = NumericProperty(1)
    max_absences = NumericProperty(2)
    conditions = StringProperty("bleble")
    max_pluses = NumericProperty(10.0)
    
    def __init__(self, title, teacher, note, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.teacher = teacher
        self.note = note




class SubjectGreenrep(DashboardBrick2):
    pass
class SubjectRedrep(DashboardBrick2):
    pass
class SubjectWhiterep(DashboardBrick2):
    pass

class repoScreen(Screen):
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        
        # 1. Czyścimy kontener na kafelki (żeby się nie dublowały przy ponownym wejściu)
        # Zakładam, że w pliku .kv tego ekranu masz GridLayout lub StackLayout z id: bricks_container
        self.ids.grid_przedmiotow.clear_widgets()
        
        # 2. Pobieramy listę obiektów (z bazy danych)
        wszystkie_przedmioty = app.get_subjects_from_db()
        
        # 3. Pętla budująca kafelki
        for przedmiot in wszystkie_przedmioty:
            # Tworzymy widżet kafelka i OD RAZU wstrzykujemy mu obiekt z danymi
            print(przedmiot.status)
            if przedmiot.status == "completed":
                nowy_kafelek = SubjectGreenrep(subject_obj=przedmiot)
            elif przedmiot.status == "inprogress":
                nowy_kafelek = SubjectWhiterep(subject_obj=przedmiot)
            elif przedmiot.status == "atrisk":
                nowy_kafelek = SubjectRedrep(subject_obj=przedmiot)
            else:
                raise ValueError()
            # Dodajemy gotowy kafelek do ekranu
            self.ids.grid_przedmiotow.add_widget(nowy_kafelek)

