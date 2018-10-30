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


    # import our chat-bot intents file
    import json
    with open('intents.json') as json_data:
    intents = json.load(json_data)


意图的 JSON 文件被加载后，我们现在可以开始组织我们的文档、文字和分类器对应的类别。


    words = []
    classes = []
    documents = []
    ignore_words = ['?']
    # 根据意图遍历所有的句子
    for intent in intents['intents']:
    for pattern in intent['patterns']:
        # 分词
        w = nltk.word_tokenize(pattern)
        # 将词添加到列表中
        words.extend(w)
        # 将文档添加到词料库
        documents.append((w, intent['tag']))
        # 将 Tag 添加到类别中
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    # 将词小写然后去掉忽略的词
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))

    # 使用 set 去掉重复的词
    classes = sorted(list(set(classes)))

    print (len(documents), "documents")
    print (len(classes), "classes", classes)
    print (len(words), "unique stemmed words", words)

我们创建了一个文档（句子）列表，每个句子都是一个词干的列表，每个文档都与一个意图（一个类）相关。

    27 documents
    9 classes ['goodbye', 'greeting', 'hours', 'mopeds', 'opentoday', 'payments', 'rental', 'thanks', 'today']
    44 unique stemmed words ["'d", 'a', 'ar', 'bye', 'can', 'card', 'cash', 'credit', 'day', 'do', 'doe', 'good', 'goodby', 'hav', 'hello', 'help', 'hi', 'hour', 'how', 'i', 'is', 'kind', 'lat', 'lik', 'mastercard', 'mop', 'of', 'on', 'op', 'rent', 'see', 'tak', 'thank', 'that', 'ther', 'thi', 'to', 'today', 'we', 'what', 'when', 'which', 'work', 'you']


词干 "tak" 将会和 "take", "taking","takers" 等词匹配。我们可以清理单词列表并删除无用的条目，但这就足够了。


但是目前的数据结构不能够被 TensorFlow 利用，我们需要进一步的转换它： 也即将文档中的词转换成数字的张量。


