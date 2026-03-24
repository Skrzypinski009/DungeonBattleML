from peewee import BlobField, TextField
from .base_model import BaseModel


class AI_Model(BaseModel):
    type = TextField()
    name = TextField()
    data = BlobField()
