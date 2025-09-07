import sqlite3
import json
from datetime import datetime

class DataStorage:
    def __init__(self, db_name='wealthflow.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS stock_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                info TEXT,
                history TEXT
            )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS crypto_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                price TEXT,
                market_chart TEXT
            )""")
        self.conn.commit()

    def save_stock_data(self, ticker, info, history):
        timestamp = datetime.now().isoformat()
        # Convert Timestamp keys in history (which is a dict of dicts) to strings
        # history is like {'Open': {Timestamp(...): value}, 'High': {Timestamp(...): value}}
        # We need to convert the inner Timestamp keys to strings as well
        history_serializable = {}
        for col, values in history.items():
            history_serializable[col] = {str(k): v for k, v in values.items()}

        self.cursor.execute(
            "INSERT INTO stock_data (ticker, timestamp, info, history) VALUES (?, ?, ?, ?)",
            (ticker, timestamp, json.dumps(info), json.dumps(history_serializable))
        )
        self.conn.commit()

    def save_crypto_data(self, coin_id, price, market_chart):
        timestamp = datetime.now().isoformat()
        self.cursor.execute(
            "INSERT INTO crypto_data (coin_id, timestamp, price, market_chart) VALUES (?, ?, ?, ?)",
            (coin_id, timestamp, json.dumps(price), json.dumps(market_chart))
        )
        self.conn.commit()

    def get_latest_stock_data(self, ticker):
        self.cursor.execute(
            "SELECT info, history FROM stock_data WHERE ticker = ? ORDER BY timestamp DESC LIMIT 1",
            (ticker,)
        )
        row = self.cursor.fetchone()
        if row:
            return {"info": json.loads(row[0]), "history": json.loads(row[1])}
        return None

    def get_latest_crypto_data(self, coin_id):
        self.cursor.execute(
            "SELECT price, market_chart FROM crypto_data WHERE coin_id = ? ORDER BY timestamp DESC LIMIT 1",
            (coin_id,)
        )
        row = self.cursor.fetchone()
        if row:
            return {"price": json.loads(row[0]), "market_chart": json.loads(row[1])}
        return None

    def close(self):
        self.conn.close()


