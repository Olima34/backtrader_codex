from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import matplotlib
matplotlib.use("Agg")
import backtrader as bt

from indicators import ConfluenceOscillator


class TestStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=14)
        self.cci = bt.indicators.CCI(self.data, period=14)
        self.atr = bt.indicators.ATR(self.data, period=14)
        self.macd = bt.indicators.MACD(self.data.close)
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=20,
                                                      devfactor=2)
        self.confluence = ConfluenceOscillator(self.data)

    def log(self, txt, dt=None):
        """Fonction d'enregistrement pour la stratégie"""
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def next(self):
        self.log(
            f"Close: {self.data.close[0]:.5f}, "
            f"RSI: {self.rsi[0]:.2f}, "
            f"CCI: {self.cci[0]:.2f}, "
            f"ATR: {self.atr[0]:.5f}, "
            f"MACD: {self.macd.macd[0]:.5f}, "
            f"BB_Mid: {self.bollinger.mid[0]:.5f}, "
            f"BB_Top: {self.bollinger.top[0]:.5f}, "
            f"BB_Bot: {self.bollinger.bot[0]:.5f}, "
            f"Confluence: {self.confluence.osc[0]:.4f}"
        )


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)

    data = bt.feeds.GenericCSVData(
        dataname="datas/EURUSD_H1.csv",
        datetime=0,
        time=1,
        open=2,
        high=3,
        low=4,
        close=5,
        volume=6,
        dtformat="%Y.%m.%d",
        tmformat="%H:%M:%S",
        fromdate=datetime.datetime(2023, 1, 1),
        todate=datetime.datetime(2023, 12, 31),
        headers=True,
        separator="\t",
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    cerebro.run()
    # Les environnements sans interface graphique ne peuvent pas afficher les graphiques
