import numpy as np
from action import Action, choose_random_action
from game_state import GameState, Stats
from action_performing import perform_action


def win_check(passive_stats: Stats) -> bool:
    if passive_stats.hp <= 0:
        return True
    return False


if __name__ == "__main__":
    state = GameState(
        player=Stats(
            _name="player",
            _hp=100,
            _energy=10,
            _action=Action.NONE,
        ),
        enemy=Stats(
            _name="enemy",
            _hp=100,
            _energy=10,
            _action=Action.NONE,
        ),
    )

    current_turn_stats = state.player
    next_turn_stats = state.enemy
    winner = None

    while winner is None:
        action = choose_random_action()
        current_turn_stats.action = action

        perform_action(current_turn_stats, next_turn_stats)
        if win_check(next_turn_stats):
            winner = current_turn_stats
            break

        current_turn_stats, next_turn_stats = next_turn_stats, current_turn_stats

    print("winner: ", current_turn_stats.name)
