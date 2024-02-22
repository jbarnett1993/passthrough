import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import tia.bbg.datamgr as dm

class DataManager:
    def __init__(self):
        self.mgr = dm.BbgDataManager()

    def get_last_prices(self, tickers):
        return self.mgr[tickers].PX_LAST

class SpotCurve:
    def __init__(self, base_spot_tickers, spot_tenors):
        self.base_spot_tickers = base_spot_tickers
        self.spot_tenors = spot_tenors
        self.spot_curves = self.extend_base_tickers()

    def extend_base_tickers(self):
        spot_curves = {}
        for currency, base_ticker in self.base_spot_tickers.items():
            spot_curves[currency] = [f'{base_ticker}{tenor} Curncy' for tenor in self.spot_tenors]
        return pd.DataFrame.from_dict(spot_curves)

    def get_updated_spot_curves(self, data_manager, batch_size=100):
        n, _ = self.spot_curves.shape
        last_prices = []

        for i in range(0, n, batch_size):
            tickers_batch = self.spot_curves.iloc[i:min(i+batch_size, n), :].stack().tolist()
            prices = data_manager.get_last_prices(tickers_batch)
            prices = prices.reindex(tickers_batch)
            last_prices.extend(prices.values.tolist())

        last_prices = np.array(last_prices).reshape(-1, len(self.base_spot_tickers))
        updated_spot_curves = pd.DataFrame(last_prices, columns=self.spot_curves.columns)
        updated_spot_curves['tenor'] = self.spot_tenors
        updated_spot_curves.set_index('tenor', inplace=True)
        return updated_spot_curves

class ForwardRateCalculator:
    def __init__(self, curve_frequency, all_tenors):
        self.curve_frequency = curve_frequency
        self.all_tenors = all_tenors

    def interpolate_spot_curves(self, updated_spot_curves):
        interpolated_spot_curves = pd.DataFrame(index=self.all_tenors)
        for currency in updated_spot_curves.columns:
            original_tenors = updated_spot_curves.index.to_list()
            original_rates = updated_spot_curves[currency].values
            spline = CubicSpline(original_tenors, original_rates, bc_type='natural')
            interpolated_rates = spline(self.all_tenors)
            interpolated_spot_curves[currency] = interpolated_rates
        return interpolated_spot_curves

    def calculate_discount_factors(self, interpolated_spot_curves):
        discount_factors = 1 + (interpolated_spot_curves.div(pd.Series(self.curve_frequency), axis=1))/100
        compounding = pd.DataFrame(
            [[self.curve_frequency[currency] * tenor for currency in self.curve_frequency] for tenor in self.all_tenors],
            index=self.all_tenors,
            columns=self.curve_frequency.keys()
        )
        return 1 / discount_factors.pow(compounding)

    def calculate_forward_rates(self, discount_factors):
        fwds = pd.DataFrame({"point": [f"{i}y{j}y" for i in self.all_tenors for j in self.all_tenors if i + j <= max(self.all_tenors)]})
        fwds['t1'] = fwds['point'].str.extract('(\d+)y', expand=False).astype(int)
        fwds['t2'] = fwds['point'].str.extract('(\d+)y$', expand=False).astype(int) + fwds['t1']

        for currency in discount_factors.columns:
            fwds[currency] = fwds.apply(lambda row: self._calculate_forward_rate(row['t1'], row['t2'], currency, discount_factors), axis=1)
        fwds.set_index('point', inplace=True)
        return fwds

    def _calculate_forward_rate(self, t1, t2, currency, discount_factors):
        D1 = discount_factors.loc[t1, currency]
        D2 = discount_factors.loc[t2, currency]
        dT = t2 - t1
        return (np.log(D1 / D2) / dT) * 100

class ReportGenerator:
    def __init__(self, interpolated_spot_curves, forward_rates):
        self.interpolated_spot_curves = interpolated_spot_curves
        self.forward_rates = forward_rates

    def generate_pdf_report(self, filename='swap_rolldowns.pdf'):
        with PdfPages(filename) as pdf:            # Plotting interpolated spot curves
            fig, axs = plt.subplots(len(self.interpolated_spot_curves.columns) // 3 + 1, 3, figsize=(15, 10))
            for i, currency in enumerate(self.interpolated_spot_curves.columns):
                ax = axs[i // 3, i % 3]
                self.interpolated_spot_curves[currency].plot(ax=ax, title=f'{currency} Interpolated Spot Curve')
                ax.set_xlabel('Tenor')
                ax.set_ylabel('Rate')

            # Adjust layout and save the page
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            # Plotting forward rates
            for currency in self.forward_rates.columns.drop(['t1', 't2']):
                fig, ax = plt.subplots(figsize=(12, 8))
                self.forward_rates[currency].plot(ax=ax, title=f'{currency} Forward Rates')
                ax.set_xlabel('Forward Period')
                ax.set_ylabel('Rate')

                # Adjust layout and save the page
                plt.tight_layout()
                pdf.savefig()
                plt.close()

def main():
    base_spot_tickers = {
        'aud': 'ADSW', 'cad': 'CDSW', 'chf': 'SFSNT',
        'eur': 'EUSA', 'gbp': 'BPSWS', 'jpy': 'JYSO',
        'nzd': 'NDSWAP', 'sek': 'SKSW', 'usd': 'USOSFR'
    }

    curve_frequency = {
        'aud': 4, 'cad': 2, 'chf': 2,
        'eur': 2, 'gbp': 2, 'jpy': 2,
        'nzd': 4, 'sek': 4, 'usd': 4
    }

    spot_tenors = list(range(1, 11)) + [15, 20, 25, 30]
    all_tenors = list(range(1, 31))

    # Initialize DataManager and SpotCurve
    data_manager = DataManager()
    spot_curve = SpotCurve(base_spot_tickers, spot_tenors)

    # Get updated spot curves with last prices
    updated_spot_curves = spot_curve.get_updated_spot_curves(data_manager)

    # Initialize ForwardRateCalculator
    calculator = ForwardRateCalculator(curve_frequency, all_tenors)
    interpolated_spot_curves = calculator.interpolate_spot_curves(updated_spot_curves)
    discount_factors = calculator.calculate_discount_factors(interpolated_spot_curves)
    forward_rates = calculator.calculate_forward_rates(discount_factors)

    # Initialize and generate report
    report_generator = ReportGenerator(interpolated_spot_curves, forward_rates)
    report_generator.generate_pdf_report()

if __name__ == '__main__':
    main()