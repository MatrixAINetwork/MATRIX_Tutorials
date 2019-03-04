### 数据科学领域十大必知机器学习算法

![](https://user-gold-cdn.xitu.io/2019/2/25/169241652e1bf48c?imageslim)

机器学习从业者们各有各自不同的信仰。有些信奉“一剑破万法”（这里“剑”就是一种算法，而万法则是各种类型的数据），有些则认为“合适的工具做对的事”。他们中许多人也赞同“样样了解，精通一门”，他们在一个领域拥有丰富的专业知识，对机器学习的不同领域也略知一二。尽管如此，不可否认的是作为一名数据科学家，必须要对常见的机器学习算法了解一二，这将帮助我们在解决新问题时提供思路。本教程带你速览常见机器学习算法和相关资源，以便快速上手。

#### 主成分分析 (PCA)/SVD

PCA 是一种无监督方法，用于了解由向量构成数据集的全局属性。这里对数据点的协方差矩阵进行分析，以了解哪些维度（较多情况下）或数据点（部分情况下）更重要。比如，它们之间的方差较高，但与其他维度的协方差较低。考虑那些具有最高特征值的特征向量，它们就有可能是上层主成分（PC）。SVD 本质上也是一种计算有序成分的方法，但是不需要得到数据点的协方差即可获得。

![](https://user-gold-cdn.xitu.io/2019/2/25/169241651a1a1813?imageslim)

这类算法通过将数据降维来解决高维数据分析难题。

工具库：
[docs.scipy.org/doc/scipy/r…](https://link.juejin.im/?target=https%3A%2F%2Fdocs.scipy.org%2Fdoc%2Fscipy%2Freference%2Fgenerated%2Fscipy.linalg.svd.html)
[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.decomposition.PCA.html)

入门教程：
[arxiv.org/pdf/1404.11…](https://link.juejin.im/?target=https%3A%2F%2Farxiv.org%2Fpdf%2F1404.1100.pdf)

2a. 最小二乘法与多项式拟合

还记的你在大学时通常用于将直线或曲线拟合到点上以求得方程式的数值分析方法吗？可以在较小的低维数据集上使用它们来拟合机器学习中的曲线。（对于大型数据或者多个维度的数据集，最终结果可能会出现严重的过拟合。因此不必多费苦心了。）最小二乘法（OLS）有闭合解，所以不需要使用复杂的优化技术。

![](https://user-gold-cdn.xitu.io/2019/2/25/169241651b7e6d41?imageslim)

显而易见，这个算法只能用于拟合简单的曲线或回归。