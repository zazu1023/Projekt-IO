from kivy.lang import Builder

from views.mojePrzedmioty import MojePrzedmiotyScreen , SzczegolyPrzedmiotuScreen
from views.startKalendarz import StartKalendarz



class ScreenHandler():
        
        def translate(self, text:str):
                return self.translations[self.language].get(text)

        def change_screen(self, target_screen , **kwargs):
            if not self.sm.has_screen(target_screen):
                
                screens = {
                    'mySubjects': {'class': MojePrzedmiotyScreen, 'kv': 'kv/mojePrzedmioty.kv'},
                    'subjectDetails': {'class': SzczegolyPrzedmiotuScreen, 'kv': 'kv/szczegolyPrzedmiotu.kv'},
                    'calendar' : {'class':StartKalendarz, 'kv': 'kv/calendar.kv'}
                }
                
                config = screens.get(target_screen)
                
                if config:
                    
                    Builder.load_file(config['kv'])
                    new_screen = config['class'](name=target_screen)
                    self.sm.add_widget(new_screen)
                else:
                    print(f"Error invaild scren name {target_screen}")
                    return
                
            new_screen = self.sm.get_screen(target_screen)

            for klucz, wartosc in kwargs.items():
                setattr(new_screen, klucz, wartosc)

            self.sm.current = target_screen
