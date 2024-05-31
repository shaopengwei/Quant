# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : run_strategy_empty
@Time         : 2024/5/30 13:48
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import backtrader as bt
from com.quant.trade_strategy.strategy_empty import Empty
from com.quant.datasource.akshare_stock import AkshareStock

if __name__ == '__main__':
    print('\n1. 设置 BT 量化回测程序入口')
    cerebro = bt.Cerebro()

    print('\n2. 设置 BT 回测初始参数及策略')
    print('\n\t2-1. 设置 BT 回测初始参数：起始资金等')
    dmoney0 = 100000.0
    cerebro.broker.setcash(dmoney0)
    dcash0 = cerebro.broker.startingcash

    print('\n\t2-2. 设置数据')
    akshareDataSource = AkshareStock()
    stock_hfq_df = akshareDataSource.get_stock_history(symbol="600887", adjust="qfq")
    data = bt.feeds.PandasData(dataname = stock_hfq_df)
    cerebro.adddata(data)  # 将数据传入回测系统

    print('\n\t2-3. 添加 BT 量化回测策略')
    cerebro.addstrategy(Empty)

    print('\n3. 调用 BT 回测入口程序，开始执行 run 量化策略')
    cerebro.run()

    print('\n4. 完成量化回测')

    print('\t 起始资金：%.2f' % dcash0)
    print('\t 剩余资金：%.2f' % cerebro.broker.getvalue())

    print('\n5. 绘制 BT 量化分析图形')
    cerebro.plot()

