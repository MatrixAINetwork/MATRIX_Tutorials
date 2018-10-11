## 背景

以著名的泰坦尼克号遇难者数据集为例。它收集了泰坦尼克号的乘客的个人信息以及是否从那场海难中生还。让我们试着用乘客的船票费用来预测一下他能否生还。

![](https://user-gold-cdn.xitu.io/2018/8/28/1657fc93d095f58b?imageslim)

泰坦尼克号上的 500 名乘客


假设你随机取了 500 名乘客。在这些样本中，30% 的人幸存下来。幸存乘客的平均票价为 100 美元，而遇难乘客的平均票价为 50 美元。现在，假设你有了一个新的乘客。你不知道他是否幸存，但你知道他买了一张 30 美元的票穿越大西洋。请你预测一下这个乘客是否幸存。



## 原理
好吧，你可能回答说这个乘客没能幸存。为什么？因为根据上文所取的乘客的随机子集中所包含的信息，本来的生还几率就很低（30%），而穷人的生还几率则更低。你会把这个乘客放在最可能的组别（低票价组）。这就是朴素贝叶斯分类器所要实现的。

## 分析

朴素贝叶斯分类器利用条件概率来聚集信息，并假设特征之间相对独立。这是什么意思呢？举个例子，这意味着我们必须假定泰坦尼克号的房间舒适度与票价无关。显然这个假设是错误的，这就是为什么我们将这个假设称为朴素（Naive）的原因。朴素假设使得计算得以简化，即使在非常大的数据集上也是如此。让我们来一探究竟。

朴素贝叶斯分类器本质上是寻找能描述给定特征条件下属于某个类别的概率的函数，这个函数写作 P(Survival | f1,…, fn)。我们使用贝叶斯定理来简化计算：


![](https://user-gold-cdn.xitu.io/2018/8/28/1657fc93ce6a589b?imageslim)


式 1：贝叶斯定理

P(Survival) 很容易计算，而我们构建分类器也不需要用到 P(f1,…, fn)，因此问题回到计算 P(f1,…, fn | Survival) 上来。我们应用条件概率公式来再一次简化计算：

式 2：初步拓展

上式最后一行的每一项的计算都需要一个包含所有条件的数据集。为了计算 {Survival, f_1, …, f_n-1} 条件下 fn 的概率（即 P(fn | Survival, f_1, …, f_n-1)），我们需要有足够多不同的满足条件 {Survival, f_1, …, f_n-1} 的 fn 值。这会需要大量的数据，并导致维度灾难。这时朴素假设(Naive Assumption)的好处就凸显出来了。假设特征是独立的，我们可以认为条件 {Survival, f_1, …, f_n-1} 的概率等于 {Survival} 的概率，以此来简化计算：

![](https://user-gold-cdn.xitu.io/2018/8/28/1657fc93cfe2872c?imageslim)

式 3：应用朴素假设

最后，为了分类，新建一个特征向量，我们只需要选择是否生还的值（1 或 0），令 P(f1, …, fn|Survival) 最高，即为最终的分类结果：

![](https://user-gold-cdn.xitu.io/2018/8/28/1657fc93c9f267f4?imageslim)


式 4：argmax 分类器

注意：常见的错误是认为分类器输出的概率是对的。事实上，朴素贝叶斯被称为差估计器，所以不要太认真地看待这些输出概率。



## 找出合适的分布函数


最后一步就是实现分类器。怎样为概率函数 P(f_i| Survival) 建立模型呢？在 Sklearn 库中有三种模型：

- 高斯分布：假设特征连续，且符合正态分布


![](https://user-gold-cdn.xitu.io/2018/8/28/1657fc944442f8a8?imageslim)


正态分布

- 多项式分布：适合离散特征。
- 贝努利分布：适合二元特征。


![](https://user-gold-cdn.xitu.io/2018/8/28/1657fc9449cce241?imageslim)


二项式分布

## Python 代码

接下来，基于泰坦尼克遇难者数据集，我们实现了一个经典的高斯朴素贝叶斯。我们将使用船舱等级、性别、年龄、兄弟姐妹数目、父母/子女数量、票价和登船口岸这些信息。


    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import time
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

    # 导入数据集
    data = pd.read_csv("data/train.csv")

    # 将分类变量转换为数字
    data["Sex_cleaned"]=np.where(data["Sex"]=="male",0,1)
    data["Embarked_cleaned"]=np.where(data["Embarked"]=="S",0,
                                  np.where(data["Embarked"]=="C",1,
                                           np.where(data["Embarked"]=="Q",2,3)
                                          )
                                 )
    # 清除数据集中的非数字值（NaN）
    data=data[[
    "Survived",
    "Pclass",
    "Sex_cleaned",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked_cleaned"
    ]].dropna(axis=0, how='any')

    # 将数据集拆分成训练集和测试集
    X_train, X_test = train_test_split(data, test_size=0.5, random_state=int(time.time()))


这个分类器的正确率为 80.95%。

