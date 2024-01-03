data = []
for ccy, asset_id in dict.items():
    # print(ccy,asset_id)
    resp = ds.get_data(datetime.date.today(), assetId=asset_id, limit=50)
    data.append(resp)

