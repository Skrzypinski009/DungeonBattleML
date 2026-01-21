from peewee import ForeignKeyField, IntegerField, BooleanField
from .base_model import BaseModel
from .actor import Actor
from .actor_type import ActorType
from .action_type import ActionType
from .battle_state import BattleState


class BattleHistory(BaseModel):
    battle_state = ForeignKeyField(BattleState, on_delete="CASCADE")

    turn_nr = IntegerField(null=False)
    action_nr = IntegerField(null=False)

    player_health = IntegerField(null=False)
    player_energy = IntegerField(null=False)

    enemy_type = ForeignKeyField(ActorType, null=False)
    enemy_health = IntegerField(null=False)
    enemy_energy = IntegerField(null=False)

    action_owner = ForeignKeyField(ActorType)
    action_type = ForeignKeyField(ActionType)
