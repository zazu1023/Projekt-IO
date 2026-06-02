from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ObjectProperty


class UiColorsGroup(EventDispatcher):
    MAIN_BG_COLOR = StringProperty("#2c2c2e")
    SECONDARY_BG_COLOR = StringProperty("#0b3d91")
    
    TOP_BAR_BG_COLOR = StringProperty("#f8f9fa")
    TOP_BAR_TEXT_COLOR = StringProperty("#1565c0")
    NAV_BAR_BG_COLOR = StringProperty("#0b3d91")

class ButtonColorsGroup(EventDispatcher):
    TOP_BAR_BG_COLOR = StringProperty("#9ea6b3")
    TOP_BAR_TEXT_COLOR = StringProperty("#000000")
    NAV_BUTTON_BG_COLOR = StringProperty("#2e588c")

class SubjectColorsGroup(EventDispatcher):
    SUBJECT_BG_COLOR_COMPLETED = StringProperty("#62c57b")
    SUBJECT_BG_COLOR_ATRISK = StringProperty("#f28b82")
    SUBJECT_BG_COLOR_INPROGRESS = StringProperty("#d9d9d7")
    SUBJECT_BG_COLOR_FAILED = StringProperty("#272724")
    SUBJECT_TEXT_COLOR_BRIGHT = StringProperty("#ffffff")
    SUBJECT_TEXT_COLOR_DARK = StringProperty("#000000")

class DefaultColorsGroup(EventDispatcher):
    DEFAULT_WHITE = StringProperty("#ffffff")
    DEFAULT_BLACK = StringProperty("#000000")


class ThemeManager(EventDispatcher):
    UiColors = ObjectProperty(UiColorsGroup())
    ButtonColors = ObjectProperty(ButtonColorsGroup())
    SubjectColors = ObjectProperty(SubjectColorsGroup())
    DefaultColors = ObjectProperty(DefaultColorsGroup())