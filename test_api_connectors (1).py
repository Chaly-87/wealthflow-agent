from api_connectors import YahooFinanceAPI, CoinGeckoAPI

def test_yahoo_finance():
    yf_api = YahooFinanceAPI()
    print("\nTesting Yahoo Finance API (AAPL):")
    data = yf_api.get_stock_data("AAPL")
    if data and "error" not in data:
        print("AAPL Info Keys:", data["info"].keys())
        print("AAPL History (last day):")
        print(data["history"])
    else:
        print("Error fetching AAPL data:", data.get("error", "Unknown error"))

def test_coingecko():
    cg_api = CoinGeckoAPI()
    print("\nTesting CoinGecko API (bitcoin):")
    price = cg_api.get_coin_price("bitcoin")
    if price and "error" not in price:
        print("Bitcoin Price:", price)
    else:
        print("Error fetching Bitcoin price:", price.get("error", "Unknown error"))

    print("\nTesting CoinGecko API (ethereum market chart):")
    market_chart = cg_api.get_coin_market_chart("ethereum", days="1")
    if market_chart and "error" not in market_chart:
        print("Ethereum Market Chart (first 5 prices):")
        if "prices" in market_chart:
            print(market_chart["prices"][:5])
        else:
            print("No 'prices' in market chart data.")
    else:
        print("Error fetching Ethereum market chart:", market_chart.get("error", "Unknown error"))

if __name__ == "__main__":
    test_yahoo_finance()
    test_coingecko()


