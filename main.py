from rateslib import *
import tia.bbg.datamgr as dm
import tia.analysis.ta as ta
import tia.analysis.model as model
import pandas as pd
import numpy as np
from tia.bbg import LocalTerminal



curves = {
    'USD':'490', 
}
# 'EUR':'45'
curve_ids = []

class SpotCurve():
    pass

for ccy, curve in curves.items():
    curve_id = 'YCSW' + curve.zfill(4) + ' Index'
    curve_ids.append(curve_id)
resp = LocalTerminal.get_reference_data(curve_ids, 'CURVE_TENOR_RATES')
df = resp.as_frame()
tenors = df['CURVE_TENOR_RATES'].iloc[0]['Tenor'].to_list()
rates = df['CURVE_TENOR_RATES'].iloc[0]['Mid Yield'].to_list()

data = pd.DataFrame({"Term": tenors,
                     "Rate":rates})


data["Termination"] = [add_tenor(dt(2024,3,6), _, "F", "nyc") for _ in data["Term"]]
print(data)
# exit()
sofr = Curve(
    id="sofr",
    convention="Act360",
    calendar="nyc",
    modifier="MF",
    interpolation="log_linear",
    nodes={
        **{dt(2024,3,4): 1.0},
        # **{dt(2024, 3, 1): 1.0},  # <- this is today's DF,
        **{_: 1.0 for _ in data["Termination"]},
    }
)

sofr_args = dict(effective=dt(2024, 3, 6), spec="usd_irs", curves="sofr")

solver = Solver(
    curves=[sofr],
    instruments=[IRS(termination=_, **sofr_args) for _ in data["Termination"]],
    s=data["Rate"],
    instrument_labels=data["Term"],
    id="us_rates",
)


data["DF"] = [float(sofr[_]) for _ in data["Termination"]]


irs = IRS(
    effective=dt(2024, 3, 6),
    termination=dt(2025, 3, 6),
    notional=-100e6,
    curves="sofr",
    spec="usd_irs",
)

npv = irs.npv(solver=solver)
dv01 = irs.delta(solver=solver).sum()
swap_rate = irs.rate(solver=solver)
print(npv)
print(dv01)
print(swap_rate)