"""This is a python script for the strategy classes."""

import pandas as pd

class SimpleMovingAverage:
    def __init__(self) -> None:
        ...
        
    def __str__(self) -> str:
        return "SMA Strategy"
    
    def sma(self, df: pd.DataFrame = None, short_lag: int = 3, long_lag: int = 5) -> pd.DataFrame:
        # Create window
        df['sma_short'] = df['adjclose'].rolling(window=short_lag).mean()
        df['sma_long'] = df['adjclose'].rolling(window=long_lag).mean()

        # Create a new DataFrame with relevant columns
        df_sma = df[['adjclose', 'sma_short', 'sma_long']].copy()

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
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return "EMA Strategy"

    def ema(self, df: pd.DataFrame = None, short_lag: int = 5, long_lag: int = 10) -> pd.DataFrame:
        # Create window
        df['ema_short'] = df['adjclose'].ewm(span=short_lag, adjust=False).mean()
        df['ema_long'] = df['adjclose'].ewm(span=long_lag, adjust=False).mean()

        # Create a new DataFrame with relevant columns
        df_ema = df[['adjclose', 'ema_short', 'ema_long']].copy()

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
    def __init__(self) -> None:
        ...
        
    def create_bands(self, df: pd.DataFrame = None, coefficient: int = 2) -> pd.DataFrame:
        
        tmp_df = df.copy()
        
        # Create 20-Day SMA
        tmp_df['20-day sma'] = tmp_df.adjclose.rolling(window=20).mean()

        # Create 20-Day SD
        tmp_df['20-day sd'] = tmp_df.adjclose.rolling(window=20).std()

        # Create bands
        tmp_df['upper_band'] = tmp_df['20-day sma'] + coefficient * tmp_df['20-day sd']
        tmp_df['lower_band'] = tmp_df['20-day sma'] - coefficient * tmp_df['20-day sd']
        
        # Calculate delta
        tmp_df['delta'] = tmp_df['upper_band'] - tmp_df['lower_band']

        return tmp_df
    
class MovingAverageConvergenceDivergence:
    def __init__(self, ) -> None:
        ...
        
    def macd(self, df: pd.DataFrame, short_lag: int = 12, long_lag: int = 26, signal_lag: int = 9) -> pd.DataFrame:
        # Calculate short-term and long-term EMAs
        df[f'{short_lag}-day ema'] = df['adjclose'].ewm(span=short_lag, adjust=False).mean()
        df[f'{long_lag}-day ema'] = df['adjclose'].ewm(span=long_lag, adjust=False).mean()
        
        # Calculate MACD line
        df['macd'] = df[f'{short_lag}-day ema'] - df[f'{long_lag}-day ema']
        
        # Calculate signal line (EMA of the MACD line)
        df['signal line'] = df['macd'].ewm(span=signal_lag, adjust=False).mean()
        
        # Calculate MACD histogram (difference between MACD and Signal line)
        df['histogram'] = df['macd'] - df['signal line']
        
        # Initialize signal and conditions columns
        df['signal'] = 0
        df['conditions'] = ''
        
        # Generate signals (Buy/Sell) based on MACD and Signal line crossover
        df.loc[(df['macd'] > df['signal line']) & (df['macd'].shift(1) <= df['signal line'].shift(1)), 'signal'] = 1 
        df.loc[(df['macd'] < df['signal line']) & (df['macd'].shift(1) >= df['signal line'].shift(1)), 'signal'] = -1 
        
        # Generate conditions (Bull/Bear) based on zero-line crossover
        df.loc[(df['macd'] > 0) & (df['macd'].shift(1) <= 0), 'conditions'] = 'bull'  
        df.loc[(df['macd'] < 0) & (df['macd'].shift(1) >= 0), 'conditions'] = 'bear' 
        
        return df

    
class RelativeStrengthIndex:
    def __init__(self) -> None:
        ...
        
    def __str__(self) -> str:
        return "RSI Oscillator"
    
    def rsi(self, df: pd.DataFrame, look_back_period: int = 14, upper_band: int = 70, lower_band: int = 30) -> pd.DataFrame:
        df = df.copy()  # Avoid modifying the original DataFrame
        
        # Calculate price changes
        df['delta'] = df['adjclose'].diff()
        
        # Calculate gains and losses
        df['gain'] = df['delta'].clip(lower=0)  # Gains: positive differences only
        df['loss'] = -df['delta'].clip(upper=0)  # Losses: negative differences only
        
        # Calculate rolling averages for the first look-back period
        avg_gain = df['gain'].rolling(window=look_back_period, min_periods=look_back_period).mean()
        avg_loss = df['loss'].rolling(window=look_back_period, min_periods=look_back_period).mean()
        
        # Calculate exponential moving averages (EMA) for gains and losses
        df['avg_gain'] = avg_gain.combine_first(df['gain'].ewm(span=look_back_period, adjust=False).mean())
        df['avg_loss'] = avg_loss.combine_first(df['loss'].ewm(span=look_back_period, adjust=False).mean())
        
        # Calculate relative strength (RS)
        df['RS'] = df['avg_gain'] / df['avg_loss']
        
        # Calculate the RSI
        df['RSI'] = 100 - (100 / (1 + df['RS']))
        
        # Add overbought and oversold columns
        df['overbought'] = df['RSI'] > upper_band
        df['oversold'] = df['RSI'] < lower_band
        
        return df