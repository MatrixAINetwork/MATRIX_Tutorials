
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


这幅图包含了很多信息。我特意选取了这家公司的股价图，因为它包含了股价的多种不同规律。这将使你的模型更健壮，也让它能更好地预测不同情形下的股价。

另一件值得注意的事情是 2017 年的股价远比上世纪七十年代的股价高且波动更大。因此，你要在数据标准化的过程中，注意让这些部分的数据落在相近的数值区间内。


### 将数据划分为训练集和测试集

首先通过对每一天的最高和最低价的平均值来算出 mid_prices。

    # 首先用最高和最低价来算出中间价
    high_prices = df.loc[:,'High'].as_matrix()
    low_prices = df.loc[:,'Low'].as_matrix()
    mid_prices = (high_prices+low_prices)/2.0

然后你就可以划分数据集了。前 11000 个数据属于训练集，剩下的都属于测试集。

    train_data = mid_prices[:11000] 
    test_data = mid_prices[11000:]


接下来我们需要一个换算器 scaler 用于标准化数据。MinMaxScalar 会将所有数据换算到 0 和 1 之间。同时，你也可以将两个数据集都调整为 [data_size, num_features] 的大小。


    # 将所有数据缩放到 0 和 1 之间
    # 在缩放时请注意，缩放测试集数据时请使用缩放训练集数据的参数
    # 因为在测试前你是不应当知道测试集数据的
    scaler = MinMaxScaler()
    train_data = train_data.reshape(-1,1)
    test_data = test_data.reshape(-1,1)


上面我们注意到不同年代的股价处于不同的价位，如果不做特殊处理的话，在标准化后的数据中，上世纪的股价数据将非常接近于 0。这对模型的学习过程没啥好处。所以我们将整个时间序列划分为若干个区间，并在每一个区间上做标准化。这里每一个区间的长度取值为 2500。

提示：因为每一个区间都被独立地初始化，所以在两个区间的交界处会引入一个“突变”。为了避免这个“突变”给我们的模型带来大麻烦，这里的每一个区间长度不要太小。

本例中会引入 4 个“突变”，鉴于数据有 11000 组，所以它们无关紧要。

    # 使用训练集来训练换算器 scaler，并且调整数据使之更平滑
    smoothing_window_size = 2500
    for di in range(0,10000,smoothing_window_size):
    scaler.fit(train_data[di:di+smoothing_window_size,:])
    train_data[di:di+smoothing_window_size,:] = scaler.transform(train_data[di:di+smoothing_window_size,:])

    # 标准化所有的数据
    scaler.fit(train_data[di+smoothing_window_size:,:])
    train_data[di+smoothing_window_size:,:] = scaler.transform(train_data[di+smoothing_window_size:,:])

将数据矩阵调整回 [data_size] 的形状。

    # 重新调整测试集和训练集
    train_data = train_data.reshape(-1)

    # 将测试集标准化
    test_data = scaler.transform(test_data).reshape(-1)

为了产生一条更平滑的曲线，我们使用一种叫做指数加权平均的算法。

注意：我们只使用训练集来训练换算器 scaler，否则在标准化测试集时将得到不准确的结果。

注意：只允许对训练集做平滑处理。


    # 应用指数加权平均
    # 现在数据将比之间更为平滑
    EMA = 0.0   
    gamma = 0.1
    for ti in range(11000):
    EMA = gamma*train_data[ti] + (1-gamma)*EMA
    train_data[ti] = EMA

    # 用于可视化和调试
    all_mid_data = np.concatenate([train_data,test_data],axis=0)


### 评估结果

为了评估训练出来的模型，我们将计算其预测值与真实值的均方误差（MSE）。将每一个预测值与真实值误差的平方取均值，即为这个模型的均方误差。


### 股价建模中的平均值

取平均值在预测单步上效果不错，但对股市预测这种需要预测许多步的情形不适用。


### 使用 LSTM 预测未来股价走势

长短期记忆网络模型是非常强大的基于时间序列的模型，它们能向后预测任意步。一个 LSTM 模块（或者一个 LSTM 单元）使用 5 个重要的参数来对长期和短期数据建模。


- 单元状态（）- 这代表了单元存储的短期和长期记忆；
- 隐藏状态（）- 这是根据当前输入、以前的隐藏状态和当前单元输入计算的用于预测未来股价的输出状态信息 。此外，隐藏状态还决定着是否- 只使用单元状态中的记忆（短期、长期或两者都使用）来进行下一次预测；
- 输入门（）- 从输入门流入到单元状态中的信息；
- 遗忘门（）- 从当前输入和前一个单元状态流到当前单元状态的信息；
- 输出门（）- 从当前单元状态流到隐藏状态的信息，这决定了 LSTM 接下来使用的记忆类型。

下图展示了一个 LSTM 单元。

![](https://user-gold-cdn.xitu.io/2019/3/7/16958396ef9e84da?imageslim)


### 数据生成器
最简单的想法是将总量为 N 的数据集，平均分割成 N/b 个序列，每个序列包含 b 个数据点。然后我们假想若干个指针，它们指向每一个序列的第一个元素。然后我们就可以开始采样生成数据了。我们将当前段的指针指向的元素下标当作输入，并在其后面的 1~5 个元素中随机挑选一个作为正确的预测值，因为模型并不总是只预测紧靠当前时间点的后一个数据。这样可以有效避免过拟合。每一次取样之后，我们将指针的下标加一，并开始生成下一个数据点。

![](https://user-gold-cdn.xitu.io/2019/3/7/16958396f6f5be97?imageslim)

### 定义超参数
在本节中，我们将定义若干个超参数。D 是输入的维数。因为你使用前一天的股价来预测后面的股价，所以 D 应当是 1。

num_unrollings 表示单个步骤中考虑的连续时间点个数，越大越好。

然后是 batch_size。它是在单个时间点中考虑的数据样本数量。它越大越好，因为选取的样本数量越大，模型可以参考的数据也就更多。
最后是 num_nodes 决定了每个单元中包含了多少隐藏神经元。在本例中，网络中包含三层 LSTM。

