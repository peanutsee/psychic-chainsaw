"""This is a python script for the strategy classes."""

import pandas as pd

class SimpleMovingAverage:
    def __init__(self, short_lag: int = 3, long_lag: int = 5) -> None:
        
        self.short_lag = short_lag
        self.long_lag = long_lag
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval

        return None
        
    def __str__(self) -> str:
        return f"SMA({self.short_lag}, {self.long_lag}) Strategy"
    
    def sma(self, df: pd.DataFrame = None) -> pd.DataFrame:
        # Create window
        df['sma_short'] = df['adjclose'].rolling(window=short_window).mean()
        df['sma_long'] = df['adjclose'].rolling(window=long_window).mean()

        # Create a new DataFrame with relevant columns
        df_sma = df[['adjclose', 'sma_short', 'sma_long']].copy()
        df_sma.rename(columns={'adjclose': 'price'}, inplace=True)

        # Initialize 'Signal' column where 1 = Buy, -1 = Sell, 0 = Hold
        df_sma['signal'] = 0

        # Add Date Column
        df_sma['date'] = df['date']

        # Iterate through the DataFrame to create buy/sell signals
        for i in range(1, len(df_sma)):
            if df_sma['sma_short'][i] > df_sma['sma_long'][i] and df_sma['sma_short'][i-1] <= df_sma['sma_long'][i-1]:
                df_sma.at[i, 'signal'] = 1  # Buy signal
            elif df_sma['sma_short'][i] < df_sma['sma_long'][i] and df_sma['sma_short'][i-1] >= df_sma['sma_long'][i-1]:
                df_sma.at[i, 'signal'] = -1  # Sell signal

        return df_sma
    
class ExponentialMovingAverage:
    