from action import Action
from dataclasses import dataclass


@dataclass
class Stats:
    _name: str
    _hp: int
    _energy: int
    _action: Action

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str) -> None:
        self._name = v

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, v: int) -> None:
        self._hp = max(0, min(100, v))

    @property
    def energy(self) -> int:
        return self._energy

    @energy.setter
    def energy(self, v: int) -> None:
        self._energy = max(0, min(10, v))

    @property
    def action(self) -> Action:
        return self._action

    @action.setter
    def action(self, v: Action) -> None:
        self._action = v


@dataclass
class GameState:
    player: Stats
    enemy: Stats
