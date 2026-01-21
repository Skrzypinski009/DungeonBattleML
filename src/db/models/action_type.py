from .base_model import BaseModel
from peewee import IntegerField, TextField


class ActionType(BaseModel):
    name = TextField(null=False)
    energy_cost = IntegerField(null=False)
