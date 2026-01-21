from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class MenuButton(Button):
    def __init__(self, text, callback):
        super().__init__(
            text=text,
            size_hint=(None, None),
            size=(300, 55),
            pos_hint={"center_x": 0.5},
            on_press=callback,
        )


class MenuContainer(BoxLayout):
    def __init__(self):
        super().__init__(
            orientation="vertical",
            spacing=20,
            size_hint_x=None,
            width=400,
            pos_hint={"center_x": 0.5},
        )
