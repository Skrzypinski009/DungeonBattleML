from peewee import *


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase("gra_walki_orm.db")
