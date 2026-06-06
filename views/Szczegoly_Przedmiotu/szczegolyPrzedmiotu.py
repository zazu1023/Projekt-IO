from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex


STATUS_BTN_IDS = {
    'completed': 'btn_status_completed',
    'inprogress': 'btn_status_inprogress',
    'atrisk': 'btn_status_atrisk',
    'failed': 'btn_status_failed',
}


class SzczegolyPrzedmiotuScreen(Screen):
    selectedSubject = ObjectProperty(None, allownone=True, rebind=True)
    repo = ObjectProperty(None)
    app = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.selectedSubject = None

    def on_pre_enter(self):
        self._populate_form()

    def _populate_form(self):
        subject = self.selectedSubject
        if not subject:
            return

        self.ids.input_title.text = str(subject.title or "")
        self.ids.input_teacher.text = str(subject.teacher or "")
        self.ids.input_conditions.text = str(subject.conditions or "")
        self.ids.input_max_absences.text = str(subject.max_absences)
        self.ids.input_max_pluses.text = str(subject.max_pluses)
        self.ids.input_max_colloquium_pluses.text = str(subject.max_colloquium_pluses)
        self.ids.input_note.text = str(subject.note or "")

        self._sync_status_buttons()

    def _sync_status_buttons(self):
        for btn_id in STATUS_BTN_IDS.values():
            self.ids[btn_id].state = 'normal'

        if not self.selectedSubject:
            return

        active_btn = STATUS_BTN_IDS.get(self.selectedSubject.status)
        if active_btn:
            self.ids[active_btn].state = 'down'

    def get_status_text_rgba(self, status):
        colors = self.app.theme.SubjectColors
        status_colors = {
            'completed': colors.SUBJECT_BG_COLOR_COMPLETED,
            'inprogress': colors.SUBJECT_BG_COLOR_INPROGRESS,
            'atrisk': colors.SUBJECT_BG_COLOR_ATRISK,
            'failed': colors.SUBJECT_BG_COLOR_FAILED,
        }
        fallback = colors.SUBJECT_BG_COLOR_FAILED
        return get_color_from_hex(status_colors.get(status, fallback))

    def change_absences(self, diff: int) -> None:
        if self.selectedSubject:
            self.selectedSubject.absences = self.repo.add_absence(
                subject_id=self.selectedSubject.id,
                amount=diff,
            )

    def change_status(self, new_status) -> None:
        if not self.selectedSubject:
            return

        if new_status not in STATUS_BTN_IDS:
            raise ValueError("Invalid status name")

        if self.selectedSubject.status == new_status:
            return

        self.selectedSubject.status = new_status
        self.repo.set_status(subject_id=self.selectedSubject.id, new_status=new_status)
        self._sync_status_buttons()

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
