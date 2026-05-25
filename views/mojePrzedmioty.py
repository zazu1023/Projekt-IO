from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
from kivy.properties import StringProperty , NumericProperty


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


class MojePrzedmiotyScreen(Screen):
    pass

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