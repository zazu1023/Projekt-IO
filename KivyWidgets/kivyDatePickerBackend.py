import calendar
from datetime import date

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from Widgets.datePicker import DatePickerBackend, DatePickerStyle

class KivyDatePickerBackend(DatePickerBackend):
    def __init__(self):
        self.root = None
        self.month_label = None
        self.calendar_layout = None
        self.confirm_button = None

        self.selected_date = None
        self.confirmed_date = None
        self.current_year = None
        self.current_month = None

    def create(self, selected_date: date, style: DatePickerStyle):
        self.selected_date=selected_date
        today = date.today()
        self.current_year = today.year
        self.current_month = today.month
        self.root=BoxLayout(
            orientation="vertical",
            spacing = 10,
            padding=20)
        header= BoxLayout(
            size_hint_y=None,
            height=50
        )
        prev_year_button = Button(text="<<", size_hint_x=0.15)
        prev_month_button = Button(text="<", size_hint_x=0.15)
        next_month_button = Button(text=">", size_hint_x=0.15)
        next_year_button = Button(text=">>", size_hint_x=0.15)
        self.month_label=Label(size_hint_x=0.4)
        prev_year_button.bind(on_press=self.previousYear)
        prev_month_button.bind(on_press=self.previousMonth)
        next_month_button.bind(on_press=self.nextMonth)
        next_year_button.bind(on_press=self.nextYear)

        header.add_widget(prev_year_button)
        header.add_widget(prev_month_button)
        header.add_widget(self.month_label)
        header.add_widget(next_month_button)
        header.add_widget(next_year_button)

        self.calendar_layout = GridLayout(cols=7)
        self.confirm_button = Button(
            text="Zatwierdź",
            size_hint_y=None,
            height=50
        )
        self.confirm_button.bind(on_press=self.confirmDate)
        self.root.add_widget(header)
        self.root.add_widget(self.calendar_layout)
        self.root.add_widget(self.confirm_button)
        self.refreshCalendar()
        return self.root
    
    def setDate(self, selected_date: date):
        self.selected_date=selected_date
        self.refreshCalendar()

    def openCalendar(self, instance):
        return self.root
    
    def refreshCalendar(self):
        self.calendar_layout.clear_widgets()
        self.month_label.text = date(
            self.current_year,
            self.current_month,
            1
        ).strftime("%B %Y")
        days_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for name in days_names:
            self.calendar_layout.add_widget(Label(text=name))
        month_days=calendar.monthcalendar(
            self.current_year,
            self.current_month
        )
        for week in month_days:
            for day in week:
                if day==0:
                    self.calendar_layout.add_widget(Label(text=""))
                else:
                    current_date = date(
                        self.current_year,
                        self.current_month,
                        day
                    )
                    day_button = Button(text=str(day))
                    if self.selected_date == current_date:
                        day_button.background_color = (1, 0.3, 0.1, 1)
                    day_button.bind(on_press=self.selectDay)
                    self.calendar_layout.add_widget(day_button)

    def selectDay(self, instance):
        day=int(instance.text)
        self.selected_date = date(
            self.current_year,
            self.current_month,
            day
        )
        self.refreshCalendar()

    def confirmDate(self, instance):
        print("Zatwierdzona data:",self.selected_date)

    def previousMonth(self,instance):
        if self.current_month==1:
            self.current_month=12
            self.current_year-=1
        else:
            self.current_month-=1
        self.refreshCalendar()
    def nextMonth(self, instance):
        if self.current_month==12:
            self.current_month=1
            self.current_year+=1
        else:
            self.current_month+=1
        self.refreshCalendar()
    def previousYear(self,instance):
        self.current_year-=1
        self.refreshCalendar()
    def nextYear(self,instance):
        self.current_year+=1
        self.refreshCalendar()
