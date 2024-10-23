"""This is a python script for the strategy classes."""

import pandas as pd

class SimpleMovingAverage:
    """Simple Moving Average (SMA) Crossover Strategy.
    
    What:
    SMA Crossover Strategy uses two simple moving averages: a short-lag SMA and a long-lag SMA.
    The SMA calculates the average price over a defined period, with equal weight given to each data point.
    
    How:
    Buy Signal: Short-lag SMA crosses over Long-lag SMA (Bullish Crossover).
    Sell Signal: Long-lag SMA crosses over Short-lag SMA (Bearish Crossover).
    
    Typically, the short-lag SMA might be a 50-day moving average, while the long-lag SMA could be a 200-day moving average for medium- or long-term trend analysis.
    """
    
    def __init__(self) -> None:
        pass
    
    def __str__(self) -> str:
        return "SMA Strategy"
    
    def sma(self, df: pd.DataFrame = None, short_lag: int = 3, long_lag: int = 5) -> pd.DataFrame:
        """SMA Crossover Strategy implementation.
        
        1. Create the short-lag and long-lag SMAs using pandas' .rolling() and .mean().
        2. Determine the buy/sell signals by checking when the short-lag SMA crosses the long-lag SMA, and vice versa.
        
        Parameters
        ----------
        df: pd.DataFrame
            This defines the ticker data in a pandas DataFrame.
            
        short_lag: int
            This defines the look-back period for the short-lag SMA (default is 50).
            
        long_lag: int
            This defines the look-back period for the long-lag SMA (default is 200).
            
        Returns
        -------
        pd.DataFrame
            A DataFrame that contains the original price data along with the short-lag SMA, long-lag SMA, and buy/sell signals.
        """
        
        # Create window
        df['sma_short'] = df['adjclose'].rolling(window=short_lag).mean()
        df['sma_long'] = df['adjclose'].rolling(window=long_lag).mean()

        # Create a new DataFrame with relevant columns
        df_sma = df[['adjclose', 'sma_short', 'sma_long']].copy()

        # Initialize 'Signal' column where 1 = Buy, -1 = Sell, 0 = Hold
        df_sma['signal'] = 0

        # Add Date Column
        df_sma['date'] = df['date']

        # Generate signals (Buy/Sell) based on short-lag and long-lag crossover 
        df_sma.loc[(df_sma['sma_short'] > df_sma['sma_long']) & (df_sma['sma_short'].shift(1) <= df_sma['sma_long'].shift(1)), 'signal'] = 1 
        df_sma.loc[(df_sma['sma_short'] < df_sma['sma_long']) & (df_sma['sma_short'].shift(1) >= df_sma['sma_long'].shift(1)), 'signal'] = -1
        
        return df_sma
    
class ExponentialMovingAverage:
    """Exponential Moving Average (EMA) Crossover Strategy.
    
    What:
    EMA Crossover Strategy uses two moving averages: a short-lag EMA and a long-lag EMA.
    The EMA places more weight on recent data compared to the Simple Moving Average (SMA),
    making it more responsive to price changes.
    
    How:
    Buy Signal: Short-lag EMA crosses over Long-lag EMA.
    Sell Signal: Long-lag EMA crosses over Short-lag EMA.
    
    Typically, the look-back periods for this strategy can vary depending on the type of trading.
    Short-term periods like 5-day and 10-day EMAs are often used for intraday or swing trading.
    """
    
    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        return "EMA Strategy"

    def ema(self, df: pd.DataFrame = None, short_lag: int = 5, long_lag: int = 10) -> pd.DataFrame:
        """EMA Crossover Strategy implementation.
        
        1. Create the short-lag and long-lag EMAs using pandas' .ewm() and .mean().
        2. Determine the buy/sell signals by checking when the short-lag EMA crosses the long-lag EMA, and vice versa.
        
        Parameters
        ----------
        df: pd.DataFrame
            This defines the ticker data in a pandas DataFrame.
            
        short_lag: int
            This defines the look-back period for the short-lag EMA.
            
        long_lag: int
            This defines the look-back period for the long-lag EMA.
            
        Returns
        -------
        pd.DataFrame
            This DataFrame contains the ticker data with EMAs and signals.
        """
        
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
        df_ema.loc[(df_ema['ema_short'] > df_ema['ema_long']) & (df_ema['ema_short'].shift(1) <= df_ema['ema_long'].shift(1)), 'signal'] = 1 
        df_ema.loc[(df_ema['ema_short'] < df_ema['ema_long']) & (df_ema['ema_short'].shift(1) >= df_ema['ema_long'].shift(1)), 'signal'] = -1

        return df_ema
    
