from actor_model import ActorModel
from base_model import BaseModel
from peewee import ForeignKeyField


class BattleModel(BaseModel):
    player = ForeignKeyField(ActorModel)
    enemy = ForeignKeyField(ActorModel)
