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

sids = ["USDSEK Curncy", "USDNOK Curncy", ...]  # truncated for brevity

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

        # Close position when price returns to mean
        df['Position'] = df['Order'].replace(to_replace='Hold', method='ffill').shift()
        df['Position'] = np.where((df['Order'] == 'Hold') & (df['Position'] != 'Hold'), 'Close', df['Position'])
        
        # Track the trades and calculate profit/loss
        df['Trade_Value'] = df['PX_LAST'] * unit_size
        df['PnL'] = 0

        position_open_price = 0
        for i, row in df.iterrows():
            if row['Position'] == 'Buy' or row['Position'] == 'Sell':
                position_open_price = row['Trade_Value']
            elif row['Position'] == 'Close':
                df.at[i, 'PnL'] = row['Trade_Value'] - position_open_price
                position_open_price = 0

        # Plotting the Bollinger Bands and signals
        plt.figure(figsize=(12,6))
        plt.title(f'{sid} Bollinger Bands\nP&L: {df["PnL"].sum()}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.plot(df['PX_LAST'], label='Price')
        plt.plot(df['SMA'], label='Middle Band (SMA)')
        plt.plot(df['Upper_Band'], label='Upper Band')
        plt.plot(df['Lower_Band'], label='Lower Band')
        plt.fill_between(df.index, df['Lower_Band'], df['Upper_Band'], color='grey', alpha=0.3)
        plt.scatter(df[df['Order'] == 'Buy'].index, df[df['Order'] == 'Buy']['PX_LAST'], label='Buy Signal', marker='^', color='green')
        plt.scatter(df[df['Position'] == 'Close'].index, df[df['Position'] == 'Close']['PX_LAST'], label='Sell/Close Signal', marker='v', color='red')
        plt.legend(loc='best')
        plt.show()
        
        # Save the plot to the PDF
        export_pdf.savefig()
        plt.close()