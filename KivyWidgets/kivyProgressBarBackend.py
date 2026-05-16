from progressBar import ProgressBarState, ProgressBarStyle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar as KivyProgressBar
from kivy.uix.label import Label

class KivyProgressBarBackend:
    def __init__(self):
        self.layout=None
        self.progress_bar=None
        self.label=None

    def create(self,value: int, max_value: int, style: ProgressBarStyle):
        self.layout=BoxLayout(orientation="vertical")
        self.progress_bar=KivyProgressBar(max=max_value,value=value)
        self.label=Label(text=str(value*100/max_value)+"%")
        self.layout.add_widget(self.progress_bar)
        self.layout.add_widget(self.label)
        return self.layout
    
    def setValue(self, value: int, max_value: int):
        self.progress_bar.max=max_value
        self.progress_bar.value=value
        self.label.text=str(value*100/max_value)+"%"