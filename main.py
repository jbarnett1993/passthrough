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
dates = ["1M","3M","6M","9M","1Y"]

sids = []
for date in dates:
    ticker = sid[0] + "V" + date + " Curncy" 
    sids.append(ticker)

print(sids)
'''
          EURUSDV1M Curncy EURUSDV3M Curncy EURUSDV6M Curncy EURUSDV9M Curncy EURUSDV1Y Curncy
                    PX_LAST          PX_LAST          PX_LAST          PX_LAST          PX_LAST
date
2022-12-28           8.6725           8.7150           8.4150           8.2800           8.2000
2022-12-29           8.4725           8.7350           8.4200           8.3100           8.2100
2022-12-30           8.5550           8.7600           8.3975           8.2600           8.1600
2023-01-02           9.4700           8.8550           8.4375           8.2800           8.1600
2023-01-03           9.8150           8.9425           8.5500           8.4150           8.2900
...                     ...              ...              ...              ...              ...
2023-12-22           6.3700           6.5050           6.5300           6.6300           6.7625
2023-12-25           6.6400           6.6200           6.5900           6.5950           6.7750
2023-12-26           6.6125           6.5875           6.5550           6.5650           6.7475
2023-12-27           6.6225           6.6100           6.5450           6.5775           6.7250
2023-12-28           6.7400           6.6750           6.5825           6.5900           6.7250



'''