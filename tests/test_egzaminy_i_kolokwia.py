import pytest
from unittest.mock import MagicMock, patch

# ==============================================================
# FIXTURE TLUMACZEN
# ==============================================================
@pytest.fixture(autouse=True)
def mock_app_translations():
    with patch('kivy.app.App.get_running_app') as mock_app:
        app_instance = MagicMock()
        app_instance.language = 'pl'
        
        translations = {
            "err_select_subject": "Najpierw wybierz przedmiot z listy powyżej!",
            "err_empty_event_title": "Tytuł wydarzenia nie może być pusty!",
            "err_invalid_date_format": "Data musi być w formacie RRRR-MM-DD\n(np. 2026-05-28)",
            "err_invalid_time_format": "Godzina musi być w formacie HH:MM\n(np. 14:30)"
        }
        
        app_instance.translate.side_effect = lambda key, lang: translations.get(key, key)
        mock_app.return_value = app_instance
        yield app_instance

# ==============================================================
# KONFIGURACJA ŚRODOWISKA TESTOWEGO
# ==============================================================
@pytest.fixture
def exam_screen_instance():
    with patch('kivy.lang.Builder.load_file'):
        with patch('database.get_connection') as mock_db:
            from views.Egzaminy_Kolokwia.egzaminy_i_kolokwia import ExamsAndColloquiumsScreen 
            
            screen = ExamsAndColloquiumsScreen()
            screen.ids['input_event_date'] = MagicMock()
            screen.ids['input_event_time'] = MagicMock()
            screen.ids['input_event_title'] = MagicMock()
            screen.ids['events_container'] = MagicMock()
            screen.ids['subjects_grid'] = MagicMock()
            screen.ids['label_selected_subject'] = MagicMock()
            screen.ids['input_event_date'].text = ""
            screen.ids['input_event_time'].text = ""
            screen.ids['input_event_title'].text = ""
            
            # symuluje, ze uzytkownik ma wybrany przedmiot
            screen.selected_subject_id = 1 
            screen.show_error_popup = MagicMock()
            
            return screen
# ==============================================================
# TESTY WIDOKU
# ==============================================================

def test_view_initialization(exam_screen_instance): #sprawdza, czy widok laduje się bez wyrzucania krytycznych wyjatkow
    assert exam_screen_instance is not None

def test_submit_fails_when_no_subject_selected(exam_screen_instance): #sprawdza, czy system zablokuje zapis, gdy nie wybrano przedmiotu
    exam_screen_instance.selected_subject_id = None
    exam_screen_instance.submit_event()
    exam_screen_instance.show_error_popup.assert_called_with("Najpierw wybierz przedmiot z listy powyżej!")

# puste tytuly
@pytest.mark.parametrize("invalid_title", ["", "   ", "\t", "\n"])
def test_validation_fails_on_empty_title(exam_screen_instance, invalid_title):
    exam_screen_instance.ids['input_event_date'].text = "2026-05-28"
    exam_screen_instance.ids['input_event_time'].text = "14:30"
    exam_screen_instance.ids['input_event_title'].text = invalid_title
    
    exam_screen_instance.submit_event()
    exam_screen_instance.show_error_popup.assert_called_with("Tytuł wydarzenia nie może być pusty!")

# zle formaty i wartosci dat
@pytest.mark.parametrize("invalid_date", [
    "2026-05-32",
    "2026-13-10",
    "2026-00-15",
    "2026-05-00",
    "-026-05-10",
    "20261-05-10",
    "abc-de-fg",
    "",
    "2026/05/28",
    "28-05-2026",
    "2026.05.28",
    "2026-05-311", 
    "2026-5-5", 
    "26-05-28", 
    "YYYY-MM-DD", 
    "!!-!!-!!"
])
def test_validation_fails_on_invalid_dates(exam_screen_instance, invalid_date): #system powinien zablokowac kazda z tych zlych dat
    exam_screen_instance.ids['input_event_date'].text = invalid_date
    exam_screen_instance.ids['input_event_time'].text = "14:30"
    exam_screen_instance.ids['input_event_title'].text = "Math Exam"
    
    exam_screen_instance.submit_event()
    exam_screen_instance.show_error_popup.assert_called_with("Data musi być w formacie RRRR-MM-DD\n(np. 2026-05-28)")

# zle formaty i wartosci czasu
@pytest.mark.parametrize("invalid_time", [
    "24:00",
    "23:60",
    "12:61",
    "25:00",
    "00:60",
    "08:60",
    "-1:30",
    "14:-5",
    "9:05",
    "14:3",
    "23:59:59",
    "01:01:01",
    "abc",
    "",
    "12-30",
    "12;30",
    "12/30", 
    "12.30", 
    "godz. 14:00", 
    "14.30", 
    "99:99"
])
def test_validation_fails_on_invalid_times(exam_screen_instance, invalid_time):
    exam_screen_instance.ids['input_event_date'].text = "2026-05-28"
    exam_screen_instance.ids['input_event_time'].text = invalid_time
    exam_screen_instance.ids['input_event_title'].text = "Physics Exam"

    exam_screen_instance.submit_event()
    exam_screen_instance.show_error_popup.assert_called_with("Godzina musi być w formacie HH:MM\n(np. 14:30)")

# poprawny zapis
@patch('database.get_connection')
def test_submit_valid_event_saves_to_db(mock_get_conn, exam_screen_instance): #sprawdza, czy po wpisaniu poprawnych danych, wydarzenie faktycznie zapisuje się do bazy."""
    mock_db = MagicMock()
    mock_get_conn.return_value = mock_db

    exam_screen_instance.ids['input_event_date'].text = "2026-05-28"
    exam_screen_instance.ids['input_event_time'].text = "14:30"
    exam_screen_instance.ids['input_event_title'].text = "Physics Exam"
    exam_screen_instance.selected_subject_id = 1
    exam_screen_instance.submit_event()
    
    exam_screen_instance.show_error_popup.assert_not_called()
    mock_db.commit.assert_called_once()