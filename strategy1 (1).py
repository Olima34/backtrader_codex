from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import backtrader as bt

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=14)
        self.cci = bt.indicators.CCI(self.data, period=14)
        self.atr = bt.indicators.ATR(self.data, period=14)
        self.macd = bt.indicators.MACD(self.data.close)
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=20, devfactor=2)
    
    def log(self, txt, dt=None):
        """Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def next(self):
        self.log(f'Close: {self.data.close[0]:.5f}, 
                 RSI: {self.rsi[0]:.2f}, 
                 CCI: {self.cci[0]:.2f}, 
                 ATR: {self.atr[0]:.5f}, 
                 MACD: {self.macd.macd[0]:.5f}, 
                 BB_Mid: {self.bollinger.mid[0]:.5f}, 
                 BB_Top: {self.bollinger.top[0]:.5f}, 
                 BB_Bot: {self.bollinger.bot[0]:.5f}')

cerebro = bt.Cerebro()

cerebro.addstrategy(TestStrategy)

data = bt.feeds.GenericCSVData(
    dataname='datas/EURUSD_H1.csv',
    
    datetime=0,  # DATE column 
    time=1,      # TIME column
    open=2,      # OPEN column
    high=3,      # HIGH column  
    low=4,       # LOW column
    close=5,     # CLOSE column
    volume=6,    # TICKVOL column
    
    dtformat='%Y.%m.%d',
    tmformat='%H:%M:%S',
    
    fromdate=datetime.datetime(2023, 1, 1),
    todate=datetime.datetime(2023, 12, 31),
    
    headers=True,
    
    separator='\t'
)

cerebro.adddata(data)

cerebro.broker.setcash(10000.0)

cerebro.run()
cerebro.plot()