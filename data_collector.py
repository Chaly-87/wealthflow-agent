from api_connectors import YahooFinanceAPI, CoinGeckoAPI, AlphaVantageAPI
from data_storage import DataStorage
import time
import os

class DataCollector:
    def __init__(self, db_name='wealthflow.db', alpha_vantage_api_key=None):
        self.yf_api = YahooFinanceAPI()
        self.cg_api = CoinGeckoAPI()
        self.av_api = AlphaVantageAPI(alpha_vantage_api_key) if alpha_vantage_api_key else None
        self.db = DataStorage(db_name)

    def collect_stock_data(self, ticker):
        print(f"Collecting stock data for {ticker}...")
        data = self.yf_api.get_stock_data(ticker)
        if data and "error" not in data:
            self.db.save_stock_data(ticker, data["info"], data["history"])
            print(f"Successfully collected and saved data for {ticker}.")
        else:
            print(f"Error collecting data for {ticker}: {data.get('error', 'Unknown error')}")

    def collect_crypto_data(self, coin_id):
        print(f"Collecting crypto data for {coin_id}...")
        price = self.cg_api.get_coin_price(coin_id)
        market_chart = self.cg_api.get_coin_market_chart(coin_id)
        if price and "error" not in price and market_chart and "error" not in market_chart:
            self.db.save_crypto_data(coin_id, price, market_chart)
            print(f"Successfully collected and saved data for {coin_id}.")
        else:
            print(f"Error collecting data for {coin_id}: price_error={price.get('error', 'N/A')}, chart_error={market_chart.get('error', 'N/A')}")

    def run_collection_loop(self, stocks, cryptos, interval=60):
        while True:
            for stock in stocks:
                self.collect_stock_data(stock)
            for crypto in cryptos:
                self.collect_crypto_data(crypto)
            print(f"\nCollection cycle finished. Waiting for {interval} seconds...")
            time.sleep(interval)

if __name__ == "__main__":
    # Example usage:
    # To run this, you would need to set the ALPHA_VANTAGE_API_KEY environment variable
    # alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    # collector = DataCollector(alpha_vantage_api_key=alpha_vantage_key)
    
    # For this example, we will not use Alpha Vantage
    collector = DataCollector()

    # Define the assets to monitor
    stocks_to_monitor = ["AAPL", "GOOGL", "MSFT"]
    cryptos_to_monitor = ["bitcoin", "ethereum", "dogecoin"]

    # Run the collection loop (for a limited number of iterations for this example)
    for _ in range(2): # Run twice for demonstration
        for stock in stocks_to_monitor:
            collector.collect_stock_data(stock)
        for crypto in cryptos_to_monitor:
            collector.collect_crypto_data(crypto)
        print("\nCollection cycle finished. Waiting for 10 seconds...")
        time.sleep(10)

    collector.db.close()
    print("\nData collection example finished.")


