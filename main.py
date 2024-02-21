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

import matplotlib.pyplot as plt


import getpass
import requests

class AnalyticsApiClient(object):
    # REQUIRED, insert your valid SG Markets token here
    token = 'eyJ0eXAiOiJKV1QiLCJraWQiOiJpcHhUM1gvWUdxZmFmbmRFM3o5clRTM2xqQ2c9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJqYW1lc19iYXJuZXR0QG1hbnVsaWZlYW0uY29tIiwiY3RzIjoiT0FVVEgyX1NUQVRFTEVTU19HUkFOVCIsImF1dGhfbGV2ZWwiOjIwLCJhdWRpdFRyYWNraW5nSWQiOiI3OWMzMWY4Yy0zMzAwLTRkYTEtODFhMS01YmZiNjA4ZmYwMzAtNzMzOTM4MDMiLCJpc3MiOiJodHRwczovL3Nzby5zZ21hcmtldHMuY29tOjQ0My9zZ2Nvbm5lY3Qvb2F1dGgyIiwidG9rZW5OYW1lIjoiYWNjZXNzX3Rva2VuIiwidG9rZW5fdHlwZSI6IkJlYXJlciIsImF1dGhHcmFudElkIjoib0o3Wnp5YXV2cUFDMWFOMUdhaTBhWldzbEdzIiwibm9uY2UiOiIgMXUyc2E2emdlNXlneWVvbXB6OWd0YnJ2dDE3NWpsYTQiLCJjbGllbnRfaWQiOiJjOWRkNTAzYS04NDRhLTQ4ZWEtYWEwNS1iZWY2YmEwOWRkMzYiLCJhdWQiOiJjOWRkNTAzYS04NDRhLTQ4ZWEtYWEwNS1iZWY2YmEwOWRkMzYiLCJuYmYiOjE3MDYwMTIxNTIsImdyYW50X3R5cGUiOiJ0b2tlbiIsInNjb3BlIjpbImFwaS5meC12b2wtYXBpLnYxIiwiYXBpLmFuYWx5dGljcy1lc2ctYm9uZC1zY3JlZW5lci52MSIsImFwaS5zaWduYWxhcGkudjEiLCJhcGkucG9ydGZvbGlvbmF2aWdhdG9yYXBpLnYxIiwibWFpbCIsImFwaS5Qb3J0Zm9saW9OYXZpZ2F0b3JBcGkudjIiLCJvcGVuaWQiLCJwcm9maWxlIiwiYXBpLmZ4ZWFnbGVleWVhcGkudjEiLCJhcGkuZXRmc2NyZWVuZXJhcGkudjEiLCJhcGkuaW5kZXh3YXRjaGFwaS52MSIsInNneEBAb3JpZ2luX25ldHdvcmtAQEludGVybmV0IiwiYXBpLmNvZmJveGFwaS52MSIsImFwaS5hbmFseXRpY3MtY3VydmUtZm9sbG93ZXIudjEiLCJhcGkucmVzZWFyY2hjb250ZW50ZG9tYWluLnYxIiwiYXBpLmFuYWx5dGljc3VzZXJkYXRhLnYxIiwiYXBpLmZ1dHVyZXNyb2xsYm94YXBpLnYxIiwiYXBpLnByaWNlcnVuYXBpLnYxIiwic2d4QEBhdXRoX2xldmVsQEBMMiIsImFwaS5CYXNrZXRTY2FuQXBpLnYyIiwiYXBpLmZ4ZXZlbnR0cmFja2VyYXBpLnYxIiwiYXBpLmFuYWx5dGljc3VwbG9hZGRhdGEudjEiLCJhcGkuYW5hbHl0aWNzYXBpZGF0YS52MSJdLCJhdXRoX3RpbWUiOjE3MDYwMTIxNTEsInJlYWxtIjoiLyIsImV4cCI6MTczNzU0ODE1MiwiaWF0IjoxNzA2MDEyMTUyLCJleHBpcmVzX2luIjozMTUzNjAwMCwianRpIjoiam43V0VhcWhrQXFfWmRMQ0Vsbmg3MzV1MFFBIn0.OJWQs5-3WN2kj8D3m__tfuRw_o17EjRkm7B7sBeUZN6rbSnMt2vkIt_kdCMmIvfArz7EO76CIu8ppZVI-wnznVxMbjeUNVRte00DeBeg3cEF8YQLJfQeCSbnRTsQIw1D6vtuds_JxtyWupPcucuArhtyU5sPrwGtCH4vUc_ohfGOVHTfmmzjYm5j-AdANuMMaw5CX94UQwmonS29eppaUTvd3PeepvpoUsCdyYMVMfj9hGr3Y4N8l89o5dpOPeNKY4kve_mGcwjPXv7JcQbhOYDTMQvSWxd8NMi-LkeWtyN0SUdnlSbKmEus1iit1cFC9FzegqC7sMWcOZh74Fghbw'
    assert(token != '')
    
    try:
        requests.get('https://www.google.com')
        proxies = dict()
    except:
        print('you will need to set the proxy')
        proxy_user = ""  # please provide your proxy username here in string format
        print('Please provide your proxy password, and other proxy settings in the code above')
        proxy_pass = ""
        proxy_address = 'proxy-mkt-p2.int.world.socgen' # please provide your proxy address here in string format - Example is for SG internals
        proxy_port = '8080' # please provide your proxy port here in string format - Example is for SG internals
        
        proxies = {'https': f'http://{proxy_user}:{proxy_pass}@{proxy_address}:{proxy_port}',
                   'http': f'http://{proxy_user}:{proxy_pass}@{proxy_address}:{proxy_port}'}

    headers = {'Authorization': 'Bearer ' + token }

    url = ''

    def __init__(self, api:str, version:int=1):
        self.url = f'https://analytics-api.sgmarkets.com/{api}/v{version}'

    def get(self, endpoint, params={}):
        url = self.url + '/' + endpoint
        r = requests.get(url, headers=self.headers, params=params, proxies=self.proxies)
        if not r.ok:
            raise Exception(f'ERROR in API GET Request: code:{r.status_code} text:{r.text} for url {url}')
        return r.json()
    
