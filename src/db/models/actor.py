from peewee import ForeignKeyField, IntegerField
from .action_type import ActionType
from .base_model import BaseModel
from .actor_type import ActorType


class Actor(BaseModel):
    type = ForeignKeyField(ActorType)
    health = IntegerField(null=False)
    energy = IntegerField(null=False)
    potions = IntegerField(null=False)
    last_action = ForeignKeyField(ActionType, null=True)
