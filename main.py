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


f_sids ={"EURUSD":"EUR12M Curncy", "USDNOK": "NOK12M Curncy", "GBPUSD": "GBP12M Curncy", "USDCAD": "CAD12M Curncy", "USDJPY": "JPY12M Curncy",
       "USDSEK": "SEK12M Curncy", "AUDUSD":"AUD12M Curncy", "USDCHF": "CHF12M Curncy", "NZDUSD":"NZD12M Curncy" } 

df = pd.DataFrame()
for ccy, fwd in f_sids.items():
    spot = mgr[ccy + ' Curncy'].get_historical('PX_LAST', start_date, end_date)
    fwd = mgr[fwd].get_historical('PX_LAST', start_date, end_date)
    carry = ((fwd - spot) / spot) * 100 * -1
    df[ccy] = carry
    # df[ccy + '_spot'] = spot
    # df[ccy + '_fwd'] = fwd
df.plot()
plt.ylabel("fwd_implied_carry (%)")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()




'''