from db.models import ActorType


def get_numerical(actor_name: str):
    return {
        "player": 1,
        "rat": 2,
        "skeleton": 3,
        "orc": 4,
    }[actor_name]
