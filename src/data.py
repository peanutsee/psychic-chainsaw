"""This is a python script for the data class."""
import pandas as pd
from yahoo_fin.stock_info import get_data

class TickerData:
    def __init__(self, ticker: str = None, start_date: str = None, end_date: str = None, interval: str = '1d') -> None:
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
    
    def get_data(self) -> pd.DataFrame:
        df = get_data(self.ticker, 
                  start_date=self.start_date, 
                  end_date=self.end_date, 
                  index_as_date = False, 
                  interval=self.interval)
    
        df['date'] = pd.to_datetime(df['date'])
        df.drop(columns='ticker', inplace=True)
        return df