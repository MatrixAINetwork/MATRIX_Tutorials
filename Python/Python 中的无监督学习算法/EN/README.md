## Unsupervised Learning with Python

    Unsupervised Learning is a class of Machine Learning techniques to find the patterns in data. The data given to unsupervised algorithm are not labelled, which means only the input variables(X) are given with no corresponding output variables. In unsupervised learning, the algorithms are left to themselves to discover interesting structures in the data.

![](https://cdn-images-1.medium.com/max/1600/1*c19D4-xJpW8EoP1d46jn8Q.jpeg)


>  **Yan Lecun, director of AI research, explains that unsupervised learning — teaching machines to learn for themselves without having to be explicitly told if everything they do is right or wrong — is the key to “true” AI.**


### Supervised Vs Unsupervised Learning.


In supervised learning, the system tries to learn from the previous examples that are given. (On the other hand, in unsupervised learning, the system attempts to find the patterns directly from the example given.) So if the dataset is labelled it comes under a supervised problem, it the dataset is unlabelled then it is an unsupervised problem.

![](https://cdn-images-1.medium.com/max/1600/1*AZMDyaifxGVdwTV-1BN7kA.png)


The image to the left is an example of supervised learning; we use regression techniques to find the best fit line between the features. While in unsupervised learning the inputs are segregated based on features and the prediction is based on which cluster it belonged.


### Important Terminology

- Feature: An input variable used in making predictions.

- Predictions: A model’s output when provided with an input example.

- Example: One row of a data set. An example contains one or more features and possibly a label.

- Label: Result of the feature.



### Preparing data for Unsupervised Learning
In this article we use, Iris dataset for making our very first predictions. The dataset contains a set of 150 records under 5 attributes — Petal Length , Petal Width , Sepal Length , Sepal width and Class. Iris Setosa, Iris Virginica and Iris Versicolor are the three classes. For our Unsupervised Algorithm we give these four features of the Iris flower and predict which class it belongs to.

We use sklearn Library in Python to load Iris dataset, and matplotlib for data visualisation. Below is the code snippet for exploring the dataset.

    # Importing Modules
    from sklearn import datasets
    import matplotlib.pyplot as plt

    # Loading dataset
    iris_df = datasets.load_iris()

    # Available methods on dataset
    print(dir(iris_df))

    # Features
    print(iris_df.feature_names)

    # Targets
    print(iris_df.target)

    # Target Names
    print(iris_df.target_names)
    label = {0: 'red', 1: 'blue', 2: 'green'}

    # Dataset Slicing
    x_axis = iris_df.data[:, 0]  # Sepal Length
    y_axis = iris_df.data[:, 2]  # Sepal Width

    # Plotting
    plt.scatter(x_axis, y_axis, c=iris_df.target)
    plt.show()

    ['DESCR', 'data', 'feature_names', 'target', 'target_names']
    ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
    [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2]
    ['setosa' 'versicolor' 'virginica']


![](https://cdn-images-1.medium.com/max/1600/1*W97xJQLjkOUqbYL5_3EZQQ.png)

Violet: Setosa, Green: Versicolor, Yellow: Virginica


### Clustering
In clustering, the data is divided into several groups. In plain words, the aim is to segregate groups with similar traits and assign them into clusters.

Visual Example,

![](https://cdn-images-1.medium.com/max/1600/1*58tBPk4oZqhZ-LUq-0Huow.jpeg)

In the above image, the image to the left is raw data where the classification isn’t done, the image in the right is clustered(the data is classified based on its features). When an input is given which is to be predicted then it checks in the cluster it belongs based on it’s features, and the prediction is made.


