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
mgr.sid_result_mode = 'frame'
start_date = (datetime.today() - relativedelta(months=6)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')




sids = {"TWI USSP Index":"USD", "TWI NKSP Index":"NOK", "TWI JPSP Index":"JPY", "TWI SFSP Index":"CHF", "TWI EUSP Index":"EUR","TWI BPSP Index":"GBP", "TWI ADSP Index":"AUD", "TWI SKSP Index":"SEK", "TWI CDSP Index":"CAD", "TWI NDSP Index":"NZD",}

p_sids = {"USD":"NYC2UNCN Index","JPY": "IMM5JNCN Index","CHF":"IMM4SNCN Index","EUR":"IMMBENCN Index", "GBP":"IMM5PNCN Index","AUD":"IMM6ANCN Index","CAD":"IMM3CNCN Index","NZD":"IMM6ZNCN Index" }

f_sids ={"EURUSD":"EUR12M Curncy", "USDNOK": "NOK12M Curncy", "GBPUSD": "GBP12M Curncy", "USDCAD": "CAD12M Curncy", "USDJPY": "JPY12M Curncy",
       "USDSEK": "SEK12M Curncy", "AUDUSD":"AUD12M Curncy", "USDCHF": "CHF12M Curncy", "NZDUSD":"NZD12M Curncy",}

# Positioning rank #
positioning = mgr[p_sids.values()].PX_LAST
for ccy, id in p_sids.items():
    positioning.rename(index={id:ccy},inplace=True)
positioning.columns = ["positioning"]
positioning["positioning_rank"] = positioning["positioning"].rank(ascending = False)
positioning = positioning.drop(columns=["positioning"])



# calculating the momentum and ranking # 
# create an empty dataframe to store the results
results = pd.DataFrame([])

# iterate over the list of securities
for sid, ccy in sids.items():
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


for sid, ccy in sids.items():
    ranked_momentum.rename(columns={sid:ccy}, inplace=True) 
ranked_momentum = ranked_momentum.T

ranked_momentum.columns = ["momentum_rank"]

def map_color(value, colormap, min_val, max_val):
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    return colormap(norm(value))

colormap = plt.cm.RdYlGn.reversed()

min_score = ranked_momentum["momentum_rank"].min()
max_score = ranked_momentum["momentum_rank"].max()


colors = ranked_momentum['momentum_rank'].apply(map_color, args=(colormap, min_score, max_score))

colors_rgba = colors.apply(mcolors.to_rgba)

cell_colors = colors_rgba.values.reshape(-1,1).tolist()



#Calculate carry and rank 


carry_start_date = (datetime.today() - relativedelta(days=1)).strftime('%Y-%m-%d')
carry_end_date = datetime.today().strftime('%Y-%m-%d')

carry_frame = pd.DataFrame()



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
carry_frame.columns= ["carry"]



carry_frame["carry_rank"] = carry_frame["carry"].rank(ascending=False)
carry_frame = carry_frame.drop(columns=["carry"])


master_frame = pd.merge(carry_frame,positioning, left_index=True, right_index=True)

master_frame = pd.merge(master_frame,ranked_momentum,left_index=True, right_index=True)
master_frame["score"] = (10 - master_frame["positioning_rank"]) + master_frame["carry_rank"] + master_frame["momentum_rank"]
master_frame["score"] = master_frame["score"].rank(ascending=True)