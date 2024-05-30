# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : run_strategy_3fall
@Time         : 2024/5/30 15:11
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import backtrader as bt
from com.quant.trade_strategy.strategy_3fall import Fall3Days
from com.quant.datasource.akshare_stock import AkshareStock

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.002)

    akshareDataSource = AkshareStock()
    stock_hfq_df = akshareDataSource.get_stock_history(symbol="600887", adjust="qfq")
    data = bt.feeds.PandasData(dataname = stock_hfq_df)
    cerebro.adddata(data)

    cerebro.addstrategy(Fall3Days)

    cerebro.run()
    print('\n4. 完成量化回测')
    print('\t 起始资金：%.2f' % cerebro.broker.startingcash)
    print('\t 剩余资金：%.2f' % cerebro.broker.getvalue())
    print('\n5. 绘制 BT 量化分析图形')
    cerebro.plot()