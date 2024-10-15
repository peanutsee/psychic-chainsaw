from src.backtesting import *
import pandas as pd
from yahoo_fin.stock_info import get_data
import yaml

with open("./config/config.yaml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if __name__ == "__main__":
    starting_fund = 100_000
    ticker = config.get("TICKER")
    start_date = '01/01/2024'
    end_date = '10/14/24'
    interval = '1d'
    strategies = [
        (3, 5), (3, 10), (3, 20), (3, 50),
        (5, 10), (5, 20), (5, 50), (5, 100),
        (10, 20), (10, 50)
    ]
    
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
    
    # Run sma
    dct_sma = obj_backtesting.test_strategy('sma', df, strategies, 0)
    
    # Run ema
    dct_ema = obj_backtesting.test_strategy('ema', df, strategies, 0)

     # Show Best Strategy
    print(f"SMA: S${dct_sma.get("fund")} {dct_sma.get('best')}\nEMA: S${dct_ema.get("fund")} {dct_ema.get("best")}")
    
    # Show Signal
    print(obj_backtesting.show_signals(dct_ema.get('best_df'), True))
     
    # Run macd
    macd = MovingAverageConvergenceDivergence()
    df_macd = macd.macd(df)
    fund_macd = obj_backtesting.test(df_macd)
    print(f"MACD: S${fund_macd}")
    
   
