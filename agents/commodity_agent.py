"""
Main AI Agent for commodity market analysis.
Orchestrates all services to provide comprehensive market insights.
"""

import logging
from utils.commodity_mapper import detect_commodity
from services.market_service import MarketService
from services.news_service import NewsService
from services.sentiment_service import SentimentService
from services.llm_service import LLMService

logger = logging.getLogger(__name__)


class CommodityAgent:
    """
    AI Agent that orchestrates commodity market analysis.
    
    Workflow:
    1. Detect commodity from user query
    2. Fetch historical price data
    3. Fetch recent news
    4. Analyze sentiment
    5. Generate LLM-powered insights
    """
    
    def __init__(self):
        """Initialize the commodity agent."""
        self.llm_service = None
        try:
            self.llm_service = LLMService()
            logger.info("✅ CommodityAgent initialized successfully")
        except Exception as e:
            logger.error(f"⚠️ LLM Service initialization failed: {e}")
            logger.warning("Analysis will work without LLM")
    
    def validate_query(self, query):
        """
        Validate user query.
        
        Args:
            query (str): User query
            
        Returns:
            tuple: (is_valid, message)
        """
        if not query or len(query.strip()) == 0:
            return False, "❌ Please enter a query about a commodity"
        
        detected = detect_commodity(query)
        
        if not detected:
            commodities = "Gold, Silver, Crude Oil, Natural Gas, Copper, Wheat, Corn, Soybeans"
            return False, f"❌ No commodity detected. Try asking about: {commodities}"
        
        return True, f"✅ Detected: {detected['display_name']}"
    
    def analyze(self, query):
        """
        Main analysis method.
        
        Args:
            query (str): User query
            
        Returns:
            dict: Analysis results
        """
        logger.info(f"🔍 Starting analysis for query: {query}")
        
        try:
            # Step 1: Detect commodity
            detected = detect_commodity(query)
            
            if not detected:
                return {
                    "success": False,
                    "error": "Could not detect commodity from your query"
                }
            
            commodity_key = detected["key"]
            symbols = detected["symbols"]
            display_name = detected["display_name"]
            news_query = detected["news_query"]
            
            logger.info(f"📊 Detected commodity: {display_name}")
            
            # Step 2: Get market data
            logger.info("📈 Fetching market data...")
            market_summary = MarketService.get_market_summary(symbols, display_name)
            chart_data = MarketService.prepare_chart_data(symbols)
            
            if not market_summary:
                return {
                    "success": False,
                    "error": f"❌ Unable to fetch market data for {display_name}. Please try again."
                }
            
            logger.info("✅ Market data fetched")
            
            # Step 3: Get news
            logger.info("📰 Fetching news...")
            news_items = NewsService.get_news(commodity_key, news_query, max_articles=5)
            logger.info(f"✅ Found {len(news_items)} news articles")
            
            # Step 4: Analyze sentiment
            logger.info("💭 Analyzing sentiment...")
            sentiment = SentimentService.analyze_sentiment(news_items) if news_items else None
            logger.info("✅ Sentiment analysis complete")
            
            # Step 5: Generate LLM analysis
            llm_analysis = None
            if self.llm_service:
                try:
                    logger.info("🤖 Generating LLM analysis...")
                    news_summary = self._format_news(news_items)
                    
                    llm_analysis = self.llm_service.generate_analysis(
                        commodity=display_name,
                        market_data=market_summary,
                        news_summary=news_summary,
                        sentiment=sentiment,
                        user_query=query
                    )
                    logger.info("✅ LLM analysis generated successfully")
                except Exception as e:
                    logger.error(f"❌ LLM analysis failed: {e}")
                    llm_analysis = f"⚠️ AI analysis failed: {str(e)}"
            else:
                logger.warning("⚠️ LLM Service not available")
                llm_analysis = "⚠️ LLM Service not initialized. Check GROQ_API_KEY in .env"
            
            return {
                "success": True,
                "commodity": display_name,
                "market_summary": market_summary,
                "news": news_items,
                "sentiment": sentiment,
                "chart_data": chart_data,
                "analysis": llm_analysis
            }
        
        except Exception as e:
            logger.error(f"❌ Analysis failed: {e}")
            return {
                "success": False,
                "error": f"Analysis failed: {str(e)}"
            }
    
    @staticmethod
    def _format_news(news_items):
        """
        Format news items for LLM.
        
        Args:
            news_items (list): News articles
            
        Returns:
            str: Formatted news
        """
        if not news_items:
            return "No recent news available"
        
        formatted = "\n".join([
            f"- {item.get('title', 'Untitled')}\n  Source: {item.get('source', 'Unknown')}"
            for item in news_items[:5]
        ])
        
        return formatted