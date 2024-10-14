from src.backtesting import *
from src.strategy import *
import pandas as pd
from yahoo_fin.stock_info import get_data

if __name__ == "__main__":
    starting_fund = 100_000
    ticker = 'D05.SI'
    start_date = '01/01/2024'
    end_date = '10/14/24'
    interval = '1d'
    
    # Get data
    df = get_data(ticker, 
                  start_date=start_date, 
                  end_date=end_date, 
                  index_as_date = False, 
                  interval=interval)
    
    df['date'] = pd.to_datetime(df['date'])
    df.drop(columns='ticker', inplace=True)
    
    # Initialize objects
    obj_backtesting = Backtesting(starting_fund)
    obj_sma = SimpleMovingAverage(3, 50)
    obj_ema = ExponentialMovingAverage(3, 50)
    
    # Run sma
    df_sma = obj_sma.sma(df)
    
    # Run ema
    df_ema = obj_ema.ema(df)
    
    # Run backtest
    final_fund_sma = obj_backtesting.test(df_sma)
    final_fund_ema = obj_backtesting.test(df_ema)
    
    print(f"SMA: S${final_fund_sma}\nEMA: S${final_fund_ema}")
