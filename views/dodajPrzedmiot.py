from Widgets.form import FormStyle,FormBackend,FormField,FormWidget,KivyFormBackend

if __name__ == "__main__":

    from kivy.app import App


    class Dodaj_przedmiot(App):

        def build(self):

            style = FormStyle(

                bg_color=(0.18, 0.34, 0.55, 1),

                text_color=(1, 1, 1, 1),

                button_color=(0.10, 0.25, 0.45, 1),

                field_background_color=(0.85, 0.85, 0.84, 1),

                field_text_color=(0, 0, 0, 1)
            )

            fields = [

                FormField(
                    name="Przedmiot",
                    width=250
                ),

                FormField(
                    name="Prowadzący",
                    width=250
                ),
                FormField(
                    name="Warunki",
                    width=900
                ),
                FormField(
                    name="Dopuszczalne Nieobecności",
                    width=100
                ),
                FormField(
                    name="Max liczba plusów",
                    width=100
                ),
                FormField(
                    name="Max punkty za kolokwia",
                    width=100
                ),
                FormField(
                    name="Godzina startu",
                    width=100
                ),
                FormField(
                    name="Czas trwania",
                    width=100
                ),

                FormField(
                    name="Początek zajęć",
                    width=250,
                    use_calendar=True
                ),
                FormField(
                    name="Koniec zajęć",
                    width=250,
                    use_calendar=True
                ),
                FormField(
                    name="Dzień tygodnia",
                    width=250
                )
            ]

            backend = KivyFormBackend()

            form = FormWidget(
                fields=fields,
                backend=backend,
                style=style
            )

            return form.render()


    Dodaj_przedmiot().run()
