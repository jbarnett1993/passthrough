from __future__ import division
import pandas as pd
import tia.bbg.datamgr as dm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import riskparityportfolio as rp

# Read the excel file and get the positions and long/short indicators
df = pd.read_excel('fund_positions.xlsx', sheet_name='Sheet1')
positions = df['Positions']
long_short = df['long/short']

# Get historical prices and returns
mgr = dm.BbgDataManager()
sids = mgr[positions]
mgr.sid_result_mode = 'frame'
start_date = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
df = sids.get_historical(['PX_OPEN'], start_date, end_date)
df_returns = df.pct_change()
for i in range(len(long_short)):
    if long_short[i] == 'short':
        df_returns.iloc[:, i] = -1 * df_returns.iloc[:, i]
df_returns.reset_index()
df_returns.columns = positions

# Normalize data and calculate covariance matrix
df_logreturns = np.log(1 + df_returns)
df_logreturns.dropna(inplace=True)
df_logreturns_norm = df_logreturns - np.mean(df_logreturns, axis=0)
V = np.cov(df_logreturns_norm.T)

# Define your budgeting vector (equal weights in this example)
b = np.array([1/len(positions)] * len(positions))

# Designing the risk parity portfolio
w_rb = rp.vanilla.design(V, b)

# Calculate risk contributions
rc = w_rb @ (V * w_rb)
rc /= np.sum(rc)

# Output the optimized weights and risk contributions
df_weights = pd.DataFrame(w_rb, index=positions, columns=['Weight'])
df_risk_contributions = pd.DataFrame(rc, index=positions, columns=['Risk Contribution'])

print(df_weights)
print(df_risk_contributions)