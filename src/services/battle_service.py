from typing import Callable, cast

from pandas import DataFrame
from db.models import GameState, BattleState, Actor
from db.models.battle_history import BattleHistory
from services import action_service, actor_service
from services.action_service import ActionTypeEnum


def create_battle(game: GameState, next_enemy_name) -> BattleState:
    game_battle = (
        BattleState.select()
        .where(BattleState.game == game)
        .order_by(BattleState.battle_nr)
        .first()
    )
    battle_nr = game_battle.battle_nr + 1 if game_battle != None else 1

    return BattleState.create(
        game=game,
        battle_nr=battle_nr,
        turn_nr=1,
        action_nr=1,
        current_actor=game.player,
        enemy=actor_service.create_actor_by_name(next_enemy_name),
    )


def get_battle_ids(game) -> tuple[int]:
    return tuple(
        BattleState.select(BattleState.id).where(BattleState.game == game).distinct()
    )


def get_battle(id: int) -> BattleState:
    return BattleState.select().where(BattleState.id == id).first()


def current_actor_turn(
    battle: BattleState,
    current_actor: Actor,
    other_actor: Actor,
    action_controller: Callable,
    action=None,
) -> BattleHistory:
    if action == None:
        if battle.current_actor == battle.enemy:
            action = action_service.action_default_schema(battle)
        else:
            action = action_controller(battle)

    enemy = cast(Actor, battle.enemy)
    history = BattleHistory.create(
        battle_state=battle,
        turn_nr=battle.turn_nr,
        action_nr=battle.action_nr,
        # player
        player_health=battle.game.player.health,
        player_energy=battle.game.player.energy,
        # enemy
        enemy_type=enemy.type,
        enemy_health=enemy.health,
        enemy_energy=enemy.energy,
        # action
        action_owner=current_actor.type,
        action_type=action,
    )

    actor_service.perform_action(
        current_actor,
        action,
        other_actor,
        battle,
    )

    if other_actor.health == 0:
        print(f"[{other_actor.type.name}] is DEAD")

        battle.winner = battle.current_actor
        battle.save()
        print(f"The winner is {battle.winner.type.name}!")
        return history

    current_actor.last_action = action  # pyright: ignore
    current_actor.save()

    battle.action_nr += 1  # pyright: ignore
    battle.save()

    return history


def fight(
    battle: BattleState, actor_controller: Callable, action=None
) -> BattleHistory:

    current_actor = cast(Actor, battle.current_actor)
    other_actor = cast(
        Actor,
        (
            battle.enemy
            if battle.game.player == battle.current_actor
            else battle.game.player
        ),
    )
    history = current_actor_turn(
        battle, current_actor, other_actor, actor_controller, action
    )

    if battle.winner != None:
        actor_service.energy_regen(battle.winner)  # pyright: ignore
        return history

    if history.action_type in [ActionTypeEnum.BLOCK, ActionTypeEnum.NONE]:
        actor_service.energy_regen(current_actor)
        battle.current_actor = other_actor  # pyright: ignore
        battle.action_nr = 1  # pyright: ignore

        if battle.current_actor == battle.game.player:
            battle.turn_nr += 1  # pyright: ignore

    battle.save()
    return history


def get_battles_list() -> DataFrame:
    Enemy = Actor.alias()
    Winner = Actor.alias()
    battles = (
        BattleState.select(
            BattleState.id.alias("Battle ID"),  # pyright: ignore
            Enemy.type.name.alias("Enemy Type"),
            Winner.type.name.alias("Winner"),
        )
        .join(Enemy, on=(BattleState.enemy == Enemy.id))
        .switch(BattleState)
        .join(Winner, on=(BattleState.winner == Winner.id))
    )
    return DataFrame(battles.dicts())


def get_all_battles() -> tuple[BattleState]:
    return BattleState.select()


def get_all_battles_count() -> int:
    return BattleState.select().count()


def get_battles_count(game: GameState) -> int:
    return BattleState.select().where(BattleState.game == game).count()


def get_finished_battles_count(game: GameState) -> int:
    return BattleState.select().where(BattleState.game == game).count()


def is_enemy_turn(battle: BattleState) -> bool:
    if battle.current_actor == battle.enemy:
        return True
    return False


def remove_unfinished_battles() -> None:
    BattleState.delete().where(BattleState.winner == None).execute()
