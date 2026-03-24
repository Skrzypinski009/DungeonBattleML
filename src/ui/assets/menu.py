from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


menu_widget_settings = {
    "size_hint": (None, None),
    "size": (300, 55),
    "pos_hint": {"center_x": 0.5},
}


class MenuButton(Button):
    def __init__(self, text, callback, **kwargs):
        super().__init__(
            text=text,
            on_press=callback,
            **menu_widget_settings,
            **kwargs,
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
