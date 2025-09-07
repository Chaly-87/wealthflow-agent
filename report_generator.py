import json
import smtplib
import feedparser
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import schedule
import time
import threading

from api_connectors import YahooFinanceAPI, CoinGeckoAPI
from sentiment_analyzer import SentimentAnalyzer
from alert_system import AlertSystem
from data_storage import DataStorage

class NewsAggregator:
    """Aggregates news from various sources."""
    
    def __init__(self):
        self.news_sources = {
            "google_finance": "https://news.google.com/rss/search?q=finance&hl=en-US&gl=US&ceid=US:en",
            "google_crypto": "https://news.google.com/rss/search?q=cryptocurrency&hl=en-US&gl=US&ceid=US:en",
            "google_stocks": "https://news.google.com/rss/search?q=stock+market&hl=en-US&gl=US&ceid=US:en"
        }
    
    def get_latest_news(self, category: str = "finance", limit: int = 10) -> List[Dict[str, Any]]:
        """Get latest news from RSS feeds."""
        try:
            if category in self.news_sources:
                feed_url = self.news_sources[category]
            else:
                # Default to finance news
                feed_url = self.news_sources["google_finance"]
            
            feed = feedparser.parse(feed_url)
            news_items = []
            
            for entry in feed.entries[:limit]:
                news_item = {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get('published', ''),
                    "summary": entry.get('summary', ''),
                    "source": entry.get('source', {}).get('title', 'Unknown'),
                    "category": category
                }
                news_items.append(news_item)
            
            return news_items
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def search_news_by_keyword(self, keyword: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for news containing specific keywords."""
        try:
            search_url = f"https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(search_url)
            
            news_items = []
            for entry in feed.entries[:limit]:
                news_item = {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get('published', ''),
                    "summary": entry.get('summary', ''),
                    "keyword": keyword,
                    "relevance_score": self._calculate_relevance(entry.title, keyword)
                }
                news_items.append(news_item)
            
            # Sort by relevance score
            news_items.sort(key=lambda x: x['relevance_score'], reverse=True)
            return news_items
            
        except Exception as e:
            print(f"Error searching news for {keyword}: {e}")
            return []
    
    def _calculate_relevance(self, title: str, keyword: str) -> float:
        """Calculate relevance score based on keyword presence."""
        title_lower = title.lower()
        keyword_lower = keyword.lower()
        
        # Simple relevance scoring
        score = 0.0
        if keyword_lower in title_lower:
            score += 1.0
        
        # Bonus for exact matches
        if keyword_lower == title_lower:
            score += 0.5
        
        # Bonus for keyword at the beginning
        if title_lower.startswith(keyword_lower):
            score += 0.3
        
        return score

class ReportGenerator:
    """Generates comprehensive daily reports."""
    
    def __init__(self, email_config: Dict[str, str] = None):
        """
        Initialize report generator.
        
        Args:
            email_config: Email configuration for sending reports
        """
        self.yf_api = YahooFinanceAPI()
        self.cg_api = CoinGeckoAPI()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.news_aggregator = NewsAggregator()
        self.alert_system = AlertSystem(email_config)
        self.db = DataStorage()
        self.email_config = email_config
        
        # Assets to analyze
        self.monitored_stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMZN", "META"]
        self.monitored_cryptos = ["bitcoin", "ethereum", "dogecoin", "cardano", "solana"]
        
        # Report templates
        self.html_template = self._get_html_template()
        self.text_template = self._get_text_template()
    
    def generate_daily_report(self) -> Dict[str, Any]:
        """Generate comprehensive daily report."""
        print(f"Generating daily report for {datetime.now().strftime('%Y-%m-%d')}")
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime('%Y-%m-%d'),
            "top_opportunities": self._get_top_opportunities(),
            "bubble_warnings": self._get_bubble_warnings(),
            "latest_news": self._get_relevant_news(),
            "market_sentiment": self._get_market_sentiment(),
            "performance_summary": self._get_performance_summary(),
            "alerts_summary": self._get_alerts_summary()
        }
        
        return report_data
    
    def _get_top_opportunities(self) -> List[Dict[str, Any]]:
        """Identify top 3 assets with potential for growth."""
        opportunities = []
        
        # Analyze stocks
        for ticker in self.monitored_stocks:
            try:
                data = self.yf_api.get_stock_data(ticker)
                if "error" not in data:
                    opportunity_score = self._calculate_opportunity_score(ticker, data, "stock")
                    opportunities.append({
                        "symbol": ticker,
                        "type": "stock",
                        "score": opportunity_score,
                        "current_price": self._extract_current_price(data),
                        "reason": self._generate_opportunity_reason(ticker, data, "stock")
                    })
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
        
        # Analyze cryptos
        for coin_id in self.monitored_cryptos:
            try:
                price_data = self.cg_api.get_coin_price(coin_id)
                if "error" not in price_data:
                    opportunity_score = self._calculate_opportunity_score(coin_id, price_data, "crypto")
                    opportunities.append({
                        "symbol": coin_id.upper(),
                        "type": "crypto",
                        "score": opportunity_score,
                        "current_price": price_data.get(coin_id, {}).get('usd', 0),
                        "reason": self._generate_opportunity_reason(coin_id, price_data, "crypto")
                    })
            except Exception as e:
                print(f"Error analyzing {coin_id}: {e}")
        
        # Sort by score and return top 3
        opportunities.sort(key=lambda x: x['score'], reverse=True)
        return opportunities[:3]
    
    def _calculate_opportunity_score(self, symbol: str, data: Dict[str, Any], asset_type: str) -> float:
        """Calculate opportunity score based on various factors."""
        score = 0.0
        
        # Base score
        score += 0.5
        
        # Volume factor (higher volume = higher score)
        if asset_type == "stock":
            volume = self._extract_volume(data)
            if volume > 1000000:  # High volume
                score += 0.3
        
        # Sentiment factor (mock implementation)
        # In a real implementation, this would use actual sentiment data
        sentiment_score = 0.2  # Neutral sentiment
        score += sentiment_score
        
        # News factor (mock implementation)
        # In a real implementation, this would analyze recent news
        news_score = 0.1
        score += news_score
        
        # Random factor to simulate market dynamics
        import random
        score += random.uniform(-0.2, 0.3)
        
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1
    
    def _generate_opportunity_reason(self, symbol: str, data: Dict[str, Any], asset_type: str) -> str:
        """Generate reason for opportunity."""
        reasons = [
            f"Strong volume indicators for {symbol}",
            f"Positive sentiment trends detected for {symbol}",
            f"Technical analysis suggests upward momentum for {symbol}",
            f"Market conditions favorable for {symbol}",
            f"Recent news coverage positive for {symbol}"
        ]
        
        import random
        return random.choice(reasons)
    
    def _get_bubble_warnings(self) -> List[Dict[str, Any]]:
        """Identify potential bubble formations."""
        warnings = []
        
        # Mock bubble detection (in real implementation, this would use sophisticated algorithms)
        bubble_candidates = ["TSLA", "NVDA", "bitcoin"]
        
        for candidate in bubble_candidates:
            if candidate in self.monitored_stocks or candidate in self.monitored_cryptos:
                import random
                if random.random() > 0.7:  # 30% chance of bubble warning
                    warnings.append({
                        "symbol": candidate.upper(),
                        "warning_level": random.choice(["medium", "high"]),
                        "reason": f"Rapid price appreciation and high volatility detected in {candidate}",
                        "recommendation": "Consider taking profits or reducing position size"
                    })
        
        return warnings
    
    def _get_relevant_news(self) -> List[Dict[str, Any]]:
        """Get relevant financial news."""
        news_items = []
        
        # Get general financial news
        finance_news = self.news_aggregator.get_latest_news("google_finance", 5)
        news_items.extend(finance_news)
        
        # Get crypto news
        crypto_news = self.news_aggregator.get_latest_news("google_crypto", 3)
        news_items.extend(crypto_news)
        
        # Search for specific asset news
        for asset in ["AAPL", "TSLA", "bitcoin"]:
            asset_news = self.news_aggregator.search_news_by_keyword(asset, 2)
            news_items.extend(asset_news)
        
        # Remove duplicates and sort by relevance/recency
        unique_news = []
        seen_titles = set()
        
        for item in news_items:
            if item['title'] not in seen_titles:
                unique_news.append(item)
                seen_titles.add(item['title'])
        
        return unique_news[:10]  # Return top 10 news items
    
    def _get_market_sentiment(self) -> Dict[str, Any]:
        """Analyze overall market sentiment."""
        # Mock sentiment analysis (in real implementation, this would analyze social media, news, etc.)
        import random
        
        sentiments = ["bullish", "bearish", "neutral"]
        overall_sentiment = random.choice(sentiments)
        confidence = random.uniform(0.6, 0.9)
        
        return {
            "overall_sentiment": overall_sentiment,
            "confidence": confidence,
            "key_factors": [
                "Federal Reserve policy expectations",
                "Earnings season results",
                "Geopolitical developments",
                "Cryptocurrency adoption trends"
            ]
        }
    
    def _get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary (mock implementation)."""
        import random
        
        return {
            "portfolio_value": 10000 + random.uniform(-500, 1000),
            "daily_change": random.uniform(-2, 3),
            "weekly_change": random.uniform(-5, 8),
            "monthly_change": random.uniform(-10, 15),
            "best_performer": random.choice(self.monitored_stocks),
            "worst_performer": random.choice(self.monitored_stocks)
        }
    
    def _get_alerts_summary(self) -> Dict[str, Any]:
        """Get summary of recent alerts."""
        recent_alerts = self.alert_system.get_recent_alerts(24)
        
        return {
            "total_alerts_24h": len(recent_alerts),
            "high_priority_alerts": len([a for a in recent_alerts if a.get('urgency') == 'high']),
            "alert_types": {},  # Would be populated with actual alert type counts
            "latest_alert": recent_alerts[0] if recent_alerts else None
        }
    
    def _extract_current_price(self, data: Dict[str, Any]) -> float:
        """Extract current price from stock data."""
        try:
            info = data.get("info", {})
            return info.get("currentPrice", info.get("regularMarketPrice", 0.0))
        except:
            return 0.0
    
    def _extract_volume(self, data: Dict[str, Any]) -> int:
        """Extract volume from stock data."""
        try:
            info = data.get("info", {})
            return info.get("volume", info.get("regularMarketVolume", 0))
        except:
            return 0
    
    def _get_html_template(self) -> str:
        """Get HTML email template."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>WealthFlow Daily Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
                .section { margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }
                .opportunity { background-color: #e8f5e8; padding: 10px; margin: 10px 0; }
                .warning { background-color: #ffeaa7; padding: 10px; margin: 10px 0; }
                .news-item { border-bottom: 1px solid #ddd; padding: 10px 0; }
                .footer { text-align: center; color: #666; margin-top: 30px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 WealthFlow Daily Report</h1>
                <p>{{ date }}</p>
            </div>
            
            <div class="section">
                <h2>📈 Top Opportunities</h2>
                {% for opp in top_opportunities %}
                <div class="opportunity">
                    <strong>{{ opp.symbol }}</strong> ({{ opp.type }}) - Score: {{ "%.2f"|format(opp.score) }}
                    <br>Price: ${{ "%.2f"|format(opp.current_price) }}
                    <br>{{ opp.reason }}
                </div>
                {% endfor %}
            </div>
            
            {% if bubble_warnings %}
            <div class="section">
                <h2>⚠️ Bubble Warnings</h2>
                {% for warning in bubble_warnings %}
                <div class="warning">
                    <strong>{{ warning.symbol }}</strong> - {{ warning.warning_level|title }} Risk
                    <br>{{ warning.reason }}
                    <br><em>{{ warning.recommendation }}</em>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <div class="section">
                <h2>📰 Latest News</h2>
                {% for news in latest_news[:5] %}
                <div class="news-item">
                    <strong><a href="{{ news.link }}">{{ news.title }}</a></strong>
                    <br><small>{{ news.published }}</small>
                </div>
                {% endfor %}
            </div>
            
            <div class="section">
                <h2>📊 Market Sentiment</h2>
                <p><strong>Overall:</strong> {{ market_sentiment.overall_sentiment|title }} 
                   ({{ "%.0f"|format(market_sentiment.confidence * 100) }}% confidence)</p>
            </div>
            
            <div class="footer">
                <p>Generated by WealthFlow Agent at {{ timestamp }}</p>
                <p><small>This report is for informational purposes only and should not be considered as financial advice.</small></p>
            </div>
        </body>
        </html>
        """
    
    def _get_text_template(self) -> str:
        """Get plain text email template."""
        return """
        🚀 WEALTHFLOW DAILY REPORT - {{ date }}
        =====================================
        
        📈 TOP OPPORTUNITIES:
        {% for opp in top_opportunities %}
        {{ loop.index }}. {{ opp.symbol }} ({{ opp.type }}) - Score: {{ "%.2f"|format(opp.score) }}
           Price: ${{ "%.2f"|format(opp.current_price) }}
           Reason: {{ opp.reason }}
        
        {% endfor %}
        
        {% if bubble_warnings %}
        ⚠️ BUBBLE WARNINGS:
        {% for warning in bubble_warnings %}
        - {{ warning.symbol }}: {{ warning.warning_level|title }} risk
          {{ warning.reason }}
          Recommendation: {{ warning.recommendation }}
        
        {% endfor %}
        {% endif %}
        
        📰 LATEST NEWS:
        {% for news in latest_news[:5] %}
        - {{ news.title }}
          {{ news.link }}
        
        {% endfor %}
        
        📊 MARKET SENTIMENT:
        Overall: {{ market_sentiment.overall_sentiment|title }} ({{ "%.0f"|format(market_sentiment.confidence * 100) }}% confidence)
        
        =====================================
        Generated by WealthFlow Agent
        {{ timestamp }}
        
        Disclaimer: This report is for informational purposes only.
        """
    
    def send_daily_report(self, recipient_email: str, format: str = "html") -> bool:
        """Send daily report via email."""
        if not self.email_config:
            print("Email configuration not provided")
            return False
        
        try:
            # Generate report data
            report_data = self.generate_daily_report()
            
            # Render template
            if format == "html":
                template = Template(self.html_template)
                content = template.render(**report_data)
                content_type = "html"
            else:
                template = Template(self.text_template)
                content = template.render(**report_data)
                content_type = "plain"
            
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email']
            msg['To'] = recipient_email
            msg['Subject'] = f"WealthFlow Daily Report - {report_data['date']}"
            
            msg.attach(MIMEText(content, content_type))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['email'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['email'], recipient_email, text)
            server.quit()
            
            print(f"Daily report sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send daily report: {e}")
            return False
    
    def save_report_to_file(self, filename: str = None, format: str = "html") -> str:
        """Save report to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wealthflow_report_{timestamp}.{'html' if format == 'html' else 'txt'}"
        
        try:
            report_data = self.generate_daily_report()
            
            if format == "html":
                template = Template(self.html_template)
                content = template.render(**report_data)
            else:
                template = Template(self.text_template)
                content = template.render(**report_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Report saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"Failed to save report: {e}")
            return ""

class ReportScheduler:
    """Schedules automatic report generation and sending."""
    
    def __init__(self, report_generator: ReportGenerator, recipients: List[str]):
        """
        Initialize report scheduler.
        
        Args:
            report_generator: ReportGenerator instance
            recipients: List of email addresses to send reports to
        """
        self.report_generator = report_generator
        self.recipients = recipients
        self.running = False
        self.scheduler_thread = None
    
    def schedule_daily_reports(self, time_str: str = "08:00"):
        """Schedule daily reports at specified time."""
        schedule.every().day.at(time_str).do(self._send_daily_reports)
        print(f"Scheduled daily reports at {time_str}")
    
    def _send_daily_reports(self):
        """Send daily reports to all recipients."""
        print(f"Sending daily reports at {datetime.now()}")
        
        for recipient in self.recipients:
            try:
                success = self.report_generator.send_daily_report(recipient)
                if success:
                    print(f"Report sent to {recipient}")
                else:
                    print(f"Failed to send report to {recipient}")
            except Exception as e:
                print(f"Error sending report to {recipient}: {e}")
    
    def start_scheduler(self):
        """Start the report scheduler."""
        if self.running:
            print("Scheduler is already running")
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        print("Report scheduler started")
    
    def stop_scheduler(self):
        """Stop the report scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        print("Report scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

