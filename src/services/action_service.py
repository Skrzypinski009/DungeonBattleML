from typing import cast

from db.models import ActionType, Actor, BattleState
from peewee import fn


def get_random(energy: int):
    return (
        ActionType.select()
        .where(ActionType.energy_cost <= energy)
        .order_by(fn.Random())
        .first()
    )


def get_by_id(action_type_id: int):
    return ActionType.select().where(ActionType.id == action_type_id).first()


def get_avaliable(energy: int, have_potions: bool) -> list:
    actions = list(ActionType.select().where(ActionType.energy_cost <= energy))
    if ActionTypeEnum.REGENERATION in actions:
        if not have_potions:
            actions.remove(ActionTypeEnum.REGENERATION)
    return actions


def get_avaliable_actor(actor: Actor):
    return get_avaliable(actor.energy, bool(actor.potions > 0))


def get_by_name(name: str) -> ActionType:
    action = ActionType.select().where(ActionType.name == name).first()
    if action is None:
        raise Exception(f"Database has no action named '{name}'!")
    return action


class ActionTypeEnum:
    NONE = get_by_name("none")
    ATTACK = get_by_name("attack")
    HEAVY_ATTACK = get_by_name("heavy attack")
    BLOCK = get_by_name("block")
    REGENERATION = get_by_name("regeneration")


def offensive_action(current_actor: Actor) -> ActionType:
    action = None
    if current_actor.energy >= 6:
        action = ActionTypeEnum.HEAVY_ATTACK
    elif current_actor.energy >= 4:
        action = ActionTypeEnum.ATTACK
    elif current_actor.energy >= 2:
        action = ActionTypeEnum.BLOCK
    else:
        action = ActionTypeEnum.NONE

    return cast(ActionType, action)


def neutral_action(current_actor: Actor) -> ActionType:
    action = None
    if current_actor.energy >= 6:
        action = ActionTypeEnum.ATTACK
    elif current_actor.energy >= 2:
        action = ActionTypeEnum.BLOCK
    else:
        action = ActionTypeEnum.NONE

    return cast(ActionType, action)


def defensive_action(current_actor: Actor) -> ActionType:
    action = None
    if current_actor.energy >= 3 and current_actor.potions > 0:
        action = ActionTypeEnum.REGENERATION
    elif current_actor.energy == 2:
        action = ActionTypeEnum.BLOCK
    else:
        return offensive_action(current_actor)

    return cast(ActionType, action)


def action_default_schema(battle_state: BattleState) -> ActionType:
    current_actor: Actor = cast(Actor, battle_state.current_actor)
    other_actor: Actor = (
        battle_state.enemy
        if current_actor == cast(Actor, battle_state.game.player)
        else cast(Actor, battle_state.game.player)
    )

    ca_health_ratio = current_actor.health / current_actor.type.max_health
    oa_health_ratio = other_actor.health / other_actor.type.max_health

    if ca_health_ratio > 0.75:
        if other_actor.energy >= 6:
            return neutral_action(current_actor)
        return offensive_action(current_actor)

    if ca_health_ratio > 0.5:
        if oa_health_ratio > 0.5:
            return neutral_action(current_actor)
        return offensive_action(current_actor)

    if other_actor.health <= 30:
        return offensive_action(current_actor)
    return defensive_action(current_actor)


def action_default_schema_old(
    current_actor: Actor,
    other_actor: Actor,
) -> ActionType:
    ca_health_ratio = current_actor.health / current_actor.type.max_health
    oa_health_ratio = other_actor.health / other_actor.type.max_health

    if ca_health_ratio > 0.75:
        return offensive_action(current_actor)

    if ca_health_ratio > 0.5:
        if oa_health_ratio > 0.5:
            return neutral_action(current_actor)
        return offensive_action(current_actor)

    if (
        current_actor.potions > 0
        or current_actor.last_action != ActionTypeEnum.BLOCK
    ):
        return defensive_action(current_actor)
    return neutral_action(current_actor)


def choose_action(actor: Actor) -> ActionType:
    print(f"[{actor.type.name}] choose action:")
    actions = list(
        get_avaliable(
            cast(int, actor.energy),
            cast(int, actor.potions),
        )
    )
    action = None
    action_dict: dict[int, ActionType] = {}

    while action is None:
        for i, a in enumerate(actions):
            action_dict[i + 1] = a
            print(f"{i+1}. {a.name}")

        choice_str: str = input("> ")
        if choice_str.isdigit():
            choice = int(choice_str)
            if choice > 0 and choice < max(action_dict.keys()) + 1:
                action = action_dict[choice]

    return action


def action_sequences():
    A = ActionTypeEnum.ATTACK
    H = ActionTypeEnum.HEAVY_ATTACK
    B = ActionTypeEnum.BLOCK
    R = ActionTypeEnum.REGENERATION
    N = ActionTypeEnum.NONE

    return [
        {"id": 0, "sequence": [A, R, N], "cost": 7},
        {"id": 1, "sequence": [A, B], "cost": 6},
        {"id": 2, "sequence": [A, N], "cost": 4},
        {"id": 3, "sequence": [H, B], "cost": 8},
        {"id": 4, "sequence": [H, N], "cost": 6},
        {"id": 5, "sequence": [R, N], "cost": 3},
        {"id": 6, "sequence": [R, B], "cost": 5},
        {"id": 7, "sequence": [B], "cost": 2},
        {"id": 8, "sequence": [N], "cost": 0},
    ]
