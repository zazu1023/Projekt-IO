
TERM_START = '2026-03-01'
TERM_END = '2026-06-30'

subjects = [
    {
        'title': 'Wstęp do informatyki',
        'teacher': 'dr Rafał Kawa',
        'status': 'atrisk',
        'conditions': 'Obecność obowiązkowa (max 3 nieobecności). Kolokwium 40%, projekt 60%.',
        'max_absences': 3,
        'max_pluses': 10,
        'max_colloquium_pluses': 30,
        'current_pluses': 2,
        'current_colloquium_pluses': 8,
        'current_absences': 2,
        'note': 'Do nadrobienia materiał z listy 4–6.',
        'term_start': TERM_START,
        'term_end': TERM_END,
        'schedule': [
            {'day_of_week': 0, 'start_time': '08:00', 'duration_minutes': 90},
            {'day_of_week': 2, 'start_time': '10:30', 'duration_minutes': 120},
        ],
    },
    {
        'title': 'Algebra liniowa',
        'teacher': 'prof. dr hab. Anna Nowak',
        'status': 'completed',
        'conditions': 'Egzamin pisemny. Zaliczenie przy min. 50% punktów.',
        'max_absences': 5,
        'max_pluses': 15,
        'max_colloquium_pluses': 35,
        'current_pluses': 14,
        'current_colloquium_pluses': 32,
        'current_absences': 0,
        'note': 'Zaliczone — powtórzyć przed sesją dla własnej satysfakcji.',
        'term_start': TERM_START,
        'term_end': TERM_END,
        'schedule': [
            {'day_of_week': 1, 'start_time': '09:00', 'duration_minutes': 90},
        ],
        'events': [
            {'type': 'Kolokwium', 'title': 'Kolokwium 1', 'date_time': '2026-06-09 09:00'},
        ],
    },
    {
        'title': 'Bazy danych',
        'teacher': 'mgr inż. Piotr Wiśniewski',
        'status': 'inprogress',
        'conditions': 'Projekt SQL + prezentacja. Brak zaliczenia projektu = 0 z przedmiotu.',
        'max_absences': 4,
        'max_pluses': 12,
        'max_colloquium_pluses': 28,
        'current_pluses': 7,
        'current_colloquium_pluses': 15,
        'current_absences': 1,
        'note': 'Projekt: schemat ER do 20.05.',
        'term_start': TERM_START,
        'term_end': TERM_END,
        'schedule': [
            {'day_of_week': 2, 'start_time': '14:00', 'duration_minutes': 120},
            {'day_of_week': 4, 'start_time': '08:00', 'duration_minutes': 100},
        ],
        'events': [
            {'type': 'Egzamin', 'title': 'Egzamin praktyczny SQL', 'date_time': '2026-06-11 08:00'},
        ],
    },
    {
        'title': 'Fizyka',
        'teacher': 'dr Jan Kowalski',
        'status': 'failed',
        'conditions': 'Laboratorium + egzamin. Wymagane zaliczenie wszystkich ćwiczeń.',
        'max_absences': 2,
        'max_pluses': 8,
        'max_colloquium_pluses': 20,
        'current_pluses': 1,
        'current_colloquium_pluses': 3,
        'current_absences': 2,
        'note': 'Poprawka w terminie sesyjnej — ustalić termin z prowadzącym.',
        'term_start': TERM_START,
        'term_end': TERM_END,
        'schedule': [
            {'day_of_week': 3, 'start_time': '11:00', 'duration_minutes': 45},
        ],
        'events': [
            {'type': 'Egzamin', 'title': 'Egzamin poprawkowy', 'date_time': '2026-06-11 11:00'},
        ],
    },
    {
        'title': 'Programowanie obiektowe',
        'teacher': 'dr inż. Maria Zielińska',
        'status': 'inprogress',
        'conditions': 'Zadania laboratoryjne co tydzień. Egzamin praktyczny na komputerze.',
        'max_absences': 3,
        'max_pluses': 20,
        'max_colloquium_pluses': 40,
        'current_pluses': 18,
        'current_colloquium_pluses': 22,
        'current_absences': 0,
        'note': 'Lab 7: wzorce projektowe — Singleton, Factory.',
        'term_start': TERM_START,
        'term_end': TERM_END,
        'schedule': [
            {'day_of_week': 0, 'start_time': '12:00', 'duration_minutes': 90},
            {'day_of_week': 3, 'start_time': '10:30', 'duration_minutes': 150},
        ],
        'events': [
            {'type': 'Kolokwium', 'title': 'Kolokwium — wzorce projektowe', 'date_time': '2026-06-11 10:30'},
        ],
    },
    {
        'title': 'Systemy operacyjne',
        'teacher': 'prof. dr hab. Tomasz Lewandowski',
        'status': 'atrisk',
        'conditions': 'Kolokwium + praca pisemna. Dopuszczalne 2 nieobecności.',
        'max_absences': 2,
        'max_pluses': 10,
        'max_colloquium_pluses': 25,
        'current_pluses': 4,
        'current_colloquium_pluses': 10,
        'current_absences': 2,
        'note': 'Zagrożenie z powodu nieobecności — wysłać usprawiedliwienie.',
        'term_start': TERM_START,
        'term_end': TERM_END,
        'schedule': [
            {'day_of_week': 1, 'start_time': '16:00', 'duration_minutes': 90},
            {'day_of_week': 4, 'start_time': '10:00', 'duration_minutes': 60},
        ],
        'events': [
            {'type': 'Kolokwium', 'title': 'Kolokwium z procesów', 'date_time': '2026-06-12 10:00'},
        ],
    },
    {
        'title': 'Język angielski B2',
        'teacher': 'mgr Anna Kowalczyk',
        'status': 'completed',
        'conditions': 'Aktywność na zajęciach + test końcowy. Min. 60% na zaliczenie.',
        'max_absences': 6,
        'max_pluses': 10,
        'max_colloquium_pluses': 20,
        'current_pluses': 10,
        'current_colloquium_pluses': 20,
        'current_absences': 1,
        'note': 'Certyfikat B2 — złożyć w dziekanacie do końca semestru.',
        'term_start': TERM_START,
        'term_end': TERM_END,
        'schedule': [
            {'day_of_week': 2, 'start_time': '08:00', 'duration_minutes': 45},
            {'day_of_week': 4, 'start_time': '12:00', 'duration_minutes': 45},
        ],
        'events': [
            {'type': 'Egzamin', 'title': 'Test końcowy B2', 'date_time': '2026-06-06 12:00'},
        ],
    },
]


