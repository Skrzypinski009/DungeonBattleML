from base_model import BaseModel
from peewee import *


class ActorModel(BaseModel):
    name = TextField(null=False)
    health = IntegerField(null=False)
    energy = IntegerField(null=False)
