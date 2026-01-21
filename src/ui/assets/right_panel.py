from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from .history_panel import HistoryPanel


class ControlButtons(BoxLayout):
    def __init__(self, play_call, next_call, pause_call, quit_call):
        super().__init__(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            height=40 * 4,
        )

        self.quit_btn = self.control_btn("Wyjdź", quit_call)
        self.play_btn = self.control_btn("Graj", play_call)
        self.next_btn = self.control_btn("Dalej", next_call)
        self.pause_btn = self.control_btn("Zatrzymaj", pause_call)

        self.add_widget(self.quit_btn)
        self.add_widget(self.play_btn)
        self.add_widget(self.next_btn)
        self.add_widget(self.pause_btn)

    def control_btn(self, text: str, callback):
        return Button(
            text=text,
            size_hint=(1, None),
            height=40,
            on_press=callback,
        )

    def mode(self, is_manual: bool):
        operation = self.remove_widget if is_manual else self.add_widget

        try:
            operation(self.play_btn)
            operation(self.next_btn)
            operation(self.pause_btn)
        except:
            pass

        self.height = 40 * len(self.children)


class RightPanel(BoxLayout):
    def __init__(self, play_call, next_call, pause_call, quit_call):
        super().__init__(
            orientation="vertical",
            spacing=20,
            size_hint_x=None,
            size_hint_y=1,
            width=300,
        )

        self.history_panel = HistoryPanel()
        self.control_buttons = ControlButtons(
            play_call, next_call, pause_call, quit_call
        )

        self.add_widget(self.control_buttons)
        self.add_widget(self.history_panel)
