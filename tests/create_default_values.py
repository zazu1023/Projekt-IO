
subjects = [
    {'title':'WDI' , 'teacher': "Rafal Kawa" , 'status': "atrisk"},
    {'title':'WDI' , 'teacher': "Rafal Kawa" , 'status': "completed"},
    {'title':'WDI' , 'teacher': "Rafal Kawa" , 'status': "inprogress"},
    {'title':'WDI' , 'teacher': "Rafal Kawa" , 'status': "failed"},
    {'title':'WDI' , 'teacher': "Rafal Kawa" , 'status': "pykpykpyk"},
]

class DatabaseStarter():
    def __init__(self , repo):
        self.repo = repo

    def remove_all_subjects(self):
        self.repo.remove_all_subjects()

    def add_test_subjects(self):
        for subject in subjects:
            self.repo.add_subject(subject)

