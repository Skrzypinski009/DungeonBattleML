from kivy.uix.label import Label

from .models_screen import ModelsScreen
from .play_screen import PlayScreen
from .base_screen import BaseScreen

from .assets.loading_circle import LoadingCircle
from .assets.screen_title import ScreenTitle
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
