from sentiment_analyzer import SentimentAnalyzer
from social_crawler import SocialCrawler
import os

def test_sentiment_analyzer():
    """Test the sentiment analyzer with sample texts."""
    print("Testing Sentiment Analyzer...")
    
    # Initialize analyzer (will use OPENAI_API_KEY from environment)
    analyzer = SentimentAnalyzer()
    
    # Test texts with different sentiments
    test_texts = [
        "AAPL to the moon! 🚀 This stock is going to squeeze hard!",
        "Bitcoin is crashing, time to sell everything",
        "TSLA earnings announcement tomorrow, could be huge",
        "Market looking neutral today, no major movements",
        "GME diamond hands! HODL until we reach Mars!"
    ]
    
    print("\nAnalyzing individual texts:")
    for i, text in enumerate(test_texts, 1):
        print(f"\nText {i}: {text}")
        result = analyzer.analyze_text_sentiment(text)
        print(f"Result: {result}")
    
    # Test batch analysis
    print("\n" + "="*50)
    print("Testing batch analysis:")
    batch_results = analyzer.batch_analyze(test_texts)
    
    # Test aggregation
    aggregated = analyzer.aggregate_sentiment(batch_results)
    print(f"\nAggregated sentiment: {aggregated}")

def test_social_crawler():
    """Test the social crawler (requires Reddit API credentials)."""
    print("\n" + "="*50)
    print("Testing Social Crawler...")
    
    # Note: This will only work if Reddit API credentials are provided
    crawler = SocialCrawler()
    
    if crawler.reddit:
        print("Reddit client initialized successfully!")
        
        # Test crawling a few posts from wallstreetbets
        print("\nCrawling recent posts from r/wallstreetbets...")
        posts = crawler.crawl_reddit_posts("wallstreetbets", limit=5)
        
        print(f"Retrieved {len(posts)} posts:")
        for post in posts[:3]:  # Show first 3 posts
            print(f"- {post['title']} (Score: {post['score']})")
        
        # Test searching for mentions
        print("\nSearching for AAPL mentions...")
        mentions = crawler.search_reddit_mentions("AAPL", limit=3)
        print(f"Found {len(mentions)} AAPL mentions")
        
    else:
        print("Reddit client not initialized (missing credentials)")
        print("To test Reddit crawling, set up Reddit API credentials:")
        print("1. Go to https://www.reddit.com/prefs/apps")
        print("2. Create a new app")
        print("3. Use the credentials in the SocialCrawler initialization")

def test_integration():
    """Test integration between crawler and sentiment analyzer."""
    print("\n" + "="*50)
    print("Testing Integration...")
    
    # Mock some social media data for testing
    mock_posts = [
        {"title": "AAPL breaking resistance! Time to buy!", "text": "Apple stock looking bullish"},
        {"title": "Bitcoin dump incoming", "text": "Whales are selling, prepare for crash"},
        {"title": "TSLA earnings beat expectations", "text": "Tesla delivered amazing results"},
    ]
    
    analyzer = SentimentAnalyzer()
    
    print("Analyzing mock social media posts:")
    for post in mock_posts:
        combined_text = f"{post['title']} {post['text']}"
        result = analyzer.analyze_text_sentiment(combined_text)
        print(f"\nPost: {post['title']}")
        print(f"Sentiment: {result.get('sentiment', 'unknown')} (Confidence: {result.get('confidence', 0):.2f})")
        print(f"Keywords: {result.get('keywords', [])}")

if __name__ == "__main__":
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables")
        print("Sentiment analysis may not work properly")
    
    test_sentiment_analyzer()
    test_social_crawler()
    test_integration()
    
    print("\n" + "="*50)
    print("Testing completed!")

