import pytest
from unittest.mock import MagicMock, patch
from views.dodaj_przedmiot import AddSubjectScreen

# =====================================================================
# KONFIGURACJA ŚRODOWISKA TESTOWEGO
# =====================================================================

@pytest.fixture
def mock_screen():
    screen = MagicMock()
    
    # domyślne, poprawne dane
    screen.ids.input_name.text = "Programowanie Obiektowe"
    screen.ids.input_teacher.text = "Inż. Anna Nowak"
    screen.ids.input_conditions.text = "Projekt i kolokwium"
    screen.ids.input_absences.text = "2"
    screen.ids.input_pluses.text = "3"
    screen.ids.input_points.text = "50"
    screen.ids.input_time.text = "10:30"
    screen.ids.input_duration.text = "2.0"
    screen.ids.input_start_date.text = "2026-10-05"
    screen.ids.input_end_date.text = "2027-01-30"

    # domyślnie zaznaczona środa
    screen.ids.chk_mon.active = False
    screen.ids.chk_tue.active = False
    screen.ids.chk_wed.active = True
    screen.ids.chk_thu.active = False
    screen.ids.chk_fri.active = False
    screen.ids.chk_sat.active = False
    screen.ids.chk_sun.active = False

    screen.save_subject = AddSubjectScreen.save_subject.__get__(screen, AddSubjectScreen)
    return screen

@pytest.fixture
def mock_db():
    with patch('views.dodaj_przedmiot.db.get_connection') as mock_get_conn:
        db_connection = MagicMock()
        db_cursor = MagicMock()
        db_cursor.lastrowid = 42 
        db_connection.cursor.return_value = db_cursor
        mock_get_conn.return_value = db_connection
        yield db_connection


def test_save_valid_data(mock_screen, mock_db):
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_not_called()
    mock_db.commit.assert_called_once()
    assert mock_db.cursor().execute.call_count == 2

def test_save_all_days_selected(mock_screen, mock_db):
    for cb in ['chk_mon', 'chk_tue', 'chk_wed', 'chk_thu', 'chk_fri', 'chk_sat', 'chk_sun']:
        getattr(mock_screen.ids, cb).active = True
    mock_screen.save_subject()
    assert mock_db.cursor().execute.call_count == 8 # 1 (subjects) + 7 (schedule)

def test_empty_name(mock_screen, mock_db):
    mock_screen.ids.input_name.text = ""
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_called()
    mock_db.commit.assert_not_called()

@pytest.mark.parametrize("bad_time", ["8:30", "24:00", "23:60", "abc", ""])
def test_invalid_time_formats(mock_screen, mock_db, bad_time):
    mock_screen.ids.input_time.text = bad_time
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_called()

@pytest.mark.parametrize("field, bad_val", [
    ("input_absences", "abc"),
    ("input_pluses", "1.2.3"),
    ("input_duration", "5,5,5")
])
def test_invalid_numeric_formats(mock_screen, mock_db, field, bad_val):
    getattr(mock_screen.ids, field).text = bad_val
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_called()

def test_no_day_selected(mock_screen, mock_db):
    for cb in ['chk_mon', 'chk_tue', 'chk_wed', 'chk_thu', 'chk_fri', 'chk_sat', 'chk_sun']:
        getattr(mock_screen.ids, cb).active = False

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()
    mock_db.commit.assert_not_called()

def test_name_only_spaces(mock_screen, mock_db):
    mock_screen.ids.input_name.text = "     "

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()
    mock_db.commit.assert_not_called()

def test_empty_teacher(mock_screen, mock_db):
    mock_screen.ids.input_teacher.text = ""

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()

def test_teacher_only_spaces(mock_screen, mock_db):
    mock_screen.ids.input_teacher.text = "     "

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()

def test_min_valid_time(mock_screen, mock_db):
    mock_screen.ids.input_time.text = "00:00"

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_not_called()

@pytest.mark.parametrize("bad_time", [
    "9:00",
    "09:0",
    "9:0"
])
def test_time_without_leading_zeros(mock_screen, mock_db, bad_time):
    mock_screen.ids.input_time.text = bad_time

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()

def test_zero_duration(mock_screen, mock_db):
    mock_screen.ids.input_duration.text = "0"

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()

@pytest.mark.parametrize("bad_date", [
    "05-10-2026",
    "2026/10/05",
    "abc",
    ""
])
def test_invalid_start_date(mock_screen, mock_db, bad_date):
    mock_screen.ids.input_start_date.text = bad_date

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()

@pytest.mark.parametrize("bad_date", [
    "30-01-2027",
    "2027/01/30",
    "abc",
    ""
])
def test_invalid_end_date(mock_screen, mock_db, bad_date):
    mock_screen.ids.input_end_date.text = bad_date

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()

def test_end_date_before_start_date(mock_screen, mock_db):
    mock_screen.ids.input_start_date.text = "2027-01-30"
    mock_screen.ids.input_end_date.text = "2026-10-05"

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_called()
    mock_db.commit.assert_not_called()

def test_numbers_with_spaces(mock_screen, mock_db):
    mock_screen.ids.input_points.text = " 50 "

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_not_called()

def test_polish_characters(mock_screen, mock_db):
    mock_screen.ids.input_name.text = "Zaawansowane Algorytmy ĄĆĘŁŃÓŚŹŻ"
    mock_screen.ids.input_teacher.text = "dr hab. Żółć"

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_not_called()

def test_emoji_in_name(mock_screen, mock_db):
    mock_screen.ids.input_name.text = "Programowanie 🚀"

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_not_called()

def test_large_duration(mock_screen, mock_db):
    mock_screen.ids.input_duration.text = "24"

    mock_screen.save_subject()

    mock_screen.show_error_popup.assert_not_called()

@pytest.mark.parametrize("field, val", [
    ("input_absences", "-1"),
    ("input_pluses", "-0.01"),
    ("input_points", "-50"),
    ("input_duration", "-1")
])
def test_negative_values(mock_screen, mock_db, field, val):
    getattr(mock_screen.ids, field).text = val
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_called()
    mock_db.commit.assert_not_called()

def test_zero_values(mock_screen, mock_db):
    mock_screen.ids.input_absences.text = "0"
    mock_screen.ids.input_pluses.text = "0"
    mock_screen.ids.input_points.text = "0"
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_not_called()
    mock_db.commit.assert_called()

def test_extreme_large_values(mock_screen, mock_db):
    mock_screen.ids.input_points.text = "2147483647" # Max int32
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_not_called()

def test_extreme_small_positive_values(mock_screen, mock_db):
    mock_screen.ids.input_points.text = "0.0000001"
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_not_called()

def test_comma_to_dot_conversion(mock_screen, mock_db):
    mock_screen.ids.input_duration.text = "1,75"
    mock_screen.save_subject()
    
    # 1.75 * 60 = 105 minut
    duration_min = mock_db.cursor().execute.call_args_list[1][0][1][3]
    assert duration_min == 105

def test_very_long_inputs(mock_screen, mock_db):
    """Testuje, czy baza przyjmuje długie teksty (name/teacher)."""
    long_str = "A" * 500
    mock_screen.ids.input_name.text = long_str
    mock_screen.ids.input_teacher.text = long_str
    mock_screen.save_subject()
    mock_screen.show_error_popup.assert_not_called()
    mock_db.commit.assert_called()

def test_db_crash_rollback(mock_screen, mock_db):
    mock_db.cursor().execute.side_effect = Exception("DB Connection Lost")
    mock_screen.save_subject()
    mock_db.rollback.assert_called_once()