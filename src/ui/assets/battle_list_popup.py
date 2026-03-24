from typing import Callable

from db.models import BattleState
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from services import battle_service


class BattleListPopup(Popup):
    def __init__(self, create_dataset_call: Callable, **kwargs):
        super().__init__(
            title="Walki",
            size_hint=(0.5, 0.8),
            width=600,
            height=400,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            **kwargs,
        )
        self.battle_ids: list[int] = []

        self.build_ui(create_dataset_call)

    def build_ui(self, create_dataset_call) -> None:
        content = BoxLayout(
            size_hint=(1, 1),
            padding=10,
            orientation="vertical",
        )

        scroll_view = ScrollView(
            size_hint=(1, 1),
        )

        self.battle_list = BoxLayout(
            size_hint=(1, None),
            orientation="vertical",
            spacing=10,
        )

        self.battle_list.bind(
            minimum_height=self.battle_list.setter("height"),
        )

        buttons = BoxLayout(
            size_hint=(None, None),
            orientation="horizontal",
            spacing=20,
            pos_hint={"center_x": 0.5},
        )

        def create_dataset():
            create_dataset_call(self.battle_ids)
            self.dismiss()

        create_btn = Button(
            text="Stwórz",
            size_hint=(None, None),
            size=(80, 50),
            on_press=lambda _: create_dataset(),
        )

        cancel_btn = Button(
            text="Anuluj",
            size_hint=(None, None),
            size=(80, 50),
            on_press=lambda _: self.dismiss(),
        )

        buttons.add_widget(create_btn)
        buttons.add_widget(cancel_btn)

        scroll_view.add_widget(self.battle_list)
        content.add_widget(scroll_view)
        content.add_widget(buttons)

        self.add_widget(content)

    def create_battle_panel(self, battle):
        battle_panel = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=40,
        )
        checkbox = CheckBox(
            size_hint=(None, None),
            size=(50, 50),
        )

        checkbox.bind(
            active=lambda _, value: self.check_battle(value, battle.id)
        )

        label = Label(text=f"Battle {battle.id}")

        battle_panel.add_widget(checkbox)
        battle_panel.add_widget(label)
        return battle_panel

    def refresh(self) -> None:
        self.battle_list.clear_widgets()
        battles: tuple[BattleState] = battle_service.get_all_battles()

        for battle in battles:
            self.battle_list.add_widget(self.create_battle_panel(battle))

    def check_battle(self, value: bool, battle_id: int) -> None:
        if value:
            return self.battle_ids.append(battle_id)
        self.battle_ids.remove(battle_id)

    def open(self, *_) -> None:
        self.battle_ids = []
        self.refresh()
        super().open()
