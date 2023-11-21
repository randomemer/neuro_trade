import os

from peewee import CharField, CompositeKey, FloatField, Model, SqliteDatabase

db_path = "./data/dataset.sqlite3"
dir_name = os.path.dirname(db_path)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

db = SqliteDatabase(db_path)


class StockCandleData(Model):
    symbol = CharField()
    timestamp = CharField()

    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = FloatField()

    class Meta:
        database = db
        primary_key = CompositeKey("symbol", "timestamp")


def connect() -> SqliteDatabase:
    db.connect()
    db.create_tables([StockCandleData])

    return db
