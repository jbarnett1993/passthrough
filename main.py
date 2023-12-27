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
                         EURUSD    USDNOK    GBPUSD    USDCAD    USDJPY    USDSEK    AUDUSD    USDCHF    NZDUSD
date
2022-12-27 -2.024537  1.694767 -0.586566  0.506631  4.957675  1.743019 -1.175178  3.605634  0.117666
2022-12-28 -2.021074  1.699083 -0.562604  0.456495  4.937025  1.720558 -1.044533  3.558242  0.206842
2022-12-29 -2.026961  1.705234 -0.580495  0.419724  5.005638  1.706141 -1.006046  3.613200  0.252479
2022-12-30 -2.024101  1.721261 -0.593230  0.442674  5.059487  1.715524 -1.062234  3.630827  0.210394
2023-01-02 -2.042960  1.730158 -0.596663  0.496316  5.078599  1.740541 -1.060446  3.631090  0.201678
...              ...       ...       ...       ...       ...       ...       ...       ...       ...
2023-12-21 -1.602039  0.617691 -0.094283  0.407828  5.001757  1.393533 -0.594543  3.447914  0.214274
2023-12-22 -1.594788  0.606950 -0.076608  0.339488  4.973036  1.387867 -0.561994  3.429173  0.246665
2023-12-25 -1.600963  0.605693 -0.074833  0.371276  4.975904  1.389688 -0.565946  3.414876  0.246469
2023-12-26 -1.659266  0.630216 -0.136224  0.392673  5.032709  1.420219 -0.615204  3.464102  0.188954
2023-12-27 -1.643864  0.629124 -0.131399  0.383741  5.008488  1.389600 -0.606464  3.424015  0.192855




'''