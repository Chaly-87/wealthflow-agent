import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable
from api_connectors import YahooFinanceAPI, CoinGeckoAPI
from data_storage import DataStorage
from sentiment_analyzer import SentimentAnalyzer
from social_crawler import SocialCrawler
from alert_system import AlertSystem

class TriggerEngine:
    def __init__(self, db_name: str = 'wealthflow.db'):
        """
        Initialize the trigger engine.
        
        Args:
            db_name: Database name for data storage
        """
        self.db = DataStorage(db_name)
        self.yf_api = YahooFinanceAPI()
        self.cg_api = CoinGeckoAPI()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.social_crawler = SocialCrawler()
        self.alert_system = AlertSystem()
        
        self.running = False
        self.monitoring_thread = None
        
        # Assets to monitor
        self.monitored_stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]
        self.monitored_cryptos = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana"]
        
        # Monitoring intervals (in seconds)
        self.stock_check_interval = 300  # 5 minutes
        self.crypto_check_interval = 180  # 3 minutes
        self.sentiment_check_interval = 600  # 10 minutes
        
        # Last check timestamps
        self.last_stock_check = datetime.min
        self.last_crypto_check = datetime.min
        self.last_sentiment_check = datetime.min
        
    def start_monitoring(self):
        """Start the monitoring engine."""
        if self.running:
            print("Trigger engine is already running")
            return
        
        self.running = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        print("Trigger engine started")
    
    def stop_monitoring(self):
        """Stop the monitoring engine."""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print("Trigger engine stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                current_time = datetime.now()
                
                # Check stocks
                if (current_time - self.last_stock_check).total_seconds() >= self.stock_check_interval:
                    self._check_stock_triggers()
                    self.last_stock_check = current_time
                
                # Check cryptos
                if (current_time - self.last_crypto_check).total_seconds() >= self.crypto_check_interval:
                    self._check_crypto_triggers()
                    self.last_crypto_check = current_time
                
                # Check sentiment
                if (current_time - self.last_sentiment_check).total_seconds() >= self.sentiment_check_interval:
                    self._check_sentiment_triggers()
                    self.last_sentiment_check = current_time
                
                # Sleep for a short interval before next check
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_stock_triggers(self):
        """Check triggers for monitored stocks."""
        print(f"Checking stock triggers at {datetime.now()}")
        
        for ticker in self.monitored_stocks:
            try:
                # Get current data
                current_data = self.yf_api.get_stock_data(ticker)
                if "error" in current_data:
                    continue
                
                # Get historical data from database
                historical_data = self._get_historical_stock_data(ticker, days=30)
                
                if not historical_data:
                    continue
                
                # Check volume anomaly
                current_volume = self._extract_current_volume(current_data)
                historical_volumes = [d["volume"] for d in historical_data if d.get("volume")]
                
                if current_volume and historical_volumes:
                    volume_result = self.alert_system.detect_volume_anomaly(current_volume, historical_volumes)
                    
                    if volume_result["anomaly_detected"]:
                        alert = self.alert_system.generate_alert(
                            "volume_anomaly", ticker, volume_result, "high"
                        )
                        print(f"Volume anomaly alert: {alert['message']}")
                
                # Check pump and dump patterns
                price_history = self._format_price_history(historical_data)
                if len(price_history) >= 10:
                    pump_dump_result = self.alert_system.detect_pump_and_dump_pattern(
                        price_history, historical_volumes
                    )
                    
                    if pump_dump_result["pattern_detected"]:
                        urgency = "high" if pump_dump_result["pump_detected"] else "medium"
                        alert = self.alert_system.generate_alert(
                            "pump_dump", ticker, pump_dump_result, urgency
                        )
                        print(f"Pump/dump alert: {alert['message']}")
                
            except Exception as e:
                print(f"Error checking triggers for {ticker}: {e}")
    
    def _check_crypto_triggers(self):
        """Check triggers for monitored cryptocurrencies."""
        print(f"Checking crypto triggers at {datetime.now()}")
        
        for coin_id in self.monitored_cryptos:
            try:
                # Get current price data
                current_price = self.cg_api.get_coin_price(coin_id)
                if "error" in current_price:
                    continue
                
                # Get market chart data
                market_chart = self.cg_api.get_coin_market_chart(coin_id, days="7")
                if "error" in market_chart:
                    continue
                
                # Extract price and volume data
                if "prices" in market_chart and "total_volumes" in market_chart:
                    prices = market_chart["prices"]
                    volumes = market_chart["total_volumes"]
                    
                    # Check for volume anomalies
                    if len(volumes) > 10:
                        current_volume = volumes[-1][1]  # Latest volume
                        historical_volumes = [v[1] for v in volumes[:-1]]  # Previous volumes
                        
                        volume_result = self.alert_system.detect_volume_anomaly(
                            current_volume, historical_volumes
                        )
                        
                        if volume_result["anomaly_detected"]:
                            alert = self.alert_system.generate_alert(
                                "volume_anomaly", coin_id, volume_result, "high"
                            )
                            print(f"Crypto volume alert: {alert['message']}")
                    
                    # Check for pump and dump patterns
                    if len(prices) > 10:
                        price_history = [{"close": p[1], "timestamp": p[0]} for p in prices]
                        volume_history = [v[1] for v in volumes]
                        
                        pump_dump_result = self.alert_system.detect_pump_and_dump_pattern(
                            price_history, volume_history
                        )
                        
                        if pump_dump_result["pattern_detected"]:
                            urgency = "high" if pump_dump_result["pump_detected"] else "medium"
                            alert = self.alert_system.generate_alert(
                                "pump_dump", coin_id, pump_dump_result, urgency
                            )
                            print(f"Crypto pump/dump alert: {alert['message']}")
                
            except Exception as e:
                print(f"Error checking crypto triggers for {coin_id}: {e}")
    
    def _check_sentiment_triggers(self):
        """Check sentiment-based triggers."""
        print(f"Checking sentiment triggers at {datetime.now()}")
        
        # Check sentiment for all monitored assets
        all_assets = self.monitored_stocks + self.monitored_cryptos
        
        for asset in all_assets:
            try:
                # Get recent social media mentions (mock data for now)
                # In a real implementation, this would use the social crawler
                mock_mentions = [
                    f"{asset} is looking bullish today!",
                    f"Big news coming for {asset}",
                    f"{asset} to the moon!",
                    f"Selling my {asset} position",
                    f"{asset} announcement tomorrow"
                ]
                
                # Analyze sentiment
                sentiment_results = []
                for mention in mock_mentions:
                    result = self.sentiment_analyzer.analyze_text_sentiment(mention, asset)
                    if "error" not in result:
                        sentiment_results.append(result)
                
                # Check for sentiment spikes
                if sentiment_results:
                    sentiment_spike_result = self.alert_system.check_news_sentiment_spike(
                        sentiment_results, asset
                    )
                    
                    if sentiment_spike_result["spike_detected"]:
                        urgency = "high" if sentiment_spike_result.get("positive_spike") else "medium"
                        alert = self.alert_system.generate_alert(
                            "sentiment_spike", asset, sentiment_spike_result, urgency
                        )
                        print(f"Sentiment alert: {alert['message']}")
                
            except Exception as e:
                print(f"Error checking sentiment for {asset}: {e}")
    
    def _get_historical_stock_data(self, ticker: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get historical stock data from database."""
        # This is a simplified version - in a real implementation,
        # you would query the database for historical data
        return []
    
    def _extract_current_volume(self, stock_data: Dict[str, Any]) -> float:
        """Extract current volume from stock data."""
        try:
            history = stock_data.get("history", {})
            volume_data = history.get("Volume", {})
            if volume_data:
                # Get the latest volume value
                return list(volume_data.values())[0]
        except:
            pass
        return 0.0
    
    def _format_price_history(self, historical_data: List[Dict[str, Any]]) -> List[Dict[str, float]]:
        """Format historical data for pump/dump detection."""
        # This is a placeholder - in a real implementation,
        # you would format the actual historical data
        return []
    
    def add_monitored_asset(self, asset_type: str, asset_name: str):
        """Add an asset to monitoring list."""
        if asset_type == "stock" and asset_name not in self.monitored_stocks:
            self.monitored_stocks.append(asset_name)
            print(f"Added {asset_name} to stock monitoring")
        elif asset_type == "crypto" and asset_name not in self.monitored_cryptos:
            self.monitored_cryptos.append(asset_name)
            print(f"Added {asset_name} to crypto monitoring")
    
    def remove_monitored_asset(self, asset_type: str, asset_name: str):
        """Remove an asset from monitoring list."""
        if asset_type == "stock" and asset_name in self.monitored_stocks:
            self.monitored_stocks.remove(asset_name)
            print(f"Removed {asset_name} from stock monitoring")
        elif asset_type == "crypto" and asset_name in self.monitored_cryptos:
            self.monitored_cryptos.remove(asset_name)
            print(f"Removed {asset_name} from crypto monitoring")
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status."""
        return {
            "running": self.running,
            "monitored_stocks": self.monitored_stocks,
            "monitored_cryptos": self.monitored_cryptos,
            "last_checks": {
                "stocks": self.last_stock_check.isoformat(),
                "cryptos": self.last_crypto_check.isoformat(),
                "sentiment": self.last_sentiment_check.isoformat()
            },
            "intervals": {
                "stock_check": self.stock_check_interval,
                "crypto_check": self.crypto_check_interval,
                "sentiment_check": self.sentiment_check_interval
            }
        }

