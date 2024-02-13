from tia.bbg import LocalTerminal
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime

class DataManager:
    def __init__(self, events, currencies):
        self.events = events
        self.currencies = currencies
        self.today = datetime.today()
        self.max_date = self.today + relativedelta(days=7)

    def get_eligible_events(self):
        eligibles = LocalTerminal.get_reference_data(self.events, ['ECO_RELEASE_DT'])
        eligibles_df = eligibles.as_frame()
        eligibles_df = eligibles_df[eligibles_df['ECO_RELEASE_DT'] < self.max_date]
        return eligibles_df.index.to_list()

    def get_data(self):
        sids = self.get_eligible_events()
        resp = LocalTerminal.get_reference_data(sids, [
            'COUNTRY', 'REGION_OR_COUNTRY', 'LONG_COMP_NAME', 'RELEVANCE_VALUE', 
            'ECO_FUTURE_RELEASE_DATE', 'ECO_RELEASE_DT', 'RT_BN_SURVEY_AVERAGE', 
            'PREVIOUS_TRADING_DATE', 'INDX_FREQ'], ignore_field_error=1)
        df = resp.as_frame()
        df['ECO_RELEASE_DT'] = pd.to_datetime(df['ECO_RELEASE_DT'])
        df = df[df['RELEVANCE_VALUE'] > 80]
        df = df[df['ECO_FUTURE_RELEASE_DATE'].str.contains(':')]
        df['ECO_FUTURE_RELEASE_DATE'] = pd.to_datetime(df['ECO_FUTURE_RELEASE_DATE'])
        df['PREVIOUS_TRADING_DATE'] = pd.to_datetime(df['PREVIOUS_TRADING_DATE'])
        df = df[~df['COUNTRY'].isin(["RU"])]
        df = df[~df['REGION_OR_COUNTRY'].isin(["UNITED STATES", "BRITAIN"])]
        df['currency'] = df['REGION_OR_COUNTRY'].map(self.currencies)
        df = df.sort_values(by='ECO_FUTURE_RELEASE_DATE')
        return df


class TickDataProcessor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def get_tick_data(self):
        tick_data = []
        for index, row in self.dataframe.iterrows():
            sid = row['currency']
            next_release = row['ECO_FUTURE_RELEASE_DATE']
            prior_release = row['PREVIOUS_TRADING_DATE']
            start = datetime.combine(prior_release.date(), next_release.time())
            end = start + relativedelta(minutes=1)
            f = LocalTerminal.get_intraday_tick(sid, "TRADE", start, end).as_frame()
            if not f.empty:
                initial_price = f.iloc[0]['value']
                end_price = f.iloc[-1]['value']
                pct_change_bps = ((initial_price - end_price) / initial_price) * 10000
            else:
                pct_change_bps = np.nan
            tick_data.append(pct_change_bps)
        return tick_data
        
        
# Instantiate the DataManager with events and currencies
data_manager = DataManager(events, currencies)
df = data_manager.get_data()

# Process tick data
tick_processor = TickDataProcessor(df)
tick_data = tick_processor.get_tick_data()