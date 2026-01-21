from ctypes import cast
from kivy.uix.bubble import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import ScrollView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from ui.assets.enemy_panel import EnemySelectPanel


class PlaySettingsPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(
            title="Wybór przeciwników",
            size_hint=(0.5, 0.7),
            size=(400, 600),
            **kwargs,
        )
        self.enemy_spinners = {}

        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(
            orientation="vertical",
            spacing=20,
            padding=20,
        )

        scroll = ScrollView(
            size_hint=(1, 1),
        )

        self.enemies_layout = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            spacing=20,
        )

        add_enemy_button = Button(
            text="Dodaj przeciwnika",
            size_hint=(None, None),
            size=(300, 50),
            on_press=lambda *_: self.add_enemy_panel(),
        )

        submit_button = Button(
            text="Zatwierdź",
            size_hint=(None, None),
            size=(300, 50),
            on_press=lambda *_: self.submit(),
        )

        scroll.add_widget(self.enemies_layout)

        layout.add_widget(add_enemy_button)
        layout.add_widget(scroll)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def update_height(self):
        self.enemies_layout.height = len(self.enemies_layout.children) * 70

    def update_disable(self, disabled=True):
        children = self.enemies_layout.children

        if len(children) == 1:
            children[0].disable(disabled)

    def remove_enemy(self, enemy_panel):
        self.enemies_layout.remove_widget(enemy_panel)
        self.update_height()
        self.update_disable()

    def add_enemy_panel(self):
        self.update_disable(False)
        enemy_panel = EnemySelectPanel()
        enemy_panel.bind_remove_btn(lambda _: self.remove_enemy(enemy_panel))

        self.enemies_layout.add_widget(enemy_panel)
        self.update_height()
        self.update_disable(True)

        return enemy_panel

    def submit(self):
        # copy of children for safe deleting
        children = [child for child in self.enemies_layout.children]
        for child in children:
            if child.get_enemy_name() == None:
                self.enemies_layout.remove_widget(child)
        self.update_height()

        self.dismiss()

    def add_enemy(self, enemy_type_name: str):
        panel = self.add_enemy_panel()
        panel.set_enemy_name(enemy_type_name)

    def get_enemy_list(self):
        return [
            x.get_enemy_name()
            for x in self.enemies_layout.children
            if x.get_enemy_name() is not None
        ]
