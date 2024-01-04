''''
ds = Dataset('GSDEER_GSFEER')
gs_data = {} 
prices = {}
master_dict = {}
for ccy, asset_id in dict.items():
    # print(ccy,asset_id)
    resp = ds.get_data(datetime.date.today(), assetId=asset_id, limit=500)
    if ccy in ['AUDUSD','EURUSD','NZDUSD','GBPUSD']:
        resp['gsdeer'] = 1/resp['gsdeer']
    else:
        continue
    cols = ['year','quarter']    
    resp['currency'] = ccy + ' Curncy'
    resp['period'] =  resp[cols].astype(str).apply('-'.join, axis=1)
    resp['period'] = pd.to_datetime(resp['period'])
    resp = resp[['currency','period','gsdeer']]
    resp.set_index('period', inplace=True)
    resp = resp[resp.index.year >= 2000]
    gs_data[ccy] = resp
    

    bbgresp = pd.DataFrame()


    start_date = datetime.date(2000, 1, 1) 
    end_date = datetime.date.today()
    bbgresp['price'] = mgr[ccy + ' Curncy'].get_historical('PX_LAST', start_date, end_date)
    bbgresp['currency'] = ccy + ' Curncy' 
    bbgresp = bbgresp[['currency','price']]
    prices[ccy] = bbgresp
    
    df = bbgresp.merge(resp,how='right',on='currency')
    master_dict[ccy] = df

print(master_dict['EURUSD'])

             currency   price    gsdeer
0       EURUSD Curncy  1.0200  1.190476
1       EURUSD Curncy  1.0306  1.190476
2       EURUSD Curncy  1.0344  1.190476
3       EURUSD Curncy  1.0286  1.190476
4       EURUSD Curncy  1.0295  1.190476
...               ...     ...       ...
626295  EURUSD Curncy  1.1074  1.219512
626296  EURUSD Curncy  1.1039  1.219512
626297  EURUSD Curncy  1.0951  1.219512
626298  EURUSD Curncy  1.0907  1.219512
626299  EURUSD Curncy  1.0943  1.219512




'''