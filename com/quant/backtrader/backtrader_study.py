# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : backtrader_study
@Time         : 2024/5/31 11:32
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import backtrader as bt


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())