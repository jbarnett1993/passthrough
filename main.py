import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_pdf import PdfPages
df = pd.read_csv("master_data.csv", parse_dates=["TRADEDATE"], date_parser = lambda x: datetime.datetime.strptime(x,'%d/%m/%Y'),low_memory=False)


df = df[["CPSESSIONID","BANKINST","SESSIONTYPE","TRADEDATE","ORDERTYPE","IS_WINNER_FLAG",
         "DIRECTION","GIVENCCY", "QUOTEPAIR","GIVENAMT","SPOTRATE","SETTLEAMT","FWDPOINTS","ALLINRATE"]]
df = df[df.SESSIONTYPE=="RFS"]
df = df[df.ORDERTYPE != "SWAP"]


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



pivot_df.columns.name = None

mask1 = np.logical_and(pivot_df["BID"]==0 , pivot_df["OFFER"]==0)
pivot_df = pivot_df[~mask1]
print(pivot_df)

pivot_df = pivot_df.reset_index()

pivot_df.reset_index(drop=True,inplace=True)
print(pivot_df)

pivot_df['SPREAD'] = np.where(pivot_df['QUOTEPAIR'].str.contains('JPY'),(pivot_df['OFFER'] - pivot_df['BID']) * 100, (pivot_df['OFFER'] - pivot_df['BID']) * 10000)

mask = pivot_df["GIVENCCY"] != pivot_df["FIRSTCCY"]
pivot_df["MIDPOINT"] = (pivot_df["BID"] + pivot_df["OFFER"]) /2 


pivot_df.loc[mask, "GIVENAMT"] = pivot_df.loc[mask, "GIVENAMT"] / pivot_df.loc[mask, "MIDPOINT"]


def assign_size_group(givenamt):
    if givenamt < 10000000:
        return "0-10"
    elif givenamt < 20000000:
        return "10-20"
    elif givenamt < 30000000:
        return "20-30"
    elif givenamt < 40000000:
        return "30-40"
    elif givenamt < 50000000:
        return "40-50"
    elif givenamt < 75000000:
        return "50-75"
    elif givenamt < 100000000:
        return "75-100"
    else:
        return "100+"

pivot_df["SIZE_GROUP"] = pivot_df["GIVENAMT"].apply(assign_size_group)

mask_jpy = pivot_df.loc[mask, 'QUOTEPAIR'].str.contains('JPY')
pivot_df.loc[mask & mask_jpy, 'SPREAD'] = -(pivot_df.loc[mask & mask_jpy, 'OFFER'] - pivot_df.loc[mask & mask_jpy, 'BID']) * 100
pivot_df.loc[mask & ~mask_jpy, 'SPREAD'] = -(pivot_df.loc[mask & ~mask_jpy, 'OFFER'] - pivot_df.loc[mask & ~mask_jpy, 'BID']) * 10000





pivot_df.reset_index(drop=True, inplace=True)


pivot_df['TRADEDATE'] = pd.to_datetime(pivot_df["TRADEDATE"])
pivot_df.to_csv("masterdata.csv")

average_spread_per_ccy_and_size = pivot_df.groupby(['CPSESSIONID','TRADEDATE','QUOTEPAIR','SIZE_GROUP'])['SPREAD'].mean()


average_spread_per_ccy_and_size = average_spread_per_ccy_and_size.reset_index()


average_spread_per_ccy_and_size = pivot_df.groupby(['CPSESSIONID','TRADEDATE','QUOTEPAIR','SIZE_GROUP'])['SPREAD'].mean()


average_spread_per_bank_ccy_and_size = pivot_df.groupby(['QUOTEPAIR','SIZE_GROUP','BANKINST'])['SPREAD'].mean()
print(average_spread_per_bank_ccy_and_size)


# for quote_pair in quote_pairs:
#     plt.figure(figsize=(12,8))
#     subset = average_spread[average_spread['QUOTEPAIR'] == quote_pair].sort_values(by='TRADEDATE')

#     for size_group in subset['SIZE_GROUP'].unique():
#         group_data = subset[subset['SIZE_GROUP'] == size_group]
#         plt.plot(group_data['TRADEDATE'], group_data['SPREAD'] , label=size_group)

#     plt.title(f"spreads over time for {quote_pair}")
#     plt.xlabel("Trade Date")
#     plt.ylabel("Spread")
#     plt.legend()
#     plt.show()


'''
QUOTEPAIR  SIZE_GROUP  BANKINST
AUD/CAD    0-10        anz          1.50
                       barcap       0.50
                       bnym        -0.40
                       boaml        0.00
                       cibc         0.90
                                   ...
USD/SGD    50-75       citi        17.20
                       gs           6.60
                       hsbcbank     8.70
                       jpmc        11.01
                       ubsw         3.30
'''