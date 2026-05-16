class KivyHelper:
    # Utilities
    def _parse_color(self, color):
        from kivy.utils import get_color_from_hex
        return get_color_from_hex(color) if isinstance(color, str) else color