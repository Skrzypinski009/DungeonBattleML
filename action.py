from enum import Enum
import numpy as np


class Action(Enum):
    NONE = 0
    REST = 1
    BLOCK = 2
    ATTACK = 3
    HEAVY_ATTACK = 4


def choose_random_action() -> Action:
    choice: int = np.random.randint(1, 5)
    return Action(choice)
