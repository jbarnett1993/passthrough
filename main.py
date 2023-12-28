import pandas as pd
import numpy as np
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
from matplotlib import gridspec
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from tia.bbg import LocalTerminal

mgr = dm.BbgDataManager()

start_date = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
# end_date = datetime.strptime('2023-12-15','%Y-%m-%d')

sid = ["EURUSD"]
dates = ["1M","2M","3M","4M","5M","6M","7M","8M", "9M","1Y"]

sids = []
for date in dates:
    ticker = sid[0] + "V" + date + " Curncy" 
    sids.append(ticker)


df = mgr.get_historical(sids, ['PX_LAST'], start_date, end_date)
percentiles = df.quantile([0.1, 0.25, 0.5,0.75,0.9])
print(percentiles)
current_vol = df.iloc[-1]
plt.figure(figsize=(10,7))
plt.plot(dates,current_vol,label="current vol",marker="o")
plt.fill_between(dates,percentiles.iloc[0],percentiles.iloc[4],color="grey",alpha=0.1,label="10/90 percentile")
plt.fill_between(dates,percentiles.iloc[1],percentiles.iloc[3],color="grey",alpha=0.3,label="25/75 percentile")
plt.plot(dates,percentiles.iloc[2],label="50th percentile",linestyle="--",color="red")
plt.title("EURUSD Vol Term Structure vs historical level (1y lookback)")
plt.xlabel("Tenor")
plt.ylabel("Volatility")
plt.legend()
plt.grid(True)
plt.show()