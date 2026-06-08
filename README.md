# 📊 AI-Based Commodity Price Analysis and Insight Agent

A professional AI agent that analyzes commodity markets by combining price data, news sentiment, and LLM-powered insights to explain market trends.

## 🎯 Project Objective

This system helps users understand commodity market dynamics by answering questions like:
- *"Why is gold price increasing?"*
- *"Analyze the crude oil market"*
- *"What factors are affecting wheat prices?"*
- *"Explain recent silver price trends"*

**Key Point:** This is **NOT a price prediction system**. The focus is on explaining market trends and factors affecting prices.

---

## ✨ Features

### 1. **Natural Language Query Processing**
- Accepts user queries in plain English
- Automatically detects mentioned commodities
- Validates queries before processing

### 2. **Market Data Analysis**
- Fetches 30-day historical price data
- Calculates price trends and changes
- Generates candlestick charts

### 3. **News Aggregation**
- Scrapes recent commodity-related news from Google News RSS
- Displays articles with sources and publication dates
- Extracts key information automatically

### 4. **Sentiment Analysis**
- Analyzes sentiment of news articles using VADER
- Calculates positive/neutral/negative percentages
- Determines overall market sentiment

### 5. **AI-Powered Insights**
- Uses Groq LLM (llama-3.3-70b-versatile)
- Generates comprehensive market analysis
- Explains price movements and market drivers
- Provides educational insights (not financial advice)

### 6. **Interactive Dashboard**
- Professional Streamlit UI
- Real-time interactive charts
- Clean data visualization
- Mobile-friendly design

---

## 🏗️ Agent Architecture

```
User Query
    ↓
Commodity Detection
    ↓
Fetch Price Data (yfinance)
    ↓
Fetch News (Google News RSS)
    ↓
Sentiment Analysis (VADER/NLTK)
    ↓
LLM Context Building
    ↓
Groq LLM Analysis
    ↓
Insight Report Generation
    ↓
Streamlit Dashboard Display
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.28.1 |
| **Backend** | Python 3.11+ |
| **LLM** | Groq API (llama-3.3-70b-versatile) |
| **Market Data** | yfinance 0.2.32 |
| **News Source** | Google News RSS |
| **News Parsing** | feedparser 6.0.10 |
| **Sentiment** | NLTK VADER 3.8.1 |
| **Visualization** | Plotly 5.18.0 |
| **Data Processing** | pandas 2.1.3, numpy 1.26.4 |
| **Environment** | python-dotenv 1.0.0 |

---

## 📦 Supported Commodities

| Commodity | Symbol | News Query |
|-----------|--------|-----------|
| Gold | GC=F | gold commodity prices |
| Silver | SI=F | silver commodity prices |
| Crude Oil | CL=F | crude oil prices market |
| Natural Gas | NG=F | natural gas prices |
| Copper | HG=F | copper commodity prices |
| Wheat | ZW=F | wheat prices commodity |
| Corn | ZC=F | corn prices commodity |
| Soybeans | ZS=F | soybeans prices commodity |

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/commodity-price-agent.git
cd commodity-price-agent
```

### Step 2: Create Virtual Environment (Windows)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data (First Run Only)

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

---

## 🔑 Environment Variables

### Step 1: Create `.env` file

```bash
copy .env.example .env
```

### Step 2: Add Your Groq API Key

Open `.env` and replace:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

**Get your API key:** https://console.groq.com/keys

---

## ▶️ Running the Application

### Windows CMD:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run Streamlit app
streamlit run app.py
```

The app will open at: `http://localhost:8501`

---

## 💡 Example Queries

Try asking:

1. **"Why is gold price increasing?"**
   - Displays current gold price
   - Shows 30-day trend chart
   - Analyzes recent gold news
   - Provides AI-powered explanation

2. **"Analyze the crude oil market"**
   - Current oil price and trend
   - Recent news about crude oil
   - Market sentiment analysis
   - Comprehensive market analysis

