import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any

class DataFetcher:
    def __init__(self, ticker: str):
        self.ticker_symbol = ticker
        self.ticker = yf.Ticker(ticker)
        self.info = {}
        self.financials = pd.DataFrame()
        self.balance_sheet = pd.DataFrame()
        self.cashflow = pd.DataFrame()

    def fetch_all(self):
        """Fetch all necessary data from yfinance."""
        try:
            self.info = self.ticker.info
            self.financials = self.ticker.financials
            self.balance_sheet = self.ticker.balance_sheet
            self.cashflow = self.ticker.cashflow
            
            if self.financials.empty or self.balance_sheet.empty:
                raise ValueError(f"Could not fetch complete financial data for {self.ticker_symbol}")
        except Exception as e:
            raise ConnectionError(f"Error fetching data for {self.ticker_symbol}: {str(e)}")

    def get_metric(self, df: pd.DataFrame, keys: list, default: float = 0.0) -> float:
        """Helper to fetch the most recent metric with fuzzy matching."""
        for key in keys:
            if key in df.index:
                val = df.loc[key].iloc[0]
                return val if not np.isnan(val) else default
        return default

    def get_historical_growth(self, df: pd.DataFrame, keys: list) -> float:
        """Calculate average historical growth rate."""
        for key in keys:
            if key in df.index:
                series = df.loc[key].dropna()
                if len(series) > 1:
                    # Reverse if needed (yfinance usually returns most recent first)
                    if series.index[0] > series.index[-1]:
                        series = series.iloc[::-1]
                    growth = series.pct_change().mean()
                    return growth if not np.isnan(growth) else 0.05
        return 0.05

    def get_lbo_inputs(self) -> Dict[str, Any]:
        """Extract key inputs for LBO modeling."""
        if not self.info:
            self.fetch_all()
            
        ebitda = self.get_metric(self.financials, ['EBITDA', 'Normalized EBITDA'])
        revenue = self.get_metric(self.financials, ['Total Revenue', 'Revenue'])
        
        return {
            'ticker': self.ticker_symbol,
            'current_price': self.info.get('currentPrice', 0),
            'market_cap': self.info.get('marketCap', 0),
            'total_debt': self.info.get('totalDebt', 0),
            'total_cash': self.info.get('totalCash', 0),
            'ebitda': ebitda,
            'revenue': revenue,
            'ebitda_margin': ebitda / revenue if revenue > 0 else 0.2,
            'tax_rate': self.get_metric(self.financials, ['Tax Provision']) / self.get_metric(self.financials, ['Pretax Income']) if self.get_metric(self.financials, ['Pretax Income']) > 0 else 0.21,
            'capex_pct_rev': abs(self.get_metric(self.cashflow, ['Capital Expenditure'])) / revenue if revenue > 0 else 0.03,
            'rev_growth': self.get_historical_growth(self.financials, ['Total Revenue', 'Revenue'])
        }
