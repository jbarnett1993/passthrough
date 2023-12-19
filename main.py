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
import matplotlib.pyplot as plt
from math import pi

# Assume 'percentiles_df' is your pre-existing DataFrame with the correct data

# Number of variables we're plotting.
categories = list(percentiles_df.index)
N = len(categories)

# What will be the angle of each axis in the plot? (divide the plot / number of variables)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]  # ensure the graph is circular by repeating the first value at the end

# Initialise the radar plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Draw one axis per variable and add labels
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([10, 20, 30, 40, 50], ["10", "20", "30", "40", "50"], color="grey", size=7)
plt.ylim(0, 50)

# Plot each percentile
for column in percentiles_df.columns:
    values = percentiles_df[column].tolist()
    values += values[:1]  # repeat the first value to close the circular graph
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=column)
    ax.fill(angles, values, alpha=0.1)

# Add a legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

plt.show()
