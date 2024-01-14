
currency_pair = "EURUSD"
ExpiryDate = ql.Date(18, 4, 2024)
datetime_expiry = datetime()
Strike = 1.0991
Sigma = LocalTerminal.get_reference_data(currency_pair+ " Curncy","RK311",RK315=ExpiryDate) 
Ccy1Rate = 0.03832
Ccy2Rate = 0.05301
OptionType = ql.Option.Call
short_long = 1 # 1 for long, -1 for short


April 22nd, 2024