class BollingerBands:
    """Bollinger Bands Strategy.
    
    What:
    Bollinger Bands are a volatility-based indicator created by plotting a Simple Moving Average (SMA)
    with upper and lower bands. These bands are typically set two standard deviations above and below
    the SMA, creating a volatility channel.
    
    How:
    Overbought Condition: Price approaches or exceeds the upper band.
    Oversold Condition: Price approaches or falls below the lower band.
    
    Traders often use Bollinger Bands to identify periods of high volatility and potential price reversals.
    """
    
    def __init__(self) -> None:
        ...
        
    def bollinger_bands(self, df: pd.DataFrame = None, coefficient: int = 2) -> pd.DataFrame:
        """Create Bollinger Bands.
        
        1. Calculate the 20-day SMA and standard deviation.
        2. Use the SMA and standard deviation to calculate the upper and lower Bollinger Bands.
        
        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame that contains the price data.
            
        coefficient: int
            The multiplier for the standard deviation, typically 2, used to create the bands.
            
        Returns
        -------
        pd.DataFrame
            This DataFrame contains the price data along with the SMA, upper band, lower band, and delta.
        """
        
        tmp_df = df.copy()
        
        # Create 20-Day SMA
        tmp_df['20-day sma'] = tmp_df.price.rolling(window=20).mean()

        # Create 20-Day SD
        tmp_df['20-day sd'] = tmp_df.price.rolling(window=20).std()

        # Create bands
        tmp_df['upper_band'] = tmp_df['20-day sma'] + coefficient * tmp_df['20-day sd']
        tmp_df['lower_band'] = tmp_df['20-day sma'] - coefficient * tmp_df['20-day sd']
        
        # Calculate delta
        tmp_df['delta'] = tmp_df['upper_band'] - tmp_df['lower_band']

        return tmp_df
    
class MovingAverageConvergenceDivergence:
    """Moving Average Convergence Divergence (MACD) Strategy.
    
    What:
    MACD is a trend-following momentum indicator that shows the relationship between two
    exponential moving averages (EMAs) of a security's price: a short-term EMA and a long-term EMA.
    
    How:
    Buy Signal: MACD line crosses above the Signal line (Bullish Crossover).
    Sell Signal: MACD line crosses below the Signal line (Bearish Crossover).
    
    MACD Histogram can be used to measure the strength of the trend, while MACD crossovers are used
    to generate buy/sell signals.
    """
    
    def __init__(self, ) -> None:
        ...
        
    def macd(self, df: pd.DataFrame, short_lag: int = 12, long_lag: int = 26, signal_lag: int = 9) -> pd.DataFrame:
        """MACD Crossover Strategy.
        
        1. Calculate short-term and long-term EMAs.
        2. Generate MACD line, Signal line, and MACD histogram.
        3. Determine buy/sell signals based on the MACD and Signal line crossovers.
        
        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame containing ticker price data.
        
        short_lag: int
            The short-term EMA period (typically 12 days).
            
        long_lag: int
            The long-term EMA period (typically 26 days).
            
        signal_lag: int
            The period for calculating the Signal line (typically 9 days).
        
        Returns
        -------
        pd.DataFrame
            The DataFrame with MACD line, Signal line, histogram, and signals.
        """
        
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
    """Relative Strength Index (RSI) Oscillator Strategy.
    
    What:
    RSI is a momentum oscillator that measures the speed and change of price movements. It ranges
    from 0 to 100 and is used to identify overbought or oversold conditions.
    
    How:
    Buy Signal: RSI crosses below the lower band (typically 30), indicating oversold conditions.
    Sell Signal: RSI crosses above the upper band (typically 70), indicating overbought conditions.
    
    RSI can also be used to detect divergences between price and momentum to anticipate potential reversals.
    """
    
    def __init__(self) -> None:
        ...
        
    def __str__(self) -> str:
        return "RSI Oscillator"
    
    def rsi(self, df: pd.DataFrame, look_back_period: int = 14, upper_band: int = 70, lower_band: int = 30) -> pd.DataFrame:
        """RSI Oscillator Calculation.
        
        1. Calculate price changes and determine gains and losses.
        2. Compute the rolling averages or EMAs of the gains and losses.
        3. Calculate the Relative Strength (RS) and RSI based on the gains/losses.
        4. Identify overbought or oversold conditions using predefined bands.
        
        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame containing the price data.
            
        look_back_period: int
            The look-back period for RSI calculation (typically 14).
            
        upper_band: int
            The upper band threshold (typically 70) to indicate overbought conditions.
            
        lower_band: int
            The lower band threshold (typically 30) to indicate oversold conditions.
        
        Returns
        -------
        pd.DataFrame
            A DataFrame with the price data, RSI values, and signals for overbought/oversold conditions.
        """
        
        df = df.copy() 
        
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

