from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from services import battle_service

from .dataset_screen import DatasetScreen
from .game_screen import GameScreen
from .main_menu_screen import MainMenuScreen
from .models_screen import ModelsScreen
from .new_model_screen import NewModelScreen
from .play_screen import PlayScreen

Window.minimum_width = 1200
Window.minimum_height = 800


class MLApp(App):
    def build(self):
        battle_service.remove_unfinished_battles()

        self.sm = ScreenManager()
        self.add_screen(MainMenuScreen)
        self.add_screen(NewModelScreen)
        self.add_screen(ModelsScreen)
        self.add_screen(PlayScreen)
        self.add_screen(DatasetScreen)
        self.add_screen(GameScreen)
        return self.sm

    def add_screen(self, screen):
        self.sm.add_widget(screen(name=screen.SCREEN_NAME))