class DatabaseStarter():
    def __init__(self, repo):
        self.repo = repo

    def remove_all_subjects(self):
        self.repo.remove_all_subjects()

    def add_test_subjects(self):
        for data in subjects:
            subject_id = self.repo.add_subject_with_schedule({
                'title': data['title'],
                'teacher': data.get('teacher', ''),
                'conditions': data.get('conditions', ''),
                'max_absences': data.get('max_absences', 0),
                'max_pluses': data.get('max_pluses', 0),
                'max_colloquium_pluses': data.get('max_colloquium_pluses', 0),
                'term_start': data.get('term_start', TERM_START),
                'term_end': data.get('term_end', TERM_END),
                'schedule': data.get('schedule', []),
            })

            status = data.get('status', 'inprogress')
            if status != 'inprogress':
                self.repo.set_status(subject_id, status)

            self.repo.update_subject(subject_id, {
                'title': data['title'],
                'teacher': data.get('teacher', ''),
                'conditions': data.get('conditions', ''),
                'max_absences': data.get('max_absences', 0),
                'max_pluses': data.get('max_pluses', 0),
                'max_colloquium_pluses': data.get('max_colloquium_pluses', 0),
                'note': data.get('note', ''),
            })

            self.repo.update_subject_progress(
                subject_id,
                data.get('current_pluses', 0),
                data.get('current_colloquium_pluses', 0),
            )

            absences = data.get('current_absences', 0)
            if absences:
                self.repo.add_absence(subject_id, absences)

            for event in data.get('events', []):
                self.repo.add_event(
                    subject_id,
                    event['type'],
                    event['title'],
                    event['date_time'],
                )