client = AnalyticsApiClient('userdata', 1)


def get_equity_factor_data(regions,list_of_factors,return_type,factor_fundamental):
    
    data_out = pd.DataFrame()
    
    if factor_fundamental !='':
        return_type = return_type + ' ' + factor_fundamental

    total_return_index = pd.DataFrame()

    for region in regions:
        equity_factors_value = client.get("quotes",
                                  params={"source": region + " Equity Factors",
                                          "instruments": list_of_factors,
                                          "fields": return_type})

        all_instruments_downloaded = equity_factors_value['source']['instruments']
        all_instruments_to_join = []
        for instrument in all_instruments_downloaded:
            data_instrument = pd.Series({x['date']: x['value'] for x in instrument['fields'][0]['values']})
            data_instrument.index = pd.to_datetime(data_instrument.index)
            data_instrument = data_instrument.sort_index()
            data_instrument.name = instrument['name']
            all_instruments_to_join.append(data_instrument)

        equity_factors_data = pd.concat(all_instruments_to_join,axis=1).astype(np.float64)[list_of_factors]
        number_of_factors   = equity_factors_data.shape[1]
        column_names = [[region]*len(list_of_factors),list_of_factors]
        equity_factors_data.columns = pd.MultiIndex.from_arrays(column_names, names=('Region', 'Factor'))
        data_out = pd.concat([data_out,equity_factors_data],axis=1)
    
    return data_out

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


def style_zero(v, props=""):
        """"""
        return props if abs(v) < 1e-10 else None


color_pallet = ["#2D575B", "#D65258", "#A2D9CE", "#A66B02", "#519BA5", "#938A8A", "#E38A8E", 
                "#BD9C4F", "#7B1D21", "#566573", "#2E86C1", "#D6C292", "#95A5A6", "#C1BCBC", 
                "#B8D8DC", "#D3D3D3", "#FCF3CF"]

def plot_bar_chart(input_bars, ylabel=None, xlabel=None, yaxis_pctformat=False, figsize=(10, 6), rot=90, 
                   grid=True, color=color_pallet, chart_title=None):
    if isinstance(input_bars, pd.Series):
        color_chosen = color[0]
    else:
        color_chosen = color[:input_bars.shape[1]]
    if chart_title is not None:
        ax = input_bars.plot(kind='bar', figsize=figsize, rot=rot, grid=grid, color=color_chosen, title=chart_title)
    else:
        ax = input_bars.plot(kind='bar', figsize=figsize, rot=rot, grid=grid, color=color_chosen)
    ax.grid(True, linestyle='--')
    if yaxis_pctformat:
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0));
    if ylabel is not None:
        ax.set_ylabel(ylabel);
    if xlabel is not None:
        ax.set_xlabel(xlabel);
    plt.show()





regions            = ['EU','US'] # other possible inputs : 'APAC ex JP','China A', 'DM', 'EM', 'EU', 'EU SmallCap', 'JP', 'Russell 2000', 'UK'
list_of_factors    = ['Value','Momentum','Low Risk','Growth'] #any of the 100 equity factors currently in our dataset
return_type        = 'Long' # other possible inputs : 'Long', 'Short', 'Long vs Short', 'Long vs Market'
factor_fundamental = '' # leave empty for performance or spefify a factor fundamental

try:
    data = get_equity_factor_data(regions,list_of_factors,return_type,factor_fundamental)
except:  # Load data from local file instead of API
    data = pd.read_excel(r'Sample Data.xlsx',sheet_name=r'performance data',index_col=0,header=[0,1], 
                         engine="openpyxl").iloc[:,[0,1,2,3,5,6,7,8]]

start = dt.datetime(2022, 12, 30)
end   = dt.datetime(2023, 12, 29)

data = data[(data.index>=start) & (data.index<=end)]
data = data/data.iloc[0]*100

covariance_matrix = data.pct_change().dropna(how='all').cov()


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

# risk_contribution = pd.Series(np.asarray(calculate_risk_contribution(weights_input, covariance_matrix).T)[0],
#                               index=data_input.columns)
# plot_bar_chart(risk_contribution, ylabel="risk contribution")

pct_risk_contribution = pd.Series(np.asarray(calculate_risk_contribution(weights_input, covariance_matrix, 
                                                                         pct_contribution=True).T)[0],
                                  index=data.columns)


# plot_bar_chart(pct_risk_contribution, ylabel="Percentage risk contribution", yaxis_pctformat=True, figsize=(10, 3))


plot_bar_chart(pd.concat([pct_risk_contribution, pd.Series(weights_input, index=data.columns)],
                         axis=1, keys=["% risk contribution", "ERC Weights"]),
               yaxis_pctformat=True, figsize=(7, 3))