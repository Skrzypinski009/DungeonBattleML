from kivy.uix.label import Label

from ui.assets.screen_title import ScreenTitle

from .assets.menu import MenuButton, MenuContainer
from .base_screen import BaseScreen


class MainMenuScreen(BaseScreen):
    SCREEN_NAME = "MainMenu"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        container = MenuContainer()
        container.add_widget(Label())
        container.add_widget(ScreenTitle("Menu"))
        container.add_widget(MenuButton("Gra", lambda x: self.go("Play")))
        container.add_widget(MenuButton("Modele", lambda x: self.go("Models")))
        container.add_widget(
            MenuButton("Zbiory danych", lambda x: self.go("Datasets"))
        )
        container.add_widget(Label())

        self.add_widget(container)
