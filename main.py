from __future__ import division
import pandas as pd
import tia.bbg.datamgr as dm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sklearn.preprocessing import normalize
import numpy as np
from matplotlib import pyplot as plt
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
df_returns.dropna(inplace = True)

df_logreturns = np.log(1 + df_returns)


df_logreturns.dropna(inplace=True)

# normalize data
df_logreturns_norm = normalize(df_logreturns)
initial_norm_returns = pd.DataFrame(df_logreturns_norm)

# calculate covariance matrix
V = np.cov(df_logreturns_norm.T)
# V2 = np.cov(df_returns.T)


df_std = np.std(df_logreturns_norm)

# define optimization constraints
def total_weight_constraint(x):
    return np.sum(x) - 1.0

# set bounds on weights
lb = np.zeros_like(positions)
ub = np.ones_like(positions)

cons = ({'type': 'eq', 'fun': total_weight_constraint})

# risk budgeting optimization
def calculate_portfolio_var(w, V):
    # function that calculates portfolio risk
    w = np.matrix(w)
    return (w * V * w.T)[0, 0]

def calculate_risk_contribution(w, V):
    # function that calculates asset contribution to total risk
    w = np.matrix(w)
    sigma = np.sqrt(calculate_portfolio_var(w, V))
    # Marginal Risk Contribution
    MRC = V * w.T
    # Risk Contribution
    RC = np.multiply(MRC, w.T) / sigma
    return RC

def risk_budget_objective(x, pars):
    # calculate portfolio risk
    V = pars[0]
    x_t = pars[1] 
    sig_p = np.sqrt(calculate_portfolio_var(x, V)) 
    risk_target = np.asmatrix(np.multiply(sig_p, x_t))
    asset_RC = calculate_risk_contribution(x, V)
    J = sum(np.square(asset_RC - risk_target.T))[0, 0]
    return J

# initial guess of weights
w0 = np.ones(len(positions)) / len(positions)
# w0 = np.array([0.204, -0.490, 0.348, 0.295, 0.340])


# run optimization to get risk budget weights
res = minimize(risk_budget_objective, w0, args=[V, w0], method='SLSQP', bounds=list(zip(lb, ub)), constraints=cons, options={'disp': False})
w_rb = np.asmatrix(res.x)



# print optimized weights
df_weights = pd.DataFrame(np.reshape(w_rb, (1, -1)), index=['Weight'], columns=positions)

print(w_rb)
print(df_weights)

# manual_weights = np.array([0.204, 0.490, 0.348,0.295,0.340])
optimised_risk_contributions = calculate_risk_contribution(w_rb, V)
df_optimised_risk_contributions = pd.DataFrame(optimised_risk_contributions, index=positions, columns=['Risk Contribution'])
print(df_optimised_risk_contributions)


weighted_returns = pd.DataFrame(df_returns*df_weights.values)

weighted_returns['port_returns'] = weighted_returns.sum(axis=1)

portfolio_returns = weighted_returns['port_returns']

df_port_std = np.std(portfolio_returns)

portfolio_volatility = df_port_std * (252**0.5)

target_volatility = 0.10
scaling_factor = target_volatility/portfolio_volatility

scaled_weights = df_weights * scaling_factor

print(scaled_weights)
