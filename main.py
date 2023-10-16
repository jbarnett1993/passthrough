import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

df = pd.read_csv("master_data.csv", infer_datetime_format=True)

df = df[["CPSESSIONID","BANKINST","SESSIONTYPE","TRADEDATE","ORDERTYPE","IS_WINNER_FLAG",
         "DIRECTION","GIVENCCY", "QUOTEPAIR","GIVENAMT","SPOTRATE","SETTLEAMT","FWDPOINTS","ALLINRATE"]]
df = df[df.SESSIONTYPE=="RFS"]
df = df[df.ORDERTYPE != "SWAP"]

sessions = df["CPSESSIONID"].unique()

df["DIRECTION"].replace("BUY","OFFER",inplace=True)

df["DIRECTION"].replace("SELL","BID",inplace=True)

df["SIZE_GROUP"] = ""#groups between 0-10,10-20,20-30,30-40,40-50,50-75,75-100,100-150
df["FIRSTCCY"] = df["QUOTEPAIR"].str.split('/').str[0]


for x,row in df.iterrows():
    if row['GIVENAMT'] < 10000000:
        df.at[x,"SIZE_GROUP"] = "0-10"
    elif row['GIVENAMT'] < 20000000: 
        df.at[x,"SIZE_GROUP"] = "10-20"
    elif row['GIVENAMT'] < 30000000: 
        df.at[x,"SIZE_GROUP"] = "20-30"
    elif row['GIVENAMT'] < 40000000: 
        df.at[x,"SIZE_GROUP"] = "30-40"
    elif row['GIVENAMT'] < 50000000: 
        df.at[x,"SIZE_GROUP"] = "40-50"
    elif row['GIVENAMT'] < 750000000: 
        df.at[x,"SIZE_GROUP"] = "50-75"
    elif row['GIVENAMT'] < 100000000: 
        df.at[x,"SIZE_GROUP"] = "75-100"
    else:
        df.at[x,"SIZE_GROUP"] = "100+"


pivot_df = df.pivot_table(index=['CPSESSIONID',"TRADEDATE",'BANKINST','QUOTEPAIR',
                                 'GIVENCCY',"FIRSTCCY",'GIVENAMT','SIZE_GROUP'], columns='DIRECTION',values='SPOTRATE')
# pivot_df["MIDPOINT"] = 
# df.loc[mask, "GIVENAMT"] = df["GIVENAMT"] / df["MIDPOINT"]



pivot_df.columns.name = None

mask1 = np.logical_and(pivot_df["BID"]==0 , pivot_df["OFFER"]==0)
pivot_df.loc[mask1,['BID','OFFER']]=np.nan


# pivot_df['SPREAD'] = np.where(pivot_df['QUOTEPAIR'].str.contains('JPY'),((pivot_df['OFFER'] - pivot_df['BID']) * 100, pivot_df['OFFER'] - pivot_df['BID']) * 10000)
# pivot_df['SPREAD'] = (pivot_df['OFFER'] - pivot_df['BID']) * 10000

pivot_df = pivot_df.reset_index()


pivot_df.reset_index(drop=True,inplace=True)



pivot_df['SPREAD'] = np.where(pivot_df['QUOTEPAIR'].str.contains('JPY'),(pivot_df['OFFER'] - pivot_df['BID']) * 100, (pivot_df['OFFER'] - pivot_df['BID']) * 10000)

mask = pivot_df["GIVENCCY"] != pivot_df["FIRSTCCY"]
pivot_df["MIDPOINT"] = (pivot_df["BID"] + pivot_df["OFFER"]) /2 


pivot_df.loc[mask, "GIVENAMT"] = pivot_df.loc[mask, "GIVENAMT"] / pivot_df.loc[mask, "MIDPOINT"]


pivot_df['SPREAD'] = np.where(pivot_df.loc[mask, 'QUOTEPAIR'].str.contains('JPY'),(pivot_df.loc[mask, 'OFFER'] - pivot_df.loc[mask, 'BID']) * 100, (pivot_df.loc[mask, 'OFFER'] - pivot_df.loc[mask, 'BID']) * 10000)



pivot_df.reset_index(drop=True, inplace=True)


average_spread = pivot_df.groupby(['CPSESSIONID','TRADEDATE','QUOTEPAIR','SIZE_GROUP'])['SPREAD'].mean()
print(average_spread)



'''
  df = pd.read_csv("master_data.csv")
      CPSESSIONID   TRADEDATE   BANKINST QUOTEPAIR GIVENCCY FIRSTCCY      GIVENAMT SIZE_GROUP        BID      OFFER  SPREAD    MIDPOINT
0     574944291.0  07/01/2022        anz   AUD/JPY      AUD      AUD  7.000000e+06       0-10   91.54500   91.57900   340.0   91.562000
1     574944291.0  07/01/2022     barcap   AUD/JPY      AUD      AUD  7.000000e+06       0-10   91.55400   91.56700   130.0   91.560500
2     574944291.0  07/01/2022       citi   AUD/JPY      AUD      AUD  7.000000e+06       0-10        NaN        NaN     NaN         NaN
3     574944291.0  07/01/2022         gs   AUD/JPY      AUD      AUD  7.000000e+06       0-10   91.55300   91.57000   170.0   91.561500
4     574944291.0  07/01/2022   hsbcbank   AUD/JPY      AUD      AUD  7.000000e+06       0-10   91.55000   91.56100   110.0   91.555500
...           ...         ...        ...       ...      ...      ...           ...        ...        ...        ...     ...         ...
2535  657376811.0  22/06/2023        ssb   USD/JPY      USD      USD  2.500000e+07      20-30  142.73900  142.76800   290.0  142.753500
2536  657376811.0  22/06/2023  stanchart   USD/JPY      USD      USD  2.500000e+07      20-30  142.74200  142.76500   230.0  142.753500
2537  657376811.0  22/06/2023       ubsw   USD/JPY      USD      USD  2.500000e+07      20-30  142.74440  142.77270   283.0  142.758550
2538  657903971.0  26/06/2023        anz   USD/CNH      CNH      USD  1.657211e+05       0-10    7.24127    7.24089    -3.8    7.241080
2539  657903971.0  26/06/2023      rbcds   USD/CNH      CNH      USD  1.657229e+05       0-10    7.24116    7.24085    -3.1    7.241005
'''