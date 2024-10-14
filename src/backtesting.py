"""This is a python script for the backtesting class."""
import pandas as pd
from .strategy import *

class Backtesting:
    def __init__(self, fund: float = 10_000) -> None:
        self.fund = fund
                
    def test(self, df: pd.DataFrame = None) -> float:

        n_stocks = 0
        curr_fund = self.fund
        stock_in_hand = False
        
        for _, row in df.iterrows():
            price, signal = row.get('price'), row.get('signal')
            if not stock_in_hand and signal == 1:
                stock_in_hand = True
                n_stocks = curr_fund // price
                curr_fund -= n_stocks * price
            if stock_in_hand and signal == -1:
                stock_in_hand = False
                curr_fund += n_stocks * price
                n_stocks = 0
                
        if stock_in_hand:
            curr_fund += n_stocks * price
        
        return round(curr_fund, 2)
            
    def _apply_strategy(self, strategy: str = 'sma', df: pd.DataFrame = None, window: list = [3, 4]) -> pd.DataFrame:
        
        short_window, long_window = window

        if strategy == 'sma':
            return SimpleMovingAverage(short_window, long_window).sma(df)
        if strategy == 'ema':
            return ExponentialMovingAverage(short_window, long_window).ema(df) 
        else:
            raise ValueError(f"Strategy {strategy} not supported.")
   
    def test_strategy(self, strategy: str = 'sma', df: pd.DataFrame = None, windows: list = [(3, 5), (5, 10)], verbose: int = 1) -> dict:
        
        best_window = None
        prev_final = None
        for window in windows:
            short_window, long_window = window
            tmp_df = self._apply_strategy(strategy, df, window)
            final_fund = self.test(tmp_df)
            
            if verbose:
                print(f"Short ({short_window} Days), Long ({long_window} Days)\nFinal Fund: ${final_fund}", end='\n\n')
            
            if best_window is None:
                best_window = window
                prev_final = final_fund
            else:
                if final_fund > prev_final:
                    prev_final = final_fund
                    best_window = window
            
        return {
            "best": best_window,
            "fund": prev_final
        }