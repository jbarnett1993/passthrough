import QuantLib as ql
import pandas as pd
import tia.bbg.datamgr as dm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tia.bbg import LocalTerminal
import numpy as np
import matplotlib.pyplot as plt

# # will use this later when i want to use bbg data more 
# resp = LocalTerminal.get_reference_data('eurusd curncy', 'dflt_vol_surf_bid')

# resp = resp.as_frame()
# print(resp.iloc[0]['dflt_vol_surf_bid'])

mgr = dm.BbgDataManager()

# Quanltib Calendar Options
Calendar = ql.UnitedStates(ql.UnitedStates.Settlement)
EvaluationDate = ql.Date.todaysDate()
SettlementDate = Calendar.advance(EvaluationDate, ql.Period('2D'))   #Evaluation +2


currency_pair = "EURUSD"
notional = 1000000
ExpiryDate = ql.Date(15, 4, 2024)
datetime_expiry = datetime(ExpiryDate.year(),ExpiryDate.month(),ExpiryDate.dayOfMonth()).strftime("%Y%m%d")
Strike = 1.0991
Sigma = LocalTerminal.get_reference_data(currency_pair+ " Curncy","RK311",RK315=datetime_expiry).as_frame().iloc[0][0] / 100
Ccy1Rate = 0.03832
Ccy2Rate = 0.05301
OptionType = ql.Option.Call
short_long = 1 # 1 for long, -1 for short

Spot = mgr[currency_pair + " Curncy"].PX_LAST





DeliveryDate = Calendar.advance(ExpiryDate,ql.Period("2D"))
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
BsPrice = Option.NPV()* short_long


ql.Settings.instance().evaluationDate = EvaluationDate
print("Premium is:", Option.NPV()*notional/Spot)
print("Gamma is:", Option.gamma()*notional*Spot/100)
print("Vega is:", Option.vega()*notional*(1/100)/Spot)
print("Theta is :", Option.thetaPerDay()*notional/Spot)
print("Delta is:", Option.delta()*notional)
