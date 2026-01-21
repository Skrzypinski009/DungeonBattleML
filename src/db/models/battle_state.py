from db.models.action_type import ActionType
from db.models.game_state import GameState
from .actor import Actor
from .base_model import BaseModel
from .actor_type import ActorType
from peewee import ForeignKeyAccessor, ForeignKeyField, IntegerField


class BattleState(BaseModel):
    game = ForeignKeyField(GameState, null=False)
    battle_nr = IntegerField(null=False)
    turn_nr = IntegerField(null=False)
    action_nr = IntegerField(null=False)
    current_actor = ForeignKeyField(Actor, null=False)
    enemy = ForeignKeyField(Actor, on_delete="CASCADE")
    winner = ForeignKeyField(Actor, null=True)

    def __str__(self) -> str:
        s = f"BattleState id: {str(self.id)}, \n"  # pyright: ignore
        s += f"battle_nr: {str(self.battle_nr)}, \n"
        s += f"round_nr: {str(self.turn_nr)}, \n"
        s += f"current_actor: {str(self.current_actor)}, \n"
        s += f"enemy: {str(self.enemy)}, \n"
        s += f"winner: {str(self.winner)}\n"
        return s
