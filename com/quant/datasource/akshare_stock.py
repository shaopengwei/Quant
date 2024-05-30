# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Package      : 
@FileName     : akshare_stock
@Time         : 2024/5/30 14:22
@Author       : shaopengwei@hotmail.com
@License      : (C)Copyright 2024
@Version      : 1.0.0
@Desc         : akshare 数据源获取股票数据
"""

import pandas as pd
import akshare as ak
import backtrader as bt


class AkshareStock:

    def get_stock_history(self,
                          symbol: str = "000001",
                          period: str = "daily",
                          start_date: str = "19700101",
                          end_date: str = "20500101",
                          adjust: str = "",
                          timeout: float = None
                          ) -> pd.DataFrame:
        # 从 ak 获取股票数据，截取前8列
        stock_df = ak.stock_zh_a_hist(symbol, period, start_date, end_date, adjust, timeout).iloc[:, 0:8]
        del stock_df['股票代码']
        # 按照 bt.feeds.pandasdata 列名重新命名
        stock_df.columns = [
            "datetime",
            "open",
            "close",
            "high",
            "low",
            "volume",
            "openinterest"
        ]
        # 将日期列转换成 datetime 类型，设置为索引，索引名为 datetime
        stock_df.index = pd.to_datetime(stock_df['datetime'])
        return stock_df
