# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : strategy_single_average
@Time         : 2024/6/2 13:32
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import backtrader as bt


class SingleAverage(bt.Strategy):
    """
    原理
    单均线策略的核心指标是简单移动平均线，简称均线。均线由美国投资专家葛兰威尔所创立，由道氏股价分析理论的“三种趋势说”演变而来，
    从数字的变动中去预测股价未来短期、中期、长期的变动方向，为投资决策提供依据。

    按照周期长短划分，均线可以分为短期均线、中期均线、长期均线三种基本类型。
    1）短期均线：5、7、10，用于预测短期走势，MA5 和 MA10 又称为短期监测线；
    2）中期均线：20、30、60，用于预测中期走势，MA20 和 MA30 又称为警戒线， MA60 则称之为生死线；
    3）长期均线：120、250，用于长期走势，MA120 又称为确认线，MA250 则通常被看做反转线，又称为牛熊分界线。

    计算均线需要先设置均线周期，将均线周期设置为20日，就能进入下面的计算：
    (1)将第 1-20个交易日的收盘价求和，除以 20，就能得到第一个均价；
    (2)向后移动一个交易日，再将第 2-21 个交易日的收盘价求和，除以 20，得到第二个均价；
    (3)重复以上步骤，将得到的所有均价连成一条线，就生成了20日均线。

    ```
    backtrader:
        self.ma20 = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)
    ```

    单均线策略核心内容就是「简单判断股票价格的趋势以及买入、卖出的时间点」。
    理论依据是：葛兰威尔买卖八大法则
    1买： 平均线从下降逐渐走平转为上升，而股价从平均线的下方突破平均线时，为买进信号。
    1卖： 平均线走势从上升逐渐走平转为下跌，而股价从平均线的上方往下跌破平均线时，是卖出信号。

    """

    params = (("maperiod", 20), ('printlog', False),)  # 全局设定交易策略的参数

    def log(self, txt, dt=None, doprint=False):
        if self.params.printlog or doprint:
            ''' Logging function fot this strategy'''
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # 20日均线处于上升趋势
            # 当天收盘价大于20日均线，开盘价小于20日均线，说明是从下往上穿收阳线。买入！
            if self.sma[0] > self.sma[-1] > self.sma[-2] \
                    and self.dataclose[0] > self.sma[0] > self.dataopen[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:
            # 20日均线处于下跌趋势
            # 当天收盘价小于20日均线，开盘价大于20日均线，说明是从上往下穿收阴线。卖出！
            if self.sma[0] < self.sma[-1] < self.sma[-2] \
                    and self.dataclose[0] < self.sma[0] < self.dataopen[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
