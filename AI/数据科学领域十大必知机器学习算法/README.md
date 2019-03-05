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

工具库：
[docs.scipy.org/doc/numpy/r…docs.scipy.org/doc/numpy-1…](https://link.juejin.im/?target=https%3A%2F%2Fdocs.scipy.org%2Fdoc%2Fnumpy-1.10.0%2Freference%2Fgenerated%2Fnumpy.polyfit.html)

入门教程：


[lagunita.stanford.edu/c4x/Humanit…](https://link.juejin.im/?target=https%3A%2F%2Flagunita.stanford.edu%2Fc4x%2FHumanitiesScience%2FStatLearning%2Fasset%2Flinear_regression.pdf)


#### 约束线性回归
最小二乘法在处理数据中的离群值、伪场和噪声会产生混淆。因此，在拟合一个数据集是需要约束来减少数据行中的方差。正确的方法是使用线性回归模型对数据集进行拟合，这样才能保证权重值不会出错。模型可以是 L1 规范（LASSO）或 L2（岭回归）或两者兼备（elastic regression）。均方损失最优化。

![](https://user-gold-cdn.xitu.io/2019/2/25/16924168244699a2?imageslim)


这类算法拟合回归线时有约束，可以避免过拟合，并降低模型中噪声维度。

工具库：

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Flinear_model.html)

入门教程：

[www.youtube.com/watch?v=5as…](https://link.juejin.im/?target=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D5asL5Eq2x0A)

[www.youtube.com/watch?v=jbw…](https://link.juejin.im/?target=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DjbwSCwoT51M)



#### K-means 聚类

这是大家最喜欢的无监督聚类算法。给定一组向量形式的数据点，可以通过它们之间的距离将其分为不同的群类。这是一种最大期望（EM）算法，它不停的移动群类的中心点，再根据群类中心对数据点进行聚类。这个算法的输入是需要生成的群类个数和聚类过程的迭代次数。


![](https://user-gold-cdn.xitu.io/2019/2/25/1692416834ee7b28?imageslim)


顾名思义，可以使用此算法使数据集分为 K 个集群。

工具库：

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.cluster.KMeans.html)

入门教程：

[www.youtube.com/watch?v=hDm…](https://link.juejin.im/?target=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DhDmNF9JG3lo)

[www.datascience.com/blog/k-mean…](https://link.juejin.im/?target=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DhDmNF9JG3lo)

#### 逻辑回归

逻辑回归是一种约束线性回归，加权具有非线性应用（常用 sigmod 函数，你也可使用 tanh），因此输出被严格限定为 +/- 类（在 sigmod 中即为 1 和 0）。使用梯度下降对交叉熵损失函数进行优化。请初学者注意：逻辑回归用于分类，而不是回归。你也可以将逻辑回归想成单层神经网络。逻辑回归会采用梯度下降或 L-BFGS 等方法进行训练。NLP 中它通常被称作最大熵分类器。

Sigmod 函数图像如下：

![](https://user-gold-cdn.xitu.io/2019/2/25/16924168223f4a44?imageslim)

可以使用LR来训练简单但非常健壮的分类器。


工具库：

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.linear_model.LogisticRegression.html)

入门教程：
[www.youtube.com/watch?v=-la…](https://link.juejin.im/?target=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D-la3q9d7AKQ)

#### SVM（支持向量机）

支持向量机是类似线性回归和逻辑回归的线性模型，它们之间的不同在于使用了不同的边际损失函数（支持向量的推导是我见过使用特征值计算的最优美的数学结果之一）。你可以使用 L-BFGS 甚至 SGD 这样的优化方法来优化损失函数。

![](https://user-gold-cdn.xitu.io/2019/2/25/1692416835e49acc?imageslim)

SVM 的另一创新之处在于数据到特征工程中的核心使用。如果你有很好的数据透视能力，你可以用更智能的核心替换原来还算不错的 RBF 并从中受益。

SVM 的一个独特之处是可以学习一个分类器。

支持向量机可以用来训练分类器（甚至是回归器）。


工具库：

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.svm.SVC.html)

入门教程：

[www.youtube.com/watch?v=eHs…](https://link.juejin.im/?target=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DeHsErlPJWUU)

注意：基于 SGD 的逻辑回归和 SVM 训练都是来源于 SKLearn 的 scikit-learn.org/stable/modu…，我常用这个，因为可以用公用接口同时检测逻辑回归和 SVM。你也可以使用小型批次利用 RAM 大小的数据集进行训练。


#### 前馈神经网络

这些本质上来说就是多层逻辑回归分类器。通过非线性函数（sigmod、tanh、relu + softmax 以及超酷的新玩意 selu）将各层的权重分割开。它也被成为多层感知机。前馈神经网络可以作为自编码器在分类器或者非监督特征学习中使用。

![](https://user-gold-cdn.xitu.io/2019/2/25/16924168357cd259?imageslim)

多层感知机

![](https://user-gold-cdn.xitu.io/2019/2/25/16924168da0ed15f?imageslim)