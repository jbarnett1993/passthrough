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
       "USDSEK": "SEK12M Curncy", "AUDUSD":"AUD12M Curncy", "USDCHF": "CHF12M Curncy", "NZDUSD":"NZD12M Curncy",}#"USDBRL":"BCN12M Curncy","USDMXN":"MXN12M Curncy" } 

df = pd.DataFrame()
for ccy, fwd in f_sids.items():
    spot = mgr[ccy + ' Curncy'].get_historical('PX_LAST', start_date, end_date)
    fwd = mgr[fwd].get_historical('PX_LAST', start_date, end_date)
    carry = ((fwd - spot) / spot) * 100 * -1
    df[ccy] = carry
    # df[ccy + '_spot'] = spot
    # df[ccy + '_fwd'] = fwd

for ccy in df.columns:
    line, = plt.plot(df.index, df[ccy], label=ccy)
    y_pos = df[ccy].iloc[-1]
    plt.annotate(ccy, xy=(1,y_pos),xytext=(8,0),xycoords=("axes fraction","data")
                 ,textcoords="offset points",color=line.get_color(), fontsize=8)

plt.title("Carry Over Time")
plt.ylabel("fwd_implied_carry (%)")
plt.savefig('carry_over_time.pdf', format="pdf", bbox_inches="tight")