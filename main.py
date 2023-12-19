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
start_date = (datetime.today() - relativedelta(years=3)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

# List of currency pairs
sids = ["EURUSD", "USDNOK", "GBPUSD", "USDCAD", "USDJPY", "USDSEK", "AUDUSD", "USDCHF", "NZDUSD"]

f_sids ={"EURUSD":"EUR12M Curncy", "USDNOK": "NOK12M Curncy", "GBPUSD": "GBP12M Curncy", "USDCAD": "CAD12M Curncy", "USDJPY": "JPY12M Curncy",
       "USDSEK": "SEK12M Curncy", "AUDUSD":"AUD12M Curncy", "USDCHF": "CHF12M Curncy", "NZDUSD":"NZD12M Curncy" } 


fwd_prices = [] 
for ccy, fwd in f_sids.items():
    fwd = mgr[fwd].PX_LAST
    fwd_prices.append(fwd)



print(fwd_prices)
'''
            spot         fwd  implied vol     carry
EURUSD    1.0977    1.115750        6.305 -1.644347
USDNOK   10.2666   10.196700       11.695  0.680849
GBPUSD    1.2754    1.276243        6.920 -0.066097
USDCAD    1.3335    1.327602        5.500  0.442295
USDJPY  143.6800  136.355000        9.645  5.098135
USDSEK   10.1588   10.009900       10.715  1.465724
AUDUSD    0.6767    0.681119        9.360 -0.653022
USDCHF    0.8605    0.829733        6.545  3.575479
NZDUSD    0.6272    0.625943        9.555  0.200415


'''