from kivy.graphics import Canvas, Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from typing import Any
from .stat_bar import StatBar
from .stat_bar_wrapper import StatBarWrapper


class StatBars(BoxLayout):
    def __init__(self):
        super().__init__(
            orientation="vertical",
            width=400,
            size_hint_x=None,
            size_hint_y=None,
        )
        self.spacing = 10

        self.bars = {}
        self.bar_height = 20

    def update(self, stats: dict[str, int]):
        for key, value in stats.items():
            if key in self.bars.keys():
                self.bars[key].value = value

    def set(self, stats: dict[str, dict[str, Any]]):
        self.clear_widgets()
        self.bars.clear()

        for key, stat in stats.items():
            sb = StatBar(
                color=stat["color"],
                height=self.bar_height,
                max=stat["max"],
                value=stat["value"],
            )
            self.bars[key] = sb
            self.add_widget(StatBarWrapper(key, sb))
        self.height = 30 * len(self.children)
