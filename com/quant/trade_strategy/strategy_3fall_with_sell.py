# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : strategy_3fall_with_sell
@Time         : 2024/5/30 15:29
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import backtrader as bt


class Fall3DaysWithSell(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.bar_executed = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        # 检查是否有待执行的订单
        if self.order:
            return

        # 检查当前股票的仓位 position
        if not self.position:
            # 如果股票仓位为0，可以进行买入操作
            # 使用经典的三连跌买入策略
            if self.dataclose[0] < self.dataclose[-1]:
                # 当天收盘价低于前一天收盘价
                if self.dataclose[-1] < self.dataclose[-2]:
                    # 前一天收盘价低于前两天收盘价
                    # 符合三连跌买入
                    # 标记买入操作
                    self.log('执行买入，买入价格为：%.2f' % self.dataclose[0])
                    self.order = self.buy()  # 默认买入一手，方法很灵活，具体使用参考文档
        else:
            # 如果仓位 > 0，则需要先卖出
            # 前一个订单执行完成 5 个周期后才能进行卖出操作??????????这个周期的判断是什么????????????
            if len(self) >= (self.bar_executed + 5):
                # 默认卖出全部股票
                # 采用 track 模式设置订单，回避2张订单连续交易问题???
                self.order = self.sell()
