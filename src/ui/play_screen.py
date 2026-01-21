from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from ui.assets.enemy import Enemy
from ui.assets.int_input import IntInput
from ui.assets.menu import MenuButton, MenuContainer
from ui.assets.play_settings_popup import PlaySettingsPopup
from ui.assets.screen_title import ScreenTitle

from services import (
    ai_model_service,
    action_service,
    battle_service,
)

from .base_screen import BaseScreen


class PlayScreen(BaseScreen):
    SCREEN_NAME = "Play"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.models: dict = {}
        self.model_names: list[str]

        self.build_ui()

    def load(self):
        battle_service.remove_unfinished_battles()
        self.load_ai_models()
        # self.battles_count.text = "1"
        self.potions_count.text = "1"
        self.actor_spinner.text = "Wybierz Aktora"

    def build_ui(self):
        layout = MenuContainer()

        self.actor_spinner = Spinner(
            values=[],
            size_hint=(None, None),
            size=(300, 55),
            pos_hint={"center_x": 0.5},
        )
        self.actor_spinner.bind(  # pyright: ignore
            text=lambda *_: self.actor_selected()
        )
        self.enemies_options = PlaySettingsPopup()
        self.enemies_options.add_enemy("rat")

        enemies_option_btn = MenuButton(
            "Wybierz przeciwników", lambda _: self.enemies_options.open()
        )

        save_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(None, None),
            size=(300, 30),
            pos_hint={"center_x": 0.5},
            spacing=0,
        )

        self.save_checkbox = CheckBox(
            size_hint=(None, None),
            size=(30, 30),
            active=True,
        )

        save_label = Label(
            text="Zapisz grę",
            halign="left",
            height=30,
            text_size=(200, 30),
        )

        save_layout.add_widget(self.save_checkbox)
        save_layout.add_widget(save_label)

        self.potions_count = IntInput(
            hint_text="Liczba mikstur zdrowia",
            multiline=False,
            size_hint=(None, None),
            size=(300, 50),
            font_size=20,
            pos_hint={"center_x": 0.5},
        )

        self.play_btn = MenuButton("Rozpocznij grę", self.play)

        layout.add_widget(Label())
        layout.add_widget(ScreenTitle("Opcje gry"))
        layout.add_widget(self.actor_spinner)
        layout.add_widget(enemies_option_btn)
        layout.add_widget(
            Label(
                text="Liczba mikstur zdrowia",
                size_hint=(1, None),
                height=20,
            )
        )
        layout.add_widget(self.potions_count)
        layout.add_widget(save_layout)
        layout.add_widget(self.play_btn)
        layout.add_widget(MenuButton("Powrót", lambda x: self.go("MainMenu", "right")))
        layout.add_widget(Label())

        self.add_widget(layout)

    def load_ai_models(self):
        self.models = ai_model_service.get_all_ai_models()
        self.model_names = [model["name"] for model in self.models]

        self.actor_spinner.values = [
            "Gracz",
            "Schemat walki",
        ] + self.model_names

    def play(self, _):
        actor_name = self.actor_spinner.text

        actor = None
        if actor_name == "Gracz":
            actor = None
        elif actor_name == "Schemat walki":
            actor = action_service.action_default_schema
        else:
            model = ai_model_service.get_model_by_name(self.actor_spinner.text)
            actions = []
            if model["type"] == "q_table":
                actor = lambda bs: next_next_action(model, bs, actions)
            else:
                actor = lambda bs: ai_model_service.get_next_action(model, bs)

        potions = int(self.potions_count.text)

        next_enemy_list = self.enemies_options.get_enemy_list()
        print(next_enemy_list)
        self.manager.get_screen("Game").new_game(
            actor,
            next_enemy_list,
            potions,
            self.save_checkbox.active,
        )
        self.go("Game")

    def actor_selected(self):
        if self.actor_spinner.text == "Wybierz Aktora":
            self.play_btn.disabled = True
        else:
            self.play_btn.disabled = False


def next_next_action(model, bs, actions: list):
    if not actions:
        actions.extend(ai_model_service.get_next_action(model, bs))
    return actions.pop(0)
