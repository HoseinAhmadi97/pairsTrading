import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class backtest_performance():
    def __init__(self, backtest_df):
        self.backtest_df = backtest_df
        
    def plot_signal(self, signal_column, symbol):
        buys = self.backtest_df[self.backtest_df[signal_column]==1]
        sells = self.backtest_df[self.backtest_df[signal_column]==-1]

        plt.figure(figsize=(20, 5))
        plt.plot(self.backtest_df[['close']])
        plt.plot(buys.index, buys['close'], '^', markersize=10, color='g')
        plt.plot(sells.index, sells['close'], 'v', markersize=10, color='r')
        plt.title(signal_column + f': {symbol}')
        plt.show()
    
    def get_portfolio_performance(self, signal_column):

        self.backtest_df['change_net_no'] = self.backtest_df[signal_column].apply(lambda x: 100 if x==1 else (-100 if x==-1 else 0))
        self.backtest_df['net_no'] = self.backtest_df['change_net_no'].cumsum()

        self.backtest_df['cash_flows'] = -1 * self.backtest_df['change_net_no'] * self.backtest_df['close']
        self.backtest_df['buy_cash_flows'] = np.where(self.backtest_df['cash_flows']<0, self.backtest_df['cash_flows'], 0)
        self.backtest_df['whole_cash_flows'] = self.backtest_df['cash_flows'].cumsum()
        self.backtest_df['whole_buy_cash_flows'] = self.backtest_df['buy_cash_flows'].cumsum()
        self.backtest_df['daily_offset_value'] = self.backtest_df['net_no'] * self.backtest_df['close']
        self.backtest_df['daily_offset_buy'] = np.where(self.backtest_df['daily_offset_value']>0, 0,
                                                        self.backtest_df['daily_offset_value'])
        self.backtest_df['portfolio_profit'] = (self.backtest_df['whole_cash_flows'] + self.backtest_df['daily_offset_value'])
        self.backtest_df['whole_portfolio_return'] = (self.backtest_df['portfolio_profit']/
                                                (-self.backtest_df['whole_buy_cash_flows'] - 
                                                 self.backtest_df['daily_offset_buy']))
        self.backtest_df['daily_portfolio_return'] = ((1 + self.backtest_df['whole_portfolio_return']) / 
                                                (1 + self.backtest_df['whole_portfolio_return']).shift())-1
        
    def get_performance_df(self):
        return self.backtest_df

    def plot_portfolio_metrics(self):
        fig, ax = plt.subplots(2, 2, figsize=(13, 6))
        fig.tight_layout()
        ax[0, 0].plot(self.backtest_df['whole_portfolio_return'].fillna(0), label = 'return')
        ax[0, 0].set_title('portfolio-return')
        ax[0, 1].plot(self.backtest_df['portfolio_profit'].fillna(0), label = 'profit')
        ax[0, 1].set_title('portfolio-profit')
        ax[1, 0].plot(self.backtest_df['close'].fillna(0), label = 'close-price')
        ax[1, 0].set_title('close-price')
        ax[1, 1].plot(self.backtest_df['net_no'].fillna(0), label = 'net_no')
        ax[1, 1].set_title('not-of-stocks-number')
        plt.subplots_adjust(wspace=0.1, hspace=0.5)
        plt.show()
        
    def get_sharp_ratio(self, N, rf):
        return_series = self.backtest_df['daily_portfolio_return']
        mean = ((1+return_series.mean()) ** (N) -1) -rf
        sigma = return_series.std() * np.sqrt(N)
        return mean / sigma