from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import json
from datetime import datetime
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from api_connectors import YahooFinanceAPI, CoinGeckoAPI
    from sentiment_analyzer import SentimentAnalyzer
    from alert_system import AlertSystem
    from strategy_executor import StrategyExecutor
    from report_generator import ReportGenerator, NewsAggregator
    from trigger_engine import TriggerEngine
except ImportError as e:
    print(f"Import error: {e}")
    # Create mock classes for development
    class MockAPI:
        def __init__(self):
            pass
        def get_stock_data(self, symbol):
            return {"info": {"currentPrice": 150.0, "volume": 1000000}}
        def get_coin_price(self, coin_id):
            return {coin_id: {"usd": 45000.0}}

wealthflow_bp = Blueprint('wealthflow', __name__)

# Initialize components (with error handling)
try:
    yf_api = YahooFinanceAPI()
    cg_api = CoinGeckoAPI()
    sentiment_analyzer = SentimentAnalyzer()
    alert_system = AlertSystem()
    strategy_executor = StrategyExecutor()
    report_generator = ReportGenerator()
    news_aggregator = NewsAggregator()
    trigger_engine = TriggerEngine()
except Exception as e:
    print(f"Error initializing components: {e}")
    # Use mock APIs for development
    yf_api = MockAPI()
    cg_api = MockAPI()
    sentiment_analyzer = None
    alert_system = None
    strategy_executor = None
    report_generator = None
    news_aggregator = None
    trigger_engine = None

