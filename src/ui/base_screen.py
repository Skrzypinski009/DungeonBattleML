from kivy.uix.screenmanager import Screen, SlideTransition


class BaseScreen(Screen):
    SCREEN_NAME = ""

    def go(self, screen_name, direction="left"):
        self.manager.transition = SlideTransition(direction=direction)
        self.manager.current = screen_name
        self.manager.get_screen(screen_name).load()

    def load(self):
        pass
