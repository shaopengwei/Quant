# 包
com.quant.backtrader

# 使用说明
回测框架的选择基于开源、社区活跃度、使用难易方面考虑，选择 backtrader

[backtrader 官网](https://www.backtrader.com/)

[backtrader 使用文档](https://www.backtrader.com/docu/)

[backtrader 中文教程](https://blog.csdn.net/yaoyefengchen/article/details/135464834)

基于 backtrader 方法，实现对业务需求的封装

开发过程中应秉持 **开源精神**，将有用合理的修改集成提交到 backtrader 开源社区，
将发现的 bug 和代码优化提交到开源社区，利用好社区资源学习和交流

# Backtrader 学习笔记
## 1.模块介绍

![Backtrader](https://img-blog.csdnimg.cn/img_convert/5f7f367f514a6fdef46104c2ff59eb94.png)

## 2.Backtrader 数据

Backtrader 使用 data feeds 接收外部数据。 Backtrader 底层数据采用了特殊的内部格式，就是Lines，
用于存储和传递内部数据流。 OHLC 金融数据中的每一列相当于 Lines 的数据组。

## 3.Backtrader 策略运行逻辑
按照时间顺序，以bar为单位读取 data feeds 数据，每一个bar执行策略的next方法，
next方法中可以下订单、 通知交易员执行订单等操作。

>1.Deliver any store notifications 
>>2.Ask data feeds to deliver the next set of ticks/bars
>>>3.Notify the strategy about queued broker notifications of orders, trades and cash/value
>>>>4.Tell the broker to accept queued orders and execute the pending orders with the new data
>>>>>5.Call the strategies’ ***next*** method to let the strategy evaluate the new data (and maybe issue orders which are queued in the broker)
>>>>>>6.Tell any writers to write the data to its target

# 接口列表