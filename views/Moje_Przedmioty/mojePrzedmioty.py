from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App

from KivyWidgets.KivyBrickBackend import DashboardBrick

from Models.SubjectData import SubjectData


class SubjectGreen(DashboardBrick):
    pass
class SubjectRed(DashboardBrick):
    pass
class SubjectWhite(DashboardBrick):
    pass

class MojePrzedmiotyScreen(Screen):
    def on_pre_enter(self, *args):
        app = App.get_running_app()
        
        self.ids.grid_przedmiotow.clear_widgets()
        

        rows = app.repo.get_all_subjects()
        
        # 3. Pętla budująca kafelki
        for row in rows:

            przedmiot = SubjectData.create_from_db_dict(row)
  
            if przedmiot.status == "completed":
                nowy_kafelek = SubjectGreen(subject_obj=przedmiot)
            elif przedmiot.status == "inprogress":
                nowy_kafelek = SubjectWhite(subject_obj=przedmiot)
            elif przedmiot.status == "atrisk":
                nowy_kafelek = SubjectRed(subject_obj=przedmiot)
            else:
                print(f"expected status value but got: {przedmiot.status}")
                raise ValueError()
    
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