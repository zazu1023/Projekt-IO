import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from views.Tracker_Progressu.trackerProgressu import ProgressCard

@pytest.fixture
def mock_card():
    container_mock = MagicMock()
    ids_mock = MagicMock()
    ids_mock.progress_container = container_mock

    app = MagicMock()
    app.translate.return_value = "Zdobyto {total} z {max} punktów ({percent}%)"
    app.language = "pl"

    repo = MagicMock()
    mock_conn = MagicMock()
    repo.get_db_connection.return_value = mock_conn

    with patch('views.Tracker_Progressu.trackerProgressu.ProgressCard.ids', new_callable=PropertyMock) as mock_ids, \
         patch('views.Tracker_Progressu.trackerProgressu.ProgressBar'):

        mock_ids.return_value = ids_mock

        card = ProgressCard(
            subject_id=1,
            name="IO",
            teacher="Dr Kowalski",
            max_activity=10,
            current_activity=5,
            max_colloquium=20,
            current_colloquium=10,
            repo=repo,
            app=app,
        )
        yield card

def test_initial_values(mock_card):
    assert mock_card.get_total() == 15
    assert mock_card.max_points == 30

def test_plus_minus_logic(mock_card):
    mock_card.change_pluses(1)
    assert mock_card.pluses_val == 6
    assert mock_card.get_total() == 16

def test_cannot_have_negative_points(mock_card):
    mock_card.change_pluses(-100)
    assert mock_card.pluses_val >= 0

def test_save_to_db(mock_card):
    mock_conn = mock_card.repo.get_db_connection.return_value
    mock_card.change_pluses(1)
    assert mock_conn.execute.called
    sql_query = mock_conn.execute.call_args[0][0]
    assert "UPDATE subjects" in sql_query

def test_points_text_formatting(mock_card):
    expected_text = "Zdobyto 15 z 30 punktów (50.0%)"
    assert mock_card.points_text == expected_text
