## 使用 Python 进行自动化特征工程

### Python 中的特征工程自动化
#### 如何自动化地创建机器学习特征


机器学习正在利用诸如 H20、TPOT 和 auto-sklearn 等工具越来越多地从手工设计模型向自动化优化管道迁移。以上这些类库，连同如 random search 等方法一起，目的是在不需要人工干预的情况下找到适合于数据集的最佳模型，以此来简化器学习的模型选择和调优部分。然而，特征工程，作为机器学习管道中一个可以说是更有价值的方面，几乎全部是手工活。


特征工程，也称为特征创建，是从已有数据中创建出新特征并且用于训练机器学习模型的过程。这个步骤可能要比实际使用的模型更加重要，因为机器学习算法仅仅从我们提供给他的数据中进行学习，创建出与任务相关的特征是非常关键的（可以参照这篇文章 "[A Few Useful Things to Know about Machine Learning](https://link.juejin.im/?target=https%3A%2F%2Fhomes.cs.washington.edu%2F~pedrod%2Fpapers%2Fcacm12.pdf)" —— 《了解机器学习的一些有用的事》，译者注）。


通常来说，特征工程是一个漫长的手工过程，依赖于某个特定领域的知识、直觉、以及对数据的操作。这个过程可能会非常乏味并且最终获得的特性会被人类的主观性和花在上面的时间所限制。自动特征工程的目标是通过从数据集中创建许多候选特征来帮助数据科学家减轻工作负担，从这些创建了候选特征的数据集中，数据科学家可以选择最佳的特征并且用来训练。



#### 特征工程基础

特征工程意味着从分布在多个相关表格中的现有数据集中构建出额外的特征。特征工程需要从数据中提取相关信息，并且将其放入一个单独的表中，然后可以用来训练机器学习模型。

构建特征的过程非常耗时，因为每获取一项新的特征都需要很多步骤才能构建出来，尤其是当需要从多于一张表格中获取信息时。我们可以把特征创建的操作分成两类：转换和聚合。让我们通过几个例子的实战来看看这些概念。

一次转换操作仅作用于一张表，该操作能从一个或多个现有列中创建新特征（比如说 Python 中，一张表就如同 Pandas 库中的一个 DataFrame）。如下面的例子所示，假如我们有如下的一张客户（clients）信息表：

![](https://user-gold-cdn.xitu.io/2018/8/11/1652824cce6e2182?imageslim)


另一方面，聚合 则是跨表执行的，其使用了一对多关系进行分组观察，然后再计算统计数据。比如说，如果我们还有另外一张含有客户贷款信息的表格，这张表里可能每个客户都有多种贷款，我们就可以计算出每位客户端诸如贷款平均值、最大值、最小值等统计数据。

这个过程包括了根据客户进行贷款表格分组、计算聚合、然后把计算结果数据合并到客户数据中。如下代码展示了我们如何使用 Python 中的 [language of Pandas](https://link.juejin.im/?target=https%3A%2F%2Fpandas.pydata.org%2Fpandas-docs%2Fstable%2Findex.html) 库进行计算的过程：

    import pandas as pd

    # 根据客户 id （client id）进行贷款分组，并计算贷款平均值、最大值、最小值
    stats = loans.groupby('client_id')['loan_amount'].agg(['mean', 'max', 'min'])
    stats.columns = ['mean_loan_amount', 'max_loan_amount', 'min_loan_amount']

    # 和客户的 dataframe 进行合并
    stats = clients.merge(stats, left_on = 'client_id', right_index=True, how = 'left')

    stats.head(10)