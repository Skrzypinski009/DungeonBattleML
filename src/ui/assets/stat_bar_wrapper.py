from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Canvas, Color, Rectangle
from kivy.uix.label import Label

from .stat_bar import StatBar


class StatBarWrapper(BoxLayout):
    def __init__(self, stat_name: str, stat_bar: StatBar, **kwargs):
        super().__init__(
            orientation="horizontal",
            spacing=10,
            size_hint_x=1,
            size_hint_y=None,
            height=stat_bar.height,
            **kwargs,
        )

        label_settings = {
            "font_size": 22,
            "size_hint": (None, 1),
            "width": 70,
        }

        name_label = Label(text=stat_name, **label_settings)
        self.stat_bar = stat_bar
        self.value_label = Label(text=f"", **label_settings)

        self.stat_bar.bind(value=self._update)  # type: ignore

        self.add_widget(name_label)
        self.add_widget(self.stat_bar)
        self.add_widget(self.value_label)
        self._update(None, None)

    def _update(self, *_):
        self.value_label.text = f"{int(self.stat_bar.value)}/{int(self.stat_bar.max)}"
