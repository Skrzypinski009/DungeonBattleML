from typing import Callable, cast
from peewee import fn
from db import queries
from db.models import GameState, Actor, BattleState, BattleHistory
from db.models.action_type import ActionType
from services import actor_service, battle_service, battle_history_service


def create_game(battles: int = 1, potions: int = 1) -> GameState:
    return GameState.create(
        player=actor_service.create_actor_by_name("player", potions),
        battles_count=battles,
    )


def play(
    game: GameState, battle: BattleState, actor_controller: Callable, action
) -> BattleHistory:

    history = battle_service.fight(battle, actor_controller, action)

    if battle.winner == battle.enemy:
        print("\n\tGAME OVER!\n")
        return history

    elif battle.winner == game.player:
        print("\n\tYOU WIN!\n")

    return history


def get_not_finished(game) -> BattleState | None:
    return (
        BattleState.select()
        .where(
            BattleState.winner == None,
            BattleState.game == game,
        )
        .first()
    )


def game_turn_data(
    game: GameState,
    current_battle: BattleState,
    actor_controller: Callable,
    action=None,
):
    history = play(
        cast(GameState, game),
        cast(BattleState, current_battle),
        actor_controller,
        action,
    )
    logs = battle_history_service.history_log(
        history, cast(BattleState, current_battle)
    )
    player = history.battle_state.game.player
    battles_count = battle_service.get_battles_count(game)
    return (history, logs, player, battles_count)


def can_continue(game: GameState) -> bool:
    finished_battles = battle_service.get_finished_battles_count(game)

    if game.battles_count > finished_battles:
        return True
    return False


def remove_game(game: GameState):
    BattleState.delete().where(BattleState.game == game).execute()
    GameState.delete_instance(game)


def finish_battle(
    game: GameState,
    new_battle_call: Callable,
    end_call: Callable,
    next_enemy_list: list,
    save_game: bool,
):
    if len(next_enemy_list) > 0:
        next_enemy = next_enemy_list.pop()
        new_battle_call(next_enemy)
        return
    if not save_game:
        remove_game(game)
    end_call()
