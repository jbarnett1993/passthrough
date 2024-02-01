import numpy as np
import pandas as pd
from utils import get_pnl_stats


class Alpha2():

    def __init__(self,insts,dfs,start,end):
        self.insts = insts
        self.dfs = dfs
        self.start = start 
        self.end = end

    def init_portfolio_settings(self, trade_range):
        portfolio_df=pd.DataFrame(index=trade_range)\
            .reset_index()\
            .rename(columns={"index":"datetime"})
        portfolio_df.at[0,'capital'] = 10000
        return portfolio_df
    
    def compute_meta_info(self, trade_range):
        '''
        mean_12(neg(minus(const_1,div(open,close))))
        '''
        for inst in self.insts:
            df=pd.DataFrame(index=trade_range)
            inst_df = self.dfs[inst]
            alpha = -1 * (1-(inst_df.open/inst_df.close)).rolling(12).mean()



            self.dfs[inst] = df.join(self.dfs[inst]).fillna(method="ffill").fillna(method="bfill")
            self.dfs[inst]["ret"] = -1 + self.dfs[inst]["close"]/self.dfs[inst]["close"].shift(1)
            self.dfs[inst]["alpha"] = alpha
            self.dfs[inst]["alpha"] = self.dfs[inst]["alpha"].fillna(method="ffill")
            sampled = self.dfs[inst]["close"] != self.dfs[inst]["close"].shift(1).fillna(method="bfill")
            eligible = sampled.rolling(5).apply(lambda x: int(np.any(x))).fillna(0)
            self.dfs[inst]["eligible"] = eligible.astype(int) & (self.dfs[inst]["close"] > 0).astype(int) & (~pd.isna(self.dfs[inst]["alpha"]))
        return 
        
    def run_simulation(self):
        print("Running backtest")
        date_range = pd.date_range(start=self.start,end=self.end,freq="D")
        self.compute_meta_info(trade_range=date_range)
        portfolio_df = self.init_portfolio_settings(trade_range=date_range)
        for i in portfolio_df.index:
            date = portfolio_df.at[i,"datetime"]

            eligibles = [inst for inst in self.insts if self.dfs[inst].at[date,"eligible"]]
            non_eligibles = [inst for inst in self.insts if inst not in eligibles]
            #for any date that isnt day one we calculate pnls
            if i != 0:
                date_prev = portfolio_df.at[i-1,"datetime"]
                day_pnl, capital_ret =   get_pnl_stats(date=date,prev=date_prev,portfolio_df=portfolio_df,insts=self.insts,idx=i,dfs=self.dfs)

            #randomly generated alpha scores for now
            alpha_scores = {}
            import random
            for inst in eligibles:
                alpha_scores[inst] = self.dfs[inst].at[date,"alpha"]
            
            #if not in the eligibles group then we set weights and units to 0
            for inst in non_eligibles:
                portfolio_df.at[i,"{} w".format(inst)] = 0
                portfolio_df.at[i,"{} units".format(inst)] = 0

            absolute_scores = np.abs([score for score in alpha_scores.values()])
            forecast_chips = np.sum(absolute_scores)
            nominal_tot = 0
            for inst in eligibles:
                forecast = alpha_scores[inst]
                dollar_allocation = portfolio_df.at[i,"capital"] / forecast_chips if forecast_chips != 0 else 0  # always fully invested
                position = forecast * dollar_allocation / self.dfs[inst].at[date,"close"]
                portfolio_df.at[i, inst + " units"] = position 
                nominal_tot += abs(position * self.dfs[inst].at[date,"close"])

            for inst in eligibles:
                units = portfolio_df.at[i, inst + " units"]
                nominal_inst = units * self.dfs[inst].at[date,"close"]
                inst_w = nominal_inst / nominal_tot
                portfolio_df.at[i, inst + " w"] = inst_w
            
            portfolio_df.at[i, "nominal"] = nominal_tot
            portfolio_df.at[i, "leverage"] = nominal_tot / portfolio_df.at[i, "capital"]
            if i%100 == 0: print(portfolio_df.loc[i])
        return portfolio_df