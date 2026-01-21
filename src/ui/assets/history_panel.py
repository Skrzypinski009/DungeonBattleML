from ctypes import alignment
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView


class HistoryPanel(ScrollView):
    def __init__(self):
        super().__init__()

        with self.canvas.before:  # type: ignore
            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(  # type: ignore
            pos=self.update,
            size=self.update,
        )

        self.container = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=0,
        )
        self.add_widget(self.container)

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def add_history_logs(self, logs: list[str]) -> None:
        for log in logs:
            self.add_history_log(log)

    def add_history_log(self, log: str):
        label = Label(
            text=log,
            size_hint_x=1,
            size_hint_y=None,
            height=25,
            halign="left",
        )
        label.bind(size=label.setter("text_size"))  # pyright: ignore
        self.container.add_widget(label)
        self.container.height = len(self.container.children) * 25

    def clear_history_logs(self):
        self.container.clear_widgets()
        self.container.height = 0
