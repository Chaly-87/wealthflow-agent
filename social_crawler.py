import praw
import requests
import time
from typing import List, Dict, Any
from datetime import datetime, timedelta

class SocialCrawler:
    def __init__(self, reddit_client_id=None, reddit_client_secret=None, reddit_user_agent=None):
        """
        Initialize the social media crawler.
        
        Args:
            reddit_client_id: Reddit API client ID
            reddit_client_secret: Reddit API client secret
            reddit_user_agent: Reddit API user agent
        """
        self.reddit = None
        if reddit_client_id and reddit_client_secret and reddit_user_agent:
            try:
                self.reddit = praw.Reddit(
                    client_id=reddit_client_id,
                    client_secret=reddit_client_secret,
                    user_agent=reddit_user_agent
                )
            except Exception as e:
                print(f"Failed to initialize Reddit client: {e}")

    def crawl_reddit_posts(self, subreddit_name: str, limit: int = 100, time_filter: str = "day") -> List[Dict[str, Any]]:
        """
        Crawl posts from a specific subreddit.
        
        Args:
            subreddit_name: Name of the subreddit (e.g., 'wallstreetbets')
            limit: Number of posts to retrieve
            time_filter: Time filter ('hour', 'day', 'week', 'month', 'year', 'all')
            
        Returns:
            List of post dictionaries
        """
        if not self.reddit:
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            # Get hot posts from the subreddit
            for submission in subreddit.hot(limit=limit):
                post_data = {
                    "id": submission.id,
                    "title": submission.title,
                    "text": submission.selftext,
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "num_comments": submission.num_comments,
                    "created_utc": submission.created_utc,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "url": submission.url,
                    "subreddit": subreddit_name,
                    "timestamp": datetime.now().isoformat()
                }
                posts.append(post_data)
            
            return posts
            
        except Exception as e:
            print(f"Error crawling Reddit posts: {e}")
            return []

    def crawl_reddit_comments(self, subreddit_name: str, post_limit: int = 10, comment_limit: int = 50) -> List[Dict[str, Any]]:
        """
        Crawl comments from recent posts in a subreddit.
        
        Args:
            subreddit_name: Name of the subreddit
            post_limit: Number of posts to check for comments
            comment_limit: Number of comments to retrieve per post
            
        Returns:
            List of comment dictionaries
        """
        if not self.reddit:
            return []
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            comments = []
            
            for submission in subreddit.hot(limit=post_limit):
                submission.comments.replace_more(limit=0)  # Remove "more comments" objects
                
                for comment in submission.comments.list()[:comment_limit]:
                    if hasattr(comment, 'body') and comment.body != '[deleted]':
                        comment_data = {
                            "id": comment.id,
                            "body": comment.body,
                            "score": comment.score,
                            "created_utc": comment.created_utc,
                            "author": str(comment.author) if comment.author else "[deleted]",
                            "post_id": submission.id,
                            "post_title": submission.title,
                            "subreddit": subreddit_name,
                            "timestamp": datetime.now().isoformat()
                        }
                        comments.append(comment_data)
            
            return comments
            
        except Exception as e:
            print(f"Error crawling Reddit comments: {e}")
            return []

    def search_reddit_mentions(self, query: str, subreddit_name: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for specific mentions across Reddit.
        
        Args:
            query: Search query (e.g., 'AAPL', 'bitcoin')
            subreddit_name: Optional specific subreddit to search in
            limit: Number of results to retrieve
            
        Returns:
            List of search result dictionaries
        """
        if not self.reddit:
            return []
        
        try:
            if subreddit_name:
                subreddit = self.reddit.subreddit(subreddit_name)
                search_results = subreddit.search(query, limit=limit, sort='new')
            else:
                search_results = self.reddit.subreddit('all').search(query, limit=limit, sort='new')
            
            results = []
            for submission in search_results:
                result_data = {
                    "id": submission.id,
                    "title": submission.title,
                    "text": submission.selftext,
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "num_comments": submission.num_comments,
                    "created_utc": submission.created_utc,
                    "author": str(submission.author) if submission.author else "[deleted]",
                    "subreddit": submission.subreddit.display_name,
                    "query": query,
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result_data)
            
            return results
            
        except Exception as e:
            print(f"Error searching Reddit mentions: {e}")
            return []

    def get_trending_topics(self, subreddit_names: List[str] = None) -> Dict[str, Any]:
        """
        Get trending topics from specified subreddits.
        
        Args:
            subreddit_names: List of subreddit names to analyze
            
        Returns:
            Dictionary with trending analysis
        """
        if not subreddit_names:
            subreddit_names = ['wallstreetbets', 'cryptocurrency', 'stocks', 'investing']
        
        trending_data = {
            "timestamp": datetime.now().isoformat(),
            "subreddits": {},
            "overall_trends": []
        }
        
        for subreddit_name in subreddit_names:
            posts = self.crawl_reddit_posts(subreddit_name, limit=50)
            
            # Extract trending keywords from titles
            all_titles = " ".join([post["title"] for post in posts])
            words = all_titles.lower().split()
            
            # Filter for potential stock/crypto symbols (3-5 uppercase letters)
            import re
            symbols = re.findall(r'\b[A-Z]{2,5}\b', all_titles)
            
            trending_data["subreddits"][subreddit_name] = {
                "post_count": len(posts),
                "top_symbols": list(set(symbols))[:10],
                "avg_score": sum([post["score"] for post in posts]) / len(posts) if posts else 0
            }
        
        return trending_data

# Mock implementations for Telegram and Discord (as these require more complex setup)
class TelegramCrawler:
    def __init__(self, bot_token=None):
        self.bot_token = bot_token
        print("Telegram crawler initialized (mock implementation)")
    
    def crawl_channel_messages(self, channel_username: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Mock implementation for Telegram channel crawling."""
        print(f"Mock: Would crawl {limit} messages from Telegram channel @{channel_username}")
        return []

class DiscordCrawler:
    def __init__(self, bot_token=None):
        self.bot_token = bot_token
        print("Discord crawler initialized (mock implementation)")
    
    def crawl_server_messages(self, server_id: str, channel_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Mock implementation for Discord server crawling."""
        print(f"Mock: Would crawl {limit} messages from Discord server {server_id}, channel {channel_id}")
        return []

