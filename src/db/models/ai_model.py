from peewee import TextField

from .base_model import BaseModel


class AI_Model(BaseModel):
    type = TextField(null=False)
    name = TextField(null=False)
    file_name = TextField(null=False)
