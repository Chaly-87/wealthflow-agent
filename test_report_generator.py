from report_generator import ReportGenerator, NewsAggregator, ReportScheduler
import json

def test_news_aggregator():
    """Test the news aggregator functionality."""
    print("Testing News Aggregator...")
    
    news_aggregator = NewsAggregator()
    
    # Test 1: Get latest finance news
    print("\n1. Testing Latest Finance News:")
    finance_news = news_aggregator.get_latest_news("google_finance", 3)
    print(f"Retrieved {len(finance_news)} finance news items:")
    for i, news in enumerate(finance_news, 1):
        print(f"  {i}. {news['title']}")
        print(f"     Source: {news['source']}")
        print(f"     Published: {news['published']}")
        print()
    
    # Test 2: Search for specific keyword
    print("\n2. Testing Keyword Search:")
    keyword_news = news_aggregator.search_news_by_keyword("Apple", 2)
    print(f"Retrieved {len(keyword_news)} news items for 'Apple':")
    for i, news in enumerate(keyword_news, 1):
        print(f"  {i}. {news['title']}")
        print(f"     Relevance: {news['relevance_score']:.2f}")
        print()

def test_report_generator():
    """Test the report generator functionality."""
    print("\n" + "="*50)
    print("Testing Report Generator...")
    
    # Initialize report generator
    report_generator = ReportGenerator()
    
    # Test 1: Generate daily report
    print("\n1. Generating Daily Report:")
    report_data = report_generator.generate_daily_report()
    
    print(f"Report generated for: {report_data['date']}")
    print(f"Top opportunities: {len(report_data['top_opportunities'])}")
    print(f"Bubble warnings: {len(report_data['bubble_warnings'])}")
    print(f"News items: {len(report_data['latest_news'])}")
    
    # Display top opportunities
    print("\nTop Opportunities:")
    for i, opp in enumerate(report_data['top_opportunities'], 1):
        print(f"  {i}. {opp['symbol']} ({opp['type']}) - Score: {opp['score']:.2f}")
        print(f"     Price: ${opp['current_price']:.2f}")
        print(f"     Reason: {opp['reason']}")
        print()
    
    # Display bubble warnings
    if report_data['bubble_warnings']:
        print("Bubble Warnings:")
        for warning in report_data['bubble_warnings']:
            print(f"  - {warning['symbol']}: {warning['warning_level']} risk")
            print(f"    {warning['reason']}")
            print()
    
    # Display market sentiment
    sentiment = report_data['market_sentiment']
    print(f"Market Sentiment: {sentiment['overall_sentiment']} ({sentiment['confidence']:.0%} confidence)")
    
    # Test 2: Save report to file
    print("\n2. Saving Report to File:")
    
    # Save HTML version
    html_file = report_generator.save_report_to_file(format="html")
    print(f"HTML report saved: {html_file}")
    
    # Save text version
    text_file = report_generator.save_report_to_file(format="text")
    print(f"Text report saved: {text_file}")
    
    return report_data

def test_report_templates():
    """Test report template rendering."""
    print("\n" + "="*50)
    print("Testing Report Templates...")
    
    report_generator = ReportGenerator()
    
    # Generate sample report data
    sample_data = {
        "timestamp": "2025-09-07T08:30:00",
        "date": "2025-09-07",
        "top_opportunities": [
            {
                "symbol": "AAPL",
                "type": "stock",
                "score": 0.85,
                "current_price": 150.25,
                "reason": "Strong earnings momentum and positive analyst sentiment"
            },
            {
                "symbol": "BTC",
                "type": "crypto",
                "score": 0.78,
                "current_price": 45000.00,
                "reason": "Institutional adoption increasing, technical breakout pattern"
            }
        ],
        "bubble_warnings": [
            {
                "symbol": "TSLA",
                "warning_level": "medium",
                "reason": "High volatility and rapid price appreciation",
                "recommendation": "Consider taking partial profits"
            }
        ],
        "latest_news": [
            {
                "title": "Federal Reserve Signals Potential Rate Changes",
                "link": "https://example.com/news1",
                "published": "2025-09-07 07:30:00"
            },
            {
                "title": "Tech Stocks Rally on AI Optimism",
                "link": "https://example.com/news2",
                "published": "2025-09-07 06:45:00"
            }
        ],
        "market_sentiment": {
            "overall_sentiment": "bullish",
            "confidence": 0.75
        }
    }
    
    # Test HTML template
    print("\n1. Testing HTML Template:")
    from jinja2 import Template
    html_template = Template(report_generator._get_html_template())
    html_content = html_template.render(**sample_data)
    
    with open("test_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("HTML template test saved to test_report.html")
    
    # Test text template
    print("\n2. Testing Text Template:")
    text_template = Template(report_generator._get_text_template())
    text_content = text_template.render(**sample_data)
    
    with open("test_report.txt", "w", encoding="utf-8") as f:
        f.write(text_content)
    print("Text template test saved to test_report.txt")
    
    print("\nTemplate rendering completed successfully!")

def test_report_scheduler():
    """Test the report scheduler (without actually scheduling)."""
    print("\n" + "="*50)
    print("Testing Report Scheduler...")
    
    # Initialize components
    report_generator = ReportGenerator()
    recipients = ["test@example.com", "admin@example.com"]
    
    scheduler = ReportScheduler(report_generator, recipients)
    
    print(f"Scheduler initialized with {len(recipients)} recipients")
    print("Recipients:", recipients)
    
    # Test scheduling setup (without actually starting)
    print("\nTesting schedule setup:")
    scheduler.schedule_daily_reports("09:00")
    print("Daily reports scheduled for 09:00")
    
    # Test manual report sending (mock)
    print("\nTesting manual report generation:")
    try:
        # This would normally send emails, but we'll just test the logic
        print("Would send reports to:")
        for recipient in recipients:
            print(f"  - {recipient}")
        print("(Email sending skipped in test mode)")
    except Exception as e:
        print(f"Error in report sending logic: {e}")

def test_integration():
    """Test integration between all report components."""
    print("\n" + "="*50)
    print("Testing Report System Integration...")
    
    # Test complete workflow
    print("\n1. Complete Report Generation Workflow:")
    
    # Initialize all components
    news_aggregator = NewsAggregator()
    report_generator = ReportGenerator()
    
    # Get news
    print("Fetching latest news...")
    news = news_aggregator.get_latest_news("google_finance", 5)
    print(f"Retrieved {len(news)} news items")
    
    # Generate report
    print("Generating comprehensive report...")
    report = report_generator.generate_daily_report()
    
    # Save report
    print("Saving report files...")
    html_file = report_generator.save_report_to_file("integration_test_report.html", "html")
    text_file = report_generator.save_report_to_file("integration_test_report.txt", "text")
    
    print(f"Integration test completed!")
    print(f"Files generated: {html_file}, {text_file}")
    
    # Display summary
    print("\n2. Report Summary:")
    print(f"Date: {report['date']}")
    print(f"Opportunities found: {len(report['top_opportunities'])}")
    print(f"Warnings issued: {len(report['bubble_warnings'])}")
    print(f"News items: {len(report['latest_news'])}")
    print(f"Market sentiment: {report['market_sentiment']['overall_sentiment']}")

if __name__ == "__main__":
    test_news_aggregator()
    test_report_generator()
    test_report_templates()
    test_report_scheduler()
    test_integration()
    
    print("\n" + "="*50)
    print("Report generator testing completed!")

