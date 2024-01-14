import QuantLib as ql
import pandas as pd
import tia.bbg.datamgr as dm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tia.bbg import LocalTerminal
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


class vanilla():
    pass

class straddle():
    def __init__(self, spot, strike, expiry, vol, ccy1rate, ccy2rate, notional, direction=1):
       self.direction = direction
       call_payoff = ql.PlainVanillaPayoff(ql.Option.Call, strike)
       call_exercise = ql.EuropeanExercise(expiry)
       self.call = ql.VanillaOption(call_payoff,call_exercise)

       put_payoff = ql.PlainVanillaPayoff(ql.Option.Put, strike)
       put_exercise = ql.EuropeanExercise(expiry)
       self.put = ql.VanillaOption(put_payoff,put_exercise)

       SpotHandle = ql.QuoteHandle(ql.SimpleQuote(spot))
       VolHandle = ql.QuoteHandle(ql.SimpleQuote,vol)
       ccy1ratehandle = ql.QuoteHandle(ql.SimpleQuote(ccy1rate))
       ccy2ratehandle = ql.QuoteHandle(ql.SimpleQuote(ccy2rate))
       calendar = ql.UnitedStates(ql.UnitedStates.Settlement)
       
       DayCountVolatility = ql.ActualActual(ql.ActualActual.ISDA)

       DayCountRate = ql.Actual360
       ccy1riskfreerate = ql.YieldTermStructureHandle(ql.FlatForward(0, calendar, ccy1ratehandle, DayCountRate))
       ccy2riskfreerate = ql.YieldTermStructureHandle(ql.FlatForward(0, calendar, ccy2ratehandle, DayCountRate))
       Volatility = ql.BlackVolTermStructure(ql.BlackConstantVol(0, calendar, VolHandle,DayCountVolatility)) 
        
       GKProcess = ql.GarmanKohlagenProcess(SpotHandle, ccy1riskfreerate, ccy2riskfreerate, Volatility)


       self.call.setPricingEngine(ql.AnalyticEuropeanEngine(GKProcess))
       self.put.setPricingEngine(ql.AnalyticEuropeanEngine(GKProcess))
    

    def calculate_greeks(self):

      premium = self.call.NPV()*self.notional/self.spot 
      return premium