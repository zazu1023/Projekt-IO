"""

tu dodawajcie ekrany do importowania

"""

from views.mojePrzedmioty import MojePrzedmiotyScreen , SzczegolyPrzedmiotuScreen , SubjectData
from views.startKalendarz import StartKalendarz
from views.egzaminy_i_kolokwia import ExamsAndColloquiumsScreen
from views.dodaj_przedmiot import AddSubjectScreen
from views.trackerProgressu import TrackerProgresuScreen

SCREENS = {
            'mySubjects': {'class': MojePrzedmiotyScreen, 'kv': 'kv/mojePrzedmioty.kv'},
            'subjectDetails': {'class': SzczegolyPrzedmiotuScreen, 'kv': 'kv/szczegolyPrzedmiotu.kv'},
            'calendar' : {'class': StartKalendarz, 'kv': 'kv/home.kv'},
            'add_subject': {'class': AddSubjectScreen, 'kv': 'kv/dodaj_przedmiot.kv'},
            'exams_tests': {'class': ExamsAndColloquiumsScreen, 'kv': 'kv/egzaminy_i_kolokwia.kv'},
            'rules_repository': {'class': StartKalendarz, 'kv': 'kv/home.kv'},
            'progress_tracker':  {'class': TrackerProgresuScreen, 'kv': 'kv/tracker_progresu.kv'}
        } 