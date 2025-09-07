import openai
import os
import re
from typing import List, Dict, Any

class SentimentAnalyzer:
    def __init__(self, openai_api_key=None):
        self.client = openai.OpenAI(
            api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
        )
        
        # Keywords to focus on for financial sentiment analysis
        self.financial_keywords = [
            "squeeze", "pump", "undervalued", "announcement", "moon", "rocket",
            "diamond hands", "hodl", "buy the dip", "to the moon", "bullish",
            "bearish", "dump", "crash", "rally", "breakout", "resistance",
            "support", "volume", "merger", "acquisition", "earnings", "ipo"
        ]

    def analyze_text_sentiment(self, text: str, asset_name: str = None) -> Dict[str, Any]:
        """
        Analyze sentiment of a given text using OpenAI GPT-4 Turbo.
        
        Args:
            text: The text to analyze
            asset_name: Optional asset name to focus the analysis
            
        Returns:
            Dictionary with sentiment analysis results
        """
        try:
            # Create a focused prompt for financial sentiment analysis
            prompt = f"""
            Analyze the following text for financial sentiment and market indicators.
            
            Text: "{text}"
            
            Please provide:
            1. Overall sentiment (positive, negative, neutral) with confidence score (0-1)
            2. Specific financial keywords found
            3. Market signals detected (pump, dump, squeeze, etc.)
            4. Urgency level (low, medium, high)
            5. Asset mentions (if any)
            
            Focus on: {asset_name if asset_name else "any financial assets"}
            
            Respond in JSON format with keys: sentiment, confidence, keywords, signals, urgency, assets
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a financial sentiment analysis expert. Analyze text for market sentiment and trading signals."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            # Try to parse JSON response
            content = response.choices[0].message.content
            try:
                import json
                result = json.loads(content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "sentiment": self._extract_sentiment_fallback(content),
                    "confidence": 0.5,
                    "keywords": self._extract_keywords(text),
                    "signals": [],
                    "urgency": "medium",
                    "assets": []
                }
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "sentiment": "neutral",
                "confidence": 0.0,
                "keywords": [],
                "signals": [],
                "urgency": "low",
                "assets": []
            }

    def _extract_sentiment_fallback(self, text: str) -> str:
        """Fallback sentiment extraction using keyword matching."""
        positive_words = ["bullish", "moon", "rocket", "buy", "pump", "squeeze"]
        negative_words = ["bearish", "dump", "crash", "sell", "drop"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract financial keywords from text."""
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in self.financial_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords

    def batch_analyze(self, texts: List[str], asset_name: str = None) -> List[Dict[str, Any]]:
        """Analyze multiple texts for sentiment."""
        results = []
        for text in texts:
            result = self.analyze_text_sentiment(text, asset_name)
            results.append(result)
        
        return results

    def aggregate_sentiment(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate multiple sentiment analyses into a summary."""
        if not analyses:
            return {"overall_sentiment": "neutral", "confidence": 0.0, "total_mentions": 0}
        
        sentiments = [a.get("sentiment", "neutral") for a in analyses if "error" not in a]
        confidences = [a.get("confidence", 0.0) for a in analyses if "error" not in a]
        
        if not sentiments:
            return {"overall_sentiment": "neutral", "confidence": 0.0, "total_mentions": 0}
        
        # Calculate weighted sentiment
        positive_count = sentiments.count("positive")
        negative_count = sentiments.count("negative")
        neutral_count = sentiments.count("neutral")
        
        total = len(sentiments)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        if positive_count > negative_count and positive_count > neutral_count:
            overall = "positive"
        elif negative_count > positive_count and negative_count > neutral_count:
            overall = "negative"
        else:
            overall = "neutral"
        
        return {
            "overall_sentiment": overall,
            "confidence": avg_confidence,
            "total_mentions": total,
            "positive_ratio": positive_count / total,
            "negative_ratio": negative_count / total,
            "neutral_ratio": neutral_count / total
        }

