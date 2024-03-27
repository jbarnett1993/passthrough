from rateslib import *
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
import pandas as pd
import numpy as np
from tia.bbg import LocalTerminal
import datetime
# from pandas.tseries.offsets import Bday

today = dt.today()
test_date = add_tenor(dt.today(),"2b","F",get_calendar("nyc"))
oneyear = add_tenor(test_date,"1Y","F",get_calendar("nyc"))

curves = {
    'USD':'490','EUR':'45' 
}
curve_ids = []

# refactor this code so that it outputs {ccy} data as it loops through the curves

for ccy, curve in curves.items():
    curve_id = 'YCSW' + curve.zfill(4) + ' Index'
    curve_ids.append(curve_id)
resp = LocalTerminal.get_reference_data(curve_ids, 'CURVE_TENOR_RATES')
df = resp.as_frame()
tenors = df['CURVE_TENOR_RATES'].iloc[0]['Tenor'].to_list()
rates = df['CURVE_TENOR_RATES'].iloc[0]['Mid Yield'].to_list()

data = pd.DataFrame({"Term": tenors,
                     "Rate":rates})

data["Termination"] = [add_tenor(test_date, _, "F", "nyc") for _ in data["Term"]]


# can i write a global curve here or do i need to write all separate curves, i.e euruer, usdusd, noknok (lol)?

usdusd = Curve(
    id="usdusd",
    convention="Act360",
    calendar="nyc",
    modifier="MF",
    interpolation="log_linear",
    nodes={
        **{today: 1.0},
        # **{dt(2024, 3, 1): 1.0},  # <- this is today's DF,
        **{_: 1.0 for _ in data["Termination"]},
    }
)


usd_kws = dict(
    effective=today,
    spec="usd_irs",
    curves="usdusd",
)


usdsolver = Solver(
    curves=[usdusd],
    instruments=[IRS(termination=_, **usd_kws) for _ in data["Termination"]],
    s=data["Rate"],
    instrument_labels=data["Term"],
    id="us_rates",
)