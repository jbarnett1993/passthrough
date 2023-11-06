from tia.bbg import LocalTerminal
import tia.bbg.datamgr as dm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

mgr = dm.BbgDataManager()


curves = {
    'AUD': '1', 'CAD': '7', 'CHF': '82',
    'GER': '16', 'GBP': '22', 'JGB': '18',
    'nzd': '49', 'sek': '21', 'BTP': '40'
}

start_date = (datetime.today() - relativedelta(days=7)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

rolldowns = []
for ccy, curve in curves.items():
    resp = LocalTerminal.get_reference_data('YCGT'+curve.zfill(4)+' Index','CURVE_TENOR_RATES')
    df = resp.as_frame()['CURVE_TENOR_RATES']['YCGT'+curve.zfill(4)+' Index']
    tenors = df['Tenor']
    tenor_tickers = df['Tenor Ticker']
    mid_yield = df['Mid Yield']

    rolldown = np.diff(mid_yield).round(4)
    rolldown = np.insert(rolldown, 0, np.nan)  # Set first rolldown as NaN

    # Create a DataFrame with necessary information
    df_info = pd.DataFrame({
        'Currency': ccy,
        'Tenor': tenors,
        'Tenor Ticker': tenor_tickers,
        'yield': mid_yield,
        'Rolldown': rolldown
    })

    rolldowns.append(df_info)

# Concatenate rolldown DataFrames into a single DataFrame
rolldowns = pd.concat(rolldowns, ignore_index=True)
rolldowns.to_csv("all_curves.csv")
sids = mgr[rolldowns['Tenor Ticker'].to_list()]


last_week = sids.get_historical('YLD_YTM_MID', start_date, start_date).T

# last_week['Tenor Ticker'] = last_week.index
last_week.reset_index(inplace=True)
last_week.columns = ['Tenor Ticker','last_week_yield']

combined_rolldowns = rolldowns.merge(last_week, on="Tenor Ticker")
combined_rolldowns['ccy_test'] = combined_rolldowns['Currency'].eq(combined_rolldowns['Currency'].shift())
combined_rolldowns['last_week_rolldown'] = np.where(combined_rolldowns['ccy_test'] == True, combined_rolldowns['last_week_yield'].diff(),np.nan)

combined_rolldowns.to_csv('combined_rolldowns.csv')



print(combined_rolldowns)


