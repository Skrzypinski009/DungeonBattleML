from typing import Callable

from kivy.uix.bubble import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import AnchorLayout
from kivy.uix.popup import Popup

from .loading_circle import LoadingCircle


class TrainPopup(Popup):
    def __init__(self, go_back_call: Callable, **kwargs):
        super().__init__(
            title="Trenowanie modelu",
            size_hint=(0.5, 0.7),
            size=(400, 600),
            **kwargs,
        )
        self.go_back_call = go_back_call
        self.initial_height = self.height

        self.build_ui()

    def build_ui(self):
        anchor = AnchorLayout(
            anchor_y="center",
            anchor_x="center",
        )
        content = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20,
            size_hint=(1, None),
        )

        self.loading_circle_slot = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
        )

        self.results_layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            size_hint=(1, None),
        )

        content.add_widget(self.loading_circle_slot)
        content.add_widget(self.results_layout)
        anchor.add_widget(content)
        self.add_widget(anchor)

    def hide_train_results(self):
        self.results_layout.clear_widgets()

    def show_train_results(self, train_results: dict) -> None:
        self.hide_loading()

        text = ""
        if "score" in train_results:
            score = train_results["score"] * 100
            text = f"Dokładność modelu: {score} %"
        label = Label(
            text=text,
            font_size=20,
            size_hint=(1, None),
        )
        ok_btn = Button(
            text="Wyjdź",
            on_press=lambda _: self.on_ok_pressed(),
            size_hint=(None, None),
            size=(200, 70),
            pos_hint={"center_x": 0.5},
        )

        self.results_layout.add_widget(label)
        self.results_layout.add_widget(ok_btn)

    def show_loading(self):
        loading_circle = LoadingCircle(
            size=(100, 100),
            size_hint=(None, None),
            pos_hint={"center_x": 0.5},
        )

        label = Label(
            text="Trenowanie...",
            font_size=20,
            size_hint=(1, None),
        )

        self.loading_circle_slot.add_widget(label)
        self.loading_circle_slot.add_widget(loading_circle)
        loading_circle.start()

    def hide_loading(self):
        loading_circle = self.loading_circle_slot.children[0]
        loading_circle.stop()
        self.loading_circle_slot.clear_widgets()

    def on_ok_pressed(self):
        self.hide_train_results()
        self.dismiss()
        self.go_back_call()
