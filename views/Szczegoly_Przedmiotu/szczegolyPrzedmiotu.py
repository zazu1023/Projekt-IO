from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex


LABEL_COLORS = {
            'completed': get_color_from_hex("#2ecc71"), 
            'inprogress': get_color_from_hex("#f1c40f"), 
            'atrisk': get_color_from_hex("#e74c3c"),    
            'failed': get_color_from_hex("#b6b8bb")      
        }
        

class SzczegolyPrzedmiotuScreen(Screen):
    selectedSubject = ObjectProperty(None, allownone=True,rebind=True)
    repo = ObjectProperty(None)
    app = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selectedSubject = None

    def on_pre_enter(self):
        if self.selectedSubject:
            self.ids.input_title.text = str(self.selectedSubject.title or "")
            self.ids.input_teacher.text = str(self.selectedSubject.teacher or "")
            self.ids.input_conditions.text = str(getattr(self.selectedSubject, 'conditions', ''))
            self.ids.input_max_absences.text = str(self.selectedSubject.max_absences or "0")
            self.ids.input_max_pluses.text = str(getattr(self.selectedSubject, 'max_pluses', '0'))
            self.ids.input_max_colloquium_pluses.text = str(getattr(self.selectedSubject, 'max_colloquium_pluses', '0'))
            self.ids.input_note.text = str(self.selectedSubject.note or "")

            status_to_btn_id = {
                'completed': 'btn_status_completed',
                'inprogress': 'btn_status_inprogress',
                'atrisk': 'btn_status_atrisk',
                'failed': 'btn_status_failed'
            }
            
  
            btn_id = status_to_btn_id.get(self.selectedSubject.status)
            
            if btn_id:
                self.ids[btn_id].state = 'down'

    def get_status_color(self , status_string) -> str:
        return LABEL_COLORS.get(status_string, get_color_from_hex("#95a5a6"))

    def change_absences(self, diff:int) -> None:
    
        if self.selectedSubject:
            self.selectedSubject.absences = self.repo.add_absence(subject_id = self.selectedSubject.id , amount = diff )

    def change_status(self , new_status) -> None:
        if self.selectedSubject:
            if( new_status not in ["inprogress" , "completed" , "atrisk", "failed"] ):
                raise ValueError("Invalid status name")

            if self.selectedSubject.status == new_status: return

            self.selectedSubject.status = new_status
            self.repo.set_status(subject_id = self.selectedSubject.id ,new_status = new_status)

    def save_changes(self) -> None:
        if self.selectedSubject:
            title = self.ids.input_title.text
            teacher = self.ids.input_teacher.text
            conditions = self.ids.input_conditions.text
            note = self.ids.input_note.text
            max_absences = int(self.ids.input_max_absences.text or 0)
            max_pluses = float(self.ids.input_max_pluses.text or 0)
            max_colloquium_pluses = float(self.ids.input_max_colloquium_pluses.text or 0)

            self.repo.update_subject(
                subject_id=self.selectedSubject.id,
                data={
                    'title': title,
                    'teacher': teacher,
                    'conditions': conditions,
                    'note': note,
                    'max_absences': max_absences,
                    'max_pluses': max_pluses,
                    'max_colloquium_pluses': max_colloquium_pluses,
                },
            )
            print("Zapisano!")