3. **"What's affecting wheat prices?"**
   - Wheat price trends
   - Latest agriculture news
   - Sentiment distribution
   - Key factors affecting prices

4. **"Compare gold and silver trends"**
   - Analyzes precious metals
   - Price comparisons
   - Market dynamics
   - Relative trends

---

## 📁 Project Structure

```
commodity-price-agent/
│
├── app.py                          # Main Streamlit application
│
├── agents/
│   └── commodity_agent.py         # Main AI Agent orchestration
│
├── services/
│   ├── market_service.py          # yfinance data fetching
│   ├── news_service.py            # Google News RSS fetching
│   ├── sentiment_service.py       # VADER sentiment analysis
│   └── llm_service.py             # Groq LLM interface
│
├── utils/
│   └── commodity_mapper.py        # Commodity mapping utility
│
├── docs/                           # Documentation
├── screenshots/                    # UI screenshots (for README)
│
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── .env.example                   # Environment template
└── LICENSE                        # MIT License
```

---

## 🔧 How It Works

### 1. **Query Processing**
```python
User: "Why is gold price increasing?"
↓
Agent detects: "gold" commodity
```

### 2. **Data Fetching**
```python
Market Data: yfinance → 30 days of GC=F prices
News Data: Google RSS → Latest gold-related articles
```

### 3. **Analysis**
```python
Sentiment: 65% Positive, 20% Neutral, 15% Negative
Trend: UP ⬆️ (+2.5% in 30 days)
```

### 4. **LLM Generation**
```python
Groq LLM receives all data and generates:
- Current market situation
- Key price drivers
- News impact analysis
- Market sentiment interpretation
- Summary and outlook
```

### 5. **Display**
```python
Streamlit renders:
- Price charts
- Sentiment visualizations
- News articles
- AI-generated analysis
```

---

## 📊 API Services Used

### Groq API
- **Endpoint:** LLaMA 3.3 70B
- **Model:** llama-3.3-70b-versatile
- **Free tier:** Sufficient for this project
- **Rate limit:** Generous free tier

### yfinance
- **Free:** ✅ No API key required
- **Data:** Historical commodity prices
- **Symbols:** Futures contracts (GC=F, CL=F, etc.)

### Google News RSS
- **Free:** ✅ No API key required
- **Data:** Recent news articles
- **Format:** RSS feeds (freely accessible)

---

## ⚠️ Error Handling

The application gracefully handles:

| Error | Handling |
|-------|----------|
| Invalid commodity | Shows friendly error + supported commodities |
| Empty query | Prompts user to enter query |
| Missing API key | Warns and continues (LLM analysis disabled) |
| Yahoo Finance unavailable | Uses fallback symbols |
| RSS feed failure | Shows cached data or message |
| Network issues | Informative error messages |

---

## 🔒 Security

- API keys stored in `.env` (never committed)
- `.gitignore` protects sensitive files
- No data persistence
- No user data collection
- All operations are local

---

## 📈 Future Improvements

Potential enhancements:

1. **Multi-commodity comparison** - Compare trends across commodities
2. **Historical analysis** - Compare trends from different time periods
3. **Alerts system** - Notify users of significant price movements
4. **Export reports** - Generate PDF reports
5. **Real-time updates** - WebSocket for live price updates
6. **Advanced NLP** - Support complex multi-commodity queries
7. **Caching** - Reduce API calls with smart caching
8. **Mobile app** - Native mobile interface

---

## 👨‍💼 Author

Built for University AI Semester Project

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

## 📞 Support

For issues or questions:

1. Check the README
2. Review project structure
3. Check error messages
4. Verify environment variables

---

## 🎓 Educational Use

This project demonstrates:

- ✅ AI agent orchestration
- ✅ Multi-service integration
- ✅ NLP and sentiment analysis
- ✅ LLM utilization
- ✅ Full-stack development
- ✅ Software architecture
- ✅ Error handling
- ✅ Clean code principles

Perfect for university AI course submission!

---

**Last Updated:** June 2026  
**Status:** Production Ready ✅