from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

from services import ai_model_service

from .base_screen import BaseScreen


class ModelsScreen(BaseScreen):
    SCREEN_NAME = "Models"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.models = tuple()
        self.build_ui()

    def load(self):
        self.load_models()

    def build_ui(self):
        main = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=20,
            size_hint=(1, 1),
        )

        self.list_layout: BoxLayout = BoxLayout(
            orientation="vertical",
            spacing=5,
            size_hint=(1, None),
        )

        self.list_layout.bind(  # pyright: ignore
            minimum_height=self.list_layout.setter("height")  # pyright: ignore
        )

        scroll = ScrollView(
            size_hint=(None, 1),
            width=400,
            pos_hint={"center_x": 0.5},
        )
        scroll.add_widget(self.list_layout)

        buttons = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            spacing=20,
        )

        buttons.add_widget(
            Button(
                text="Powrót",
                size_hint=(None, None),
                size=(200, 50),
                on_press=lambda x: self.go("MainMenu", "right"),
            )
        )
        buttons.add_widget(
            Button(
                text="Dodaj model",
                size_hint=(None, None),
                size=(200, 50),
                on_press=self.on_add_pressed,
            )
        )

        main.add_widget(buttons)
        main.add_widget(Label(text="Modele SI:", size_hint_y=None))
        main.add_widget(scroll)

        self.add_widget(main)

    def on_add_pressed(self, *_):
        self.go("NewModel", "left")

    def remove(self, id: int):
        ai_model_service.remove_model(id)
        self.load_models()

    def load_models(self):
        self.models = ai_model_service.get_all_ai_models()
        self.refresh()

    def refresh(self):
        self.list_layout.clear_widgets()
        for model in self.models:

            row = BoxLayout(
                size_hint=(1, None),
                height=40,
                spacing=10,
            )

            model_name = model["name"]
            model_type = model["type"]

            row.add_widget(
                Label(
                    text=f"{model_name} : {model_type}",
                    halign="left",
                )
            )

            row.add_widget(
                Button(
                    text="Usuń",
                    size_hint=(None, None),
                    size=(80, 30),
                    on_press=lambda x: self.remove(model["id"]),  # pyright: ignore
                )
            )
            self.list_layout.add_widget(row)
