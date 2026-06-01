from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
from kivy.properties import StringProperty , NumericProperty
from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from KivyWidgets.KivyBrickBackend import DashboardBrick2

from Models.SubjectData import SubjectData

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
        
       
        rows = app.repo.get_all_subjects()
        
        # 3. Pętla budująca kafelki
        for row in rows:

            przedmiot = SubjectData.create_from_db_dict(row)
  
            if przedmiot.status == "completed":
                nowy_kafelek = SubjectGreenrep(subject_obj=przedmiot)
            elif przedmiot.status == "inprogress":
                nowy_kafelek = SubjectRedrep(subject_obj=przedmiot)
            elif przedmiot.status == "atrisk":
                nowy_kafelek = SubjectWhiterep(subject_obj=przedmiot)
            elif przedmiot.status == "failed":
                nowy_kafelek = SubjectWhiterep(subject_obj=przedmiot)
            else:
                print(f"expected status value but got: {przedmiot.status}")
                raise ValueError()
    
            self.ids.grid_przedmiotow.add_widget(nowy_kafelek)
