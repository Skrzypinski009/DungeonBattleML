from db.database_manager import DatabaseManager
from db.models import (
    ActionType,
    Actor,
    ActorType,
    BattleState,
    BattleHistory,
    GameState,
    Dataset,
    AI_Model,
)


def fill_database():
    try:
        ActorType.create(name="player", max_health=100, max_energy=8, attack_damage=15)
        ActorType.create(name="rat", max_health=50, max_energy=5, attack_damage=12)
        ActorType.create(name="skeleton", max_health=75, max_energy=6, attack_damage=15)
        ActorType.create(name="orc", max_health=100, max_energy=7, attack_damage=20)

        ActionType.create(name="attack", energy_cost=4)
        ActionType.create(name="heavy attack", energy_cost=6)
        ActionType.create(name="block", energy_cost=2)
        ActionType.create(name="regeneration", energy_cost=3)
        ActionType.create(name="none", energy_cost=0)
    except:
        print("Database fill failed!")

        q1 = ActorType.delete()
        q1.execute()

        q2 = ActionType.delete()
        q2.execute()
    else:
        print("Database fill succeded!")


def create_tables():
    try:
        DatabaseManager.create_tables(
            [
                ActionType,
                Actor,
                ActorType,
                BattleState,
                BattleHistory,
                GameState,
                Dataset,
                AI_Model,
            ],
        )

    except:
        print("Database initialization failed!")
    else:
        print("Database initialization succeded!")


if __name__ == "__main__":
    if DatabaseManager.is_exist():
        DatabaseManager.delete_database()

    create_tables()
    fill_database()
