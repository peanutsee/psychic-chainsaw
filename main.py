from src.backtesting import *
import pandas as pd
from yahoo_fin.stock_info import get_data
import yaml

with open("./config/config.yaml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

if __name__ == "__main__":
    starting_fund = config.get("FUND")
    ticker = config.get("TICKER")
    start_date = config.get("START_DATE")
    end_date = config.get("END_DATE")
    interval = config.get("INTERVAL")
    strategies = config.get("STRATEGIES")
    
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