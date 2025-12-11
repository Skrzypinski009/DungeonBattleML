from base_model import BaseModel
from actor_model import ActorModel
from action_model import ActionModel
from battle_model import BattleModel
from peewee import IntegerField, ForeignKeyField


class ActionHistoryModel(BaseModel):
    turn = IntegerField(null=False)
    action_sequence = IntegerField(null=False)
    actor = ForeignKeyField(ActorModel, backref="actions_history")
    action = ForeignKeyField(ActionModel)
    battle = ForeignKeyField(BattleModel)
