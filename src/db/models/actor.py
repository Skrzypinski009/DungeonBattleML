from peewee import ForeignKeyField, IntegerField

from .action_type import ActionType
from .actor_type import ActorType
from .base_model import BaseModel


class Actor(BaseModel):
    type = ForeignKeyField(ActorType)
    health = IntegerField(null=False)
    energy = IntegerField(null=False)
    potions = IntegerField(null=False)
    last_action = ForeignKeyField(ActionType, null=True)
