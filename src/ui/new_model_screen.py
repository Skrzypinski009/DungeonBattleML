from threading import Thread
from joblib.memory import _build_func_identifier
from kivy.base import Clock
from kivy.lang.builder import create_handler
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from pandas import DataFrame

from services import ai_model_service, dataset_service
from services.actor_service import create_random_enemy
from ui.assets.menu import MenuContainer
from ui.assets.play_settings_popup import PlaySettingsPopup
from ui.assets.screen_title import ScreenTitle
from ui.assets.train_popup import TrainPopup
from ui.assets.menu import MenuButton

from .base_screen import BaseScreen


class NewModelScreen(BaseScreen):
    SCREEN_NAME = "NewModel"

    model_translations = {
        "Drzewo decyzyjne": "decision_tree",
        "Las losowy": "random_forest",
        "Sieć Neuronowa": "mlp",
        "Q Table": "q_table",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datasets = []
        self.dataset_names = []

        self.build_ui()

    def load(self):
        self.load_datasets()
        self.name_input.text = ""
        self.model_type_spinner.text = "Wybierz typ modelu"
        self.dataset_spinner.text = "Wybierz zbiór danych"

    def build_ui(self):
        self.build_main_layout()
        self.train_popup = TrainPopup(lambda: self.go("Models", "right"))

        self.enemies_options = PlaySettingsPopup()
        self.enemies_options.add_enemy("rat")

    def build_main_layout(self):
        layout = MenuContainer()

        self.supervised_model_types = [
            "Drzewo decyzyjne",
            "Las losowy",
            "Sieć Neuronowa S",
        ]
        self.reinforcement_model_types = [
            "Q Table",
        ]

        self.name_input = TextInput(
            multiline=False,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={"center_x": 0.5},
            font_size=20,
            hint_text="Nazwa modelu",
        )
        self.name_input.bind(text=lambda *_: self.name_update())  # pyright: ignore

        self.form_layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            size_hint=(1, None),
            height=0,
            pos_hint={"center_x": 0.5},
        )

        self.model_type_spinner = Spinner(
            values=self.supervised_model_types + self.reinforcement_model_types,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={"center_x": 0.5},
        )
        self.model_type_spinner.bind(  # pyright: ignore
            text=lambda *_: self.model_type_selected()
        )

        self.dataset_spinner = Spinner(
            values=self.dataset_names,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint={"center_x": 0.5},
        )
        self.dataset_spinner.bind(  # pyright: ignore
            text=lambda *_: self.dataset_selected()
        )

        self.enemies_option_btn = MenuButton(
            "Wybierz przeciwników", lambda _: self.enemies_options.open()
        )

        self.train_btn = Button(
            text="Trenuj",
            size_hint=(None, None),
            size=(250, 50),
            on_press=lambda _: self.train(),
            disabled=True,
            pos_hint={"center_x": 0.5},
        )

        back_btn = Button(
            text="Powrót",
            size_hint=(None, None),
            size=(250, 50),
            on_press=lambda _: self.go("Models", "right"),
            pos_hint={"center_x": 0.5},
        )

        layout.add_widget(Label())
        layout.add_widget(ScreenTitle("Nowy model"))
        layout.add_widget(self.name_input)
        layout.add_widget(self.model_type_spinner)
        layout.add_widget(self.form_layout)
        layout.add_widget(self.train_btn)
        layout.add_widget(back_btn)
        layout.add_widget(Label())

        self.add_widget(layout)

    def load_datasets(self):
        self.datasets = dataset_service.get_datasets()
        self.dataset_names = [
            f"Dataset: {dataset[0].dataset_nr}" for dataset in self.datasets
        ]
        self.dataset_spinner.values = self.dataset_names

    def fill_form_layout(self):
        self.form_layout.clear_widgets()

        if self.model_type_spinner.text in self.supervised_model_types:
            self.form_layout.height = self.dataset_spinner.height
            self.form_layout.add_widget(self.dataset_spinner)

        elif self.model_type_spinner.text in self.reinforcement_model_types:
            self.form_layout.add_widget(self.enemies_option_btn)
            self.form_layout.height = self.enemies_option_btn.height

    def train_task(self, model_type, dataset_df=None):
        train_result = None
        if dataset_df:
            train_result = ai_model_service.train_model(model_type, dataset_df)
        else:
            train_result = ai_model_service.train_in_env(
                model_type,
                self.enemies_options.get_enemy_list(),
            )

        self.train_after(train_result)
        Clock.schedule_once(lambda _: self.show_result(train_result))

    def train(self):
        spinner_text = self.model_type_spinner.text
        model_type = self.model_translations[spinner_text]
        if spinner_text in self.supervised_model_types:
            self.train_on_datasets(model_type)
        elif spinner_text in self.reinforcement_model_types:
            self.train_in_environment(model_type)

    def train_on_datasets(self, model_type):
        try:
            dataset_id_str = self.dataset_spinner.text.split(" ")[-1]
            dataset_id = int(dataset_id_str)
        except:
            # TODO: show error message
            return

        dataset_df = DataFrame(
            dataset_service.get_dataset_by_id(dataset_id).dicts(),
        )
        print(dataset_df)

        self.train_popup.open()
        self.train_popup.show_loading()

        thread = Thread(target=self.train_task, args=(model_type, dataset_df))
        thread.start()

    def train_in_environment(self, model_type):
        self.train_popup.open()
        self.train_popup.show_loading()
        thread = Thread(target=self.train_task, args=(model_type,))
        thread.start()

    def train_after(self, train_result) -> None:
        ai_model_service.create_ai_model(
            train_result["type"],
            self.name_input.text,
            train_result["model"],
        )

    def show_result(self, train_result: dict) -> None:
        self.train_popup.show_train_results(train_result)

    def dataset_selected(self):
        self.options_selected()

    def model_type_selected(self):
        self.fill_form_layout()
        self.options_selected()

    def name_update(self):
        self.options_selected()

    def options_selected(self):
        if (
            self.model_type_spinner.text in self.model_type_spinner.values
            and self.name_input.text != ""
        ):
            if (
                self.model_type_spinner.text in self.supervised_model_types
                and self.dataset_spinner.text in self.dataset_spinner.values
                or self.model_type_spinner.text in self.reinforcement_model_types
            ):
                self.train_btn.disabled = False
                return
        self.train_btn.disabled = True
