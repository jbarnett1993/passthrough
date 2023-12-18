import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tia.bbg.datamgr as dm

mgr = dm.BbgDataManager()

# Define the date range for the past year
start_date = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# List of currency pairs
sids = ["EURUSD", "USDNOK", "GBPUSD", "USDCAD", "USDJPY", "USDSEK", "AUDUSD", "USDCHF", "NZDUSD"]
volatility_data = {}

for sid in sids:
    # Construct the Bloomberg tickers for 3-month and 1-year volatility
    q_ticker = sid + "V3M Curncy"
    y_ticker = sid + "V1Y Curncy"
    
    # Fetch the historical data for 3-month and 1-year volatility
    try:
        df_3m = mgr[q_ticker].get_historical('PX_LAST', start_date, end_date)
        df_1y = mgr[y_ticker].get_historical('PX_LAST', start_date, end_date)
        
        # Join the two DataFrames on their index (date)
        df_combined = df_3m.join(df_1y, lsuffix='_3m', rsuffix='_1y')
        
        # Store the combined dataframe in the dictionary with key as SID
        volatility_data[sid] = df_combined
    except Exception as e:
        print(f"An error occurred while fetching data for {sid}: {e}")

# Now volatility_data contains the combined dataframes for each SID with both 3-month and 1-year volatilities