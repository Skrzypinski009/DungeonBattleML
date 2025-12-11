from models.action_model import ActionModel
from models.actor_model import ActorModel
from models.battle_model import BattleModel
from models.history_model import ActionHistoryModel
from peewee import SqliteDatabase


class Database:
    db = SqliteDatabase("app.db")

    @classmethod
    def get_database(cls) -> SqliteDatabase:
        return cls.db

    @classmethod
    def create_tables(cls) -> None:
        cls.db.connect()
        cls.db.create_tables(
            [
                ActorModel,
                ActionModel,
                BattleModel,
                ActionHistoryModel,
            ]
        )
        cls.db.close()

    @classmethod
    def initialize_actions_table(cls) -> None:
        cls.db.connect()
        ActionModel.create(name="attack")
        ActionModel.create(name="heavy attack")
        ActionModel.create(name="block")
        ActionModel.create(name="regeneration")
        cls.db.close()
