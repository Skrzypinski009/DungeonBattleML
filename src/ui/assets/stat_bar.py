from kivy.graphics import Color, Rectangle
from kivy.uix.progressbar import ProgressBar


class StatBar(ProgressBar):
    def __init__(self, color, **kwargs):
        super().__init__(
            size_hint_x=1,
            size_hint_y=None,
            **kwargs,
        )

        self.color = color
        with self.canvas:
            Color(0.8, 0.8, 0.8, 1)
            self.border = Rectangle(pos=self.pos, size=self.size)

            Color(0, 0, 0, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

            Color(*color)
            self.fg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update, size=self._update, value=self._update)

    def _update(self, *args):
        pos = (self.pos[0] + 1, self.pos[1] + 1)
        size = (self.width - 2, self.height - 2)

        self.border.pos = self.pos
        self.border.size = self.size

        self.bg.pos = pos
        self.bg.size = size

        self.fg.pos = pos
        self.fg.size = (size[0] * self.value / self.max, size[1])
