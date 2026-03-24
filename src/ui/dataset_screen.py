from db.models import Dataset
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from services import dataset_service

from ui.assets.battle_list_popup import BattleListPopup

from .base_screen import BaseScreen


class DatasetScreen(BaseScreen):
    SCREEN_NAME = "Datasets"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datasets: list[tuple[Dataset]] = []
        self.build_ui()

    def load(self):
        self.load_datasets()

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

        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))

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
                text="Dodaj dataset",
                size_hint=(None, None),
                size=(200, 50),
                on_press=self.on_add_pressed,
            )
        )

        main.add_widget(buttons)
        main.add_widget(Label(text="Zbiory danych:", size_hint_y=None))
        main.add_widget(scroll)

        self.battles_popup = BattleListPopup(self.create_dataset)

        self.add_widget(main)

    def on_add_pressed(self, *_):
        self.battles_popup.open()

    def create_dataset(self, *_):
        dataset_service.create_dataset_from_battle_ids(
            self.battles_popup.battle_ids,
        )
        self.load_datasets()

    def remove(self, id: int):
        dataset_service.remove_dataset(id)
        self.load_datasets()

    def load_datasets(self):
        self.datasets = dataset_service.get_datasets()
        self.refresh()

    def refresh(self):
        self.list_layout.clear_widgets()
        for dataset in self.datasets:

            row = BoxLayout(
                size_hint=(1, None),
                height=40,
                spacing=10,
            )
            row.add_widget(
                Label(
                    text=f"Dataset {dataset[0].dataset_nr} ( {len(dataset)} )",
                    halign="left",
                )
            )

            row.add_widget(
                Button(
                    text="Usuń",
                    size_hint=(None, None),
                    size=(80, 30),
                    on_press=lambda x: self.remove(dataset[0].dataset_nr),
                )
            )
            self.list_layout.add_widget(row)
