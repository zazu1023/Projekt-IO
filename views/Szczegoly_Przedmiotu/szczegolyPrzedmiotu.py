from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class SzczegolyPrzedmiotuScreen(Screen):
    selectedSubject = ObjectProperty(None, allownone=True,rebind=True)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selectedSubject = None

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