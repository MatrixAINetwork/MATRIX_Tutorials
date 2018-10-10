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