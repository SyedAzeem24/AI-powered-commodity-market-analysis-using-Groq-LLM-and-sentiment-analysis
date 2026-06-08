"""
News service for fetching commodity-related news from Google News RSS feeds.
"""

import feedparser
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)


class NewsService:
    """Service for fetching commodity-related news."""
    
    @staticmethod
    def get_news(commodity_key, news_query, max_articles=5):
        """
        Fetch news articles related to a commodity.
        
        Args:
            commodity_key (str): Commodity key
            news_query (str): Search query for news
            max_articles (int): Maximum articles to fetch
            
        Returns:
            list: List of news articles
        """
        try:
            # Properly encode the URL
            encoded_query = quote(news_query)
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            
            logger.info(f"Fetching news for: {commodity_key}")
            logger.info(f"URL: {url}")
            
            feed = feedparser.parse(url)
            
            if not feed.entries:
                logger.warning(f"No news found for {commodity_key}")
                return []
            
            articles = []
            for entry in feed.entries[:max_articles]:
                try:
                    article = {
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", ""),
                        "source": entry.get("source", {}).get("title", "Unknown") if isinstance(entry.get("source"), dict) else str(entry.get("source", "Unknown")),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                    }
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Error parsing article: {e}")
                    continue
            
            logger.info(f"✅ Fetched {len(articles)} articles for {commodity_key}")
            return articles
        
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []