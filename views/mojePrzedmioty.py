from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
class MojePrzedmiotyScreen(Screen):
    pass

class SzczegolyPrzedmiotuScreen(Screen):
    selectedSubject = ObjectProperty(None, allownone=True)

    def on_pre_enter(self):
        if self.selectedSubject:
            # Ręczne odświeżenie pól tekstowych po wejściu w nowy kafelek
            self.ids.input_title.text = self.selectedSubject.title
            self.ids.input_teacher.text = self.selectedSubject.teacher
            self.ids.input_note.text = self.selectedSubject.note