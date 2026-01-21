from peewee import Model
from db.database_manager import DatabaseManager


class BaseModel(Model):
    class Meta:
        database = DatabaseManager.get_database()
