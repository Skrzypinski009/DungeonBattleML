from threading import Thread
from time import sleep
from typing import Callable, cast

from db.models import ActionType, Actor, BattleHistory, BattleState, GameState
from kivy.clock import Clock
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import RelativeLayout
from services import action_service, battle_service, game_service
from services.action_service import ActionTypeEnum

from ui.assets.battle_end_popup import BattleEndPopup

from .assets.battle_title import BattleTitle
from .assets.enemy import Enemy, EnemyWrapper
from .assets.icon_bar import IconBar
from .assets.right_panel import RightPanel
from .assets.stat_bars import StatBars
from .base_screen import BaseScreen


class GameScreen(BaseScreen):
    SCREEN_NAME = "Game"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.paused: bool = True
        self.game: GameState
        self.current_battle: BattleState
        self.actor_controller = None
        self.save_game = True
        self.next_enemy_list: list = []

        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation="horizontal", padding=20)
        inner_layout = RelativeLayout(size_hint_x=1, size_hint_y=1)
        self.right_panel = RightPanel(
            self.play, self.next, self.pause, self.quit
        )
        self.history_panel = self.right_panel.history_panel

        background = Image(
            source="img/background.jpg",
            size_hint=(None, None),
            width=1920,
            height=1080,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        battle_title = BattleTitle("Battle 1")

        self.icon_bar = IconBar(self.next_action)
        self.stat_bar = StatBars()

        bottom_bars = BoxLayout(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            height=self.icon_bar.height + self.stat_bar.height,
            spacing=0,
        )

        bottom_bars_anchor = AnchorLayout(
            anchor_x="center",
            anchor_y="bottom",
        )

        self.enemy_wrapper = EnemyWrapper()

        main_layout.add_widget(inner_layout)
        main_layout.add_widget(self.right_panel)

        bottom_bars.add_widget(self.icon_bar)
        bottom_bars.add_widget(self.stat_bar)
        bottom_bars_anchor.add_widget(bottom_bars)

        inner_layout.add_widget(background)
        inner_layout.add_widget(self.enemy_wrapper)
        inner_layout.add_widget(battle_title)
        inner_layout.add_widget(bottom_bars_anchor)

        self.add_widget(main_layout)

    def set_ui_manual_mode(self, is_manual: bool):
        self.play_manual = is_manual
        self.icon_bar.mode(is_manual)
        self.right_panel.control_buttons.mode(is_manual)

    def play(self, *_) -> None:
        if self.game is None:
            print("game is None")
            return

        if self.paused:
            self.paused = False
            print("game is running")
            Thread(target=self.full_auto_mode, daemon=True).start()

    def next(self, *_) -> None:
        if self.game is None or not self.paused:
            return

        Thread(target=self.one_action_mode, daemon=True).start()

    def pause(self, *_) -> None:
        if self.game is None:
            return

        self.paused = True

    def quit(self, *_) -> None:
        self.game = None
        self.paused = True

        self.go("Play", "right")

    def new_game(
        self,
        actor_controller=None,
        next_enemy_list: list = [],
        potions_count: int = 1,
        save_game: bool = True,
    ):
        self.save_game = save_game
        self.actor_controller = actor_controller
        self.next_enemy_list = next_enemy_list

        if self.actor_controller is None:
            self.set_ui_manual_mode(True)
        else:
            self.set_ui_manual_mode(False)

        self.history_panel.clear_history_logs()

        self.game = game_service.create_game(1, potions_count)

        player = self.game.player
        stats = {
            "health": {
                "max": player.type.max_health,
                "value": player.health,
                "color": (1, 0, 0, 1),
            },
            "energy": {
                "max": player.type.max_energy,
                "value": player.energy,
                "color": (0, 0, 1, 1),
            },
        }
        self.stat_bar.set(stats)
        self.new_battle(self.next_enemy_list.pop())
        self.icon_bar.enabled_icons([1, 2, 3, 4])
        self.icon_bar.select_icon(0)

    def new_battle(self, next_enemy_name: str):
        if self.game is None:
            return

        self.current_battle = battle_service.create_battle(
            self.game, next_enemy_name
        )
        enemy = self.current_battle.enemy
        enemy_ui = Enemy(
            {
                "health": {
                    "max": enemy.type.max_health,
                    "value": enemy.health,
                    "color": (1, 0, 0, 1),
                },
                "energy": {
                    "max": enemy.type.max_energy,
                    "value": enemy.energy,
                    "color": (0, 0, 1, 1),
                },
            },
            "",
        )
        self.enemy_wrapper.enemy_update(enemy_ui)
        self.history_panel.add_history_logs(
            [
                "New battle started!",
                f"Your enemy is {enemy.type.name}",
            ]
        )

    def full_auto_mode(self):
        while not self.paused:
            self.one_action_mode()

    def half_auto_mode(self, actor: Actor):
        while not self.paused:
            self.one_action_mode()

            if self.current_battle.current_actor != actor:
                self.paused = True

    def one_action_mode(self, action=None):
        self.ui_update(
            *game_service.game_turn_data(
                self.game,
                self.current_battle,
                cast(Callable, self.actor_controller),
                action,
            )
        )

    def manual_mode(self, action):
        self.one_action_mode(action)

        if battle_service.is_enemy_turn(self.current_battle):
            self.paused = False
            self.half_auto_mode(cast(Actor, self.current_battle.enemy))

    def ui_update(self, history, logs, player, battles_count):
        Clock.schedule_once(
            lambda _: self.history_panel.add_history_logs(logs)
        )
        Clock.schedule_once(lambda _: self.selected_action_update(history))
        Clock.schedule_once(lambda _: self.icon_bar.disable_all())

        sleep(0.5)
        Clock.schedule_once(lambda _: self.update_stats(history))
        Clock.schedule_once(
            lambda _: self.enabled_actions_update(history, player)
        )

        if (
            history.battle_state.winner is not None
            and history.battle_state.battle_nr == battles_count
        ):
            Clock.schedule_once(
                lambda _: self.game_end(history.battle_state.winner)
            )
            self.paused = True
            return

    def update_stats(self, history: BattleHistory):
        player_stats = {
            "health": history.battle_state.game.player.health,
            "energy": history.battle_state.game.player.energy,
        }
        enemy_stats = {
            "health": history.battle_state.enemy.health,
            "energy": history.battle_state.enemy.energy,
        }
        self.stat_bar.update(player_stats)

        self.enemy_wrapper.enemy.stat_bars.update(enemy_stats)

    def selected_action_update(self, history: BattleHistory):
        if history.action_type == ActionTypeEnum.NONE:
            self.enemy_wrapper.show_action(0)
            self.icon_bar.select_icon(0)
            return

        elif history.action_owner == self.game.player.type:
            self.enemy_wrapper.show_action(0)
            self.icon_bar.select_icon(history.action_type.id)

        else:
            print(history.action_type.id)
            self.enemy_wrapper.show_action(history.action_type.id)
            self.icon_bar.select_icon(0)

    def enabled_actions_update(self, history, player: Actor):
        actions: list[ActionType] = action_service.get_avaliable(
            cast(int, player.energy),
            bool(player.potions > 0),
        )

        self.icon_bar.enabled_icons([action.id for action in actions])

        if history.battle_state.current_actor == history.battle_state.enemy:
            self.icon_bar.disable_all()
        else:
            self.icon_bar.disable_all(False)

    def game_end(self, winner: Actor):
        player = self.game.player
        enemy = self.current_battle.enemy

        win = bool(winner == player)
        name = player.type.name if win else enemy.type.name

        BattleEndPopup(
            win=win,
            winner_name=name,
            quit_call=self.quit,
            finish_call=self.finish_battle,
        ).open()

    def finish_battle(self):
        game_service.finish_battle(
            self.game,
            self.new_battle,
            self.quit,
            self.next_enemy_list,
            self.save_game,
        )

    def next_action(self, action_id: int):
        action = action_service.get_by_id(action_id)
        Thread(target=self.manual_mode, args=(action,), daemon=True).start()
