"""This is a python script for the backtesting class."""
import pandas as pd

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
            
    # def test_strategy(self, df: pd.DataFrame = None, strategies: list = [(3, 5), (5, 10)], verbose: int = 1) -> dict:
        
    #     best_strategy = None
    #     prev_final = None
    #     for strategy in strategies:
    #         short_window, long_window = strategy
    #         final_fund = backtesting(df)
            
    #         if verbose:
    #             print(f"Short ({short_window} Days), Long ({long_window} Days)\nFinal Fund: ${final_fund}", end='\n\n')
            
    #         if best_strategy is None:
    #             best_strategy = strategy
    #             prev_final = final_fund
    #         else:
    #             if final_fund > prev_final:
    #                 prev_final = final_fund
    #                 best_strategy = strategy
            
    #     return {
    #         "best": best_strategy,
    #         "fund": prev_final
    #     }