"""This is a python script for the data class."""
import pandas as pd
from yahoo_fin.stock_info import get_data

class TickerData:
    """Class for retrieving historical stock data for a given ticker.

    Attributes
    ----------
    ticker : str
        The stock ticker symbol for the desired stock (e.g., 'AAPL', 'GOOGL').
    start_date : str
        The start date for the historical data retrieval in 'YYYY-MM-DD' format.
    end_date : str
        The end date for the historical data retrieval in 'YYYY-MM-DD' format.
    interval : str
        The frequency of the data retrieval (default is '1d'). 
        Options include '1d', '1wk', '1mo', etc.

    Methods
    -------
    get_data():
        Retrieves historical stock data for the specified ticker within the date range 
        and returns it as a pandas DataFrame.
    """
    
    def __init__(self, ticker: str = None, start_date: str = None, end_date: str = None, interval: str = '1d') -> None:
        """Initializes the TickerData object with ticker symbol, date range, and interval.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol for the desired stock (default is None).
        start_date : str
            The start date for the historical data retrieval in 'YYYY-MM-DD' format (default is None).
        end_date : str
            The end date for the historical data retrieval in 'YYYY-MM-DD' format (default is None).
        interval : str
            The frequency of the data retrieval (default is '1d'). 
            Options include '1d', '1wk', '1mo', etc.
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
    
    def get_data(self) -> pd.DataFrame:
        """Retrieves historical stock data for the specified ticker.

        Uses the Yahoo Finance API to fetch the stock data and processes it into a 
        pandas DataFrame with a datetime index.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing historical stock data including date, open, high, 
            low, close, volume, and adjusted close prices. The 'date' column is 
            converted to datetime format.
        """
        df = get_data(self.ticker, 
                      start_date=self.start_date, 
                      end_date=self.end_date, 
                      index_as_date=False, 
                      interval=self.interval)

        df['date'] = pd.to_datetime(df['date'])
        df.drop(columns='ticker', inplace=True)
        return df
