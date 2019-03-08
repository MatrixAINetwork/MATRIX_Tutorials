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

作为自编码器的前馈神经网络

前馈神经网络可以用来训练分类器或者作为自编码器提取特征。

工具库：

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.neural_network.MLPClassifier.html%23sklearn.neural_network.MLPClassifier)

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.neural_network.MLPRegressor.html)

[github.com/keras-team/…](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fkeras-team%2Fkeras%2Fblob%2Fmaster%2Fexamples%2Freuters_mlp_relu_vs_selu.py)

入门教程：

[www.deeplearningbook.org/contents/ml…](https://link.juejin.im/?target=http%3A%2F%2Fwww.deeplearningbook.org%2Fcontents%2Fmlp.html)

[www.deeplearningbook.org/contents/au…](https://link.juejin.im/?target=http%3A%2F%2Fwww.deeplearningbook.org%2Fcontents%2Fautoencoders.html)

[www.deeplearningbook.org/contents/re…](https://link.juejin.im/?target=http%3A%2F%2Fwww.deeplearningbook.org%2Fcontents%2Frepresentation.html)


#### 卷积神经网络（卷积网）

目前世界上几乎所有最先进的基于视觉的机器学习成果都是通过卷积神经网络实现的。它们可以用于图像分类、目标检测甚至图像分割。卷积网是由 Yann Lecun 在 80 年代末 90 年代初发明的，它以卷积层为主要特征，这些卷积层起到分层特征提取的作用。可以在文本（甚至图表）中使用它们。



![](https://user-gold-cdn.xitu.io/2019/2/25/16924168e5d3aa60?imageslim)


使用卷积网进行最新的图像和文本分类，目标检测，图像分割。

工具库：

developer.nvidia.com/digits

github.com/kuangliu/to…

github.com/chainer/cha…

keras.io/application…

入门教程：

cs231n.github.io/

adeshpande3.github.io/A-Beginner%…

#### 循环神经网络 (RNN)

RNN 通过将同一权重集递归应用到 t 时的聚合器状态和 t 时的输入，来对序列数据进行建模。（给定一个在时间点 0..t..T 处输入的序列，并在各个 t 处有一个由 RNN 中 t-1 步输出的隐藏状态）。纯粹的 RNN 现在很少使用，但它的相似架构，比如 LSTM 和 GRAS，在大多数序列型建模任务中都是最先进的。

![](https://user-gold-cdn.xitu.io/2019/2/25/16924168cad2a9c1?imageslim)

RNN（如果这是一个密集联接单元并具有非线性，那么现在 f 通常是 LSTM 或 GRU）。LSTM 单元通常用来代替 RNN 结构中的普通密集层。

![](https://user-gold-cdn.xitu.io/2019/2/25/16924168dfda2ca9?imageslim)

工具库：

[github.com/tensorflow/…](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Ftensorflow%2Fmodels) (Many cool NLP research papers from Google are here)

[github.com/wabyking/Te…](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fwabyking%2FTextClassificationBenchmark)

[opennmt.net/](https://link.juejin.im/?target=http%3A%2F%2Fopennmt.net%2F)

入门教程：

[cs224d.stanford.edu/](https://link.juejin.im/?target=http%3A%2F%2Fcs224d.stanford.edu%2F)

[www.wildml.com/category/ne…](https://link.juejin.im/?target=http%3A%2F%2Fwww.wildml.com%2Fcategory%2Fneural-networks%2Frecurrent-neural-networks%2F)

[colah.github.io/posts/2015-…
](https://link.juejin.im/?target=http%3A%2F%2Fcolah.github.io%2Fposts%2F2015-08-Understanding-LSTMs%2F)


#### 条件随机场（CRF）

CRF 可能是概率图模型（PGM）家族中最常用的模型。它们可以像 RNN 一样用于序列型建模，也可以与 RNN 结合使用。在神经网络机器翻译系统出现之前，CRF 是最先进的，在许多小数据集的顺序型标记任务中，它们仍比需要大量数据才能归纳推理的 RNN 学习得更好。它们还可以用于其他结构化的预测任务中，比如图像分割等。CRF 对序列中的每个元素（比如句子）进行建模，以便相邻元素影响序列中某个组件的标签，而不是所有标签彼此独立。

使用 CRF 标记序列（文本、图像、时间序列、DNA等）

工具库：

[sklearn-crfsuite.readthedocs.io/en/latest/](https://link.juejin.im/?target=https%3A%2F%2Fsklearn-crfsuite.readthedocs.io%2Fen%2Flatest%2F)

入门教程：

blog.echen.me/2012/01/03/…

油管上 Hugo Larochelle 的 7 部系列演讲：[www.youtube.com/watch?v=GF3…](https://link.juejin.im/?target=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DGF3iSJkgPbA)




#### 决策树

比方来说，我收到了一张 Excel 表格，上面有关于各种水果的数据，我必须说出哪些看起来像苹果。我要做的就是问一个问题“哪个水果是红色且是圆形的？”，把所有回答“是”与“不是”的水果分为两个部分。现在红色且是圆形的水果不一定是苹果，所有苹果不一定都是红色且圆形的。所以我要问下一个问题，对于红色且圆形的水果问：“哪个水果有红色或者黄色？”而对不红且不圆的水果问：“哪些水果是绿色且圆形的？”。根据这些问题，可以相当准确的说出哪些是苹果。这一系列的问题就是决策树。然而，这是一个我直观描述的决策树。直觉不能用于高维的复杂数据。我们必须通过查看标记的数据自动提出一连串的问题。这就是基于机器学习的决策树所做的工作。像 CART 树这样较早的版本曾经用于简单的数据，但是随着数据集越来越大，偏差和方差之间的权衡需要更好的算法来解决。目前常用的两种决策树算法是随机森林算法（在属性的子集上建立不同的分类器，并将它们组合在一起进行输出）和增强树算法（在其他树之上训练一系列树，并纠正其子树中的错误）。
决策树可以用来对数据点（甚至回归）进行分类。

决策树可以用来对数据点（甚至回归）进行分类。


工具库：

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.ensemble.RandomForestClassifier.html)

[scikit-learn.org/stable/modu…](https://link.juejin.im/?target=http%3A%2F%2Fscikit-learn.org%2Fstable%2Fmodules%2Fgenerated%2Fsklearn.ensemble.GradientBoostingClassifier.html)

[xgboost.readthedocs.io/en/latest/](https://link.juejin.im/?target=http%3A%2F%2Fxgboost.readthedocs.io%2Fen%2Flatest%2F)

[catboost.yandex/](https://link.juejin.im/?target=https%3A%2F%2Fcatboost.yandex%2F)

入门教程：

[xgboost.readthedocs.io/en/latest/m…](https://link.juejin.im/?target=http%3A%2F%2Fxgboost.readthedocs.io%2Fen%2Flatest%2Fmodel.html)

[arxiv.org/abs/1511.05…](https://link.juejin.im/?target=https%3A%2F%2Farxiv.org%2Fabs%2F1511.05741)

[arxiv.org/abs/1407.75…](https://link.juejin.im/?target=https%3A%2F%2Farxiv.org%2Fabs%2F1407.7502)

[education.parrotprediction.teachable.com/p/practical…](https://link.juejin.im/?target=http%3A%2F%2Feducation.parrotprediction.teachable.com%2Fp%2Fpractical-xgboost-in-python)

