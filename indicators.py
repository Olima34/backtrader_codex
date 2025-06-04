import backtrader as bt

class ConfluenceOscillator(bt.Indicator):
    lines = ('osc',)
    params = dict(
        rsi_period=14,
        cci_period=14,
        atr_period=14,
        bb_period=20,
        bb_devfactor=2,
        macd_me1=12,
        macd_me2=26,
        macd_signal=9,
        w_rsi=0.25,
        w_cci=0.25,
        w_macd=0.25,
        w_bb=0.15,
        w_atr=0.10,
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.p.rsi_period)
        self.cci = bt.indicators.CCI(self.data, period=self.p.cci_period)
        self.atr = bt.indicators.ATR(self.data, period=self.p.atr_period)
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.p.macd_me1,
            period_me2=self.p.macd_me2,
            period_signal=self.p.macd_signal,
        )
        self.boll = bt.indicators.BollingerBands(
            self.data.close,
            period=self.p.bb_period,
            devfactor=self.p.bb_devfactor,
        )
        self.atr_ema = bt.indicators.EMA(self.atr, period=self.p.atr_period)

    def next(self):
        rsi_norm = max(-1.0, min(1.0, (self.rsi[0] - 50.0) / 50.0))
        cci_norm = max(-1.0, min(1.0, self.cci[0] / 100.0))
        macd_norm = 0.0
        if self.macd.signal[0] != 0:
            macd_val = self.macd.macd[0] - self.macd.signal[0]
            macd_norm = max(-1.0, min(1.0, macd_val / abs(self.macd.signal[0])))
        bb_range = self.boll.top[0] - self.boll.mid[0]
        bb_norm = (self.data.close[0] - self.boll.mid[0]) / bb_range if bb_range != 0 else 0.0
        bb_norm = max(-1.0, min(1.0, bb_norm))
        atr_norm = 0.0
        if self.atr_ema[0] != 0:
            atr_norm = (self.atr[0] - self.atr_ema[0]) / self.atr_ema[0]
        atr_norm = max(-1.0, min(1.0, atr_norm))

        total_weight = self.p.w_rsi + self.p.w_cci + self.p.w_macd + self.p.w_bb + self.p.w_atr
        osc = (
            self.p.w_rsi * rsi_norm
            + self.p.w_cci * cci_norm
            + self.p.w_macd * macd_norm
            + self.p.w_bb * bb_norm
            + self.p.w_atr * atr_norm
        ) / total_weight
        self.lines.osc[0] = osc
