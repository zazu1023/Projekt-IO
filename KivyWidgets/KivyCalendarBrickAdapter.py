
class SafeKivyBrickBackend():
    def bind_hover(self, on_enter=None, on_leave=None):
        pass

    def apply_state(self, *args, **kwargs):
        pass

    def set_label(self, *args, **kwargs):
        pass

    def update_content(self, *args, **kwargs):
        pass

    def update_style(self, *args, **kwargs):
        pass
        
    # NOWA METODA - Nadpisujemy tworzenie kafelka, żeby dodać nasze teksty
    def create(self, data, style, on_click):
        # 1. Pozwalamy oryginalnej, zablokowanej klasie zrobić swoją robotę
        # widget = super().create(data, style, on_click)
        widget = BrickWidget()
        
        # 2. Wstrzykujemy nasze customowe teksty z pliku .kv!
        widget.title_text = data.title
        # Łączymy czas rozpoczęcia i czas trwania, żeby uzyskać np. "10:30 | 1.5 h"
        widget.info_text = f"{data.start_time} | {data.end_time}"
        
        return widget