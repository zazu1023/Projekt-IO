import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock, patch
from KivyWidgets.calendarWidget import CalendarWidget
from Widgets.Brick import CalendarBrickData

@pytest.fixture
def mock_calendar():
    with patch('KivyWidgets.calendarWidget.CalendarWidget.refresh_calendar'):
        app = MagicMock()
        app.language = "pl"
        repo = MagicMock()
        cal = CalendarWidget()
        cal.app = app
        cal.repo = repo
        cal.ids = {'days_box': MagicMock()}
        return cal

def test_get_monday(mock_calendar):
    tuesday = date(2026, 5, 26)
    assert mock_calendar.get_monday(tuesday) == date(2026, 5, 25)

def test_navigation_next(mock_calendar):
    start = mock_calendar.current_week_start
    mock_calendar.next_week()
    assert mock_calendar.current_week_start == start + timedelta(days=7)

def test_navigation_prev(mock_calendar):
    start = mock_calendar.current_week_start
    mock_calendar.previous_week()
    assert mock_calendar.current_week_start == start - timedelta(days=7)

def test_current_week(mock_calendar):
    mock_calendar.next_week()
    mock_calendar.current_week()
    assert mock_calendar.current_week_start == date.today() - timedelta(days=date.today().weekday())

def test_events_filtering(mock_calendar):
    day = date(2026, 5, 30)
    events = mock_calendar.get_events_for_day(day)
    assert len(events) == 1
    assert events[0].title == "IO"

def test_no_events_day(mock_calendar):
    day = date(2020, 1, 1)
    assert mock_calendar.get_events_for_day(day) == []

def test_week_label_update(mock_calendar):
    with patch.object(mock_calendar, 'create_day_column', return_value=MagicMock()):
        mock_calendar.refresh_calendar()
        week_end = mock_calendar.current_week_start + timedelta(days=6)
        assert mock_calendar.week_label == f"{mock_calendar.current_week_start} - {week_end}"

def test_multiple_events_same_day(mock_calendar):
    day = date(2026, 5, 30)
    mock_calendar.events.append({"date": day, "data": "Extra"})
    events = mock_calendar.get_events_for_day(day)
    assert len(events) >= 2

def test_current_week_logic(mock_calendar):
    mock_calendar.current_week_start = date(2020, 1, 1)
    mock_calendar.current_week()
    expected = date.today() - timedelta(days=date.today().weekday())
    assert mock_calendar.current_week_start == expected

def test_events_empty_date(mock_calendar):
    assert mock_calendar.get_events_for_day(date(1900, 1, 1)) == []

def test_language_binding(mock_calendar):
    mock_calendar.on_kv_post(None)
    mock_calendar.app.bind.assert_called_once()

def test_multiple_events_day(mock_calendar):
    day = date(2026, 5, 12)
    events = mock_calendar.get_events_for_day(day)
    assert len(events) >= 3

def test_reset_to_today(mock_calendar):
    mock_calendar.current_week_start = date(2000, 1, 1)
    mock_calendar.current_week()
    expected = date.today() - timedelta(days=date.today().weekday())
    assert mock_calendar.current_week_start == expected

def test_far_future_date(mock_calendar):
    future = date(2050, 1, 1)
    assert mock_calendar.get_monday(future) == date(2049, 12, 27)

@pytest.mark.parametrize("day, expected", [
    (date(2026, 5, 25), date(2026, 5, 25)),
    (date(2026, 5, 31), date(2026, 5, 25)),
])
def test_get_monday_cases(mock_calendar, day, expected):
    assert mock_calendar.get_monday(day) == expected

def test_unknown_event_type(mock_calendar):
    event = CalendarBrickData(id="1", title="Test", start_time="10:00", end_time="1h", category_id="test", event_type="???")
    brick = mock_calendar.create_brick(event, date(2026, 5, 30))
    assert brick.style.bg_color is not None

def test_leap_year_boundary(mock_calendar):
    day = date(2028, 2, 29)
    assert mock_calendar.get_monday(day) == date(2028, 2, 28)

def test_empty_note_string(mock_calendar):
    mock_calendar.repo.get_daily_note.return_value = "   "
    event = CalendarBrickData(id="1", title="Test", start_time="10:00", end_time="1h", category_id="test")
    brick = mock_calendar.create_brick(event, date(2026, 5, 30))
    assert brick.has_note is False

def test_date_type_safety(mock_calendar):
    with pytest.raises(AttributeError):
        mock_calendar.get_monday(12345)

def test_multiple_events_order(mock_calendar):
    day = date(2026, 5, 30)
    mock_calendar.events = [
        {"date": day, "data": CalendarBrickData(id="1", title="A", start_time="08:00", end_time="1h", category_id="test")},
        {"date": day, "data": CalendarBrickData(id="2", title="B", start_time="09:00", end_time="1h", category_id="test")}
    ]
    events = mock_calendar.get_events_for_day(day)
    assert len(events) == 2
