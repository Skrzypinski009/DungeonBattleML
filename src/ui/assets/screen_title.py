from kivy.uix.label import Label


class ScreenTitle(Label):
    def __init__(self, text: str):
        super().__init__(
            font_size=24,
            size_hint=(1, None),
            text=text,
            height=70,
        )
