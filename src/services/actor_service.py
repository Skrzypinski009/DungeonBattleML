import math
from random import choice
from typing import cast

from db.models import ActionType, Actor, ActorType

from services.action_service import ActionTypeEnum


def create_actor_by_name(type_name: str, potions: int = 1):
    actor_type = ActorType.get(ActorType.name == type_name)
    return Actor.create(
        type=actor_type,
        health=actor_type.max_health,
        energy=actor_type.max_energy,
        potions=potions,
    )


def create_random_enemy():
    return create_actor_by_name(
        choice(["rat", "skeleton", "orc"]),
    )


def take_damage(actor: Actor, damage: int) -> None:
    if actor.last_action == ActionTypeEnum.BLOCK:
        blocked_dmg = math.floor(damage * 0.5)
        damage -= blocked_dmg
        print(f"Blocked damage: {blocked_dmg}")

    print(f"[{actor.type.name}] taking {str(damage)} damage")
    actor.health = max(actor.health - damage, 0)
    actor.save()


def energy_regen(actor: Actor) -> None:
    actor.energy = min(
        cast(int, actor.energy + 4),
        actor.type.max_energy,
    )
    actor.save()


def perform_action(
    current_actor: Actor, action: ActionType, other_actor: Actor
) -> None:
    current_actor_type = cast(ActorType, current_actor.type)
    action_name = cast(str, action.name)

    current_actor.energy -= action.energy_cost

    match action_name:
        case "regeneration":
            current_actor.health = current_actor.type.max_health
            current_actor.potions -= 1
            current_actor.save()

        case "attack":
            take_damage(
                other_actor,
                math.floor(cast(float, current_actor_type.attack_damage)),
            )

        case "heavy attack":
            take_damage(
                other_actor,
                math.floor(cast(float, current_actor_type.attack_damage * 2)),
            )


def action_validate(actor: Actor, action_type: ActionType) -> ActionType:
    match action_type:
        case ActionTypeEnum.ATTACK:
            if actor.energy < 4:
                return ActionTypeEnum.NONE

        case ActionTypeEnum.HEAVY_ATTACK:
            if actor.energy < 6:
                return ActionTypeEnum.NONE

        case ActionTypeEnum.BLOCK:
            if actor.energy < 2:
                return ActionTypeEnum.NONE

        case ActionTypeEnum.REGENERATION:
            if actor.energy < 3 or actor.potions <= 0:
                return ActionTypeEnum.NONE

    return action_type
