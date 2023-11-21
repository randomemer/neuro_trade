import os
from typing import Any, Dict, List

import database
import requests
from alpaca.data import MostActivesRequest
from alpaca.data.historical.screener import ScreenerClient
from database import StockCandleData
from dotenv import load_dotenv
from ratelimiter import RateLimiter

load_dotenv()

api_key = os.getenv("ALPACA_API_KEY")
secret_key = os.getenv("ALPACA_SECRET_KEY")

rate_limiter = RateLimiter(200, 60)


class AlpacaScraper:
    BASE_URL = "https://data.alpaca.markets/v2"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": secret_key,
    }

    def get_top_stocks(self, count: int):
        """Get the top stocks by volume of trade"""
        with rate_limiter:
            client = ScreenerClient(api_key, secret_key)
            request = MostActivesRequest(top=count)

            return client.get_most_actives(request)

    def fetch_stock_history(
        self, symbol: str, page_token: str | None
    ) -> Dict[str, Any]:
        """Fetch historical data for a given symbol"""
        params = {
            "timeframe": "5Min",
            "start": "2015-01-01",
            "limit": 10_000,
            "page_token": page_token,
        }

        with rate_limiter:
            resp = requests.get(
                f"{self.BASE_URL}/stocks/{symbol}/bars",
                headers=self.headers,
                params=params,
            )

            return resp.json()

    def save_bars_database(self, bars: List[Dict[str, Any]]):
        # Save to sqlite db
        models = []
        for bar in bars:
            candle = StockCandleData(
                symbol=symbol,
                timestamp=bar["t"],
                open=bar["o"],
                high=bar["h"],
                low=bar["l"],
                close=bar["c"],
                volume=bar["v"],
            )
            models.append(candle)

        with db.atomic():
            StockCandleData.bulk_create(models, batch_size=100)


if __name__ == "__main__":
    scraper = AlpacaScraper()
    db = database.connect()

    # Get top 50 most active stocks
    symbols = scraper.get_top_stocks(50)
    print("Fetched 50 stocks by volume\n")

    # Get all candlestick data for 5 Min intervals since 2015
    for i, stock in enumerate(symbols.most_actives):
        symbol = stock.symbol
        bars = []

        # Fetch candlesticks for this stock
        res = None
        while True:
            page_token = res["next_page_token"] if res else None
            res = scraper.fetch_stock_history(symbol, page_token)

            bars.extend(res["bars"])

            if not res or not res["next_page_token"]:
                break

            print(f"({i+1}/50) {symbol} : Fetched candles till {bars[-1]['t']}")

        scraper.save_bars_database(bars)
        print(f"({i+1}/50) {symbol} : Added {len(bars)} candlesticks to database\n")

    print("Completed scraping job")
