from src.backtesting import *
from src.data import *
from src.strategy import *
import yaml
from typing import Callable, Any
import pandas as pd

with open("./config/config.yaml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
def run_strategy(strategy_name: str = None, 
                 strategy_function: Callable = None, 
                 df: pd.DataFrame = None, 
                 obj_backtesting: Any = None, 
                 strategies: list = None) -> None:
    
    # Test the strategy with multiple configurations
    strat_result = obj_backtesting.test_strategy(strategy_function, df, strategies, verbose=0)
    print(f"Best {strategy_name}: S${strat_result.get('fund')} ({strat_result.get('best')})")
    
    # Show the signals
    signals = obj_backtesting.show_signals(strategy_function(df), latest=True)
    print(f"Signals for {strategy_name} strategy: {signals}\n")

if __name__ == "__main__":
    starting_fund = config.get("FUND")
    ticker = config.get("TICKER")
    start_date = config.get("START_DATE")
    end_date = config.get("END_DATE")
    interval = config.get("INTERVAL")
    strategies = config.get("STRATEGIES")
    
    # Initialize objects
    obj_ticker_data = TickerData(ticker, start_date, end_date, interval)
    obj_backtesting = Backtesting(starting_fund)
    obj_sma = SimpleMovingAverage()
    obj_ema = ExponentialMovingAverage()
    obj_macd = MovingAverageConvergenceDivergence()
    obj_rsi = RelativeStrengthIndex()
    obj_msi = MoneyFlowIndex()
    obj_so = StochasticOscillator()
    obj_roc = RateOfChange()
    
    # Get data
    df = obj_ticker_data.get_data()
    
    # Perform Strategies
    run_strategy("SMA", obj_sma.sma, df, obj_backtesting, strategies)
    run_strategy("EMA", obj_ema.ema, df, obj_backtesting, strategies)
    run_strategy("MACD", obj_macd.macd, df, obj_backtesting, strategies)
    
    # Run RSI
    rsi_signal = obj_backtesting.show_signals(obj_rsi.rsi(df), is_oscillator = True, latest=True)
    print(f"RSI Signal {rsi_signal[0].title()} between {rsi_signal[1]} and {rsi_signal[2]}")
    
    # Run MSI
    msi_signal = obj_backtesting.show_signals(obj_msi.msi(df), is_oscillator = True, latest=True)
    print(f"MSI Signal {msi_signal[0].title()} between {msi_signal[1]} and {msi_signal[2]}")
    
    # Run SO
    so_signal = obj_backtesting.show_signals(obj_so.so(df), is_oscillator = True, latest=True)
    print(f"SO Signal {so_signal[0].title()} between {so_signal[1]} and {so_signal[2]}")
    
    # Run ROC
    roc_signal = obj_roc.roc(df)
    last_price_trend = roc_signal.movement.to_list()[-1]
    print(f"ROC Latest Trend: {last_price_trend.title()}")