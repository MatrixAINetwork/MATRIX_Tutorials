## 基于 TensorFlow 的上下文机器人


在对话中， 语境决定了一切！ ，在这篇文章中我们将使用 TensorFlow 构建一个能够处理上下文的聊天机器人框架。

有没有想过为什么大多数聊天机器人都不能够理解语境的上下文？

怎么可能在所有的对话中考虑到上下文的重要性？

我们将创建一个“聊天机器人”框架，并为一个岛上的汽车出租店建立一个会话模型，这个小型的聊天机器人需要能够处理关于时间计算，预订选择等简单的功能。我们还希望他能够响应一些上下文的操作，譬如询问当天的租金。这样的话，我们的工作就可以减轻不少。

我们将通过下面三步来实现这个功能：

- 首先，把对话意图的定义转换成 TensoFlow 模型
- 接下来，我们构建一个聊天机器人框架来处理响应
- 最后，我们将展示如何将基本的上下文合并到我们的相应处理模块中


我们将使用在 TensorFlow 上构建的高层次 API，也即 tflearn ，当然还有 Python ，同时还使用 iPython notebook 来更好的完成我们的工作


### 将会话意图的定义转换为 TensorFlow 模型

一个聊天机器人框架需要一个结构，而其中就定义了会话的意图，在这里我们使用了 json 文件来定义他，如这个文件中所示

![](https://camo.githubusercontent.com/784a471c9105773a61b3001b9b271591d6757d0a/68747470733a2f2f63646e2d696d616765732d312e6d656469756d2e636f6d2f6d61782f3830302f312a706362775f59346163543735302d6c4c3938697732512e706e67)


聊天机器人的意图 每个对话的意图都包含：

- 一个 标签（tag，唯一标识的名字）
- 模式（神经网络文本分类器的句子模式）
- 响应（用作响应）
- 晚些我们将 添加一些基本的上下文元素

首先 import 需要的库

    # NLP 相关的处理库
    import nltk
    from nltk.stem.lancaster import LancasterStemmer
    stemmer = LancasterStemmer()

    # TensorFlow 相关的库
    import numpy as np
    import tflearn
    import tensorflow as tf
    import random

