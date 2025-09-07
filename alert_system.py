import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import statistics
import requests

class AlertSystem:
    def __init__(self, email_config: Dict[str, str] = None):
        """
        Initialize the alert system.
        
        Args:
            email_config: Dictionary with email configuration
                         {'smtp_server': 'smtp.gmail.com', 'smtp_port': 587, 
                          'email': 'your_email@gmail.com', 'password': 'your_password'}
        """
        self.email_config = email_config
        self.alert_history = []
        
        # Thresholds for different alert types
        self.volume_threshold_multiplier = 3.0  # 3x normal volume
        self.price_change_threshold = 0.15  # 15% price change
        self.sentiment_threshold = 0.7  # High confidence sentiment
        
    def detect_volume_anomaly(self, current_volume: float, historical_volumes: List[float]) -> Dict[str, Any]:
        """
        Detect if current volume is anomalously high.
        
        Args:
            current_volume: Current trading volume
            historical_volumes: List of historical volumes for comparison
            
        Returns:
            Dictionary with anomaly detection results
        """
        if not historical_volumes or len(historical_volumes) < 5:
            return {"anomaly_detected": False, "reason": "Insufficient historical data"}
        
        avg_volume = statistics.mean(historical_volumes)
        std_volume = statistics.stdev(historical_volumes) if len(historical_volumes) > 1 else 0
        
        # Calculate z-score
        z_score = (current_volume - avg_volume) / std_volume if std_volume > 0 else 0
        
        # Check if volume is significantly higher than normal
        volume_multiplier = current_volume / avg_volume if avg_volume > 0 else 0
        
        anomaly_detected = (
            volume_multiplier > self.volume_threshold_multiplier or 
            z_score > 2.5  # 2.5 standard deviations above mean
        )
        
        return {
            "anomaly_detected": anomaly_detected,
            "current_volume": current_volume,
            "average_volume": avg_volume,
            "volume_multiplier": volume_multiplier,
            "z_score": z_score,
            "threshold_multiplier": self.volume_threshold_multiplier
        }
    
    def detect_pump_and_dump_pattern(self, price_history: List[Dict[str, float]], 
                                   volume_history: List[float]) -> Dict[str, Any]:
        """
        Detect potential pump and dump patterns.
        
        Args:
            price_history: List of price data with timestamps
            volume_history: List of volume data
            
        Returns:
            Dictionary with pump and dump detection results
        """
        if len(price_history) < 10 or len(volume_history) < 10:
            return {"pattern_detected": False, "reason": "Insufficient data"}
        
        # Get recent price changes
        recent_prices = [p["close"] for p in price_history[-10:]]
        recent_volumes = volume_history[-10:]
        
        # Calculate price change over recent period
        price_change = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
        
        # Calculate volume spike
        avg_volume = statistics.mean(recent_volumes[:-3])  # Exclude last 3 periods
        recent_avg_volume = statistics.mean(recent_volumes[-3:])  # Last 3 periods
        volume_spike = recent_avg_volume / avg_volume if avg_volume > 0 else 0
        
        # Pump detection: rapid price increase with high volume
        pump_detected = (
            price_change > self.price_change_threshold and 
            volume_spike > 2.0
        )
        
        # Dump detection: rapid price decrease after recent high
        max_recent_price = max(recent_prices)
        current_price = recent_prices[-1]
        dump_from_high = (max_recent_price - current_price) / max_recent_price
        
        dump_detected = dump_from_high > 0.1  # 10% drop from recent high
        
        return {
            "pump_detected": pump_detected,
            "dump_detected": dump_detected,
            "price_change": price_change,
            "volume_spike": volume_spike,
            "dump_from_high": dump_from_high,
            "pattern_detected": pump_detected or dump_detected
        }
    
    def check_news_sentiment_spike(self, sentiment_data: List[Dict[str, Any]], 
                                 asset_name: str) -> Dict[str, Any]:
        """
        Check for sudden spikes in news sentiment.
        
        Args:
            sentiment_data: List of sentiment analysis results
            asset_name: Name of the asset being analyzed
            
        Returns:
            Dictionary with sentiment spike detection results
        """
        if not sentiment_data:
            return {"spike_detected": False, "reason": "No sentiment data"}
        
        # Filter for high-confidence sentiments
        high_confidence_sentiments = [
            s for s in sentiment_data 
            if s.get("confidence", 0) > self.sentiment_threshold
        ]
        
        if len(high_confidence_sentiments) < 3:
            return {"spike_detected": False, "reason": "Insufficient high-confidence data"}
        
        # Count positive vs negative sentiments
        positive_count = sum(1 for s in high_confidence_sentiments if s.get("sentiment") == "positive")
        negative_count = sum(1 for s in high_confidence_sentiments if s.get("sentiment") == "negative")
        total_count = len(high_confidence_sentiments)
        
        # Calculate sentiment ratios
        positive_ratio = positive_count / total_count
        negative_ratio = negative_count / total_count
        
        # Detect sentiment spikes
        positive_spike = positive_ratio > 0.7  # 70% positive sentiment
        negative_spike = negative_ratio > 0.7  # 70% negative sentiment
        
        return {
            "spike_detected": positive_spike or negative_spike,
            "positive_spike": positive_spike,
            "negative_spike": negative_spike,
            "positive_ratio": positive_ratio,
            "negative_ratio": negative_ratio,
            "total_mentions": total_count,
            "asset_name": asset_name
        }
    
    def generate_alert(self, alert_type: str, asset_name: str, 
                      data: Dict[str, Any], urgency: str = "medium") -> Dict[str, Any]:
        """
        Generate an alert based on detected patterns.
        
        Args:
            alert_type: Type of alert ('volume_anomaly', 'pump_dump', 'sentiment_spike')
            asset_name: Name of the asset
            data: Detection data
            urgency: Alert urgency level ('low', 'medium', 'high')
            
        Returns:
            Alert dictionary
        """
        alert = {
            "id": f"{alert_type}_{asset_name}_{int(datetime.now().timestamp())}",
            "type": alert_type,
            "asset_name": asset_name,
            "timestamp": datetime.now().isoformat(),
            "urgency": urgency,
            "data": data,
            "message": self._generate_alert_message(alert_type, asset_name, data)
        }
        
        self.alert_history.append(alert)
        return alert
    
    def _generate_alert_message(self, alert_type: str, asset_name: str, 
                              data: Dict[str, Any]) -> str:
        """Generate human-readable alert message."""
        if alert_type == "volume_anomaly":
            multiplier = data.get("volume_multiplier", 0)
            return f"🚨 VOLUME ALERT: {asset_name} trading volume is {multiplier:.1f}x normal levels!"
        
        elif alert_type == "pump_dump":
            if data.get("pump_detected"):
                price_change = data.get("price_change", 0) * 100
                return f"📈 PUMP ALERT: {asset_name} up {price_change:.1f}% with high volume!"
            elif data.get("dump_detected"):
                dump_pct = data.get("dump_from_high", 0) * 100
                return f"📉 DUMP ALERT: {asset_name} down {dump_pct:.1f}% from recent high!"
        
        elif alert_type == "sentiment_spike":
            if data.get("positive_spike"):
                ratio = data.get("positive_ratio", 0) * 100
                return f"🚀 SENTIMENT ALERT: {asset_name} has {ratio:.0f}% positive mentions!"
            elif data.get("negative_spike"):
                ratio = data.get("negative_ratio", 0) * 100
                return f"⚠️ SENTIMENT ALERT: {asset_name} has {ratio:.0f}% negative mentions!"
        
        return f"Alert for {asset_name}: {alert_type}"
    
    def send_email_alert(self, alert: Dict[str, Any], recipient_email: str) -> bool:
        """
        Send alert via email.
        
        Args:
            alert: Alert dictionary
            recipient_email: Email address to send alert to
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.email_config:
            print("Email configuration not provided")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email']
            msg['To'] = recipient_email
            msg['Subject'] = f"WealthFlow Alert: {alert['asset_name']} - {alert['urgency'].upper()}"
            
            body = f"""
            WealthFlow Agent Alert
            
            Asset: {alert['asset_name']}
            Type: {alert['type']}
            Urgency: {alert['urgency']}
            Time: {alert['timestamp']}
            
            Message: {alert['message']}
            
            Data: {json.dumps(alert['data'], indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['email'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['email'], recipient_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Failed to send email alert: {e}")
            return False
    
    def send_webhook_alert(self, alert: Dict[str, Any], webhook_url: str) -> bool:
        """
        Send alert via webhook (e.g., Slack, Discord, etc.).
        
        Args:
            alert: Alert dictionary
            webhook_url: Webhook URL to send alert to
            
        Returns:
            True if webhook sent successfully, False otherwise
        """
        try:
            payload = {
                "text": f"WealthFlow Alert: {alert['message']}",
                "attachments": [
                    {
                        "color": "danger" if alert['urgency'] == "high" else "warning",
                        "fields": [
                            {"title": "Asset", "value": alert['asset_name'], "short": True},
                            {"title": "Type", "value": alert['type'], "short": True},
                            {"title": "Urgency", "value": alert['urgency'], "short": True},
                            {"title": "Time", "value": alert['timestamp'], "short": True}
                        ]
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=payload)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Failed to send webhook alert: {e}")
            return False
    
    def get_recent_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get alerts from the last N hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_alerts = []
        for alert in self.alert_history:
            alert_time = datetime.fromisoformat(alert['timestamp'])
            if alert_time > cutoff_time:
                recent_alerts.append(alert)
        
        return recent_alerts
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of all alerts."""
        if not self.alert_history:
            return {"total_alerts": 0}
        
        total_alerts = len(self.alert_history)
        alert_types = {}
        urgency_levels = {}
        
        for alert in self.alert_history:
            alert_type = alert['type']
            urgency = alert['urgency']
            
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            urgency_levels[urgency] = urgency_levels.get(urgency, 0) + 1
        
        return {
            "total_alerts": total_alerts,
            "alert_types": alert_types,
            "urgency_levels": urgency_levels,
            "recent_alerts_24h": len(self.get_recent_alerts(24))
        }

