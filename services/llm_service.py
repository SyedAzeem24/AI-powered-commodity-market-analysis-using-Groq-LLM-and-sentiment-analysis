"""
LLM service using Groq API for generating commodity analysis.
"""

import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM-based analysis using Groq."""
    
    def __init__(self):
        """Initialize Groq client."""
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key or api_key.strip() == "":
            logger.error("GROQ_API_KEY is empty or not set")
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        try:
            # Initialize Groq client - NO EXTRA PARAMETERS
            self.client = Groq(api_key=api_key)
            logger.info("✅ Groq LLM Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise
    
    def generate_analysis(self, commodity, market_data, news_summary, sentiment, user_query):
        """
        Generate AI-powered analysis using Groq.
        
        Args:
            commodity (str): Commodity name
            market_data (str): Market summary
            news_summary (str): Recent news summary
            sentiment (dict): Sentiment analysis
            user_query (str): Original user query
            
        Returns:
            str: Generated analysis
        """
        try:
            sentiment_text = f"""
Sentiment Analysis:
- Overall: {sentiment['overall']}
- Positive: {sentiment['positive']}%
- Neutral: {sentiment['neutral']}%
- Negative: {sentiment['negative']}%
            """ if sentiment else "Sentiment data unavailable"
            
            prompt = f"""You are a professional commodity market analyst. Analyze the following information and provide an educational insight report.

User Query: {user_query}

Commodity: {commodity}

{market_data}

Recent News Headlines:
{news_summary if news_summary else "No news available"}

{sentiment_text}

Please provide a comprehensive analysis that includes:
1. Current Market Situation - What is happening in the {commodity} market right now?
2. Key Price Drivers - What factors are influencing the price movement?
3. News Impact - How are recent news events affecting the market?
4. Market Sentiment - What does the overall sentiment tell us about market expectations?
5. Summary - A brief conclusion about the {commodity} market outlook.

IMPORTANT RULES:
- This is for EDUCATIONAL purposes only
- Do NOT provide investment advice or trading recommendations
- Focus on explaining market dynamics and factors
- Be factual and balanced in your analysis
- Keep the response concise but informative (200-400 words)

Generate the analysis now:"""
            
            logger.info("🤖 Calling Groq API...")
            
            message = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            analysis = message.choices[0].message.content
            logger.info("✅ Groq API call successful - Analysis generated")
            return analysis
        
        except Exception as e:
            logger.error(f"❌ Groq API error: {e}")
            raise