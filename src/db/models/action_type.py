from peewee import IntegerField, TextField

from .base_model import BaseModel


class ActionType(BaseModel):
    name = TextField(null=False)
    energy_cost = IntegerField(null=False)
