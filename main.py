from tia.bbg import LocalTerminal
import tia.bbg.datamgr as dm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

mgr = dm.BbgDataManager()

# Dictionary of curves
curves = {
    'USD':'25','AUD': '1', 'CAD': '7', 'CHF': '82',
    'GER': '16', 'GBP': '22', 'JGB': '18',
    'nzd': '49', 'sek': '21', 'BTP': '40'
}

# Define start and end dates for the last week and last month
start_date = (datetime.today() - relativedelta(days=7)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')
start_last_month = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')
end_last_month = start_last_month

# Initialize lists for rolldowns
rolldowns = []
last_week_values = []
last_month_values = []

# Loop through each curve to fetch data
for ccy, curve in curves.items():
    curve_id = 'YCGT' + curve.zfill(4) + ' Index'
    resp = LocalTerminal.get_reference_data(curve_id, 'CURVE_TENOR_RATES')
    df = resp.as_frame()['CURVE_TENOR_RATES'][curve_id]
    tenors = df['Tenor']
    tenor_tickers = df['Tenor Ticker']
    mid_yield = df['Mid Yield']

    # Calculate the rolldown
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

# Fetch historical data
sids = mgr[rolldowns['Tenor Ticker'].to_list()]
last_week = sids.get_historical('YLD_YTM_MID', start_date, start_date).T
print(last_week)
last_week.reset_index(inplace=True)
last_week.columns = ['Tenor Ticker', 'last_week_yield']

last_month = sids.get_historical('YLD_YTM_MID', start_last_month, start_last_month).T
last_month.reset_index(inplace=True)
last_month.columns = ['Tenor Ticker', 'last_month_yield']

# Merge the historical data with the rolldown DataFrame
combined_rolldowns = rolldowns.merge(last_week, on="Tenor Ticker")
combined_rolldowns = combined_rolldowns.merge(last_month, on="Tenor Ticker")

# Add columns for last week and last month rolldown
combined_rolldowns['ccy_test'] = combined_rolldowns['Currency'].eq(combined_rolldowns['Currency'].shift())

combined_rolldowns['last_week_rolldown'] = np.where(
    combined_rolldowns['ccy_test'],
    combined_rolldowns['yield'] - combined_rolldowns.groupby('Currency')['last_week_yield'].shift(),
    np.nan
)

combined_rolldowns['last_month_rolldown'] = np.where(
    combined_rolldowns['ccy_test'],
    combined_rolldowns['yield'] - combined_rolldowns.groupby('Currency')['last_month_yield'].shift(),
    np.nan
)

# Save the combined DataFrame to CSV
combined_rolldowns.to_csv('combined_rolldowns_test.csv')

# Print the combined DataFrame
print(combined_rolldowns)

# Plotting each currency's yield curve on a separate page in a PDF
with PdfPages('yield_curves.pdf') as pdf:
    for currency in combined_rolldowns['Currency'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))
        currency_data = combined_rolldowns[combined_rolldowns['Currency'] == currency]
        
        # Plot current yield
        ax.plot(currency_data['Tenor'], currency_data['yield'], marker='o', label='Current Yield')

        # Plot last week's yield if available
        if 'last_week_yield' in currency_data.columns:
            ax.plot(currency_data['Tenor'], currency_data['last_week_yield'], marker='x', linestyle='--', label='Last Week Yield')

        # Plot last month's yield if available
        if 'last_month_yield' in currency_data.columns:
            ax.plot(currency_data['Tenor'], currency_data['last_month_yield'], marker='^', linestyle='--', label='Last Month Yield')

        # Formatting the plot
        ax.set_title(f'{currency} Yield Curve')
        ax.set_xlabel('Tenor')
        ax.set_ylabel('Yield')
        ax.legend()
        ax.grid(True)
        
        # Save the current figure to its page
        pdf.savefig(fig)
        plt.close(fig)




        '''
        
           Currency Tenor   Tenor Ticker  yield  Rolldown last_week_yield last_month_yield  ccy_test last_week_rolldown last_month_rolldown
0        USD    1M  912797HN Govt  5.395       NaN           5.393            5.499     False                NaN                 NaN
1        USD    2M  912797HX Govt  5.421     0.026           5.431            5.471      True              0.028              -0.078
2        USD    3M  912797GE Govt  5.421     0.000           5.467            5.507      True              -0.01               -0.05
3        USD    4M  912797JG Govt  5.467     0.046             NaN              NaN      True                0.0               -0.04
4        USD    6M  912797HH Govt  5.480     0.013           5.558              NaN      True                NaN                 NaN
..       ...   ...            ...    ...       ...             ...              ...       ...                ...                 ...
151      BTP   15Y  BW763624 Corp  4.919     0.280           5.052            5.198      True               0.13              -0.036
152      BTP   20Y  ZM337817 Corp  5.077     0.158           5.204            5.345      True              0.025              -0.121
153      BTP   25Y  AX099966 Corp  5.029    -0.048           5.175            5.302      True             -0.175              -0.316
154      BTP   30Y  ZL106368 Corp  5.134     0.105           5.276            5.395      True             -0.041              -0.168
155      BTP   50Y  BO952242 Corp  4.703    -0.431           4.838            4.912      True             -0.573              -0.692 
        
        # ... your existing code above

# Plotting each currency's yield curve with rolldown annotations on a separate page in a PDF
with PdfPages('yield_curves.pdf') as pdf:
    for currency in combined_rolldowns['Currency'].unique():
        fig, ax = plt.subplots(figsize=(10, 6))
        currency_data = combined_rolldowns[combined_rolldowns['Currency'] == currency]
        
        # Plot current yield and annotate rolldown
        ax.plot(currency_data['Tenor'], currency_data['yield'], marker='o', label='Current Yield')
        for i in range(len(currency_data)):
            ax.annotate(f"{currency_data.iloc[i]['Rolldown']:.2f}",
                        (currency_data.iloc[i]['Tenor'], currency_data.iloc[i]['yield']),
                        textcoords="offset points", xytext=(0,10), ha='center')

        # Plot last week's yield and annotate rolldown if available
        if 'last_week_yield' in currency_data.columns:
            ax.plot(currency_data['Tenor'], currency_data['last_week_yield'], marker='x', linestyle='--', label='Last Week Yield')
            for i in range(len(currency_data)):
                if pd.notnull(currency_data.iloc[i]['last_week_rolldown']):
                    ax.annotate(f"{currency_data.iloc[i]['last_week_rolldown']:.2f}",
                                (currency_data.iloc[i]['Tenor'], currency_data.iloc[i]['last_week_yield']),
                                textcoords="offset points", xytext=(0,-15), ha='center')

        # Plot last month's yield and annotate rolldown if available
        if 'last_month_yield' in currency_data.columns:
            ax.plot(currency_data['Tenor'], currency_data['last_month_yield'], marker='^', linestyle='--', label='Last Month Yield')
            for i in range(len(currency_data)):
                if pd.notnull(currency_data.iloc[i]['last_month_rolldown']):
                    ax.annotate(f"{currency_data.iloc[i]['last_month_rolldown']:.2f}",
                                (currency_data.iloc[i]['Tenor'], currency_data.iloc[i]['last_month_yield']),
                                textcoords="offset points", xytext=(0,-15), ha='center')

        # Formatting the plot
        ax.set_title(f'{currency} Yield Curve')
        ax.set_xlabel('Tenor')
        ax.set_ylabel('Yield')
        ax.legend()
        ax.grid(True)
        
        # Save the current figure to its page
        pdf.savefig(fig)
        plt.close(fig)

# ... any remaining code you have
        
        
        '''