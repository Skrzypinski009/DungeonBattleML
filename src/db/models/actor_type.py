from peewee import IntegerField, TextField

from .base_model import BaseModel


class ActorType(BaseModel):
    name = TextField(null=False)
    max_health = IntegerField(null=False)
    max_energy = IntegerField(null=False)
    attack_damage = IntegerField(null=False)
