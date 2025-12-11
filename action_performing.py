from game_state import Stats
from action import Action


def perform_action(initiative_stats: Stats, passive_stats: Stats) -> None:
    if initiative_stats.name == "enemy":
        print(" " * 50, end="")
    print(f"[{initiative_stats.name}]", end=":  ")

    match (initiative_stats.action):
        case Action.ATTACK:
            perform_attack(initiative_stats, passive_stats)

        case Action.HEAVY_ATTACK:
            perform_heavy_attack(initiative_stats, passive_stats)

        case Action.REST:
            perform_rest(initiative_stats)

        case Action.BLOCK:
            perform_block()

    if initiative_stats.name == "enemy":
        print(" " * 50, end="")

    print(
        f"życie: {initiative_stats.hp}, energia: {initiative_stats.energy}",
        end="\n\n",
    )


def perform_attack(initiative_stats: Stats, passive_stats: Stats):
    # Sprawdzenie możliwości wykonania ataku
    if initiative_stats.energy < 3:
        print("Nie udało się wykonać ataku, zbyt mała ilość energii")
    else:
        # wykonanie ataku
        initiative_stats.energy -= 3
        if passive_stats.action != Action.BLOCK:
            passive_stats.hp -= 30
            print("Atak ⚔️")
        else:
            print("Atak zablokowany ⚔️ 🛡️")


def perform_heavy_attack(initiative_stats: Stats, passive_stats: Stats):
    # Sprawdzenie możliwości wykonania ataku
    if initiative_stats.energy < 6:
        print("Nie udało się wykonać ataku, zbyt mała ilość energii")
    else:
        # wykonanie ataku
        initiative_stats.energy -= 6
        if passive_stats.action != Action.BLOCK:
            passive_stats.hp -= 60
            print("Mocny atak ⚔️ ⚔️")
        else:
            print("Mocny atak zablokowany ⚔️️️ 🛡")


def perform_rest(initiative_stats: Stats):
    # odnowienie hp
    initiative_stats.hp += 40
    initiative_stats.hp = min(initiative_stats.hp, 100)

    # odnowienie energii
    initiative_stats.energy += 5
    initiative_stats.energy = min(initiative_stats.energy, 10)
    print("Regeneracja")


def perform_block() -> None:
    print("Block")
