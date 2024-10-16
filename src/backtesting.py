"""This is a python script for the backtesting class."""
import pandas as pd
from .strategy import *
from typing import Callable

class Backtesting:
    def __init__(self, fund: float = 10_000) -> None:
        self.fund = fund
                
    def test(self, df: pd.DataFrame = None) -> float:

        n_stocks = 0
        curr_fund = self.fund
        stock_in_hand = False
        
        for _, row in df.iterrows():
            price, signal = row.get('adjclose'), row.get('signal')
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
   
    def test_strategy(self, strategy_func: Callable = None, df: pd.DataFrame = None, windows: list = [(3, 5), (5, 10)], verbose: int = 1) -> dict:
        
        best_window = None
        prev_final = None
        best_df = None
        
        for window in windows:
            short_window, long_window = window
            tmp_df = strategy_func(df, short_window, long_window)
            final_fund = self.test(tmp_df)
            
            if verbose:
                print(f"Short ({short_window} Days), Long ({long_window} Days)\nFinal Fund: ${final_fund}", end='\n\n')
            
            if best_window is None:
                best_window = window
                prev_final = final_fund
                best_df = tmp_df
            else:
                if final_fund > prev_final:
                    prev_final = final_fund
                    best_window = window
                    best_df = tmp_df
            
        return {
            "best": best_window,
            "fund": prev_final,
            "best_df": best_df
        }
    
    def show_signals(self, df: pd.DataFrame, latest: bool = False) -> type[list, tuple]:
        lst_signal_date = []

        for _, row in df[(df.signal == -1) | (df.signal == 1)].sort_values(by='date').iterrows():
            signal, date = row.get("signal"), row.get('date')
            lst_signal_date.append((signal, date))
            
        if latest:
            date = date.strftime("%d/%m/%Y") 
            return f"Buy Signal on {date}" if lst_signal_date[-1][0] == 1 else f"Sell Signal on {date}"
        else:
            return lst_signal_date