from base_model import BaseModel
from peewee import TextField


class ActionModel(BaseModel):
    name = TextField(null=False)
