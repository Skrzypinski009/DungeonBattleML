from db.database_manager import DatabaseManager
from peewee import Model


class BaseModel(Model):
    class Meta:
        database = DatabaseManager.get_database()
