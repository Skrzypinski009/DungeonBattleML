from peewee import SqliteDatabase
import os


class DatabaseManager:
    db = SqliteDatabase("data/app.db")

    @classmethod
    def get_database(cls) -> SqliteDatabase:
        return cls.db

    @classmethod
    def is_exist(cls) -> bool:
        if os.path.exists("data/app.db"):
            return True
        return False

    @classmethod
    def delete_database(cls) -> None:
        os.remove("data/app.db")

    @classmethod
    def create_tables(cls, models) -> None:
        cls.db.connect()
        cls.db.create_tables(models)
        cls.db.close()
