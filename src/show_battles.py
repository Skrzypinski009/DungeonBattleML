from services import battle_service


def show_battles():
    print(battle_service.get_battles_list())


if __name__ == "__main__":
    show_battles()
    exit()
