import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tia.bbg.datamgr as dm
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore

mgr = dm.BbgDataManager()

# Define the date range for the past year
start_date = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# List of currency pairs
sids = ["EURUSD", "USDNOK", "GBPUSD", "USDCAD", "USDJPY", "USDSEK", "AUDUSD", "USDCHF", "NZDUSD"]
percentiles = {'percentile_3m': {}, 'percentile_1y': {}}
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

        # Calculate the percentile for the most recent 3m and 1y volatility values
        last_3m_vol = df_combined.iloc[-1]['PX_LAST_3m']
        last_1y_vol = df_combined.iloc[-1]['PX_LAST_1y']
        percentile_3m = percentileofscore(df_combined['PX_LAST_3m'], last_3m_vol)
        percentile_1y = percentileofscore(df_combined['PX_LAST_1y'], last_1y_vol)
        percentiles['percentile_3m'][sid] = percentile_3m
        percentiles['percentile_1y'][sid] = percentile_1y


    except Exception as e:
        print(f"An error occurred while fetching data for {sid}: {e}")
percentile_df = pd.DataFrame(percentiles)
print(percentile_df)

'''
        percentile_3m  percentile_1y
EURUSD       7.442748      17.175573
USDNOK       8.396947      14.122137
GBPUSD       1.526718       6.106870
USDCAD       3.435115       1.908397
USDJPY      42.175573      45.419847
USDSEK      21.755725      27.862595
AUDUSD       6.106870      11.259542
USDCHF       5.725191      11.259542
NZDUSD      12.595420      12.977099




'''