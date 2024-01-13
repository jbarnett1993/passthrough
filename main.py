from __future__ import division
import pandas as pd
import tia.bbg.datamgr as dm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from scipy.stats import norm
import math

currency_pair = "EURUSD"

mgr = dm.BbgDataManager()


spot = mgr[currency_pair + " Curncy"].PX_LAST
# spot = 1.0951
strike = 1.0991
ccy1 = 0.03832 # EUR
ccy2 = 0.05301 # USD
sigma = 0.06397
days = 90 
t = days/365
f = 1.101070



def fxo_pricer(F, K, t, ccy2, sigma):
    d1 = (math.log(F/K) +  0.5*sigma**2*t ) / (sigma*math.sqrt(t))
    d2 = d1 - sigma*math.sqrt(t)
    c = math.exp(-ccy2*t)*(F*norm.cdf(d1) - K*norm.cdf(d2))
    p = math.exp(-ccy2*t)*(-F*norm.cdf(-d1) + K*norm.cdf(-d2))
    print(c, p ,d1, d2)

fxo_pricer(f,strike,t,ccy2,sigma)
