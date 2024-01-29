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

sids = ["USDSEK Curncy", "USDNOK Curncy",]  # truncated for brevity

N = 20  # number of periods for moving average
K = 2   # multiplier for standard deviation
unit_size = 1_000_000  # size of a trade in units of base currency

with PdfPages('bollinger_bands.pdf') as export_pdf:
    for sid in sids:
        # get the historical data for the current security
        df = mgr.get_historical(sid, ['PX_LAST'], start_date, end_date)

        # Calculate moving average
        df['SMA'] = df['PX_LAST'].rolling(window=N).mean()

        # Calculate the standard deviation
        df['STD'] = df['PX_LAST'].rolling(window=N).std()

        # Calculate upper and lower bands
        df['Upper_Band'] = df['SMA'] + (df['STD'] * K)
        df['Lower_Band'] = df['SMA'] - (df['STD'] * K)

        # Create an 'Order' column to hold the buy/sell signals
        df['Order'] = np.where(df['PX_LAST'] < df['Lower_Band'], 'Buy', 
                               np.where(df['PX_LAST'] > df['Upper_Band'], 'Sell', 'Hold'))

        # Initialize Position and Trade_Value columns
        df['Position'] = None
        df['Trade_Value'] = df['PX_LAST'] * unit_size

        # Initialize PnL and trade counter
        df['PnL'] = 0
        trade_counter = 0
        position_open_price = None
        
        # Iterate through rows to determine position changes and calculate PnL
        for i, row in df.iterrows():
            if row['Order'] in ['Buy', 'Sell'] and pd.isna(df.at[i, 'Position']):
                # Open position at the first valid signal
                df.at[i, 'Position'] = row['Order']
                position_open_price = row['Trade_Value']
            elif row['Order'] == 'Hold' and df.at[i, 'Position'] in ['Buy', 'Sell']:
                # Close position when price returns to mean
                df.at[i, 'Position'] = 'Close'
                df.at[i, 'PnL'] = row['Trade_Value'] - position_open_price if df.at[i, 'Position'] == 'Buy' else position_open_price - row['Trade_Value']
                trade_counter += 1
                position_open_price = None
            else:
                
                
                
for i, row in df.iterrows():
    current_position = df.at[i, 'Position']
    
    # Open position at the first valid signal
    if row['Order'] in ['Buy', 'Sell'] and current_position is None:
        df.at[i, 'Position'] = row['Order']
        position_open_price = row['Trade_Value']
    elif current_position in ['Buy', 'Sell']:
        # Close position if the price crosses the SMA again
        if (current_position == 'Buy' and row['PX_LAST'] > row['SMA']) or \
           (current_position == 'Sell' and row['PX_LAST'] < row['SMA']):
            df.at[i, 'Position'] = 'Close'
            pnl = row['Trade_Value'] - position_open_price if current_position == 'Buy' else position_open_price - row['Trade_Value']
            df.at[i, 'PnL'] = pnl
            trade_counter += 1
            position_open_price = None
        else:
            # Continue holding the position if it hasn't returned to the mean
            df.at[i, 'Position'] = current_position
    # If no open position and no signal, continue holding
    else:
        df.at[i, 'Position'] = 'Hold'