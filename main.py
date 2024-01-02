import pandas as pd
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.backends.backend_pdf import PdfPages
from tabulate import tabulate
import matplotlib.pyplot as plt


# Define Bloomberg DataManager object
mgr = dm.BbgDataManager()

# Define currency pairs to retrieve data for
sids = ["USDSEK Curncy","USDNOK Curncy","USDDKK Curncy","USDCHF Curncy","USDCAD Curncy",
            "USDJPY Curncy","EURSEK Curncy","EURNOK Curncy","EURDKK Curncy","EURCHF Curncy","EURNZD Curncy",
            "EURAUD Curncy","EURCAD Curncy","EURGBP Curncy","EURJPY Curncy","EURUSD Curncy","GBPSEK Curncy",
            "GBPNOK Curncy","GBPDKK Curncy","GBPCHF Curncy","GBPNZD Curncy","GBPAUD Curncy","GBPCAD Curncy",
            "GBPJPY Curncy","GBPUSD Curncy","CADSEK Curncy","CADNOK Curncy","CADDKK Curncy","CADCHF Curncy",
            "CADJPY Curncy","CADEUR Curncy","CADUSD Curncy","AUDSEK Curncy","AUDNOK Curncy","AUDDKK Curncy",
            "AUDCHF Curncy","AUDNZD Curncy","AUDCAD Curncy","AUDGBP Curncy","AUDJPY Curncy","AUDUSD Curncy",
            "NZDSEK Curncy","NZDNOK Curncy","NZDDKK Curncy","NZDCHF Curncy","NZDAUD Curncy","NZDCAD Curncy",
            "NZDGBP Curncy","NZDJPY Curncy","NZDUSD Curncy","CHFJPY Curncy","NOKSEK Curncy",]

            # "WN1 Comdty","US1 Comdty",
            # "UXY1 Comdty","TY1 Comdty","FV1 Comdty","TU1 Comdty","CA1 Comdty","UB1 Comdty","RX1 Comdty","OE1 Comdty",
            # "DU1 Comdty","G 1 Comdty","IK1 Comdty","OAT1 Comdty","BTS1 Comdty","BTO1 Comdty","JB1 Comdty","XM1 Comdty",
            # "YM1 Comdty","DM1 Index","ES1 Index","NQ1 Index","PT1 Index","IS1 Index","BZ1 Index","VG1 Index","Z 1 Index",
            # "CF1 Index","GX1 Index","IB1 Index","ST1 Index","EO1 Index","QC1 Index","SM1 Index","NK1 Index","HI1 Index","IFB1 Index",
            # "XP1 Index","CL1 Comdty"]



# Define start and end dates for data
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')

# Define empty lists to store currency pairs and corresponding RSI values
rsi_below = []
rsi_above = []

# Loop through each security in sids and check RSI for today's date
for sid in sids:
    # Retrieve data for current security
    df = mgr[sid].get_historical(['PX_LAST'], start_date, end_date)
    # Calculate RSI using default 14-day period
    rsi = ta.RSI(df['PX_LAST'], n=14)[-1]
    # Check RSI value and add currency pair and RSI value to the corresponding list
    if rsi < 35:
        rsi_below.append([sid, round(rsi, 2)])
    elif rsi > 65:
        rsi_above.append([sid, round(rsi, 2)])

# Create dataframes for currency pairs with RSI below 30 and above 70
df_rsi_below = pd.DataFrame(rsi_below, columns=['Security', 'RSI (<35)'])
df_rsi_above = pd.DataFrame(rsi_above, columns=['Security', 'RSI (>65)'])

# Create a PDF file
pdf = PdfPages('rsi_tables.pdf')
# Format the dataframes as tabulated strings
table_rsi_below = tabulate(df_rsi_below, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f")
table_rsi_above = tabulate(df_rsi_above, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f")

# Create a figure for the PDF page
fig = plt.figure(figsize=(10,7))

# plt.title("RSI's")
# Create subplots for each table
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# Turn off the axis and set the title
ax1.axis('off')


ax2.axis('off')


# Add the tabulated strings to the subplots
ax1.text(0.1, 0.1, table_rsi_below, {'fontsize': 10, 'fontfamily': 'monospace'})
ax2.text(0.1, 0.1, table_rsi_above, {'fontsize': 10, 'fontfamily': 'monospace'})

# Save the figure to the PDF file
pdf.savefig(fig)

# Close the PDF file
pdf.close()