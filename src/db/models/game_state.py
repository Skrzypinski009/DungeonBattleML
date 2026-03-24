from peewee import ForeignKeyField, IntegerField

from .actor import Actor
from .base_model import BaseModel


class GameState(BaseModel):
    player = ForeignKeyField(Actor, null=False, on_delete="CASCADE")
    battles_count = IntegerField(null=False)

    def __str__(self) -> str:
        return f"player: {str(self.player)}"
