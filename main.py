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

start_date = (datetime.today() - relativedelta(years=5)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

sids = ["USDSEK Curncy","USDNOK Curncy","USDDKK Curncy","USDCHF Curncy","USDCAD Curncy",
            "USDJPY Curncy","EURSEK Curncy","EURNOK Curncy","EURDKK Curncy","EURCHF Curncy","EURNZD Curncy",
            "EURAUD Curncy","EURCAD Curncy","EURGBP Curncy","EURJPY Curncy","EURUSD Curncy","GBPSEK Curncy",
            "GBPNOK Curncy","GBPDKK Curncy","GBPCHF Curncy","GBPNZD Curncy","GBPAUD Curncy","GBPCAD Curncy",
            "GBPJPY Curncy","GBPUSD Curncy","CADSEK Curncy","CADNOK Curncy","CADDKK Curncy","CADCHF Curncy",
            "CADJPY Curncy","CADEUR Curncy","CADUSD Curncy","AUDSEK Curncy","AUDNOK Curncy","AUDDKK Curncy",
            "AUDCHF Curncy","AUDNZD Curncy","AUDCAD Curncy","AUDGBP Curncy","AUDJPY Curncy","AUDUSD Curncy",
            "NZDSEK Curncy","NZDNOK Curncy","NZDDKK Curncy","NZDCHF Curncy","NZDAUD Curncy","NZDCAD Curncy",
            "NZDGBP Curncy","NZDJPY Curncy","NZDUSD Curncy","CHFJPY Curncy","NOKSEK Curncy",]
            
            
for sid in sids:
    # get the historical data for the current security
    df = mgr.get_historical(sid, ['PX_LAST'], start_date, end_date)