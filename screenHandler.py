"""

tu dodawajcie ekrany do importowania

"""

from views.mojePrzedmioty import MojePrzedmiotyScreen , SzczegolyPrzedmiotuScreen , SubjectData
from views.startKalendarz import StartKalendarz

SCREENS = {
            'mySubjects': {'class': MojePrzedmiotyScreen, 'kv': 'kv/mojePrzedmioty.kv'},
            'subjectDetails': {'class': SzczegolyPrzedmiotuScreen, 'kv': 'kv/szczegolyPrzedmiotu.kv'},
            'calendar' : {'class': StartKalendarz, 'kv': 'kv/home.kv'}
        }