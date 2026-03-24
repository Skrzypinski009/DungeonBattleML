import gymnasium as gym
import numpy as np
from db.models import BattleState, GameState
from gymnasium import spaces
from numpy.random import randint
from services import (
    action_service,
    battle_service,
    dataset_service,
    game_service,
)


class GameEnv(gym.Env):
    N_STATES = 31  # 25 + 5 + 1
    SEQUENCES = action_service.action_sequences()
    N_ACTIONS = len(SEQUENCES)

    def __init__(self, enemy_list: list, player_potions: int) -> None:
        super().__init__()
        self.enemy_list = enemy_list
        self.game: GameState
        self.current_battle: BattleState

        self.action_space = spaces.Discrete(self.N_ACTIONS)
        self.player_potions = player_potions

        low = [1, 1, 100, 8, 15, 0, 0, 10, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0]
        high = [999, 10, 100, 8, 15, 100, 8, 999, 99, 100, 999, 99, 5, 5]
        high += [1, 1, 1, 1]

        self.observation_space = spaces.Box(
            low=np.array(low, np.float32),
            high=np.array(high, np.float32),
            dtype=np.float32,
        )

        self.state: np.ndarray = np.array([])

    def reset(self, *, seed=None, options=None, **kwargs) -> tuple:
        super().reset(seed=seed)

        self.game = game_service.create_game(0, self.player_potions)

        self.new_battle()
        self.state = self.get_current_state()
        return (self.state, {})

    def step(self, action) -> tuple:

        self.play_turn(action)
        reward, terminated, truncated, info = self.turn_learning_data()
        self.state = self.get_current_state()

        if terminated or truncated:
            self.end()

        return self.state, reward, terminated, truncated, info

    def new_battle(self):
        self.current_battle = battle_service.create_battle(
            self.game,
            self.enemy_list[randint(0, len(self.enemy_list))],
        )

    def end(self):
        game_service.finish_battle(self.game, lambda: 0, lambda: 0, [], False)

    def get_current_state(self) -> np.ndarray:
        return np.array(
            dataset_service.get_state_tuple(self.current_battle),
            dtype=np.float32,
        )

    def play_turn(self, sequence):
        for action in sequence:
            game_service.game_turn_data(
                self.game,
                self.current_battle,
                lambda: 0,
                action,
            )

        while (
            self.current_battle.current_actor == self.current_battle.enemy
            and not self.current_battle.winner
        ):
            game_service.game_turn_data(
                self.game,
                self.current_battle,
                lambda: 0,
            )

    def turn_learning_data(self):
        reward = 0
        terminated = False
        truncated = False
        info = {}

        player_hp_ratio, enemy_hp_ratio = self.get_hp_ratio(self.state)
        hp_ratio = player_hp_ratio - enemy_hp_ratio
        reward += hp_ratio * 2

        if self.current_battle.winner:
            terminated = True
            if self.current_battle.winner == self.game.player:
                reward += 20
                info["winner"] = "player"
            else:
                reward -= 20
                info["winner"] = "enemy"

        if self.current_battle.turn_nr >= 25:
            truncated = True

        return reward, terminated, truncated, info

    @classmethod
    def get_hp_ratio(cls, state):
        d = dataset_service.state_to_dict(state)
        player_hp_ratio = d["player_health"] / d["player_max_health"]
        enemy_hp_ratio = d["enemy_health"] / d["enemy_max_health"]
        return (player_hp_ratio, enemy_hp_ratio)

    @classmethod
    def state_to_idx(cls, state):
        player_hp_ratio, enemy_hp_ratio = cls.get_hp_ratio(state)
        player_idx = int(np.floor(player_hp_ratio * 5))  # 0, 1, 2, 3, 4
        enemy_idx = int(np.floor(enemy_hp_ratio * 5)) * 5  # 0, 5, 10, ...

        return player_idx + enemy_idx
