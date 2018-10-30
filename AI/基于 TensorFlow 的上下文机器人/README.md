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


    # 创建训练数据
    training = []
    output = []
    # 创建一个空数组来储存输出
    output_empty = [0] * len(classes)

    # 每个句子的训练集和词袋
    for doc in documents:
    # 初始化词袋
    bag = []
    # 列出文档中所有的词
    pattern_words = doc[0]
    # 让词成为词干
    pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    # 创建我们的词袋数组
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # 如果是当前的标记输出 1 ，否的话输出 0
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

    # 打乱训练集并且转换成 np.array 类型
    random.shuffle(training)
    training = np.array(training)

    # 创建训练集
    train_x = list(training[:,0])
    train_y = list(training[:,1])

注意，我们的数据被打乱了。TensorFlow 会使用其中一部分数据用作测试， 以评估训练模型的准确性。

下面是一个 x 和 y 的列表元素，也即词袋数组，一个是意图的模式，另一个是意图所对应的类。

train_x example: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
train_y example: [0, 0, 1, 0, 0, 0, 0, 0, 0]


我们已经准备好了，可以创建我们的模型了。


    # 重置底层图数据
    tf.reset_default_graph()
    # 创建神经网络
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    # 定义模型并创建 tensorboard
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    # 使用梯度下降方法训练模型
    model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
    model.save('model.tflearn')


这个张量的结构与[另一篇文章](https://link.juejin.im/?target=https%3A%2F%2Fchatbotslife.com%2Fdeep-learning-in-7-lines-of-code-7879a8ef8cfb)中使用的 2 层神经网络是相同的，训练模型的方式是不会过时的。

![](https://camo.githubusercontent.com/c9a83adfa9909dcf6d901e1740c66d16625c2480/68747470733a2f2f63646e2d696d616765732d312e6d656469756d2e636f6d2f6d61782f3830302f312a355549716e6564427a735954584a38317745552d76672e676966)


使用 tflearn 交互式构建模型 为了完成这部分的工作，我们将序列化保存（pickle）模型和文档以便我们在以后的 Jupyter Notebook 中可以使用他们。

# 保存我们所有的数据结构
    import pickle
    pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data", "wb" ) )


### 创建我们的聊天机器人框架


我们创建了一个简单的状态机来处理响应，用我们的意图模型（上一步训练的结果）作为分类器。 聊天机器人是如何工作的

    上下文的聊天机器人框架是 状态机 内的一个分类器。


加载相同的导入模块后，我们将 反序列化 我们的模型和文档并且重新加载我们的意图文件。记住我们的 chat-bot 框架是和我们的模型分开来构建的—你不需要重新构建你的模型除非意图模式发生改变。因为有几百个意图和数千个模式，所以这个模型可能需要几分钟的时间来构建。


    # 重置变量
    import pickle
    data = pickle.load( open( "training_data", "rb" ) )
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']

    # 导入聊天机器人的意图文件
    import json
    with open('intents.json') as json_data:
    intents = json.load(json_data)


接下来将加载我们保存在 TensorFlow (tflearn framework) 上的模型。首先我们需要和前面章节所述的一样来定义 TensorFlow 模型的结构。

    # 加载保存的模型
    model.load('./model.tflearn')


在开始处理意图之前，我们需要 从用户的输入 中生成词袋（bag-of-words），这和我们之前创建训练文档时使用的技术是一样的。

    def clean_up_sentence(sentence):
    # 分词
    sentence_words = nltk.word_tokenize(sentence)
    # 转换句子为词干
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

    # 返回词袋数组，每个数组的下标表示词的序号，如果句子包含该词，则该数组词为 1，否为 0
    def bow(sentence, words, show_details=False):
    # pattern 分词
    sentence_words = clean_up_sentence(sentence)
    # 词袋
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


    p = bow("is your shop open today?", words)
    print (p)
    [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0]


我们现在可以构建我们的响应处理器了。


    ERROR_THRESHOLD = 0.25
    def classify(sentence):
    # 得出预测的概率
    results = model.predict([bow(sentence, words)])[0]
    # 根据概率值过滤结果
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # 根据返回值长度降序排序
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # 返回包含意图和概率的元组
    return return_list

    def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # results 不为空则循环找到匹配的 tag
    if results:
        # 循环找到匹配的 tag
        while results:
            for i in intents['intents']:
                # 是否匹配
                if i['tag'] == results[0][0]:
                    # 随机输出一个响应？？
                    return print(random.choice(i['responses']))
            results.pop(0)


句子传递到 response() 方法后会被分类。我们分类器使用 model.predict() 方法是响应很快的。模型返回的响应结果的概率列表是和我们的意图定义一起处理的。

如果一个或多个分类器超过一个阈值，那么我们就会看到一个标记是否匹配一个意图然后再处理它。分类器列表将会当成栈，然后不断的从栈中弹出一个元素来进行匹配是否符合，直到空栈为止。

让我们来看一个分类器的例子，我们看到最可能的标记和它所对应的概率值被返回了。


    classify('is your shop open today?')
    [('opentoday', 0.9264171123504639)]

注意到“你的商店今天营业吗”并不是这种意图的模式之一： 模式：["你今天开着吗?"，"你今天什么时候开?"，"你今天营业几小时?"] ，然而词“开”和“今天”对我们的模式来说是很重要的（也就是说他们决定了模型会选择什么意图）。

所以我们就可以根据用户的输入生成一个 chat-bot 的回应


    response('is your shop open today?')
    Our hours are 9am-9pm every day


下面是另外一个上下文无关的响应。

    response('do you take cash?')
    We accept VISA, Mastercard and AMEX
    response('what kind of mopeds do you rent?')
    We rent Yamaha, Piaggio and Vespa mopeds
    response('Goodbye, see you later')
    Bye! Come back again soon.