## Python 中的无监督学习算法

无监督学习是一种用于在数据中查找模式的机器学习技术。提供给无监督算法的数据是没有标记的，这意味着只给出输入变量（X）而没有相应的输出变量。在无监督学习中，算法自己来发现数据中有趣的结构。


    人工智能研究专家 Yan Lecun 解释说，无监督学习 —— 在不明确告诉他们所做的一切是对还是错的情况下教机器自我学习 —— 是“真正的”人工智能的关键所在。

### 监督学习 Vs 无监督学习

在监督学习中，系统试图从先前给出的示例中学习。（另一方面，在无监督学习中，系统会尝试直接从给定的示例中查找模式。）因此，如果数据集被标记则为监督问题，如果数据集未标记，则是无监督问题。

![](https://user-gold-cdn.xitu.io/2018/9/26/1661439f9399b457?imageslim)


上面的图像是监督学习的一个例子; 我们使用回归算法找到特征之间的最佳拟合线。在无监督学习中，输入的数据以特征为基础而被分隔成不同的群集，并且预测它所属的群集。


### 重要术语

Feature: 用于进行预测的输入变量。

Predictions: 输入示例时的模型输出。

Example: 一行数据集。一个 example 包含一个或多个特征以及可能的标签。

Label: 特征结果。


### 无监督学习数据准备
在本文中，我们使用鸢尾花（Iris）数据集进行第一次预测。数据集包含一组有 150 个记录的集合，拥有 5 个属性 —— 花瓣长度、花瓣宽度、萼片长度、萼片宽度和类别。Iris Setosa、Iris Virginica 和 Iris Versicolor 是这三个类别。在我们的无监督算法中，我们给出了鸢尾花的这四个特征并预测它属于哪个类别。

我们使用 Python 中的 sklearn 库来加载鸢尾花数据集，使用 matplotlib 库来实现数据可视化。以下是用于研究数据集的代码段。



    # 引入模块
    from sklearn import datasets
    import matplotlib.pyplot as plt

    # 加载数据集
    iris_df = datasets.load_iris()

    # 数据集上的可用方法
    print(dir(iris_df))

    # 特征
    print(iris_df.feature_names)

    # 目标
    print(iris_df.target)

    # 目标名称
    print(iris_df.target_names)
    label = {0: 'red', 1: 'blue', 2: 'green'}

    # 数据集切片
    x_axis = iris_df.data[:, 0]  # Sepal Length
    y_axis = iris_df.data[:, 2]  # Sepal Width

    # 绘制
    plt.scatter(x_axis, y_axis, c=iris_df.target)
    plt.show()


    ['DESCR', 'data', 'feature_names', 'target', 'target_names']
    ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']

    [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2]

    ['setosa' 'versicolor' 'virginica']


![](https://user-gold-cdn.xitu.io/2018/9/26/1661439f93d9aa91?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)


紫色：Setosa，绿色： Versicolor，黄色：Virginica


### 聚类

在群集中，数据分为几组。简而言之，目的是将具有相似特征的群体分开并将其分配到对应的群集中。

可视化的例子，

![](https://user-gold-cdn.xitu.io/2018/9/26/1661439f93eacce8?imageslim)


在上图中，左边的图像是未进行分类的原始数据，右边的图像是聚类的（数据根据其特征进行分类）。当给出要预测的输入时，它根据它的特征检查它所属的群集，并进行预测。


### Python 中的 K-均值 聚类算法

K 均值是一种迭代聚类算法，旨在在每次迭代中找到局部最大值。最初选择所需数量的群集。由于我们知道涉及 3 个类别，因此我们将算法编程为将数据分组为 3 个类别，方法是将参数 “n_clusters” 传递给我们的 K 均值模型。现在随机将三个点（输入）分配到三个群集中。基于每个点之间的质心距离，下一个给定的输入被分配到相应的群集。现在，重新计算所有群集的质心。

群集的每个质心都是一组特征值，用于定义结果组。检查质心特征权重可用于定性地解释每个群集代表什么类型的组。

我们从 sklearn 库导入 K 均值模型，拟合特征并预测。

Python 中的 K 均值算法实现

    # 引入模块
    from sklearn import datasets
    from sklearn.cluster import KMeans

    # 加载数据集
    iris_df = datasets.load_iris()

    # 声明模型
    model = KMeans(n_clusters=3)

    # 拟合模型
    model.fit(iris_df.data)

    # 预测单个输入
    predicted_label = model.predict([[7.2, 3.5, 0.8, 1.6]])

    # 预测整个数据
    all_predictions = model.predict(iris_df.data)

    # 打印预测结果
    print(predicted_label)
    print(all_predictions)