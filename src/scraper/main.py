import os

from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data import MostActivesRequest


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


if __name__ == "__main__":
    # Get top 50 most active stocks
    symbols = get_top_stocks(50)

    print(symbols)
