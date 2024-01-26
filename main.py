from __future__ import division
import numpy as np
import pandas as pd
import getpass
import requests
import json
import os
import datetime as dt 
import cvxpy as cp
import xpress
from datetime import datetime
from matplotlib.dates import DateFormatter
from matplotlib.ticker import PercentFormatter
from matplotlib.gridspec import GridSpec
from scipy.optimize import minimize
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import tia.bbg.datamgr as dm
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


start = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end   = datetime.today().strftime('%Y-%m-%d')

covariance_matrix = df_returns.dropna(how='all').cov()





def calculate_min_var_weight(asset_covariance):
    n = asset_covariance.shape[0]
    w = cp.Variable(n)
    w_constraints = [cp.sum(w) == 1, w >= 0]
    
    risk = cp.quad_form(w, asset_covariance)
    problem = cp.Problem(cp.Minimize(risk), w_constraints)
    problem.solve()
    return pd.Series(w.value, index=asset_covariance.columns)



def calculate_portfolio_var(weights, covar_matrix):
    # function that calculates portfolio risk
    weights = np.matrix(weights)
    return np.dot(weights, np.dot(covar_matrix, weights.T))[0, 0]



def calculate_risk_contribution(weights, covar_matrix, pct_contribution=False):
    # function that calculates asset contribution to total risk
    weights = np.matrix(weights)
    var = calculate_portfolio_var(weights, covar_matrix)
    # Marginal Risk Contribution
    MRC = np.dot(covar_matrix, weights.T)
    # Risk Contribution
    if pct_contribution:
        RC = np.multiply(MRC, weights.T) / var
    else:
        RC = np.multiply(MRC, weights.T) / np.sqrt(var)
    return RC



def risk_budget_objective(x, covar_matrix, risk_budget):
    risk_target = np.asmatrix(risk_budget)
    asset_RC = calculate_risk_contribution(x, covar_matrix, pct_contribution=True)
    J = sum(np.square(asset_RC - risk_target.T))[0, 0]  # sum of squared error
    return J

def equal_risk_contribution_weights(covar_matrix, risk_budget_=None):
    initial_weights = np.asarray([1 / covar_matrix.shape[1]] * covar_matrix.shape[1])
    if risk_budget_ is None:
        # equal risk budget for all
        risk_budget_ = np.asarray([1 / covar_matrix.shape[1]] * covar_matrix.shape[1])

    # CONSTRAINTS
    # sum of weights = 1
    constr = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
    # Lower and upper bound of each strategy weight is equal to 0 and 1 respectively
    lower_bound = np.asarray([0.] * covar_matrix.shape[1])
    upper_bound = np.asarray([1.] * covar_matrix.shape[1])
    bounds = list(zip(lower_bound, upper_bound))

    res = minimize(risk_budget_objective, initial_weights, args=(covar_matrix, risk_budget_, ), constraints=constr,
                   bounds=bounds, options={'ftol': 1e-15, 'maxiter': 100000},
                   method='SLSQP')
    
    return pd.Series(res.x, index=covar_matrix.columns)


weights_input = equal_risk_contribution_weights(covariance_matrix)
print(weights_input)

pct_risk_contribution = pd.Series(np.asarray(calculate_risk_contribution(weights_input, covariance_matrix, 
                                                                         pct_contribution=True).T)[0],
                                  index=df.columns)

