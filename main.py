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

mask_jpy = pivot_df.loc[mask, 'QUOTEPAIR'].str.contains('JPY')
pivot_df.loc[mask & mask_jpy, 'SPREAD'] = -(pivot_df.loc[mask & mask_jpy, 'OFFER'] - pivot_df.loc[mask & mask_jpy, 'BID']) * 100
pivot_df.loc[mask & ~mask_jpy, 'SPREAD'] = -(pivot_df.loc[mask & ~mask_jpy, 'OFFER'] - pivot_df.loc[mask & ~mask_jpy, 'BID']) * 10000

pivot_df.reset_index(drop=True, inplace=True)


average_spread = pivot_df.groupby(['CPSESSIONID','TRADEDATE','QUOTEPAIR','SIZE_GROUP'])['SPREAD'].mean()
print(average_spread)



'''
CPSESSIONID  TRADEDATE   QUOTEPAIR  SIZE_GROUP
574944291.0  07/01/2022  AUD/JPY    0-10          1.757778
574981451.0  07/01/2022  USD/JPY    0-10          0.930000
575406801.0  07/05/2022  USD/SGD    20-30         3.728000
575430951.0  07/05/2022  EUR/USD    20-30         1.718000
575475501.0  07/05/2022  USD/JPY    30-40         3.232500
                                                    ...
655899861.0  15/06/2023  USD/JPY    20-30         2.426667
656244801.0  16/06/2023  USD/JPY    20-30         2.420909
657250631.0  22/06/2023  USD/SGD    20-30         3.390909
657376811.0  22/06/2023  USD/JPY    20-30         2.197273
657903971.0  26/06/2023  USD/CNH    0-10          3.450000
'''