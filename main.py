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

start_date = (datetime.today() - relativedelta(months=6)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')




sids = ["TWI USSP Index",
"TWI NKSP Index",
"TWI JPSP Index",
"TWI SFSP Index",
"TWI EUSP Index",
"TWI BPSP Index",
"TWI ADSP Index",
"TWI SKSP Index",
"TWI CDSP Index",
"TWI NDSP Index",]





f_sids ={"EURUSD":"EUR12M Curncy", "USDNOK": "NOK12M Curncy", "GBPUSD": "GBP12M Curncy", "USDCAD": "CAD12M Curncy", "USDJPY": "JPY12M Curncy",
       "USDSEK": "SEK12M Curncy", "AUDUSD":"AUD12M Curncy", "USDCHF": "CHF12M Curncy", "NZDUSD":"NZD12M Curncy",}

# create an empty dataframe to store the results
results = pd.DataFrame([])

# iterate over the list of securities
for sid in sids:
    df = mgr.get_historical(sid, ['PX_LAST'], start_date, end_date)
    df[sid+'_100dma'] = df['PX_LAST'].rolling(window=100).mean()
    df[sid+'_RSI']= ta.RSI(df['PX_LAST'],n=14)

    #calculate divergence from 100 day MA 

    df[sid+'_divergence'] = ((df['PX_LAST'] - df[sid+'_100dma'])/df['PX_LAST']) * 100

    results = pd.concat([results, df], axis=1)

results = results.last('5D')

# Calculate average rank of deviation and RSI 
deviation_columns = results.filter(like='_divergence').columns 

RSI_columns = results.filter(like='_RSI').columns
ranked_deviations = results[deviation_columns].rank("columns", ascending=False)

ranked_rsi = results[RSI_columns].rank("columns", ascending=False)


deviation_mean = ranked_deviations.mean().to_frame().T
rsi_mean = ranked_rsi.mean().to_frame().T

momentum = pd.DataFrame([])

for sid in sids:
    col = rsi_mean.filter(like=sid).columns 
    col2 = deviation_mean.filter(like=sid).columns
    mom = rsi_mean[col].values + deviation_mean[col2].values
    momentum[sid] = pd.DataFrame(mom)   
    mmomentum = pd.concat([momentum, momentum[sid]])

ranked_momentum = momentum.rank("columns", ascending=True)

ranked_momentum = ranked_momentum.T
ranked_momentum.reset_index(inplace=True)
ids = ranked_momentum["index"].to_list()
resp = LocalTerminal.get_reference_data(ids,["SECURITY_NAME"],ignore_field_error=1)
names = resp.as_frame()
ranked_momentum.columns = ["index", "score"]
ranked_momentum.set_index("index", inplace=True)
ranked_momentum = ranked_momentum.merge(names, how='left', left_index=True, right_index=True)

ranked_momentum.set_index("SECURITY_NAME",inplace=True)


def map_color(value, colormap, min_val, max_val):
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    return colormap(norm(value))

colormap = plt.cm.RdYlGn.reversed()

min_score = ranked_momentum["score"].min()
max_score = ranked_momentum["score"].max()


colors = ranked_momentum['score'].apply(map_color, args=(colormap, min_score, max_score))

colors_rgba = colors.apply(mcolors.to_rgba)

cell_colors = colors_rgba.values.reshape(-1,1).tolist()



carry_start_date = (datetime.today() - relativedelta(days=1)).strftime('%Y-%m-%d')
carry_end_date = datetime.today().strftime('%Y-%m-%d')

carry_frame = pd.DataFrame()
plt.figure(figsize=(10,7))
for ccy, fwd in f_sids.items():
    spot = mgr[ccy + ' Curncy'].get_historical('PX_LAST', carry_end_date, carry_end_date)
    fwd = mgr[fwd].get_historical('PX_LAST', carry_end_date, carry_end_date)
    carry = ((fwd - spot) / spot) * 100 * -1
    carry_frame[ccy] = carry

for column in carry_frame.columns:
    if column[:3] == "USD":
        carry_frame[column] = carry_frame[column] * -1
        carry_frame.rename(columns={column:column[3:]}, inplace=True)
    else:
        carry_frame.rename(columns={column:column[:3]},inplace=True)

carry_frame["USD"] = 0
carry_frame=carry_frame.T





pdf_filename = "short_term_momentum.pdf"
# plt.figure(figsize=(10,7))
with PdfPages(pdf_filename) as pdf:
    fig, ax = plt.subplots(figsize=(5,7))
    ax.axis('tight')
    ax.axis('off')
    fig.suptitle('Short Term Momentum',fontsize=12)
    mom_table = table(ax, ranked_momentum,loc='center',cellLoc='center', cellColours=cell_colors)
    ax.text(0.5,-0.1,'*FX Momentum rank (avg. rank of deviation from 100-day MA & 30 day RSI) (1= high mom., 10 = low)', transform=ax.transAxes, ha='center', va = 'top', fontsize='9' )
    pdf.savefig(fig,bbox_inches='tight')





# coloumns*Gap between signal implied positioning and actual CTA positioning (1=most positive, 8=most negative)
# 
# **FX Momentum rank (avg. rank of deviation from 100-day MA & 30 day RSI) (1= high mom., 10 = low)