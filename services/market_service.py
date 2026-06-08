"""
Market data service for fetching commodity prices from yfinance with fallback to mock data.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MarketService:
    """Service for fetching commodity market data."""
    
    @staticmethod
    def _generate_mock_data(days=30):
        """Generate realistic mock data when yfinance fails."""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        start_price = np.random.uniform(1500, 2500)
        
        prices = start_price + np.cumsum(np.random.normal(0, 10, days))
        
        data = pd.DataFrame({
            'open': prices + np.random.uniform(-5, 5, days),
            'high': prices + np.abs(np.random.normal(0, 5, days)),
            'low': prices - np.abs(np.random.normal(0, 5, days)),
            'close': prices,
            'volume': np.random.uniform(1000000, 5000000, days)
        }, index=dates)
        
        return data
    
    @staticmethod
    def _clean_dataframe(data):
        """Clean yfinance MultiIndex DataFrame."""
        try:
            # Flatten MultiIndex columns if present
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(0)
            
            # Ensure columns are lowercase
            data.columns = data.columns.str.lower()
            
            return data
        except Exception as e:
            logger.warning(f"Could not clean dataframe: {e}")
            return data
    
    @staticmethod
    def get_data_with_fallback(symbols, period='30d'):
        """
        Try multiple symbols until one works, fallback to mock data.
        
        Args:
            symbols (list): List of symbols to try
            period (str): Period for data
            
        Returns:
            tuple: (DataFrame, used_symbol) or (None, None)
        """
        for symbol in symbols:
            try:
                logger.info(f"Trying symbol: {symbol}")
                data = yf.download(
                    symbol, 
                    period=period, 
                    progress=False,
                    timeout=5
                )
                
                if data is not None and not data.empty and len(data) > 0:
                    data = MarketService._clean_dataframe(data)
                    logger.info(f"✅ Success with symbol: {symbol}")
                    return data, symbol
                else:
                    logger.warning(f"Empty data for {symbol}")
            except Exception as e:
                logger.warning(f"Failed with {symbol}: {str(e)}")
                continue
        
        # Fallback to mock data
        logger.warning(f"All symbols failed, using mock data")
        days = int(period.replace('d', '')) if 'd' in period else 30
        mock_data = MarketService._generate_mock_data(days)
        return mock_data, symbols[0] if symbols else "MOCK"
    
    @staticmethod
    def get_price_trend(symbols, days=30):
        """
        Calculate price trend.
        
        Args:
            symbols (list): List of symbols
            days (int): Number of days to analyze
            
        Returns:
            dict: Trend information or None
        """
        try:
            data, used_symbol = MarketService.get_data_with_fallback(symbols)
            
            if data is None or len(data) < 2:
                logger.warning("Insufficient data for trend calculation")
                return None
            
            # Find close column
            close_col = 'close'
            if close_col not in data.columns:
                logger.error(f"Close column not found. Columns: {data.columns.tolist()}")
                return None
            
            start_price = float(data[close_col].iloc[0])
            end_price = float(data[close_col].iloc[-1])
            change = end_price - start_price
            change_percent = (change / start_price) * 100 if start_price != 0 else 0
            
            trend = "UP ⬆️" if change > 0 else "DOWN ⬇️" if change < 0 else "STABLE ➡️"
            
            # Get high and low
            high_col = 'high'
            low_col = 'low'
            
            high_price = float(data[high_col].max()) if high_col in data.columns else end_price
            low_price = float(data[low_col].min()) if low_col in data.columns else end_price
            
            return {
                "current_price": end_price,
                "start_price": start_price,
                "change": change,
                "change_percent": change_percent,
                "trend": trend,
                "high": high_price,
                "low": low_price,
                "used_symbol": used_symbol
            }
        except Exception as e:
            logger.error(f"Error calculating trend: {e}")
            return None
    
    @staticmethod
    def prepare_chart_data(symbols, days=30):
        """
        Prepare data for charting.
        
        Args:
            symbols (list): List of symbols
            days (int): Number of days to fetch
            
        Returns:
            dict: Chart data or None
        """
        try:
            data, used_symbol = MarketService.get_data_with_fallback(symbols)
            
            if data is None or data.empty:
                return None
            
            close_col = 'close'
            high_col = 'high'
            low_col = 'low'
            vol_col = 'volume'
            
            if close_col not in data.columns:
                logger.error("Close column not found for charting")
                return None
            
            data_dict = {
                'date': data.index.strftime('%Y-%m-%d').tolist(),
                'close': data[close_col].tolist(),
                'high': data[high_col].tolist() if high_col in data.columns else data[close_col].tolist(),
                'low': data[low_col].tolist() if low_col in data.columns else data[close_col].tolist(),
                'volume': data[vol_col].tolist() if vol_col in data.columns else [0] * len(data),
                'symbol': used_symbol
            }
            
            return data_dict
        except Exception as e:
            logger.error(f"Error preparing chart data: {e}")
            return None
    
    @staticmethod
    def get_market_summary(symbols, display_name):
        """
        Get text summary of market.
        
        Args:
            symbols (list): List of symbols
            display_name (str): Display name of commodity
            
        Returns:
            str: Market summary or None
        """
        try:
            trend = MarketService.get_price_trend(symbols)
            
            if not trend:
                logger.warning("Could not get trend for market summary")
                return None
            
            summary = f"""
**{display_name} Market Summary**

🔹 Current Price: ${trend['current_price']:.2f}
🔹 30-Day Trend: {trend['trend']}
🔹 Change: ${trend['change']:.2f} ({trend['change_percent']:.2f}%)
🔹 30-Day High: ${trend['high']:.2f}
🔹 30-Day Low: ${trend['low']:.2f}
🔹 Data Source: {trend['used_symbol']}
            """
            
            return summary
        except Exception as e:
            logger.error(f"Error getting market summary: {e}")
            return None