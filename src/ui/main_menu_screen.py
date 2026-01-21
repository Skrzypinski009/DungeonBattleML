from kivy.uix.label import Label

from ui.assets.loading_circle import LoadingCircle
from ui.assets.screen_title import ScreenTitle
from ui.play_screen import PlayScreen
from ui.models_screen import ModelsScreen
from .base_screen import BaseScreen
from .assets.menu import MenuContainer, MenuButton


class MainMenuScreen(BaseScreen):
    SCREEN_NAME = "MainMenu"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        container = MenuContainer()
        container.add_widget(Label())
        container.add_widget(ScreenTitle("Menu"))
        container.add_widget(MenuButton("Gra", lambda x: self.go("Play")))
        container.add_widget(MenuButton("Modele", lambda x: self.go("Models")))
        container.add_widget(MenuButton("Zbiory danych", lambda x: self.go("Datasets")))
        container.add_widget(Label())

        self.add_widget(container)
