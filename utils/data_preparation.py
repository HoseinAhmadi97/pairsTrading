import pandas as pd
import numpy as np
from stockstats import StockDataFrame

class preparation():
    """
    A Class for preparation on price data and adding features of technical
    """
    def __init__(self, data):
        self.data = data
    
    #add indicatos features 
    def add_indicators(self, indicators_list = ['macd', 'rsi', 'cci', 'atr']):
        self.data = (
            self.data.merge(StockDataFrame(self.data).get(indicators_list)).set_index('date')
              .drop(columns = ['macds', 'macdh'])
              )
    
    #add momentume features
    def add_momentume(self, lags_list = [3, 7, 14, 21]):
        for lag in lags_list:
            self.data[f'log_return_{lag}'] = np.log(self.data['close'] / self.data['close'].shift(lag))
                
    #add labels to data
    def create_label(self, up_thre, down_thre):
        self.data['f_return_1'] = ((-1 * self.data['close'].diff(-1)) / self.data['close']).round(3)
        self.data['label'] = np.where(self.data['f_return_1']>up_thre, 1, self.data['f_return_1'])
        self.data['label'] = np.where(self.data['f_return_1']<down_thre, -1, self.data['label'])
        self.data['label'] = np.where((self.data['label']==1) | (self.data['label']==-1), self.data['label'], 0)