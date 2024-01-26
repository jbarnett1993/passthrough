from __future__ import division
import numpy as np
import pandas as pd
import datetime as dt 
import cvxpy as cp
from datetime import datetime
from scipy.optimize import minimize
from dateutil.relativedelta import relativedelta
import tia.bbg.datamgr as dm
from dateutil.relativedelta import relativedelta
import numpy as np
from numpy.linalg import inv,pinv
from scipy.optimize import minimize

# read the excel file and get the positions and long/short indicators
df = pd.read_excel('fund_positions.xlsx', sheet_name='Sheet1')
# print(df)
positions = df['Positions']
long_short = df['long/short']

print(df)
# get historical prices and returns
mgr = dm.BbgDataManager()
sids = mgr[positions]
mgr.sid_result_mode = 'frame'
start_date = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
df = sids.get_historical(['PX_OPEN'], start_date, end_date)
df_returns = df.pct_change()
for i in range(len(long_short)):
    if long_short[i] == 'short':
        df_returns.iloc[:,i] = -1*df_returns.iloc[:,i]
df_returns.reset_index()
df_returns.columns = positions


start = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end   = datetime.today().strftime('%Y-%m-%d')
covariance_matrix = df_returns.dropna(how='all').cov()

def portfolio_annualized_sharpe(weights, returns):

    portfolio_returns = np.dot(returns, weights)
    portfolio_total_return = np.prod(1 + portfolio_returns) - 1
    nb_years = (returns.index[-1] - returns.index[0]).days / 365
    portfolio_std_dev = np.std(portfolio_returns)
    annual_r = (portfolio_total_return + 1) ** (1 / nb_years) - 1
    annual_std = portfolio_std_dev * np.sqrt(252)

    if annual_std == 0:
        return np.nan
    return annual_r / annual_std




# Optimization constraints and bounds
constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]  # Sum of weights must be 1
bounds = [(-0.20, 0.20) for _ in range(len(positions))]  # Long/short constraints

# Objective function (to be minimized)
def objective_function(weights):
    return portfolio_annualized_sharpe(weights, df_returns)

# Initial guess for weights
initial_weights = np.array([1. / len(positions)] * len(positions))

# Optimization
optimal_weights = minimize(objective_function, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)

# Display optimized weights
optimized_weights = pd.Series(optimal_weights.x, index=positions)
print(optimized_weights)