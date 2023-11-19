import os
from datetime import datetime

from alpaca.data import MostActivesRequest, StockBarsRequest, TimeFrame
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical.screener import ScreenerClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")


def get_top_stocks(count: int):
    """Get the top stocks by volume of trade"""
    client = ScreenerClient(api_key, secret_key)

    request = MostActivesRequest(top=count)
    return client.get_most_actives(request)


def fetch_stock_history(symbol: str):
    """Fetch historical data for a given symbol"""
    stock_client = StockHistoricalDataClient(api_key, secret_key)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        limit=10_000,
        timeframe=TimeFrame(5, TimeFrame.Minute),
        start=datetime(2015, 1, 1),
    )
    resp = stock_client.get_stock_bars(request)

    return resp


if __name__ == "__main__":
    # Get top 50 most active stocks
    symbols = get_top_stocks(50)

    for stock in symbols.most_actives:
        pass

    h = fetch_stock_history(symbols.most_actives[0].symbol)
    print(h["CYTO"])
