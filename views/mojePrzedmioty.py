from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
from kivy.properties import StringProperty , NumericProperty
from kivy.app import App

from KivyWidgets.KivyBrickBackend import DashboardBrick

class SubjectData(EventDispatcher):
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




class SubjectGreen(DashboardBrick):
    pass
class SubjectRed(DashboardBrick):
    pass
class SubjectWhite(DashboardBrick):
    pass

class MojePrzedmiotyScreen(Screen):
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
                nowy_kafelek = SubjectGreen(subject_obj=przedmiot)
            elif przedmiot.status == "inprogress":
                nowy_kafelek = SubjectWhite(subject_obj=przedmiot)
            elif przedmiot.status == "atrisk":
                nowy_kafelek = SubjectRed(subject_obj=przedmiot)
            else:
                raise ValueError()
            # Dodajemy gotowy kafelek do ekranu
            self.ids.grid_przedmiotow.add_widget(nowy_kafelek)

class SzczegolyPrzedmiotuScreen(Screen):
    selectedSubject = ObjectProperty(None, allownone=True,rebind=True)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selectedSubject = SubjectData(
            title="Wybierz przedmiot", 
            teacher="Brak", 
            note=""
        )

    def on_pre_enter(self):
        if self.selectedSubject:
            # Ręczne odświeżenie pól tekstowych po wejściu w nowy kafelek
            self.ids.input_title.text = self.selectedSubject.title
            self.ids.input_teacher.text = self.selectedSubject.teacher
            self.ids.input_note.text = self.selectedSubject.note

    def increment_absences(self) -> None:
        
        if self.selectedSubject:
            self.selectedSubject.absences += 1
            print(self.selectedSubject.absences)

    def decrement_absences(self) -> None:
        if self.selectedSubject:
            self.selectedSubject.absences -= 1
            self.selectedSubject.absences = max(self.selectedSubject.absences,0) 
            print(self.selectedSubject.absences)
    def change_status(self , new_status) -> None:
        if self.selectedSubject.status == new_status: return

        self.selectedSubject.status = new_status