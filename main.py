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

mgr = dm.BbgDataManager()

start_date = (datetime.today() - relativedelta(years=1)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

sids = ["EURUSD", "USDNOK", "GBPUSD","USDCAD","USDJPY","USDSEK","AUDUSD", "USDCHF","NZDUSD"]
vols = {} 
for sid in sids:
    q_ticker = sid + "V3M Curncy"
    y_ticker = sid + "V1Y Curncy"

    df = mgr[q_ticker].get_historical('PX_LAST', start_date, end_date)
    vols[sid] = df
