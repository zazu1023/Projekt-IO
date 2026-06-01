"""

tu dodawajcie ekrany do importowania

"""

KV_FILE_PATH = "views"


from views.Moje_Przedmioty.mojePrzedmioty import MojePrzedmiotyScreen
from views.Szczegoly_Przedmiotu.szczegolyPrzedmiotu import SzczegolyPrzedmiotuScreen
from views.Kalendarz.startKalendarz import StartKalendarz
from views.Egzaminy_Kolokwia.egzaminy_i_kolokwia import ExamsAndColloquiumsScreen
from views.Dodaj_Przedmioty.dodaj_przedmiot import AddSubjectScreen
from views.Tracker_Progressu.trackerProgressu import TrackerProgresuScreen, ProgressCard, PointControlRow
from views.Repozytorium_Zasad.repozytoriumZadan import RepozytoriumZasadScreen

SCREENS = {
            'mySubjects': {'class': MojePrzedmiotyScreen, 'kv': f'{KV_FILE_PATH}/Moje_Przedmioty/mojePrzedmioty.kv'},
            'subjectDetails': {'class': SzczegolyPrzedmiotuScreen, 'kv': f'{KV_FILE_PATH}/Szczegoly_Przedmiotu/szczegolyPrzedmiotu.kv'},
            'calendar' : {'class': StartKalendarz, 'kv': f'{KV_FILE_PATH}/Kalendarz/home.kv'},
            'add_subject': {'class': AddSubjectScreen, 'kv': f'{KV_FILE_PATH}/Dodaj_Przedmioty/dodaj_przedmiot.kv'},
            'exams_tests': {'class': ExamsAndColloquiumsScreen, 'kv': f'{KV_FILE_PATH}/Egzaminy_Kolokwia/egzaminy_i_kolokwia.kv'},
            'rules_repository': {'class': RepozytoriumZasadScreen, 'kv': f'{KV_FILE_PATH}/Repozytorium_Zasad/rules_repository.kv'},
            'progress_tracker': {'class': TrackerProgresuScreen, 'kv': f'{KV_FILE_PATH}/Tracker_Progressu/tracker_progresu.kv'},
        }