@wealthflow_bp.route('/portfolio', methods=['GET'])
@cross_origin()
def get_portfolio():
    """Get portfolio overview."""
    try:
        if strategy_executor:
            portfolio = strategy_executor.get_portfolio_summary()
        else:
            # Mock portfolio data
            portfolio = {
                "account_info": {
                    "balance": 10000.0,
                    "equity": 13500.0,
                    "buying_power": 8500.0,
                    "positions_count": 3
                },
                "positions": [
                    {
                        "symbol": "AAPL",
                        "quantity": 10,
                        "entry_price": 150.0,
                        "current_price": 175.5,
                        "side": "long",
                        "unrealized_pnl": 255.0
                    },
                    {
                        "symbol": "GOOGL",
                        "quantity": 5,
                        "entry_price": 2400.0,
                        "current_price": 2500.0,
                        "side": "long",
                        "unrealized_pnl": 500.0
                    }
                ],
                "total_unrealized_pnl": 755.0,
                "active_strategies": ["RSI_Strategy", "Mean_Reversion"]
            }
        
        return jsonify({
            "success": True,
            "data": portfolio,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/opportunities', methods=['GET'])
@cross_origin()
def get_opportunities():
    """Get top investment opportunities."""
    try:
        # Mock opportunities data
        opportunities = [
            {
                "symbol": "AAPL",
                "type": "stock",
                "score": 0.92,
                "current_price": 175.50,
                "change": 2.3,
                "reason": "Strong earnings momentum and positive analyst sentiment"
            },
            {
                "symbol": "BTC",
                "type": "crypto",
                "score": 0.88,
                "current_price": 45000.0,
                "change": -1.2,
                "reason": "Technical breakout pattern forming"
            },
            {
                "symbol": "NVDA",
                "type": "stock",
                "score": 0.85,
                "current_price": 420.75,
                "change": 4.1,
                "reason": "AI sector growth driving demand"
            }
        ]
        
        return jsonify({
            "success": True,
            "data": opportunities,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/alerts', methods=['GET'])
@cross_origin()
def get_alerts():
    """Get recent alerts."""
    try:
        if alert_system:
            alerts = alert_system.get_recent_alerts(24)
        else:
            # Mock alerts data
            alerts = [
                {
                    "id": 1,
                    "type": "volume_anomaly",
                    "symbol": "TSLA",
                    "message": "Volume spike detected - 3.2x normal levels",
                    "urgency": "high",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "id": 2,
                    "type": "sentiment_spike",
                    "symbol": "ETH",
                    "message": "Positive sentiment surge on social media",
                    "urgency": "medium",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "id": 3,
                    "type": "price_alert",
                    "symbol": "GOOGL",
                    "message": "Price target reached: $2,500",
                    "urgency": "low",
                    "timestamp": datetime.now().isoformat()
                }
            ]
        
        return jsonify({
            "success": True,
            "data": alerts,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/strategies', methods=['GET'])
@cross_origin()
def get_strategies():
    """Get active strategies."""
    try:
        if strategy_executor:
            metrics = strategy_executor.get_performance_metrics()
            strategies_data = {
                "active_strategies": list(strategy_executor.active_strategies),
                "performance_metrics": metrics
            }
        else:
            # Mock strategies data
            strategies_data = {
                "active_strategies": [
                    {
                        "name": "RSI Momentum",
                        "status": "active",
                        "performance": 12.5,
                        "trades": 23
                    },
                    {
                        "name": "Mean Reversion",
                        "status": "active",
                        "performance": 8.2,
                        "trades": 15
                    },
                    {
                        "name": "Sentiment Analysis",
                        "status": "paused",
                        "performance": -2.1,
                        "trades": 8
                    }
                ]
            }
        
        return jsonify({
            "success": True,
            "data": strategies_data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/strategies/<strategy_name>/toggle', methods=['POST'])
@cross_origin()
def toggle_strategy(strategy_name):
    """Toggle strategy active/inactive."""
    try:
        if strategy_executor:
            if strategy_name in strategy_executor.active_strategies:
                strategy_executor.deactivate_strategy(strategy_name)
                status = "deactivated"
            else:
                strategy_executor.activate_strategy(strategy_name)
                status = "activated"
        else:
            status = "mock_toggled"
        
        return jsonify({
            "success": True,
            "message": f"Strategy {strategy_name} {status}",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/monitoring/status', methods=['GET'])
@cross_origin()
def get_monitoring_status():
    """Get monitoring status."""
    try:
        if trigger_engine:
            status = trigger_engine.get_monitoring_status()
        else:
            # Mock monitoring status
            status = {
                "running": True,
                "monitored_stocks": ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"],
                "monitored_cryptos": ["bitcoin", "ethereum", "dogecoin"],
                "last_checks": {
                    "stocks": datetime.now().isoformat(),
                    "cryptos": datetime.now().isoformat(),
                    "sentiment": datetime.now().isoformat()
                }
            }
        
        return jsonify({
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/monitoring/toggle', methods=['POST'])
@cross_origin()
def toggle_monitoring():
    """Toggle monitoring on/off."""
    try:
        if trigger_engine:
            if trigger_engine.running:
                trigger_engine.stop_monitoring()
                status = "stopped"
            else:
                trigger_engine.start_monitoring()
                status = "started"
        else:
            status = "mock_toggled"
        
        return jsonify({
            "success": True,
            "message": f"Monitoring {status}",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/reports/daily', methods=['GET'])
@cross_origin()
def get_daily_report():
    """Get daily report."""
    try:
        if report_generator:
            report = report_generator.generate_daily_report()
        else:
            # Mock report data
            report = {
                "date": datetime.now().strftime('%Y-%m-%d'),
                "top_opportunities": [
                    {
                        "symbol": "AAPL",
                        "score": 0.92,
                        "reason": "Strong earnings momentum"
                    }
                ],
                "bubble_warnings": [],
                "market_sentiment": {
                    "overall_sentiment": "bullish",
                    "confidence": 0.75
                },
                "latest_news": [
                    {
                        "title": "Market Update: Tech Stocks Rally",
                        "link": "https://example.com/news1"
                    }
                ]
            }
        
        return jsonify({
            "success": True,
            "data": report,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/news', methods=['GET'])
@cross_origin()
def get_news():
    """Get latest financial news."""
    try:
        if news_aggregator:
            news = news_aggregator.get_latest_news("google_finance", 10)
        else:
            # Mock news data
            news = [
                {
                    "title": "Federal Reserve Signals Rate Changes",
                    "link": "https://example.com/news1",
                    "published": datetime.now().isoformat(),
                    "source": "Financial Times"
                },
                {
                    "title": "Tech Stocks Rally on AI Optimism",
                    "link": "https://example.com/news2",
                    "published": datetime.now().isoformat(),
                    "source": "Reuters"
                }
            ]
        
        return jsonify({
            "success": True,
            "data": news,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/execute-signal', methods=['POST'])
@cross_origin()
def execute_signal():
    """Execute a trading signal."""
    try:
        signal_data = request.get_json()
        
        if strategy_executor:
            result = strategy_executor.execute_signal(signal_data)
        else:
            # Mock execution result
            result = {
                "success": True,
                "order_id": "mock_order_123",
                "message": "Signal executed successfully (mock)"
            }
        
        return jsonify({
            "success": True,
            "data": result,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@wealthflow_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """Health check endpoint."""
    return jsonify({
        "success": True,
        "message": "WealthFlow Agent API is running",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api_connectors": yf_api is not None,
            "sentiment_analyzer": sentiment_analyzer is not None,
            "alert_system": alert_system is not None,
            "strategy_executor": strategy_executor is not None,
            "report_generator": report_generator is not None,
            "trigger_engine": trigger_engine is not None
        }
    })

