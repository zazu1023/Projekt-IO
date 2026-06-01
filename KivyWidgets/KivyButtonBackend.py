
from kivy.uix.button import Button as KivyButton
from Widgets.Button import ButtonStyle , ButtonState

from kivy.properties import ObjectProperty , BooleanProperty , StringProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class CustomButtonWidget(KivyButton):
    style = ObjectProperty(None)
    hovered = BooleanProperty(False)
    btn_state = ObjectProperty(ButtonState.NORMAL)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):

        if not self.get_root_window():
            return

        local_pos = self.to_widget(*pos)

        inside = self.collide_point(*local_pos)

        if self.hovered != inside:
            self.hovered = inside

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
            
        local_pos = self.to_widget(*pos)
        inside = self.collide_point(*local_pos)

        if self.hovered != inside:
            self.hovered = inside
            self._update_logic_state()
     
    def on_state(self, instance, value):
        # Ta wbudowana metoda odpala się, gdy Kivy wykryje wciśnięcie (value == 'down') 
        # lub puszczenie przycisku (value == 'normal')
        self._update_logic_state()

    def on_disabled(self, instance, value):
        # Ta wbudowana metoda odpala się, gdy zrobisz: moj_przycisk.disabled = True
        self._update_logic_state()

    # --- MÓZG: Przeliczanie Enuma ---
    def _update_logic_state(self):
        """Jedna metoda, która decyduje o ostatecznym stanie przycisku"""

        if self.disabled:
            self.btn_state = ButtonState.DISABLED
        elif self.state == 'down':
            self.btn_state = ButtonState.PRESSED
        elif self.hovered:
            self.btn_state = ButtonState.HOVER
        else:
            self.btn_state = ButtonState.NORMAL

    def get_current_bg_color(self,current_state,style_obj):
        if not style_obj:
            return [0.2, 0.2, 0.2, 1]
        
        base_color = get_color_from_hex(style_obj.bg_color)

        if current_state == ButtonState.DISABLED:
            return get_color_from_hex(style_obj.disabled_bg_color)
            
        elif current_state == ButtonState.PRESSED:
        
            if style_obj.pressed_bg_color:
                return get_color_from_hex(style_obj.pressed_bg_color)
            return [base_color[0] * 0.5, base_color[1] * 0.5, base_color[2] * 0.5, 1]
            
        elif current_state == ButtonState.HOVER:
            if style_obj.hover_bg_color:
                return get_color_from_hex(style_obj.hover_bg_color)
            return [base_color[0] * 0.8, base_color[1] * 0.8, base_color[2] * 0.8, 1]

        return base_color
