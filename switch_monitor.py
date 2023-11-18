

bonds = []
for ticker in unique_tickers:
    universe = bq.univ.filter(bq.univ.bonds(ticker),bq.data.CRNCY()==tickers.loc[ticker]['CRNCY'])
    data_item = bq.data.px_last()

    request = bql.Request(universe, data_item)
    response = bq.execute(request)

    fetch = response[0].df()
    bonds.append(fetch)

'''
[                    DATE CURRENCY  PX_LAST()
 ID                                          
 ZN417074 Corp 2023-11-18     None   99.18076
 ZS368164 Corp 2023-11-18     None   94.64562
 AO563305 Corp 2023-11-18     None   95.08434
 ZQ225609 Corp 2023-11-18     None   93.06542
 BK746243 Corp 2023-11-18     None   85.62323
 BQ817745 Corp 2023-11-18     None   83.50963
 QZ981658 Corp 2023-11-18     None   98.35541
 ZP995826 Corp 2023-11-18     None   88.13470
 AP085425 Corp 2023-11-18     None   93.78728,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 DD107143 Corp 2023-11-18     None  103.83840
 BJ108920 Corp 2023-11-18     None  272.87360
 ZP519345 Corp 2023-11-18     None  100.07040
 ZP519351 Corp 2023-11-18     None  104.49190
 AP338435 Corp 2023-11-18     None   93.69889
 BZ179444 Corp 2023-11-18     None   99.21598
 BP473330 Corp 2023-11-18     None   86.09001
 BM210631 Corp 2023-11-18     None   96.11222
 BP473325 Corp 2023-11-18     None   93.46977,
                     DATE CURRENCY  PX_LAST()
 ID                                          
 ZM244766 Corp 2023-11-18     None   99.90406
 ZJ054796 Corp 2023-11-18     None   98.65904
 ZK028186 Corp 2023-11-18     None   97.44985
 AP153633 Corp 2023-11-18     None   80.71000
 ZK028184 Corp 2023-11-18     None   98.68353
 ...                  ...      ...        ...
 AS460805 Corp 2023-11-18     None   91.78384
 AU385526 Corp 2023-11-18     None   91.46111
 AU057237 Corp 2023-11-18     None   91.06326
 BO217298 Corp 2023-11-18     None   88.37935
 AP122077 Corp 2023-11-18     None   90.80504
 
 [98 rows x 3 columns],
                     DATE CURRENCY  PX_LAST()
 ID                                          
 BR383861 Corp 2023-11-18     None   79.34182
 BR383862 Corp 2023-11-18     None   67.45230
 AP955201 Corp 2023-11-18     None   87.37179
 EI267147 Corp 2023-11-18     None  102.15140
 AP954927 Corp 2023-11-18     None   96.21011
 AX667786 Corp 2023-11-18     None   93.45038
 AP955170 Corp 2023-11-18     None   89.88506
 BK692651 Corp 2023-11-18     None   99.30822
 EJ789364 Corp 2023-11-18     None   77.58130
 EG818677 Corp 2023-11-18     None  101.48510
 AN134368 Corp 2023-11-18     None   90.19600
 AN134353 Corp 2023-11-18     None   95.84901
 AN134367 Corp 2023-11-18     None   87.93723
 EJ324559 Corp 2023-11-18     None   74.74226,
                     DATE CURRENCY  PX_LAST()


'''