class MoneyFlowIndex:
    """Money Flow Index (MSI) Oscillator Strategy.
    
    What:
    MFI is a technical oscillator that uses price and volume to identify overbought or oversold signals in assets. It can be used to spot
    divergences which warns of a trend change in price. The oscillator moves between 0 and 100.
    Divergences is defined as opposite trends in MFI and securities price.
    
    How:
    MFI above 80 = overbought conditions, may signal a price reversal. Threshold of 90 is also used.
    MFI below 20 = oversold conditions, may signal a price breakout. Threshold of 10 is also used.
    """
    
    def __init__(self) -> None:
        pass
    
    def __str__(self) -> str:
        return "MFI Oscillator"
    
    def msi(self, df: pd.DataFrame, look_back_period: int = 14, upper_band: int = 80, lower_band: int = 20) -> pd.DataFrame:
        """Calculate the Money Flow Index (MFI) Calculation.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing at least the following columns: 'high', 'low', 'close', and 'volume'.
        look_back_period : int, optional
            The number of periods over which to calculate the MFI (default is 14).
        upper_band : int, optional
            The threshold for determining an overbought condition (default is 80).
        lower_band : int, optional
            The threshold for determining an oversold condition (default is 20).

        Returns
        -------
        pd.DataFrame
            The input DataFrame with added columns for 'MFI', 'overbought', and 'oversold' signals.
        
        Notes
        -----
        The Money Flow Index (MFI) is a momentum indicator that uses both price and volume data
        to measure buying and selling pressure. The formula used for the calculation is:

            MFI = 100 - (100 / (1 + Money Flow Ratio))

        where the Money Flow Ratio is the ratio of positive to negative money flows over the 
        look-back period.
        """

        # Calculate typical price
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        
        # Calculate raw money flow
        df['raw_money_flow'] = df['typical_price'] * df['volume']
        
        # Mark periods as up or down by using 1 or -1
        df['money_flow_sign'] = df['typical_price'].diff().apply(lambda x: 1 if x > 0 else -1)
        
        # Apply the sign to raw money flow to get positive and negative money flow
        df['signed_money_flow'] = df['raw_money_flow'] * df['money_flow_sign']
        
        # Separate positive and negative money flows
        df['positive_flow'] = df['signed_money_flow'].apply(lambda x: x if x > 0 else 0)
        df['negative_flow'] = df['signed_money_flow'].apply(lambda x: -x if x < 0 else 0)
        
        # Calculate the sum of positive and negative money flows over the look-back period
        df['sum_positive_flow'] = df['positive_flow'].rolling(window=look_back_period).sum()
        df['sum_negative_flow'] = df['negative_flow'].rolling(window=look_back_period).sum()
        
        # Calculate the money flow ratio
        df['money_flow_ratio'] = df['sum_positive_flow'] / df['sum_negative_flow']
        
        # Calculate the Money Flow Index (MFI)
        df['MFI'] = 100 - (100 / (1 + df['money_flow_ratio']))
        
        # Add signals for overbought or oversold
        df['overbought'] = df['MFI'] > upper_band
        df['oversold'] = df['MFI'] < lower_band
        
        return df
    
class StochasticOscillator:
    """Stochastic Oscillator Strategy.
    
    What:
    SO is a momentum oscillator that uses closing price to identify overbought or oversold signals. It assumes that closing price follows trends in the momentum.
    The oscillator moves between 0 and 100.
    
    How:
    SO above 80 = overbought conditions, may signal a price reversal. 
    SO below 20 = oversold conditions, may signal a price breakout.
    """
    def __init__(self) -> None:
        pass
    
    def __str__(self) -> str:
        return "Stochastic Oscillator"
    
    def so(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """Calculate the Stochastic Oscillator Calculation.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing at least the following column: 'close'.

        Returns
        -------
        pd.DataFrame
            The input DataFrame with added columns for 'SO', 'overbought', and 'oversold' signals.
        
        Notes
        -----
        The Stochastic Oscillator is a momentum indicator that uses closing price to determine the trends in prices.
        The formula used for the calculation is:

            %K = [(C - L14) / (H14 - L14)] * 100
        
        where %K is the current value of the Stochastic Oscillator, L14 is the min(closing of past 14D), H14 is the max(closing of past 14D) and
        C is the most recent closing price.
        """       
        
        # Determine L14
        df['L14'] = df['close'].rolling(window=14).min()
        
        # Determine H14
        df['H14'] = df['close'].rolling(window=14).max()
        
        # Determine %K
        df['stoch_k'] = 100 * ((df['close'] - df['L14']) / (df['H14'] - df['L14']))
        
        # Add signals for overbought or oversold
        df['overbought'] = df['stoch_k'] > 80
        df['oversold'] = df['stoch_k'] < 20
        
        return df
        
class RateOfChange:
    # TODO: Implement this class