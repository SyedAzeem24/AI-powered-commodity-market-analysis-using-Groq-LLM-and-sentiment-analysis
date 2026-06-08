"""
Sentiment analysis service using VADER sentiment analyzer.
"""

from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import logging

logger = logging.getLogger(__name__)

# Download VADER lexicon
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')


class SentimentService:
    """Service for sentiment analysis of news articles."""
    
    @staticmethod
    def analyze_sentiment(news_items):
        """
        Analyze sentiment of news articles.
        
        Args:
            news_items (list): List of news articles
            
        Returns:
            dict: Sentiment analysis results
        """
        if not news_items:
            return None
        
        try:
            sia = SentimentIntensityAnalyzer()
            
            sentiments = []
            for article in news_items:
                text = f"{article.get('title', '')} {article.get('summary', '')}"
                scores = sia.polarity_scores(text)
                sentiments.append(scores)
            
            # Calculate aggregates
            positive_count = sum(1 for s in sentiments if s['compound'] > 0.05)
            negative_count = sum(1 for s in sentiments if s['compound'] < -0.05)
            neutral_count = len(sentiments) - positive_count - negative_count
            
            total = len(sentiments)
            
            positive_pct = (positive_count / total * 100) if total > 0 else 0
            negative_pct = (negative_count / total * 100) if total > 0 else 0
            neutral_pct = (neutral_count / total * 100) if total > 0 else 0
            
            # Determine overall sentiment
            avg_compound = sum(s['compound'] for s in sentiments) / total if total > 0 else 0
            
            if avg_compound > 0.05:
                overall = "Positive 📈"
            elif avg_compound < -0.05:
                overall = "Negative 📉"
            else:
                overall = "Neutral ➡️"
            
            result = {
                "overall": overall,
                "positive": round(positive_pct, 1),
                "neutral": round(neutral_pct, 1),
                "negative": round(negative_pct, 1),
                "average_compound": round(avg_compound, 3)
            }
            
            logger.info(f"✅ Sentiment analysis complete: {result['overall']}")
            return result
        
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return None