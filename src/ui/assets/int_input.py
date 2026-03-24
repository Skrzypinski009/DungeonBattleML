from kivy.uix.textinput import TextInput


def clamp(num: int, min_num: int, max_num: int) -> int:
    return min(max_num, max(min_num, num))


class IntInput(TextInput):
    def __init__(self, min_val: int = 1, max_val: int = 100, **kwargs):
        super().__init__(halign="center", **kwargs)
        self.min_val = min_val
        self.max_val = max_val
        self.text = str(min_val)

    def insert_text(self, substring: str, from_undo=False):
        if substring.isdigit():
            super().insert_text(substring, from_undo)
            self.clamp_text()

    def _validate(self):
        if self.text == "":
            self.text = str(self.min_val)
            return

        self.clamp_text()

    def on_focus(self, _, value):
        if not value:
            self._validate()

    def clamp_text(self):
        self.text = str(clamp(int(self.text), self.min_val, self.max_val))

    def get_value(self):
        return int(self.text)
