# import pandas as pd
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# import tia.bbg.datamgr as dm
# import numpy as np
# from math import pi
# import matplotlib.pyplot as plt
# from scipy.stats import percentileofscore

# mgr = dm.BbgDataManager()

# # Define the date range for the past year
# start_date = (datetime.today() - relativedelta(years=3)).strftime('%Y-%m-%d')
# end_date = datetime.today().strftime('%Y-%m-%d')

# # List of currency pairs
# sids = ["EURUSD Curncy", "USDNOK Curncy", "GBPUSD Curncy", "USDCAD Curncy", "USDJPY Curncy", "USDSEK Curncy", "AUDUSD Curncy", "USDCHF Curncy", "NZDUSD Curncy"]

# f_sids ={"EURUSD":"EUR12M Curncy", "USDNOK": "NOK12M Curncy", "GBPUSD": "GBP12M Curncy", "USDCAD": "CAD12M Curncy", "USDJPY": "JPY12M Curncy",
#        "USDSEK": "SEK12M Curncy", "AUDUSD":"AUD12M Curncy", "USDCHF": "CHF12M Curncy", "NZDUSD":"NZD12M Curncy" } 


# fwd_prices = pd.DataFrame()
# for ccy, fwd in f_sids.items():
#     spot = mgr[ccy +' Curncy'].PX_LAST
#     fwd = mgr[fwd].PX_LAST
#     fwd_prices.at['spot',ccy] = spot
#     fwd_prices.at['fwd',ccy] = fwd
#     fwd_prices.at['implied vol', ccy] = mgr[ccy + 'V3M Curncy'].PX_LAST

# fwd_prices = fwd_prices.T

# fwd_prices['fx_fwd_implied_carry'] = ((fwd_prices['fwd'] - fwd_prices['spot']) / fwd_prices["spot"]) * 100 *-1

# fwd_prices.to_csv("df.csv")
# print(fwd_prices)
# # df = pd.read_csv("df.csv")
# # print(df.index.values())


'''
            spot         fwd  implied vol  fx_fwd_implied_carry
ccy
EURUSD    1.1054    1.123550        6.610             -1.641940
USDNOK   10.1669   10.105200       12.105              0.606871
GBPUSD    1.2716    1.273250        7.300             -0.129758
USDCAD    1.3200    1.314959        5.730              0.381894
USDJPY  142.5800  135.438900       10.315              5.008486
USDSEK    9.9881    9.849184       11.095              1.390815
AUDUSD    0.6832    0.687340        9.610             -0.605972
USDCHF    0.8528    0.823542        7.100              3.430816
NZDUSD    0.6323    0.631087        9.705              0.191839





'''