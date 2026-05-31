from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.app import App


LABEL_COLORS = {
            'completed': get_color_from_hex("#2ecc71"), 
            'inprogress': get_color_from_hex("#f1c40f"), 
            'atrisk': get_color_from_hex("#e74c3c"),    
            'failed': get_color_from_hex("#b6b8bb")      
        }
        

class SzczegolyPrzedmiotuScreen(Screen):
    selectedSubject = ObjectProperty(None, allownone=True,rebind=True)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selectedSubject = None
        self.app = App.get_running_app()
    def on_pre_enter(self):
        if self.selectedSubject:
            # Ręczne odświeżenie pól tekstowych po wejściu w nowy kafelek
            self.ids.input_title.text = self.selectedSubject.title
            self.ids.input_teacher.text = self.selectedSubject.teacher
            self.ids.input_note.text = self.selectedSubject.note


    def get_status_color(self , status_string) -> str:
        return LABEL_COLORS.get(status_string, get_color_from_hex("#95a5a6"))

    def change_absences(self, diff:int) -> None:
    
        if self.selectedSubject:
            self.selectedSubject.absences = self.app.repo.add_absence(subject_id = self.selectedSubject.id , amount = diff )

    def change_status(self , new_status) -> None:
        if self.selectedSubject:
            if( new_status not in ["inprogress" , "completed" , "atrisk", "failed"] ):
                raise ValueError("Invalid status name")

            if self.selectedSubject.status == new_status: return

            self.selectedSubject.status = new_status
            self.app.repo.set_status(subject_id = self.selectedSubject.id ,new_status = new_status)