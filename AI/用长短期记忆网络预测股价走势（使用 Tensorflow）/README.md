
###  用长短期记忆网络预测股价走势（使用 Tensorflow）


![](https://user-gold-cdn.xitu.io/2019/3/7/16958396f1714e51?imageslim)


在本教程中，你将了解到如何使用被称作长短期记忆网络（LSTM）的时间序列模型。LSTM 模型在保持长期记忆方面非常强大。阅读这篇教程时，你将：

- 明白预测股市走势的动机；
- 下载股票数据 — 你将使用由 Alpha Vantage 或 Kaggle 收集的股票数据；
- 将数据划分为训练集和测试集，并将其标准化；
- 简要讨论一下为什么 LSTM 模型可以预测未来多步的情形；
- 使用现有数据预测股票趋势，并将结果可视化。

注意：请不要认为 LSTM 是一种可以完美预测股票趋势的可靠模型，也不要盲目使用它进行股票交易。我只是出于对机器学习的兴趣做了这个实验。在大部分情况下，这个模型的确能发现数据中的特定规律并准确预测股票的走势。但是否将其用于实际的股票市场取决于你自己。



### 为什么要用时间序列模型？

作为一名股民，如果你能对股票价格进行正确的建模，你就可以通过在合适的时机买入或卖出来获取利益。因此，你需要能通过一组历史数据来预测未来数据的模型——时间序列模型。

警告：股价本身因受到诸多因素影响而难以预测，这意味着你难以找到一种能完美预测股价的模型。并不只有我一人如此认为。普林斯顿大学的经济学教授 Burton Malkiel 在他 1973 年出版的《A Random Walk Down Wall Street》一书中写道：“如果股市足够高效，以至于人们能从公开的股价中知晓影响它的全部因素，那么人人都能像投资专业人士那样炒股”。

但是，请保持信心，用机器学习的方法来预测这完全随机的股价仍有一丝希望。我们至少能通过建模来预测这组数据的实际走势。换而言之，不必知晓股价的确切值，你只要能预测股价要涨还是要跌就万事大吉了。

    # 请确保你安装了这些包，并且能运行成功以下代码
    from pandas_datareader import data
    import matplotlib.pyplot as plt
    import pandas as pd
    import datetime as dt
    import urllib.request, json 
    import os
    import numpy as np
    import tensorflow as tf # TensorFlow 1.6 版本下测试通过
    from sklearn.preprocessing import MinMaxScaler

### 下载数据

你可以从以下来源下载数据：

Alpha Vantage。首先，你必须从 这个网站 获取所需的 API key。在此之后，将它的值赋给变量 api_key。
从 这个页面 下载并将其中的 Stocks 文件夹拷贝到你的工程目录下。

股价中包含几种不同的数据，它们是：

- 开盘价：一天中股票刚开盘时的价格；
- 收盘价：一天中股票收盘时的价格；
- 最高价：一天中股价的最大值；
- 最低价：一天中股价的最小值。

### 从 Alpha Vantage 获取数据

为了从 Alpha Vantage 上下载美国航空公司的股价数据用于分析，你要将行情显示代号 ticker 设置为 "AAL"。同时，你也要定义一个 url_string 变量来获取包含最近 20 年内的全部股价信息的 JSON 文件，以及文件保存路径 file_to_save。别忘了用你的 ticker 变量来帮助你命名你下载下来的文件。

接下来，设定一个条件：如果本地没有保存的数据文件，就从 url_string 指明的 URL 下载数据，并将其中的日期、最低价、最高价、交易量、开盘价和收盘价存入 Pandas 的 DataFrame df 中，再将其保存到 file_to_save；否则直接从本地读取 csv 文件就好了。

### 从 Kaggle 获取数据


从 Kaggle 上找到的数据是一系列 csv 表格，你不需要对它进行任何处理就可以直接读入 Pandas 的 DataFrame 中。确保你正确地将 Stocks 文件夹放在项目的主目录中。


### 读取数据

现在，将这些数据打印到 DataFrame 中吧！由于数据的顺序在时间序列模型中至关重要，所以请确保你的数据已经按照日期排好序了。

    # 按日期排序
    df = df.sort_values('Date')

    # 检查结果
    df.head()

### 数据可视化

看看你的数据，并从中找到伴随时间推移而具有的不同规律。


    plt.figure(figsize = (18,9))
    plt.plot(range(df.shape[0]),(df['Low']+df['High'])/2.0)
    plt.xticks(range(0,df.shape[0],500),df['Date'].loc[::500],rotation=45)
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Mid Price',fontsize=18)
    plt.show()


![](https://user-gold-cdn.xitu.io/2019/3/7/169583970d0164c3?imageslim)