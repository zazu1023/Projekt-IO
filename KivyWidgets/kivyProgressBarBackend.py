from Widgets.progressBar import ProgressBarState, ProgressBarStyle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex

class ThickProgressBar(Widget):
    def __init__(self, max_value, value, **kwargs):
        super().__init__(**kwargs)
        self.max_value = max_value
        self.value = value
        self.size_hint_y = None
        self.height = dp(14) 
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(rgba=get_color_from_hex("#c4c4c4"))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.height / 2])
            
            Color(rgba=get_color_from_hex("#1c4271"))
            fill_width = self.width * (self.value / self.max_value) if self.max_value > 0 else 0
            RoundedRectangle(pos=self.pos, size=(fill_width, self.height), radius=[self.height / 2])

    def update_values(self, value, max_value):
        self.value = value
        self.max_value = max_value
        self.update_canvas()

class KivyProgressBarBackend:
    def __init__(self):
        self.layout = None
        self.progress_bar = None

    def create(self, value: int, max_value: int, style: ProgressBarStyle):
        # Wysokość zmniejszona, bo nie ma już tekstu pod spodem
        self.layout = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(15))
        
        self.progress_bar = ThickProgressBar(max_value=max_value, value=value)
        self.layout.add_widget(self.progress_bar)
        
        return self.layout
    
    def setValue(self, value: int, max_value: int):
        # Aktualizujemy już tylko sam pasek, bez tekstu
        self.progress_bar.update_values(value, max_value)