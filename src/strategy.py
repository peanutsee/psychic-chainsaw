"""This is a python script for the strategy classes."""

import pandas as pd

class SimpleMovingAverage:
    def __init__(self, short_lag: int = 3, long_lag: int = 5) -> None:
        
        self.short_lag = short_lag
        self.long_lag = long_lag

        return None
        
    def __str__(self) -> str:
        return f"SMA({self.short_lag}, {self.long_lag}) Strategy"
    
    def sma(self, df: pd.DataFrame = None) -> pd.DataFrame:
        # Create window
        df['sma_short'] = df['adjclose'].rolling(window=self.short_lag).mean()
        df['sma_long'] = df['adjclose'].rolling(window=self.long_lag).mean()

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
    def __init__(self, short_lag: int = 3, long_lag: int = 5) -> None:
        
        self.short_lag = short_lag
        self.long_lag = long_lag

        return None

    def __str__(self) -> str:
        return f"EMA({self.short_lag}, {self.long_lag}) Strategy"

    def ema(self, df: pd.DataFrame = None) -> pd.DataFrame:
        # Create window
        df['ema_short'] = df['adjclose'].ewm(span=self.short_lag, adjust=False).mean()
        df['ema_long'] = df['adjclose'].ewm(span=self.long_lag, adjust=False).mean()

        # Create a new DataFrame with relevant columns
        df_ema = df[['adjclose', 'ema_short', 'ema_long']].copy()
        df_ema.rename(columns={'adjclose': 'price'}, inplace=True)

        # Initialize 'Signal' column where 1 = Buy, -1 = Sell, 0 = Hold
        df_ema['signal'] = 0

        # Add Date Column
        df_ema['date'] = df['date']

        # Iterate through the DataFrame to create buy/sell signals
        for i in range(1, len(df_ema)):
            if df_ema['ema_short'][i] > df_ema['ema_long'][i] and df_ema['ema_short'][i-1] <= df_ema['ema_long'][i-1]:
                df_ema.at[i, 'signal'] = 1  # Buy signal
            elif df_ema['ema_short'][i] < df_ema['ema_long'][i] and df_ema['ema_short'][i-1] >= df_ema['ema_long'][i-1]:
                df_ema.at[i, 'signal'] = -1  # Sell signal

        return df_ema
    
class BollingerBands:
    def __init__(self, coefficient: int = 2) -> None:
        self.coefficient = coefficient
        
    def create_bands(self, df: pd.DataFrame = None) -> pd.DataFrame:
        
        tmp_df = df.copy()
        
        # Create 20-Day SMA
        tmp_df['20-day sma'] = tmp_df.adjclose.rolling(window=20).mean()

        # Create 20-Day SD
        tmp_df['20-day sd'] = tmp_df.adjclose.rolling(window=20).std()

        # Create bands
        tmp_df['upper_band'] = tmp_df['20-day sma'] + self.coefficient * tmp_df['20-day sd']
        tmp_df['lower_band'] = tmp_df['20-day sma'] - self.coefficient * tmp_df['20-day sd']
        
        # Calculate delta
        tmp_df['delta'] = tmp_df['upper_band'] - tmp_df['lower_band']

        return tmp_df
    
class MovingAverageConvergenceDivergence:
    def __init__(self, short_lag: int = 12, long_lag: int = 26, signal_lag: int = 9) -> None:

        self.short_lag = short_lag
        self.long_lag = long_lag
        self.signal_lag = signal_lag
        
    def macd(self, df) -> pd.DataFrame:
        
        # Calculate short-term and long-term EMAs
        df[f'{self.short_lag}-day ema'] = df['adjclose'].ewm(span=self.short_lag, adjust=False).mean()
        df[f'{self.long_lag}-day ema'] = df['adjclose'].ewm(span=self.long_lag, adjust=False).mean()
        
        # Calculate MACD line
        df['macd'] = df[f'{self.short_lag}-day ema'] - df[f'{self.long_lag}-day ema']
        
        # Calculate signal line (EMA of the MACD line)
        df['signal line'] = df['macd'].ewm(span=self.signal_lag, adjust=False).mean()
        
        # Calculate MACD histogram (difference between MACD and Signal line)
        df['histogram'] = df['macd'] - df['signal line']
        
        # Initialize columns for buy and sell signals
        df['signal'] = 0
        
        # Generate signals (Buy when MACD crosses above Signal, Sell when MACD crosses below Signal)
        for i in range(1, len(df)):
            if df['macd'].iloc[i] > df['signal line'].iloc[i] and df['macd'].iloc[i-1] <= df['signal line'].iloc[i-1]:
                df['signal'].iloc[i] = 1  # Buy signal
            elif df['macd'].iloc[i] < df['signal line'].iloc[i] and df['macd'].iloc[i-1] >= df['signal line'].iloc[i-1]:
                df['signal'].iloc[i] = -1  # Sell signal   
                     
        return df