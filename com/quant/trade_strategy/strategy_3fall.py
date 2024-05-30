# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : strategy_3fall
@Time         : 2024/5/30 15:03
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import backtrader as bt


class Fall3Days(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        # 使用经典的三连跌买入策略
        if self.dataclose[0] < self.dataclose[-1]:
            # 当天收盘价低于前一天收盘价
            if self.dataclose[-1] < self.dataclose[-2]:
                # 前一天收盘价低于前两天收盘价
                # 符合三连跌买入
                # 标记买入操作
                self.log('执行买入，买入价格为：%.2f' % self.dataclose[0])
                self.buy() # 默认买入一手，方法很灵活，具体使用参考文档
