import pandas as pd
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
from collections import OrderedDict
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from fpdf import FPDF
from tabulate import tabulate

mgr = dm.BbgDataManager()

# Set the base ticker values for each currency
base_spot_tickers = {
    'aud': 'ADSW', 'cad': 'CDSW', 'chf': 'SFSNT',
    'eur': 'EUSA', 'gbp': 'BPSWS', 'jpy': 'JYSO',
    'nzd': 'NDSWAP', 'sek': 'SKSW', 'usd': 'USOSFR'
}

curve_frequency = {
    'aud': 4, 'cad': 2, 'chf': 2,
    'eur': 2, 'gbp': 2, 'jpy': 2,
    'nzd': 4, 'sek': 4, 'usd': 4
}

# Create an empty dictionary to hold the extended tickers
spot_curves = {}

# Specify the desired tenors
# spot_tenors = list(range(1,5))
spot_tenors = list(range(1, 11)) + [15, 20, 25, 30]

# Extend the base tickers for each currency to include specified tenors
for currency, base_ticker in base_spot_tickers.items():
    spot_curves[currency] = [base_ticker + str(tenor) + ' Curncy' for tenor in spot_tenors]

# Convert the spot_curves dictionary to a pandas DataFrame
spot_curves = pd.DataFrame.from_dict(spot_curves)
print(spot_curves)


def get_last_prices(tickers):
    return mgr[tickers].PX_LAST

# Retrieve the last prices for all tickers in batches
n = len(spot_curves)
batch_size = 100  # You can adjust the batch size as needed

last_prices = []
for i in range(0, n, batch_size):
    tickers_batch = spot_curves.iloc[:, i:i+batch_size].stack().tolist()
    prices = get_last_prices(tickers_batch)
    prices = prices.reindex(tickers_batch)
    last_prices.extend(prices.values.tolist())

# Shape the last_prices list to match the spot_curves DataFrame
last_prices = np.array(last_prices).reshape(n, -1)

# Create the updated_spot_curves DataFrame with last prices
updated_spot_curves = pd.DataFrame(last_prices, columns=spot_curves.columns)

updated_spot_curves['tenor'] = spot_tenors
updated_spot_curves.set_index('tenor', inplace=True)


all_tenors = (list(range(1, 31)))
interpolated_spot_curves = pd.DataFrame(index=all_tenors)

for currency in updated_spot_curves.columns:
    original_tenors = spot_tenors
    original_rates = updated_spot_curves[currency].values

    spline = CubicSpline(original_tenors,original_rates, bc_type='natural')
    interpolated_rates = spline(all_tenors)
    interpolated_spot_curves[currency] = interpolated_rates

discountf1 = 1 + (interpolated_spot_curves.div(pd.Series(curve_frequency), axis=1))/100


# Calculate the compounding DataFrame
compounding = pd.DataFrame(
    [[curve_frequency[currency] * tenor for currency in curve_frequency] for tenor in all_tenors],
    index=all_tenors,
    columns=curve_frequency.keys()
)



discountf1 = 1 / (discountf1.pow(compounding))



# build out the forward curves 
fwds = pd.DataFrame({"point": []})

fwds["point"] = [f"{i}y{j}y" for i in all_tenors for j in all_tenors if i + j <= 30]
forward_rates = {}
fwds['t1'] = fwds['point'].str.extract('(\d+)y', expand=False).astype(int)
fwds['t2'] = fwds['point'].str.extract('(\d+)y$', expand=False).astype(int) + fwds['t1']

for currency in interpolated_spot_curves.columns:
    forward_rates[currency] = pd.DataFrame(index=all_tenors)



def calculate_forward_rate(t1, t2, currency):
    D1 = discountf1.loc[t1, currency]
    D2 = discountf1.loc[t2, currency]
    dT = t2 - t1
    return (np.log(D1 / D2) / dT)*100
for currency in interpolated_spot_curves.columns:
    fwds[currency] = fwds.apply(lambda row: calculate_forward_rate(row['t1'], row['t2'], currency), axis=1)


fwds.set_index('point', inplace=True)
print(fwds)
# Create a copy of the fwds DataFrame
rolldowns = fwds.copy()
interpolated_spot_curves.reset_index(inplace=True)
interpolated_spot_curves.rename(columns={'index': 't2'}, inplace=True)

# Iterate over each row
for index, row in fwds.iterrows():
    t1 = row['t1']
    t2 = row['t2']

    # Check if t1 is greater than 1
    if t1 > 1:
        # Get the corresponding row where t1 and t2 are reduced by 1
        rolled_back_row = fwds[(fwds['t1'] == (t1 - 1)) & (fwds['t2'] == (t2 - 1))]
    
        # Perform the subtraction for each value in the copy dataframe
        for column in fwds.columns:
            if column not in ['t1', 't2']:
                rolled_back_value = rolled_back_row[column].values[0]
                rolldowns.at[index, column] -= rolled_back_value
    else:
        # Handle the situation where t1 equals 1
        interpolated_row = interpolated_spot_curves[interpolated_spot_curves['t2'] == t2 - 1]
        for column in fwds.columns:
            if column not in ['t1', 't2']:
                interpolated_value = interpolated_row[column].values[0]
                rolldowns.at[index, column] -= interpolated_value
    
interpolated_spot_curves.drop(['t2'],axis=1, inplace=True)

rolldowns.drop(['t1','t2'],axis=1, inplace=True)


# rolldowns.to_csv('raw_rolldowns.csv')
with PdfPages('swap_rolldowns.pdf') as pdf:
    fig, axs = plt.subplots(3, 3, figsize=(15,15))  # We're assuming 9 different currencies to create a 3x3 grid of plots
    
    for i, currency in enumerate(interpolated_spot_curves.columns):
        ax = axs[i//3, i%3]  # Get the subplot to be used
        
        data = interpolated_spot_curves[currency]
        ax.plot(data, label=currency)
        ax.set_title(currency)
        ax.legend()
        
    # Remove empty subplots
    for ax in axs.flatten():
        if not ax.lines:
            fig.delaxes(ax)
    
    plt.tight_layout()
    pdf.savefig()  

    # Other pages
    for currency in rolldowns.columns:
        fig, axs = plt.subplots(1, 2, figsize=(12, 8))

        data = rolldowns[currency]

        # Get highest 5 and round to 4 significant figures
        top_five = data.nlargest(5).round(4).reset_index()
        top_five.columns = ['Point', 'Value']

        # Create table for top five
        top_table = axs[0].table(cellText=top_five.values, colLabels=top_five.columns, cellLoc = 'center', loc = 'center')
        axs[0].set_title(f"{currency} - Best Rolldown")
        axs[0].axis('tight')
        axs[0].axis('off')

        # Get lowest 5 and round to 4 significant figures
        bottom_five = data.nsmallest(5).round(4).reset_index()
        bottom_five.columns = ['Point', 'Value']

        # Create table for bottom five
        bottom_table = axs[1].table(cellText=bottom_five.values, colLabels=bottom_five.columns, cellLoc = 'center', loc = 'center')
        axs[1].set_title(f"{currency} - Worst Rolldown")
        axs[1].axis('tight')
        axs[1].axis('off')

        plt.tight_layout()

        pdf.savefig(fig, bbox_inches='tight')  
        plt.close()



