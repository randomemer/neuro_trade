from peewee import SqliteDatabase, Model, CharField, FloatField, CompositeKey

db = SqliteDatabase("./data/dataset.sqlite3")


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
