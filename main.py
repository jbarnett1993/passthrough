import QuantLib as ql


Spot = 1.1
Strike = 1.101
Sigma = 10/100
Ccy1Rate = 5/100
Ccy2Rate = 10/100
OptionType = ql.Option.Call

#Option dates in quantlib objects
EvaluationDate = ql.Date(3, 1,2022)
SettlementDate = ql.Date(5, 1, 2022) #Evaluation +2
ExpiryDate = ql.Date(10, 1, 2022) #Evaluation + term which is 1 week
DeliveryDate = ql.Date(12, 1, 2022) #Expiry +2
NumberOfDaysBetween = ExpiryDate - EvaluationDate
#print(NumberOfDaysBetween)

#Generate continuous interest rates
EurRate = Ccy1Rate
UsdRate = Ccy2Rate

#Create QuoteHandle objects. Easily to adapt later on.
#You can only access SimpleQuote objects. When you use setvalue, you can change it.
#These global variables will then be used in pricing the option.
#Everything will be adaptable except for the strike.
SpotGlobal = ql.SimpleQuote(Spot)
SpotHandle = ql.QuoteHandle(SpotGlobal)
VolGlobal = ql.SimpleQuote(Sigma)
VolHandle = ql.QuoteHandle(VolGlobal)
UsdRateGlobal = ql.SimpleQuote(UsdRate)
UsdRateHandle = ql.QuoteHandle(UsdRateGlobal)
EurRateGlobal = ql.SimpleQuote(EurRate)
EurRateHandle = ql.QuoteHandle(EurRateGlobal)

#Settings such as calendar, evaluationdate; daycount
Calendar = ql.UnitedStates()
ql.Settings.instance().evaluationDate = EvaluationDate
DayCountRate = ql.Actual360()
DayCountVolatility = ql.ActualActual()

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