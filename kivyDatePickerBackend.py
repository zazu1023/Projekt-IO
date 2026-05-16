from datePicker import DatePickerBackend, DatePickerStyle
from datetime import date
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

class KivyDatePickerBackend(DatePickerBackend):
    def __init__(self):
        self.button=None
        self.popup=None

    def create(self, selected_date: date, style: DatePickerStyle):
        self.button= Button(text=str(selected_date))
        self.button.bind(on_press=self.openCalendar)
        return self.button
    
    def setDate(self, selected_date: date):
        self.button.text = str(selected_date)

    def openCalendar(self, instance):
        layout = GridLayout(cols=7)
        for day in range(1,32):
            day_button = Button(text=str(day))
            day_button.bind(on_press=self.selectDay)
            layout.add_widget(day_button)
        self.popup = Popup(title="Choose date", content=layout, size_hint=(0.8, 0.8))
        self.popup.open()
    
    def selectDay(self, instance):
        day=int(instance.text)
        selected_date = date(2026,5,day)
        self.setDate(selected_date)
        self.popup.dismiss()