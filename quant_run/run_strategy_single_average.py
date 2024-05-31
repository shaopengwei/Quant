# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : run_strategy_single_average
@Time         : 2024/6/2 14:05
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import matplotlib.pyplot as plt
import backtrader as bt
from datetime import datetime
from com.quant.datasource.akshare_stock import AkshareStock
from constant.stock_code import StockCode

from com.quant.trade_strategy.strategy_single_average import SingleAverage

if __name__ == '__main__':
    cerebro = bt.Cerebro()  # 初始化回测系统

    # 获取回测数据
    # 利用 AKShare 获取股票的后复权数据
    akshareDataSource = AkshareStock()
    stock_hfq_df = akshareDataSource.get_stock_history(symbol='002572',
                                                       adjust="hfq",
                                                       start_date="20220101",
                                                       end_date="20230101")
    data = bt.feeds.PandasData(dataname=stock_hfq_df)
    cerebro.adddata(data)  # 将数据传入回测系统

    # 获取回测策略
    cerebro.addstrategy(SingleAverage)  # 将交易策略加载到回测系统中

    # 设置回测初始条件
    start_cash = 1000000
    cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
    cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)  # 每次交易100股

    # 运行回测系统
    cerebro.run()

    # 处理回测结果
    start_date = datetime(2019, 1, 1)  # 回测开始时间
    end_date = datetime(2024, 1, 1)  # 回测结束时间
    print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
    print(f"总资金: {round(cerebro.broker.getvalue(), 2)}")
    print(f"净收益: {round((cerebro.broker.getvalue() - start_cash), 2)}")

    # 画图
    cerebro.plot(style='candlestick')
