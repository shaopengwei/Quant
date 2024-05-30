# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : run_strategy_test
@Time         : 2024/5/29 17:04
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : None
"""

import matplotlib.pyplot as plt
import akshare as ak
import pandas as pd
import backtrader as bt
from datetime import datetime

from com.quant.strategy.strategy_test import StrategyTest

if __name__ == '__main__':
    cerebro = bt.Cerebro()  # 初始化回测系统

    # 获取回测数据
    # 利用 AKShare 获取股票的后复权数据
    stock_hfq_df = ak.stock_zh_a_hist(symbol="000001", adjust="hfq").iloc[:, 0:8]
    del stock_hfq_df['股票代码']
    # 按照 bt.feeds.pandasdata 列名重新命名
    stock_hfq_df.columns = bt.feeds.PandasData.datafields
    # 将日期列转换成 datetime类型，设置为索引，索引名为 datetime
    stock_hfq_df.index = pd.to_datetime(stock_hfq_df['datetime'])
    data = bt.feeds.PandasData(dataname=stock_hfq_df)
    cerebro.adddata(data)  # 将数据传入回测系统

    # 获取回测策略
    cerebro.addstrategy(StrategyTest)  # 将交易策略加载到回测系统中

    # 设置回测初始条件
    start_cash = 1000000
    cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
    cerebro.broker.setcommission(commission=0.002)  # 设置交易手续费为 0.2%

    # 运行回测系统
    cerebro.run()

    # 处理回测结果
    start_date = datetime(1991, 4, 3)  # 回测开始时间
    end_date = datetime(2020, 6, 16)  # 回测结束时间
    print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
    print(f"总资金: {round(cerebro.broker.getvalue(), 2)}")
    print(f"净收益: {round((cerebro.broker.getvalue() - start_cash), 2)}")

    # 画图
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    cerebro.plot(style='candlestick')
