import matplotlib.colors as mcolors
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
from pandas.plotting import table

mgr = dm.BbgDataManager()
mgr.sid_result_mode = 'frame'
start_date = (datetime.today() - relativedelta(months=6)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')




sids = {"TWI USSP Index":"USD", "TWI NKSP Index":"NOK", "TWI JPSP Index":"JPY", "TWI SFSP Index":"CHF", "TWI EUSP Index":"EUR","TWI BPSP Index":"GBP", "TWI ADSP Index":"AUD", "TWI SKSP Index":"SEK", "TWI CDSP Index":"CAD", "TWI NDSP Index":"NZD",}

p_sids = {"USD":"NYC2UNCN Index","JPY": "IMM5JNCN Index","CHF":"IMM4SNCN Index","EUR":"IMMBENCN Index", "GBP":"IMM5PNCN Index","AUD":"IMM6ANCN Index","CAD":"IMM3CNCN Index","NZD":"IMM6ZNCN Index" }

f_sids ={"EURUSD":"EUR12M Curncy", "USDNOK": "NOK12M Curncy", "GBPUSD": "GBP12M Curncy", "USDCAD": "CAD12M Curncy", "USDJPY": "JPY12M Curncy",
       "USDSEK": "SEK12M Curncy", "AUDUSD":"AUD12M Curncy", "USDCHF": "CHF12M Curncy", "NZDUSD":"NZD12M Curncy",}

positioning = mgr[p_sids.values()].PX_LAST
print(positioning)
print(type(positioning))
for ccy, id in p_sids.items():
    positioning.rename(index={id,ccy},inplace=True)

print(positioning)

master_frame["score"] = [(master_frame["positioning_rank"] + master_frame["carry_rank"] + master_frame["momentum_rank"]) / 3].rank(ascending = False)