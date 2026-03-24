from peewee import ForeignKeyField, IntegerField

from .action_type import ActionType
from .actor_type import ActorType
from .base_model import BaseModel


class Actor(BaseModel):
    type = ForeignKeyField(ActorType)
    health = IntegerField()
    energy = IntegerField()
    potions = IntegerField()
    last_action = ForeignKeyField(ActionType, null=True)
