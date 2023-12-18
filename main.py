import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import tia.bbg.datamgr as dm
import numpy as np
from math import pi
import matplotlib.pyplot as plt

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

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# There are 9 currency pairs, and we need to "close" the loop, so we use 10.
num_vars = len(sids)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Complete the loop

# Draw the outline of our data.
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angles[:-1]), sids)

# Plot each currency pair's volatility percentiles
for sid in sids:
    df = volatility_data[sid]

    # Calculate the percentile rank of the 3m and 1y volatilities.
    df['percentile_3m'] = df[df.columns[0]].rank(pct=True) * 100
    df['percentile_1y'] = df[df.columns[1]].rank(pct=True) * 100

    # Fetch the last percentile ranks for the plot
    values = df.iloc[-1][['percentile_3m', 'percentile_1y']].tolist()
    values += values[:1]  # Complete the loop

    # Plot data and fill with color
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=sid)
    ax.fill(angles, values, alpha=0.25)

# Add a legend and title for the chart
ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.title('FX Volatility Percentile Ranks')

# Show the plot
plt.show()


''''Traceback (most recent call last):
  File ".\main.py", line 62, in <module>
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=sid)
  File "C:\Users\barnjam\Anaconda3\lib\site-packages\matplotlib\axes\_axes.py", line 1688, in plot
    lines = [*self._get_lines(*args, data=data, **kwargs)]
  File "C:\Users\barnjam\Anaconda3\lib\site-packages\matplotlib\axes\_base.py", line 311, in __call__  
    yield from self._plot_args(
  File "C:\Users\barnjam\Anaconda3\lib\site-packages\matplotlib\axes\_base.py", line 504, in _plot_args
    raise ValueError(f"x and y must have same first dimension, but "
ValueError: x and y must have same first dimension, but have shapes (10,) and (3,) '''