from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from services import battle_service
from kivy.config import Config
from .dataset_screen import DatasetScreen
from .game_screen import GameScreen
from .main_menu_screen import MainMenuScreen
from .models_screen import ModelsScreen
from .new_model_screen import NewModelScreen
from .play_screen import PlayScreen

Config.set("kivy", "log_level", "info")
Config.set("graphics", "width", "1200")
Config.set("graphics", "height", "800")
Config.set("graphics", "resizable", "1")

Config.write()


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
