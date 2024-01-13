import QuantLib as ql
import pandas as pd
import tia.bbg.datamgr as dm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tia.bbg import LocalTerminal

# # will use this later when i want to use bbg data more 
# resp = LocalTerminal.get_reference_data('eurusd curncy', 'dflt_vol_surf_bid')

# resp = resp.as_frame()
# print(resp.iloc[0]['dflt_vol_surf_bid'])

mgr = dm.BbgDataManager()

currency_pair = "EURUSD"
Spot = mgr[currency_pair + " Curncy"].PX_LAST
Strike = 1.0991
Sigma = 0.06397
Ccy1Rate = 0.03832
Ccy2Rate = 0.05301
OptionType = ql.Option.Call

# Option dates in quantlib objects
EvaluationDate = ql.Date(13, 1,2024)
SettlementDate = ql.Date(17, 4, 2024) #Evaluation +2
ExpiryDate = ql.Date(15, 4, 2024) #Evaluation + term which is 1 week
DeliveryDate = ql.Date(19, 1, 2024) #Expiry +2
NumberOfDaysBetween = ExpiryDate - EvaluationDate

#Generate continuous interest rates
EurRate = Ccy1Rate
UsdRate = Ccy2Rate

SpotGlobal = ql.SimpleQuote(Spot)
SpotHandle = ql.QuoteHandle(SpotGlobal)
VolGlobal = ql.SimpleQuote(Sigma)
VolHandle = ql.QuoteHandle(VolGlobal)
UsdRateGlobal = ql.SimpleQuote(UsdRate)
UsdRateHandle = ql.QuoteHandle(UsdRateGlobal)
EurRateGlobal = ql.SimpleQuote(EurRate)
EurRateHandle = ql.QuoteHandle(EurRateGlobal)

#Settings such as calendar, evaluationdate; daycount
Calendar = ql.UnitedStates(ql.UnitedStates.Settlement)
ql.Settings.instance().evaluationDate = EvaluationDate
DayCountRate = ql.Actual360()
DayCountVolatility = ql.ActualActual(ql.ActualActual.ISDA)

#Create rate curves, vol surface and GK process
RiskFreeRateEUR = ql.YieldTermStructureHandle(ql.FlatForward(0, Calendar, EurRateHandle, DayCountRate))
RiskFreeRateUSD = ql.YieldTermStructureHandle(ql.FlatForward(0, Calendar, UsdRate, DayCountRate))
Volatility = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(0, Calendar, VolHandle, DayCountVolatility))
GKProcess = ql.GarmanKohlagenProcess(SpotHandle, RiskFreeRateEUR, RiskFreeRateUSD, Volatility)

#Generate option
Payoff = ql.PlainVanillaPayoff(OptionType, Strike)
Exercise = ql.EuropeanExercise(ExpiryDate)
Option = ql.VanillaOption(Payoff, Exercise)
Option.setPricingEngine(ql.AnalyticEuropeanEngine(GKProcess))
BsPrice = Option.NPV()



ql.Settings.instance().evaluationDate = EvaluationDate
print("Premium is:", Option.NPV()*1000000/Spot)
print("Gamma is:", Option.gamma()*1000000*Spot/100)
print("Vega is:", Option.vega()*1000000*(1/100)/Spot)
print("Theta is:", Option.theta()*1000000*(1/365)/Spot)
print("Delta is:", Option.delta()*1000000)


