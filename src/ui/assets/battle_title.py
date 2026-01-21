from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label


class BattleTitle(AnchorLayout):
    def __init__(self, title: str):
        super().__init__(
            anchor_x="center",
            anchor_y="top",
            padding=30,
        )
        self.title_label = Label(
            text=title,
            size_hint_y=0,
            size_hint_x=1,
            font_size=30,
        )
        self.add_widget(self.title_label)
