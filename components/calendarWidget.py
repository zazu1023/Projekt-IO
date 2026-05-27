from datetime import date, timedelta

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty

from Widgets.Brick import CalendarBrickData
from Widgets.Button import ButtonStyle
from KivyWidgets.KivyBrickBackend import KivyBrickBackend


class SafeKivyBrickBackend(KivyBrickBackend):
    def bind_hover(self, on_enter=None, on_leave=None):
        pass


class CalendarWidget(BoxLayout):
    week_label = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_week_start = self.get_monday(date.today())

        self.events = [
            {
                "date": date(2026, 5, 12),
                "data": CalendarBrickData(
                    id="1",
                    title="SK",
                    start_time="10:30",
                    end_time="1.5 h",
                    category_id="IO"
                )
            },
            {
                "date": date(2026, 5, 13),
                "data": CalendarBrickData(
                    id="2",
                    title="3referfd",
                    start_time="08:00",
                    end_time="1.5 h",
                    category_id="IO"
                )
            },
            {
                "date": date(2026, 5, 14),
                "data": CalendarBrickData(
                    id="3",
                    title="3referfd",
                    start_time="08:00",
                    end_time="1.5 h",
                    category_id="IO"
                )
            },
        ]

    def get_monday(self, selected_date):
        return selected_date - timedelta(days=selected_date.weekday())

    def on_kv_post(self, base_widget):
        self.refresh_calendar()

    def refresh_calendar(self):
        week_end = self.current_week_start + timedelta(days=6)
        self.week_label = f"{self.current_week_start} - {week_end}"

        self.ids.days_box.clear_widgets()

        for i in range(7):
            day_date = self.current_week_start + timedelta(days=i)
            day_column = self.create_day_column(day_date)
            self.ids.days_box.add_widget(day_column)

    def create_day_column(self, day_date):
        column = BoxLayout(
            orientation="vertical",
            padding=6,
            spacing=8
        )

        day_names = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Ndz"]

        header = Label(
            text=f"{day_names[day_date.weekday()]}\n{day_date.strftime('%m-%d')}",
            size_hint_y=None,
            height=45,
            color=(1, 1, 1, 1),
            bold=True,
            halign="center",
            valign="middle"
        )
        header.bind(size=lambda instance, value: setattr(instance, "text_size", instance.size))
        column.add_widget(header)

        events_for_day = self.get_events_for_day(day_date)

        if not events_for_day:
            empty = Label(
                text="-",
                size_hint_y=None,
                height=35,
                color=(1, 1, 1, 0.5)
            )
            column.add_widget(empty)
        else:
            for event in events_for_day:
                brick = self.create_brick(event)
                column.add_widget(brick)

        column.add_widget(BoxLayout())

        return column

    def get_events_for_day(self, day_date):
        result = []

        for event in self.events:
            if event["date"] == day_date:
                result.append(event["data"])

        return result

    def create_brick(self, event_data):
        style = ButtonStyle(
            bg_color=(45 / 255, 88 / 255, 140 / 255, 1),
            text_color=(1, 1, 1, 1)
        )

        backend = SafeKivyBrickBackend()

        return backend.create(
            data=event_data,
            style=style,
            on_click=lambda: self.on_event_click(event_data)
        )

    def on_event_click(self, event_data):
        print("Kliknięto:", event_data.title)

    def previous_week(self):
        self.current_week_start -= timedelta(days=7)
        self.refresh_calendar()

    def next_week(self):
        self.current_week_start += timedelta(days=7)
        self.refresh_calendar()

    def current_week(self):
        self.current_week_start = self.get_monday(date.today())
        self.refresh_calendar()