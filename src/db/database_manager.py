import os

from peewee import SqliteDatabase


class DatabaseManager:
    db = SqliteDatabase("data/app.db")

    @classmethod
    def get_database(cls) -> SqliteDatabase:
        return cls.db

    @staticmethod
    def is_exist() -> bool:
        if os.path.exists("data/app.db"):
            return True
        return False

    @staticmethod
    def delete_database() -> None:
        os.remove("data/app.db")

    @classmethod
    def create_tables(cls, models) -> None:
        cls.db.connect()
        cls.db.create_tables(models)
        cls.db.close()
