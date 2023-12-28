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
    ticker = sid + "V" + date + " Curncy" 
    print(ticker)