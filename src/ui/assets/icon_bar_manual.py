from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from .icon import Icon


class IconBarManual(RelativeLayout):
    def __init__(self):
        self.icon_size = 75
        self.icon_spacing = 20

        super().__init__(
            size_hint_y=None,
            size_hint_x=None,
        )

        self.width = self.icon_size * 4 + self.icon_spacing * 3
        self.height = self.icon_size

        self.icon_selection = Image(
            source="data/img/skill_icon_select.png",
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

        self.icons.add_widget(attack_icon)
        self.icons.add_widget(heavy_attack_icon)
        self.icons.add_widget(block_icon)
        self.icons.add_widget(regen_icon)
        self.add_widget(self.icons)
        self.add_widget(self.icon_selection)

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
        for i, icon in enumerate(reversed(self.icons.children)):
            if i + 1 in ids:
                icon.opacity = 1
            else:
                icon.opacity = 0.5
