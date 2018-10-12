## 用 Scikit-Learn 实现 SVM 和 Kernel SVM

支持向量机（SVM）是一种监督学习分类算法。支持向量机提出于 20 世纪 60 年代在 90 年代得到了进一步的发展。然而，由于能取得很好的效果，最近才开始变得特别受欢迎。与其他机器学习算法相比，SVM 有其独特之处。


本文先简明地介绍支持向量机背后的理论和如何使用 Python 中的 Scikit-Learn 库来实现。然后我们将学习高级 SVM 理论如 Kernel SVM，同样会使用 Scikit-Learn 来实践。




### 简单 SVM

考虑二维线性可分数据，如图 1，典型的机器学习算法希望找到使得分类错误最小的分类边界。如果你仔细看图 1，会发现能把数据点正确分类的边界不唯一。两条虚线和一条实线都能正确分类所有点。


![](https://user-gold-cdn.xitu.io/2018/8/24/1656b52b11b94056?imageslim)



图 1：多决策边界
SVM 通过最大化所有类中的数据点到决策边界的最小距离的方法来确定边界，这是 SVM 和其他算法的主要区别。SVM 不只是找一个决策边界；它能找到最优决策边界。

能使所有类到决策边界的最小距离最大的边界是最优决策边界。如图 2 所示，那些离决策边界最近的点被称作支持向量。在支持向量机中决策边界被称作最大间隔分类器，或者最大间隔超平面。


![](https://user-gold-cdn.xitu.io/2018/8/24/1656b52b13a9809c?imageslim)


图 2：决策边界的支持向量

寻找支持向量、计算决策边界和支持向量之间的距离和最大化该距离涉及到很复杂的数学知识。本教程不打算深入到数学的细节，我们只会看到如何使用 Python 的 Scikit-Learn 库来实现 SVM 和 Kernel-SVM。


### 通过 Scikit-Learn 实现 SVM



我们的任务是通过四个属性来判断纸币是不是真的，四个属性是小波变换图像的偏度、图像的方差、图像的熵和图像的曲率。我们将使用 SVM 解决这个二分类问题。剩下部分是标准的机器学习流程。

#### 导入库

下面的代码导入所有需要的库：


    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    %matplotlib inline


#### 导入数据


数据可以从下面的链接下载：

[drive.google.com/file/d/13nw…](https://link.juejin.im/?target=https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2F13nw-uRXPY8XIZQxKRNZ3yYlho-CYm_Qt%2Fview)

数据的详细信息可以参考下面的链接：

[archive.ics.uci.edu/ml/datasets…](https://link.juejin.im/?target=https%3A%2F%2Farchive.ics.uci.edu%2Fml%2Fdatasets%2Fbanknote%2Bauthentication)

从 Google drive 链接下载数据并保存在你本地。这个例子中数据集保存在我 Windows 电脑的 D 盘 “Datasets” 文件夹下的 CSV 文件里。下面的代码从文件路径中读取数据。你可以根据文件在你自己电脑上的路径修改。

读取 CSV 文件的最简单方法是使用 pandas 库中的 read_csv 方法。下面的代码读取银行纸币数据记录到 pandas 的  dataframe:
