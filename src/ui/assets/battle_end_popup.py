from typing import Callable

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class BattleEndPopup(Popup):
    def __init__(
        self,
        winner_name: str,
        win: bool,
        quit_call: Callable,
        finish_call: Callable,
    ):
        super().__init__(
            title="Koniec walki",
            content=self.create_content(win, winner_name),
            size_hint=(None, None),
            size=(400, 200),
            auto_dismiss=False,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.quit_call = quit_call
        self.finish_call = finish_call

    def create_content(self, win, winner_name):
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        self.label = Label(text=f"Wygrywa: {winner_name}!")
        if win:
            self.btn = Button(text="OK", size_hint_y=None, height=40)
            self.btn.bind(on_release=self.finish)
        else:
            self.btn = Button(text="Wyjdź", size_hint_y=None, height=40)
            self.btn.bind(on_release=self.go_back)

        content.add_widget(self.label)
        content.add_widget(self.btn)

        return content

    def go_back(self, *_):
        self.dismiss()
        self.quit_call()

    def finish(self, *_):
        self.dismiss()
        self.finish_call()
