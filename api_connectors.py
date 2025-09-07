import yfinance as yf
import requests
import json

class YahooFinanceAPI:
    def get_stock_data(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1d")
            return {"info": info, "history": hist.to_dict()}
        except Exception as e:
            return {"error": str(e)}

class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_coin_price(self, coin_id, vs_currencies="usd"):
        try:
            url = f"{self.BASE_URL}/simple/price?ids={coin_id}&vs_currencies={vs_currencies}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_coin_market_chart(self, coin_id, vs_currency="usd", days="1"):
        try:
            url = f"{self.BASE_URL}/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={days}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

class AlphaVantageAPI:
    # This class will be implemented later, as it requires an API key and has rate limits.
    # For now, we'll focus on Yahoo Finance and CoinGecko.
    def __init__(self, api_key):
        self.api_key = api_key
        self.BASE_URL = "https://www.alphavantage.co/query"

    def get_daily_adjusted(self, symbol):
        try:
            params = {
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": symbol,
                "apikey": self.api_key
            }
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_intraday(self, symbol, interval="5min"):
        try:
            params = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": interval,
                "apikey": self.api_key
            }
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}



