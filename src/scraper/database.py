from peewee import SqliteDatabase, Model, CharField, FloatField

db = SqliteDatabase("./data/dataset.sqlite3")


class StockCandleData(Model):
    stock_symbol = CharField()
    timestamp = CharField()

    open_price = FloatField()
    high_price = FloatField()
    low_price = FloatField()
    close_price = FloatField()

    class Meta:
        database = db


def connect() -> SqliteDatabase:
    db.connect()
    db.create_tables([StockCandleData])

    return db
