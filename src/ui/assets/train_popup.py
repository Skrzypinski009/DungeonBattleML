from typing import Callable
from kivy.uix.bubble import BoxLayout, RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import AnchorLayout
from kivy.uix.popup import Popup
from .loading_circle import LoadingCircle
from kivy.uix.scrollview import ScrollView

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns

from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


class TrainPopup(Popup):
    def __init__(self, go_back_call: Callable, **kwargs):
        super().__init__(
            title="Trenowanie modelu",
            size_hint=(0.8, 0.9),
            size=(400, 600),
            **kwargs,
        )
        self.go_back_call = go_back_call
        self.initial_height = self.height

        self.build_ui()
        self.show_loading()

    def build_ui(self):
        print(1)
        content = BoxLayout(
            size_hint=(1, 1),
            padding=10,
            orientation="vertical",
        )

        scroll = ScrollView(
            size_hint=(1, 1),
        )
        self.box = BoxLayout(
            size_hint=(1, None),
            orientation="vertical",
            spacing=40,
        )

        self.box.add_widget(Label(height=200))
        scroll.add_widget(self.box)
        content.add_widget(scroll)
        self.add_widget(content)

    def clear_content(self):
        self.box.clear_widgets()
        self.box.height = 0

    def canvas_from_fig(self, fig):

        canvas = FigureCanvasKivyAgg(fig)
        canvas.size_hint = (None, None)
        canvas.size = (400, 400)
        canvas.pos_hint = {"center_x": 0.5}
        return canvas

    def subplots(
        self,
        title: str = "Wykres",
        xlabel: str | None = None,
        ylabel: str | None = None,
    ):
        fig, ax = plt.subplots(figsize=(4, 3))

        ax.set_title(title, color="white", fontsize=16, pad=20)
        if xlabel:
            ax.set_xlabel(xlabel, color="white", fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, color="white", fontsize=12)

        color = "white"
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")
        ax.tick_params(colors=color, which="both")
        ax.yaxis.label.set_color(color)
        ax.xaxis.label.set_color(color)
        ax.title.set_color(color)
        ax.grid(True, color=color, linestyle="--", linewidth=0.5, alpha=0.3)

        return fig, ax

    def report_plot(self, df_report):
        fig, ax = self.subplots()
        plot = sns.heatmap(
            df_report,
            ax=ax,
            annot=True,
            annot_kws={"color": "white"},
            cmap="viridis",
        )
        cbar = plot.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color="white")
        plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")
        return self.canvas_from_fig(fig)

    def result_label(self, text: str):
        return Label(
            text=text,
            font_size=20,
            size_hint=(1, None),
            height=40,
        )

    def reward_plot(self, reward_list):
        fig, ax = self.subplots("Nagrody na epizod", "epizody", "nagroda")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        x_values = range(1, len(reward_list) + 1)
        sns.lineplot(x=x_values, y=reward_list, ax=ax)
        return self.canvas_from_fig(fig)

    def reward_label(self, reward):
        return self.result_label(f"Nagroda z walki: {reward}")

    def reward_widget(self, reward_list):
        if len(reward_list) > 1:
            return self.reward_plot(reward_list)
        else:
            return self.reward_label(reward_list[0])

    def win_rate_label(self, win_rate):
        win_rate_p = round(win_rate * 100, 2)
        return self.result_label(f"Wygrane: {win_rate_p}%")

    def length_plot(self, length_list):
        fig, ax = self.subplots("Długość walki na epizod", "epizody", "długość walki")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        x_values = range(1, len(length_list) + 1)
        sns.lineplot(x=x_values, y=length_list, ax=ax)
        return self.canvas_from_fig(fig)

    def score_label(self, score):
        score = round(score * 100, 2)
        text = f"Dokładność modelu: {score} %"

        return Label(
            text=text,
            font_size=20,
            size_hint=(1, None),
            height=60,
        )

    def show_train_results(self, train_results: dict) -> None:
        self.clear_content()

        ok_btn = Button(
            text="Wyjdź",
            on_press=lambda _: self.on_ok_pressed(),
            size_hint=(None, None),
            size=(200, 70),
            pos_hint={"center_x": 0.5},
        )
        height = 100

        self.box.add_widget(Label(height=50))
        if "score" in train_results:
            label = self.score_label(train_results["score"])
            self.box.add_widget(label)
            height += label.height

        if "report" in train_results:
            plot = self.report_plot(train_results["report"])
            self.box.add_widget(plot)
            height += plot.height

        if "history" in train_results:
            history = train_results["history"]

            if "win_rate" in history:
                label = self.win_rate_label(history["win_rate"])
                self.box.add_widget(label)
                height += label.height

            if "episode_rewards" in history:
                reward_widget = self.reward_widget(history["episode_rewards"])
                self.box.add_widget(reward_widget)
                height += reward_widget.height

            if "episode_lengths" in history:
                plot = self.length_plot(history["episode_lengths"])
                self.box.add_widget(plot)
                height += plot.height

        self.box.add_widget(ok_btn)
        spacing = self.box.spacing * (len(self.box.children) - 1)
        self.box.height = height + spacing

    def show_loading(self):
        self.clear_content()
        loading_circle = LoadingCircle(
            size=(100, 100),
            size_hint=(None, None),
            pos_hint={"center_x": 0.5},
        )

        label = Label(
            text="Trenowanie...",
            font_size=20,
            size_hint=(1, None),
        )

        self.box.add_widget(Label(height=50))
        self.box.add_widget(label)
        self.box.add_widget(loading_circle)
        self.box.height = 50 + loading_circle.height + label.height

        loading_circle.start()

    def on_ok_pressed(self):
        self.clear_content()
        self.dismiss()
        self.go_back_call()
