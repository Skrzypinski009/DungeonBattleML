from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from .icon import Icon


class IconBar(RelativeLayout):
    def __init__(self, action_call=None):
        self.icon_size = 75
        self.icon_spacing = 20
        self.action_call = action_call
        self.enabled_actions = [1, 2, 3, 4]

        super().__init__(
            size_hint_y=None,
            size_hint_x=None,
        )

        self.width = self.icon_size * 4 + self.icon_spacing * 3
        self.height = self.icon_size

        self.icon_selection = Image(
            source="img/skill_icon_select.png",
            size_hint_x=None,
            size_hint_y=None,
            width=self.icon_size,
            height=self.icon_size,
        )
        self.icon_selection.opacity = 0

        self.icons = BoxLayout(
            orientation="horizontal",
            size_hint_x=1,
            size_hint_y=None,
            height=self.icon_size,
            spacing=self.icon_spacing,
            padding=0,
        )

        attack_icon = Icon(1, self.icon_size)
        heavy_attack_icon = Icon(2, self.icon_size)
        block_icon = Icon(3, self.icon_size)
        regen_icon = Icon(4, self.icon_size)

        self.button_overlay = self.create_button_overlay()

        self.icons.add_widget(attack_icon)
        self.icons.add_widget(heavy_attack_icon)
        self.icons.add_widget(block_icon)
        self.icons.add_widget(regen_icon)
        self.add_widget(self.icons)
        self.add_widget(self.icon_selection)
        self.add_widget(self.button_overlay)

    def select_icon(self, action_type_id: int):
        if action_type_id == 0:
            self.icon_selection.opacity = 0
            return

        self.icon_selection.opacity = 1
        self.icon_selection.pos = (
            (action_type_id - 1) * (self.icon_size + self.icon_spacing),
            0,
        )

    def enabled_icons(self, ids: list[int]):
        self.enabled_actions = ids
        for i, icon in enumerate(reversed(self.icons.children)):
            if i + 1 in ids:
                icon.opacity = 1
            else:
                icon.opacity = 0.5

    def create_button_overlay(self):
        button_overlay = BoxLayout(
            orientation="horizontal",
            size_hint_x=1,
            size_hint_y=None,
            height=self.icon_size,
            spacing=self.icon_spacing,
            padding=0,
        )

        self.button1 = self.create_overlay_button()
        self.button2 = self.create_overlay_button()
        self.button3 = self.create_overlay_button()
        self.button4 = self.create_overlay_button()
        self.end_button = self.create_end_turn_button()

        self.button1.bind(on_press=self.action_1_selected)
        self.button2.bind(on_press=self.action_2_selected)
        self.button3.bind(on_press=self.action_3_selected)
        self.button4.bind(on_press=self.action_4_selected)
        self.end_button.bind(on_press=self.end_turn)

        button_overlay.add_widget(self.button1)
        button_overlay.add_widget(self.button2)
        button_overlay.add_widget(self.button3)
        button_overlay.add_widget(self.button4)
        button_overlay.add_widget(self.end_button)

        return button_overlay

    def action_selected(self, nr):
        if nr not in self.enabled_actions:
            return

        self.disable_all(True)
        self.select_icon(nr)
        print(f"Action {nr} selected")
        self.action_call(nr)

    def action_1_selected(self, *_):
        self.action_selected(1)

    def action_2_selected(self, *_):
        self.action_selected(2)

    def action_3_selected(self, *_):
        self.action_selected(3)

    def action_4_selected(self, *_):
        self.action_selected(4)

    def end_turn(self, *_):
        self.action_selected(5)

    def create_overlay_button(self):
        return Button(
            size_hint=(None, None),
            width=self.icon_size,
            height=self.icon_size,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(1, 1, 1, 0),
        )

    def create_end_turn_button(self):
        return Button(
            text="End\nturn",
            font_size=30,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            width=self.icon_size,
            height=self.icon_size,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            background_color=(0, 0, 0, 1),
        )

    def mode(self, is_manual: bool):
        self.button_overlay.opacity = 1 if is_manual else 0
        self.disable_all(not is_manual)

    def disable_all(self, disabled: bool = True):
        print(disabled)
        self.button1.disabled = disabled
        self.button2.disabled = disabled
        self.button3.disabled = disabled
        self.button4.disabled = disabled
        self.end_button.disabled = disabled
