gs_data = {} 
prices = {}
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
    bbgresp['currency'] = ccy + ' Curncy'
    bbgresp['price'] = mgr[ccy + ' Curncy'].get_historical('PX_LAST', start_date, end_date)
    prices[ccy] = bbgresp
print(prices['EURUSD'])