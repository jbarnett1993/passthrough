from __future__ import division
import pandas as pd
import tia.bbg.datamgr as dm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from scipy.stats import norm
import math

currency_pair = "EURUSD"

spot = 1.1
f = 1.101070
strike = 1.101
ccy1 = 0.05 # EUR
ccy2 = 0.1 # USD
vol = 0.1
days = 7
t = days/365




def fxo_pricer(F, K, t, ccy2, sigma):
    d1 = (math.log(F/K) +  0.5*sigma**2*t ) / (sigma*math.sqrt(t))
    d2 = d1 - sigma*math.sqrt(t)
    c = math.exp(-ccy2*t)*(F*norm(d1) - K*norm(d2))
    p = math.exp(-ccy2*t)*(-F*norm(-d1) + K*norm(-d2))
    print(c, p ,d1, d2)


fxo_pricer(f,strike,t,ccy2,sigma=vol)
