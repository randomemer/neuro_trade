import os

from peewee import CharField, CompositeKey, FloatField, Model, SqliteDatabase

db_path = "./data/dataset.sqlite3"
if not os.path.exists(db_path):
    os.makedirs(db_path)
db = SqliteDatabase(db_path)


class StockCandleData(Model):
    symbol = CharField()
    timestamp = CharField()

    open_price = FloatField()
    high_price = FloatField()
    low_price = FloatField()
    close_price = FloatField()

    class Meta:
        database = db
        primary_key = CompositeKey("symbol", "timestamp")


def connect() -> SqliteDatabase:
    db.connect()
    db.create_tables([StockCandleData])

    return db
