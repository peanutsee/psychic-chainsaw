import pandas as pd
from typing import Callable, List, Dict, Tuple

class Backtesting:
    """Class for performing backtesting on trading strategies.

    Attributes
    ----------
    fund : float
        The initial amount of capital available for trading (default is $10,000).

    Methods
    -------
    test(df: pd.DataFrame) -> float:
        Simulates the trading strategy based on the provided DataFrame and returns the final fund amount.
    test_strategy(strategy_func: Callable, df: pd.DataFrame, windows: List[Tuple[int, int]], verbose: int) -> Dict[str, object]:
        Tests multiple trading strategy parameters and returns the best-performing one.
    show_signals(df: pd.DataFrame, latest: bool, is_oscillator: bool) -> List[Tuple[str, str]] or Tuple[str, str, str]:
        Displays trading signals based on the provided DataFrame.
    """
    
    def __init__(self, fund: float = 10_000) -> None:
        """Initializes the Backtesting object with the given fund amount.

        Parameters
        ----------
        fund : float
            The initial amount of capital available for trading (default is 10,000).
        """
        self.fund = fund
                
    def test(self, df: pd.DataFrame = None) -> float:
        """Simulates the trading strategy based on the provided DataFrame.

        The method assumes a simple buy/sell strategy based on signals provided in the DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            A DataFrame containing stock data with columns 'adjclose' and 'signal'. 
            The 'signal' column should have values of 1 (buy) and -1 (sell).

        Returns
        -------
        float
            The final fund amount after executing the buy/sell signals.
        """
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
   
    def test_strategy(self, strategy_func: Callable, df: pd.DataFrame, windows: List[Tuple[int, int]] = [(3, 5), (5, 10)], verbose: int = 1) -> Dict[str, object]:
        """Tests multiple trading strategy parameters and returns the best-performing one.

        The method evaluates different short and long window parameters for the strategy 
        function and returns the one that results in the highest final fund amount.

        Parameters
        ----------
        strategy_func : Callable
            A function that implements the trading strategy and takes the DataFrame and window parameters.
        df : pd.DataFrame
            A DataFrame containing stock data needed for strategy execution.
        windows : List[Tuple[int, int]]
            A list of tuples representing different (short_window, long_window) combinations to test (default is [(3, 5), (5, 10)]).
        verbose : int
            If set to 1, the method will print details of each test (default is 1).

        Returns
        -------
        Dict[str, object]
            A dictionary containing the best window parameters, the final fund amount, 
            and the DataFrame resulting from the best strategy.
        """
        
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
    
    def show_signals(self, df: pd.DataFrame, latest: bool = False, is_oscillator: bool = False) -> List[Tuple[str, str]] or Tuple[str, str, str]:
        """Displays trading signals based on the provided DataFrame.

        Depending on the flags, the method can return either a list of signals or
        the most recent signal.

        Parameters
        ----------
        df : pd.DataFrame
            A DataFrame containing stock data with a 'signal' column for buy/sell signals 
            and optional 'overbought'/'oversold' indicators for oscillator signals.
        latest : bool
            If True, returns only the most recent signal (default is False).
        is_oscillator : bool
            If True, indicates that the method should look for oscillator signals 
            (default is False).

        Returns
        -------
        List[Tuple[str, str]] or Tuple[str, str, str]
            If `is_oscillator` is False, returns a list of signals in the format 
            [(signal, date), ...] or the most recent signal as a tuple (signal, start_date, end_date) 
            if `latest` is True. If `is_oscillator` is True, returns a list of oscillator signals.
        """
        if not is_oscillator:
            lst_signal_date = []
            for _, row in df[(df.signal == -1) | (df.signal == 1)].sort_values(by='date').iterrows():
                signal, date = row.get("signal"), row.get('date')
                lst_signal_date.append((signal, date))
                
            if latest:
                date = date.strftime("%d/%m/%Y") 
                return f"Buy Signal on {date}" if lst_signal_date[-1][0] == 1 else f"Sell Signal on {date}"
            else:
                return lst_signal_date
        else:
            tmp_lst_signals = []
            
            # Gather signals
            for _, row in df.iterrows():
                if row.get("overbought"):
                    tmp_lst_signals.append(("overbought", row.get('date')))
                if row.get("oversold"):
                    tmp_lst_signals.append(("oversold", row.get('date')))

            lst_signals = []
            i = 0

            # Loop through the signals list
            while i < len(tmp_lst_signals):
                signal = tmp_lst_signals[i]
                current_flag = signal[0]
                start_date = signal[1].strftime("%d/%m/%Y") 
                
                # Look ahead for the next signal with a different flag
                i += 1
                while i < len(tmp_lst_signals) and tmp_lst_signals[i][0] == current_flag:
                    i += 1
                
                # If there is a valid next signal with a different flag
                if i < len(tmp_lst_signals):
                    end_date = tmp_lst_signals[i][1].strftime("%d/%m/%Y") 
                    lst_signals.append((current_flag, start_date, end_date))
                
            if latest:
                return lst_signals[-1] if lst_signals else ["NO DATA", 'NO DATA', 'NO DATA']
            else:
                return lst_signals
