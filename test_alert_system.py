from alert_system import AlertSystem
from trigger_engine import TriggerEngine
import time

def test_alert_system():
    """Test the alert system functionality."""
    print("Testing Alert System...")
    
    # Initialize alert system
    alert_system = AlertSystem()
    
    # Test volume anomaly detection
    print("\n1. Testing Volume Anomaly Detection:")
    historical_volumes = [1000, 1200, 900, 1100, 1050, 980, 1150]
    current_volume = 3500  # 3x normal volume
    
    volume_result = alert_system.detect_volume_anomaly(current_volume, historical_volumes)
    print(f"Volume anomaly result: {volume_result}")
    
    if volume_result["anomaly_detected"]:
        alert = alert_system.generate_alert("volume_anomaly", "AAPL", volume_result, "high")
        print(f"Generated alert: {alert['message']}")
    
    # Test pump and dump detection
    print("\n2. Testing Pump and Dump Detection:")
    # Simulate price history with a pump pattern
    price_history = [
        {"close": 100, "timestamp": 1}, {"close": 102, "timestamp": 2},
        {"close": 101, "timestamp": 3}, {"close": 103, "timestamp": 4},
        {"close": 105, "timestamp": 5}, {"close": 110, "timestamp": 6},
        {"close": 115, "timestamp": 7}, {"close": 125, "timestamp": 8},
        {"close": 130, "timestamp": 9}, {"close": 135, "timestamp": 10}
    ]
    volume_history = [1000, 1100, 950, 1200, 1500, 2500, 3000, 3500, 4000, 2000]
    
    pump_dump_result = alert_system.detect_pump_and_dump_pattern(price_history, volume_history)
    print(f"Pump and dump result: {pump_dump_result}")
    
    if pump_dump_result["pattern_detected"]:
        alert = alert_system.generate_alert("pump_dump", "TSLA", pump_dump_result, "high")
        print(f"Generated alert: {alert['message']}")
    
    # Test sentiment spike detection
    print("\n3. Testing Sentiment Spike Detection:")
    sentiment_data = [
        {"sentiment": "positive", "confidence": 0.8},
        {"sentiment": "positive", "confidence": 0.9},
        {"sentiment": "positive", "confidence": 0.75},
        {"sentiment": "positive", "confidence": 0.85},
        {"sentiment": "neutral", "confidence": 0.6}
    ]
    
    sentiment_result = alert_system.check_news_sentiment_spike(sentiment_data, "BTC")
    print(f"Sentiment spike result: {sentiment_result}")
    
    if sentiment_result["spike_detected"]:
        alert = alert_system.generate_alert("sentiment_spike", "BTC", sentiment_result, "medium")
        print(f"Generated alert: {alert['message']}")
    
    # Test alert summary
    print("\n4. Alert Summary:")
    summary = alert_system.get_alert_summary()
    print(f"Alert summary: {summary}")

def test_trigger_engine():
    """Test the trigger engine functionality."""
    print("\n" + "="*50)
    print("Testing Trigger Engine...")
    
    # Initialize trigger engine
    trigger_engine = TriggerEngine()
    
    # Test monitoring status
    print("\n1. Initial Monitoring Status:")
    status = trigger_engine.get_monitoring_status()
    print(f"Status: {status}")
    
    # Test adding/removing monitored assets
    print("\n2. Testing Asset Management:")
    trigger_engine.add_monitored_asset("stock", "AMZN")
    trigger_engine.add_monitored_asset("crypto", "litecoin")
    
    status = trigger_engine.get_monitoring_status()
    print(f"After adding assets: {status['monitored_stocks']}, {status['monitored_cryptos']}")
    
    trigger_engine.remove_monitored_asset("stock", "AMZN")
    trigger_engine.remove_monitored_asset("crypto", "litecoin")
    
    status = trigger_engine.get_monitoring_status()
    print(f"After removing assets: {status['monitored_stocks']}, {status['monitored_cryptos']}")
    
    # Test starting monitoring (for a short time)
    print("\n3. Testing Monitoring Engine:")
    print("Starting monitoring for 10 seconds...")
    trigger_engine.start_monitoring()
    
    # Let it run for a short time
    time.sleep(10)
    
    trigger_engine.stop_monitoring()
    print("Monitoring stopped.")

def test_integration():
    """Test integration between components."""
    print("\n" + "="*50)
    print("Testing Integration...")
    
    # This would test the full integration between all components
    # For now, we'll just verify that all components can be initialized together
    
    try:
        alert_system = AlertSystem()
        trigger_engine = TriggerEngine()
        
        print("✓ All components initialized successfully")
        print("✓ Integration test passed")
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")

if __name__ == "__main__":
    test_alert_system()
    test_trigger_engine()
    test_integration()
    
    print("\n" + "="*50)
    print("Alert system testing completed!")

