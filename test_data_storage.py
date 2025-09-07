from data_storage import DataStorage
import json

def test_data_storage():
    db = DataStorage(db_name="test_wealthflow.db")

    # Test saving stock data
    stock_info = {"symbol": "AAPL", "price": 150.0}
    stock_history = {"2025-09-01": {"Open": 149.0, "Close": 150.0}}
    db.save_stock_data("AAPL", stock_info, stock_history)
    print("Saved AAPL data.")

    # Test retrieving stock data
    retrieved_stock = db.get_latest_stock_data("AAPL")
    print("Retrieved AAPL data:", retrieved_stock)
    assert retrieved_stock["info"] == stock_info
    assert retrieved_stock["history"] == stock_history

    # Test saving crypto data
    crypto_price = {"bitcoin": {"usd": 50000}}
    crypto_market_chart = {"prices": [[1678886400000, 50000]]}
    db.save_crypto_data("bitcoin", crypto_price, crypto_market_chart)
    print("Saved bitcoin data.")

    # Test retrieving crypto data
    retrieved_crypto = db.get_latest_crypto_data("bitcoin")
    print("Retrieved bitcoin data:", retrieved_crypto)
    assert retrieved_crypto["price"] == crypto_price
    assert retrieved_crypto["market_chart"] == crypto_market_chart

    db.close()
    print("Data storage tests completed.")

if __name__ == "__main__":
    test_data_storage()


