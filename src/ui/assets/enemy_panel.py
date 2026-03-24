from typing import Callable

from kivy.uix.bubble import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner


class EnemySelectPanel(BoxLayout):
    translation = {
        "Szczór": "rat",
        "Szkielet": "skeleton",
        "Ork": "orc",
    }

    def __init__(self):
        super().__init__(
            orientation="horizontal",
            spacing=20,
            size_hint=(1, None),
            height=50,
        )
        self.build_ui()

    def build_ui(self):
        self.spinner = Spinner(
            text="Wybierz przeciwnika",
            values=[
                "Szczór",
                "Ork",
                "Szkielet",
            ],
            size_hint=(1, None),
            size=(250, 50),
        )

        self.delete_btn = Button(
            text="Usuń",
            size_hint=(None, None),
            size=(100, 50),
        )

        self.add_widget(self.spinner)
        self.add_widget(self.delete_btn)

    def disable(self, disabled: bool = True) -> None:
        self.delete_btn.disabled = disabled

    def bind_remove_btn(self, remove_call: Callable):
        self.delete_btn.bind(
            on_press=remove_call,
        )

    def get_enemy_name(self):
        if self.spinner.text in self.translation.keys():
            return self.translation[self.spinner.text]
        return None

    def set_enemy_name(self, enemy_type_name: str):
        translation_reverse = {v: k for k, v in self.translation.items()}
        self.spinner.text = translation_reverse[enemy_type_name]
