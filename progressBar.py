from abc import ABC , abstractmethod
from enum import Enum, auto

class ProgressBarState(Enum):
    NORMAL = auto()
    COMPLETED = auto()
    DISABLED = auto()
    LOADING = auto()

class ProgressBarStyle:
    def __init__(self, bg_color, fill_color, text_color):
        self.bg_color=bg_color
        self.fill_color=fill_color
        self.text_color=text_color

class ProgressBarBackend(ABC):
    @abstractmethod
    def create(self,value: int, max_value: int, style: ProgressBarStyle):
        # stworz progress bar
        pass
    @abstractmethod
    def setValue(self, value: int, max_value: int):
        # zmieniasz value
        pass

class ProgressBar:
    def __init__ (self,value:int, max_value: int, backend: ProgressBarBackend,style: ProgressBarStyle):
        self.value=value
        self.max_value=max_value
        self._backend=backend
        self.style=style
        self._state=ProgressBarState.NORMAL
        self._validate_values()

    def render(self):
        return self._backend.create(self.value, self.max_value, self.style)
    
    def updateValue(self, new_value: int):
        self.value = new_value
        self._validate_values()
        if self.value == self.max_value:
            self._state=ProgressBarState.COMPLETED
        else:
            self._state=ProgressBarState.NORMAL
        self._backend.setValue(self.value,self.max_value)

    def getPercentage(self):
        return int(self.value*100/self.max_value)
    
    def _validate_values(self):
        if self.max_value<=0:
            raise ValueError("max_value must be greater than 0")
        if self.value<0:
            self.value=0
        if self.value>self.max_value:
            self.value=self.max_value