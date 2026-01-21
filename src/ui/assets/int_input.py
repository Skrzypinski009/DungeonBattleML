from decimal import Clamped
from re import sub
from kivy.uix.textinput import TextInput


def clamp(num: int, min_num: int, max_num: int) -> int:
    return min(max_num, max(min_num, num))


class IntInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def insert_text(self, substring: str, from_undo=False):
        if substring.isdigit():
            super().insert_text(substring, from_undo)

        self.text = str(clamp(int(self.text), 1, 100))
