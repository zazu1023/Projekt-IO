import json
import Widgets.notifications

from Database.database_sqllite import SqliteAppRepository
from Style.Colors import ThemeManager


from kivy.config import Config

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '600')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty , ObjectProperty

from datetime import datetime
from Widgets.countdown import CountdownWidget, CountdownStyle, KivyCountdownBackend

from tests.create_default_values import DatabaseStarter

from screenHandler import *

class StudentPlannerApp(App):

    language = StringProperty("pl")
    # Motyw: ThemeManager.with_palette('midnight' | 'rose')  — Style/palettes.py
    # theme = ObjectProperty(ThemeManager())
    theme = ObjectProperty(ThemeManager.with_palette('default'))
    def __init__(self, repository, **kwargs):
        super().__init__(**kwargs)
        self.repo = repository

    def build(self):

        self.screens = SCREENS # wczytanie screenow z screenHandler

        with open('translation.json' , 'r' , encoding='utf-8') as file:
            data = json.load(file)
        
        self.translations = data
        
        Builder.load_file('Style/universalWidgets.kv')
        Builder.load_file('views/Kalendarz/calendar.kv')

        root_widget = Builder.load_file('views/main.kv')

        self.sesja_countdown = CountdownWidget(
            target_date=datetime(2026, 6, 22, 0, 0),
            backend=KivyCountdownBackend(),
            style=CountdownStyle(bg_color=(0, 0, 0, 0), text_color=(1, 1, 1, 1))
        )

        self.sm = root_widget.ids.sm
        self.change_screen(target_screen='calendar')
        return root_widget


    def translate(self, text:str, langtrigger ):
                return self.translations[self.language].get(text)

    def change_screen(self, target_screen , **kwargs):
        if not self.sm.has_screen(target_screen):
            
            
            
            config = self.screens.get(target_screen)
            
            if config:
                
                Builder.load_file(config['kv'])
                screen_kwargs = {
                    'name': target_screen,
                    'repo': self.repo,
                    'app': self,
                }
                new_screen = config['class'](**screen_kwargs)
                self.sm.add_widget(new_screen)
            else:
                print(f"Error invaild scren name {target_screen}")
                return
            
        new_screen = self.sm.get_screen(target_screen)

        for klucz, wartosc in kwargs.items():
            setattr(new_screen, klucz, wartosc)

        self.sm.current = target_screen

    def change_language(self):
        if self.language == "pl":
            self.language = "en"
        else:
            self.language = "pl"

        print("Zmieniono język na:", self.language)

    def events(self)->str:
        events_list = self.repo.get_upcoming_events() or []
    
        self._events = events_list
        if not events_list:
            return self.translate("no_events", self.language)
        else:
            sorted_events = sorted(events_list, key=lambda e: e.get('date_time', ''))
            return sorted_events[0].get('title', '')+ " " + sorted_events[0].get('date_time', '') + " " + self.translate(sorted_events[0].get('type', ''),self.language)


if __name__ == "__main__":

    # inicjalizacja bazy
    repo = SqliteAppRepository(db_connection=None)
    repo.init_db()

    DS = DatabaseStarter(repo)

    # DS.remove_all_subjects()
    # DS.add_test_subjects()

    StudentPlannerApp(repository=repo).run()
