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

# create an empty dataframe to store the results
results = pd.DataFrame([])

# iterate over the list of securities
for sid in sids:
    df = mgr.get_historical(sid, ['PX_LAST'], start_date, end_date)
    df[sid+'_100dma'] = df['PX_LAST'].rolling(window=100).mean()
    df[sid+'_RSI']= ta.RSI(df['PX_LAST'],n=30)

    #calculate divergence from 100 day MA 

    df[sid+'_divergence'] = ((df['PX_LAST'] - df[sid+'_100dma'])/df['PX_LAST']) * 100

    results = pd.concat([results, df], axis=1)



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


print(ranked_momentum)








# coloumns*Gap between signal implied positioning and actual CTA positioning (1=most positive, 8=most negative)
# 
# **FX Momentum rank (avg. rank of deviation from 100-day MA & 30 day RSI) (1= high mom., 10 = low)