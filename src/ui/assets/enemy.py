from typing import Any

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import RelativeLayout

from .icon import Icon
from .stat_bars import StatBars


class Enemy(BoxLayout):
    def __init__(self, stats: dict[str, dict[str, Any]], enemy_name: str):
        super().__init__(
            orientation="vertical",
            size_hint_x=None,
            size_hint_y=None,
            width=400,
            height=600,
        )
        self.stat_bars = StatBars()
        self.stat_bars.set(stats)
        print(enemy_name)
        self.image = Image(
            source=f"data/img/{enemy_name}.png",
            size_hint_x=None,
            size_hint_y=None,
            height=500,
        )
        self.image.width = (
            self.image.height
            * self.image.texture_size[1]
            / self.image.texture_size[1]
        )

        image_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="top",
        )
        image_anchor.add_widget(self.image)
        self.add_widget(self.stat_bars)
        self.add_widget(image_anchor)


class EnemyWrapper(RelativeLayout):
    def __init__(self):
        super().__init__(
            size_hint_x=None,
            size_hint_y=None,
            height=600,
            width=500,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.action_icon = Icon(
            action_type_id=1,
            size=50,
        )
        self.show_action(0)

        icon_anchor = AnchorLayout(
            anchor_x="right",
            anchor_y="top",
            size_hint=(None, None),
            size=(400, 400),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.enemy_anchor = AnchorLayout(
            anchor_y="center",
            anchor_x="center",
        )

        icon_anchor.add_widget(self.action_icon)

        self.add_widget(self.enemy_anchor)
        self.add_widget(icon_anchor)

    def show_action(self, action_type_id: int):
        self.action_icon.change_to(action_type_id)

    def enemy_update(self, enemy):
        self.enemy = enemy
        self.enemy_anchor.clear_widgets()
        self.enemy_anchor.add_widget(self.enemy)
