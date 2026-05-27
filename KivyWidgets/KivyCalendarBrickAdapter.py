from KivyWidgets.KivyCalendarBrick import KivyBrickBackend


class SafeKivyBrickBackend(KivyBrickBackend):
    def create_button(self, text, on_click):
        button = super().create_button(text, on_click)

        original_on_release = button.on_release

        def safe_release():
            if button.disabled:
                return
            if original_on_release:
                original_on_release()

        button.on_release = safe_release
        return button