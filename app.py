"""
Streamlit dashboard for AI-Based Commodity Price Analysis and Insight Agent
"""

import streamlit as st
import plotly.graph_objects as go
import logging
from agents.commodity_agent import CommodityAgent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page configuration
st.set_page_config(
    page_title="Commodity Price Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_agent():
    """Initialize the commodity agent."""
    if "agent" not in st.session_state:
        st.session_state.agent = CommodityAgent()
    return st.session_state.agent


def create_price_chart(chart_data):
    """Create interactive price chart using Plotly."""
    if not chart_data:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(
        x=chart_data['date'],
        open=[chart_data['close'][0]] * len(chart_data['date']),
        high=chart_data['high'],
        low=chart_data['low'],
        close=chart_data['close'],
        name='Price'
    ))
    
    fig.update_layout(
        title=f"30-Day Price Trend",
        yaxis_title="Price (USD)",
        xaxis_title="Date",
        template="plotly_white",
        height=400,
        hovermode='x unified'
    )
    
    return fig


def display_sentiment(sentiment):
    """Display sentiment analysis results."""
    if not sentiment:
        st.warning("Sentiment data not available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Sentiment", sentiment['overall'])
    
    with col2:
        st.metric("Positive", f"{sentiment['positive']}%", delta=None)
    
    with col3:
        st.metric("Neutral", f"{sentiment['neutral']}%", delta=None)
    
    with col4:
        st.metric("Negative", f"{sentiment['negative']}%", delta=None)
    
    # Sentiment pie chart
    fig = go.Figure(data=[go.Pie(
        labels=['Positive', 'Neutral', 'Negative'],
        values=[sentiment['positive'], sentiment['neutral'], sentiment['negative']],
        marker=dict(colors=['#2ecc71', '#95a5a6', '#e74c3c'])
    )])
    
    fig.update_layout(
        title="Sentiment Distribution",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_news(news_items):
    """Display news articles."""
    if not news_items:
        st.info("No recent news found")
        return
    
    st.subheader("📰 Latest News")
    
    for i, article in enumerate(news_items, 1):
        with st.expander(f"📄 {article['title'][:60]}..."):
            st.write(f"**Source:** {article['source']}")
            st.write(f"**Summary:** {article['summary'][:300]}...")
            if article['link']:
                st.markdown(f"[Read Full Article]({article['link']})")


def main():
    """Main Streamlit application."""
    
    # Initialize session state
    agent = initialize_agent()
    
    # Header
    st.markdown('<div class="header-title">Commodity Price Analysis & Insight Agent</div>', 
                unsafe_allow_html=True)
    st.markdown("### Understand commodity market trends using AI")
    
    st.divider()
    
    # Sidebar information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This AI agent analyzes commodity markets by:
        
        1. **Detecting** commodities from your query
        2. **Fetching** historical price data
        3. **Gathering** recent news articles
        4. **Analyzing** market sentiment
        5. **Generating** AI-powered insights
        
        **Supported Commodities:**
        - Gold
        - Silver
        - Crude Oil
        - Natural Gas
        - Copper
        - Wheat
        - Corn
        - Soybeans
        """)
        
        st.divider()
        st.markdown("**Example Queries:**")
        examples = [
            "Why is gold price increasing?",
            "Analyze crude oil market",
            "What's affecting wheat prices?",
            "Compare silver and gold trends"
        ]
        for example in examples:
            st.caption(f"• {example}")
    
    # Query input
    st.subheader("Ask about a Commodity")
    user_query = st.text_input(
        "Enter your question about commodities:",
        placeholder="e.g., Why is gold price increasing?",
        key="user_query"
    )
    
    col1, col2 = st.columns([4, 1])
    
    with col2:
        analyze_button = st.button("Analyz  e", use_container_width=True)
    
    # Analysis logic
    if analyze_button or user_query:
        if not user_query:
            st.error("Please enter a query")
        else:
            # Validate query
            is_valid, message = agent.validate_query(user_query)
            
            if not is_valid:
                st.error(message)
            else:
                st.success(message)
                
                # Show loading spinner
                with st.spinner("🔄 Analyzing commodity market..."):
                    result = agent.analyze(user_query)
                
                if result["success"]:
                    st.divider()
                    
                    # Market Summary
                    st.subheader(f"💰 {result['commodity']} Market Summary")
                    st.markdown(result['market_summary'])
                    
                    st.divider()
                    
                    # Price Chart
                    if result['chart_data']:
                        st.subheader("📈 30-Day Price Trend")
                        chart = create_price_chart(result['chart_data'])
                        if chart:
                            st.plotly_chart(chart, use_container_width=True)
                    
                    # Sentiment Analysis
                    if result['sentiment']:
                        st.divider()
                        st.subheader("💭 Market Sentiment Analysis")
                        display_sentiment(result['sentiment'])
                    
                    # News
                    if result['news']:
                        st.divider()
                        display_news(result['news'])
                    
                    # AI Analysis
                    st.divider()
                    st.subheader("🤖 AI-Powered Market Analysis")
                    
                    if result['analysis']:
                        st.markdown(result['analysis'])
                    else:
                        st.info("AI analysis not available")
                    
                    st.divider()
                    st.success("✅ Analysis complete!")
                
                else:
                    st.error(f"❌ {result['error']}")


if __name__ == "__main__":
    main()