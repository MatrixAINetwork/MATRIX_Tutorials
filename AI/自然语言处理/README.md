# 自然语言处理真是有趣


### 计算机如何理解人类的语言


计算机擅长处理结构化的数据，像电子表格和数据库表之类的。但是我们人类的日常沟通是用词汇来表达的，而不是表格，对计算机而言，这真是件棘手的事。


遗憾的是，我们并不是生活在处处都是结构化数据的时代。

这个世界上的许多信息都是非结构化的 —— 不仅仅是英语或者其他人类语言的原始文本。我们该如何让一台计算机去理解这些非结构化的文本并且从中提取信息呢？


自然语言处理，简称 NLP，是人工智能领域的一个子集，目的是为了让计算机理解并处理人类语言。让我们来看看 NLP 是如何工作的，并且学习一下如何用 Python 写出能够从原始文本中提取信息的程序。

注意：如果你不关心 NLP 是如何工作的，只想剪切和粘贴一些代码，直接跳过至“用 Python 处理 NLP 管道”部分。


### 计算机能理解语言吗？


自从计算机诞生以来，程序员们就一直尝试去写出能够理解像英语这样的语言的程序。这其中的原因显而易见 —— 几千年来，人类都是用写的方式来记录事件，如果计算机能够读取并理解这些数据将会对人类大有好处。

目前，计算机还不能像人类那样完全了解英语 —— 但它们已经能做许多事了！在某些特定领域，你能用 NLP 做到的事看上去就像魔法一样。将 NLP 技术应用到你的项目上能够为你节约大量时间。

更好的是，在 NLP 方面取得的最新进展就是可以轻松地通过开源的 Python 库比如 spaCy、textacy 和 neuralcoref 来进行使用。你需要做的只是写几行代码。

### 从文本中提取含义是很难的


读取和理解英语的过程是很复杂的 —— 即使在不考虑英语中的逻辑性和一致性的情况下。比如，这个新闻的标题是什么意思呢？

    环境监管机构盘问了非法烧烤的业主。(“Environmental regulators grill business owner over illegal coal fires.”)


环境监管机构就非法燃烧煤炭问题对业主进行了询问？或者按照字面意思，监管机构把业主烤了？正如你所见，用计算机来解析英语是非常复杂的一件事。

在机器学习中做一件复杂的事通常意味着建一条管道。这个办法就是将你的问题分成细小的部分，然后用机器学习来单独解决每一个细小的部分。再将多个相互补充的机器学习模型进行链接，这样你就能搞定非常复杂的事。

而且这正是我们将要对 NLP 所使用的策略。我们将理解英语的过程分解为多个小块，并观察每个小块是如何工作的。


### 一步步构建 NLP 管道

一段来自维基百科的文字：

    伦敦是英格兰首都，也是英国的人口最稠密的城市。伦敦位于英国大不列颠岛东南部泰晤士河畔，两千年来一直是一个主要定居点。它是由罗马人建立的，把它命名为伦蒂尼恩。(London is the capital and most populous city of England and the United Kingdom. Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia. It was founded by the Romans, who named it Londinium.)


这段文字包含了几个有用的信息。如果电脑能够阅读这段文字并且理解伦敦是一个由罗马人建立的，位于英国的城市等等，那就最好不过了。但是要达到这个要求，我们需要先将有关书面知识的最基本的概念传授给电脑，然后不断深入。


#### 第一步：语句分割
在管道中所要做的第一件事就是将这段文字分割成独立的句子，由此我们可以得到：

“伦敦是英国的首都，也是英格兰和整个联合王国人口最稠密的城市。(London is the capital and most populous city of England and the United Kingdom.)”

“位于泰晤士河流域的伦敦，在此后两个世纪内为这一地区最重要的定居点之一。(Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia.)”

它由罗马人建立，取名为伦蒂尼恩。(It was founded by the Romans, who named it Londinium.)”

我们假设每一个句子都代表一个独立的想法。那么相较于能理解整篇文章的程序而言，我们可以更加容易地写出能够理解独立语句的程序。
创建一个语句分割模型就像使用标点符号来分割语句一样简单。但是现代 NLP 管道通常需要更加复杂的技术来解决文档排版不整齐的情况。

#### 第二步：文字符号化
现在我们已经把文档分割成了句子，我们可以一步一步地处理这些句子，让我们从文档中的第一个句子开始：

    “London is the capital and most populous city of England and the United Kingdom.”

下一步就是在管道中将这个句子分割成独立的词语或符号。这就称作分词。接下来看看对这个句子分词的结果：

    “London”, “is”, “ the”, “capital”, “and”, “most”, “populous”, “city”, “of”, “England”, “and”, “the”, “United”, “Kingdom”, “.”


分词在英语中是容易完成的。我们只要分割那些空格分隔的词语。我们也将标点符号作为单词，因为它们也具有含义。


#### 第三步：猜测每个词的属性
接下来，我们需要猜测一下每一个词的属性 —— 名词，动词和形容词等等。知道每个词在句子中所扮演的角色之后，就能够帮助我们推断句子的含义。

#### 第四步：文本词形还原

在英语（以及其它大多数语言）中，词语以不同的形式出现。来看看下面这两个句子：

I had a pony.

I had two ponies.

两句话都讲到了名词小马 (pony)，但是它们有着不同的词形变化。知道词语的基本形式对计算机处理文本是有帮助的，这样你就能知道两句话在讨论同一个概念。否则，“pony” 和 “ponies” 对于电脑来说就像两个完全不相关的词语。

在 NLP 中，我们称这个过程为词形还原 —— 找出句子中每一个词的最基本的形式或词元。

对于动词也一样。我们也能够通过寻找动词最初的非结合形式来进行词形还原。所以 “I had two ponies” 变为 “I [have] two [pony]”。
词形还原一般是通过具有基于其词性的词汇形式的查找表来完成工作的，并且可能具有一些自定义的规则来处理之前从未见过的词语。

#### 第五步：识别终止词
接下来，我们需要考虑句子中的每个单词的重要性。英语有很多频繁出现的填充词比如 “and”、“the” 和 “a”。 在对文本进行统计的时候，随着这些词出现频率的升高，将会出现很多歧义。一些 NLP 管道将这些词语标记为“终止词” —— 在进行任何分析之前需要过滤掉的词语。


终止词的识别通常是由查询一个硬编码的已知终止词列表来完成。但是不存在对于所有应用来说通用的标准终止词列表。这个列表极大程度上是由你的应用所决定的。

举个例子，如果你正在建立一个与摇滚乐队有关的搜索引擎，需要确保你没有忽略单词 “The”。不仅是因为这个单词出现在很多乐队名中，而且还有一个 80 年代的著名摇滚乐队叫做 The The！


#### 第六步：依存语法解析
下一步就是找出句子中的每一个词之间的依存关系，这就做依存语法解析。

目标就是构建一棵树，为句子中的每一个词赋予一个父类词语。树的根是句子中的主要动词。根据这个句子构造的解析树的开头就是这个样子：

![](https://i.imgur.com/vtylZMh.png)

但我们还可以做的更多。为了识别每一个词的父类词，我们还可以预测这两个词之间存在的关系：

![](https://i.imgur.com/inAZUVK.png)


这颗解析树为我们展示了这个句子的主体是名词伦敦，而且它和首都之间有着 be 关系。我们最终发现了一些有用的信息 —— 伦敦是一个首都!如果我们遵循着这个句子的整颗解析树（不仅是图示信息），甚至能够发现伦敦是英国的首都。

就像我们早前使用机器学习模型来预测词性那样，以将词语输入机器学习模型并输出结果的方式来完成依存语法分析。 但是分析依存语法是一项十分复杂的任务，它需要用一整篇文章来作为分析某些细节的上下文。

但是尽管这位作者在 2015 年发表了一条说明称这种方法现在已成为标准，但它已经过时甚至不再被作者使用过。在 2016 年，谷歌推出了一种新的依存语法分析方法，称为 Parsey McParseface，它采用了一种新的深度学习方法，超越了之前的表现，并在业界内快速流传。一年之后，他们又发布了新的模型，称为 ParseySaurus，对某些方面做了进一步改善。换句话说，解析技术依旧是搜索领域的一项热门技术，并且在不断地变化和改进。

很多英语语句是十分模糊且难以解析的，这一点需要牢记在心。在那些例子中，模型会根据之前解析过的最相似的句子来进行猜测，但这并不完美，有时这个模型会产生令人尴尬的错误。但随着时间的推移，我们的 NLP 模型将会继续以合理的方式更好地解析文本。


#### 第六步（下）：查找名词短语
到现在为止，我们将句子中的每一个词语都作为一个独立的实体。但有时将一些词语连接起来能够更加合理地表达一个想法或事件。我们能够用依存关系解析树中的信息来自动地将所有阐述相同事物的词语组合在一起。


#### 第七步：命名实体识别（NER）

现在我们已经完成所有困难的工作，终于可以抛弃书面的语法并开始动手实现想法了。在我们的句子中，有着以下名词：

![](https://i.imgur.com/hfcNOlm.png)

这些名词中，有一部分与实际意义相同。比如说“伦敦”、“英格兰”和“英国”代表了地图上的物理位置。如果能检测到这些那真是太棒了！有了这些信息，我们就能够使用 NLP 在自动地提取一个在文档中提及的真实世界地理位置列表。

命名实体识别（NER）的目标就是为了检测和标记这些代表真实世界中某些事物的名词。在使用我们的 NER 标记模型对句子中的每个词语进行处理之后，句子就变成这样：

![](https://i.imgur.com/aCWZp0D.png)

但 NER 系统并不只是做这些简单的查找字典的工作。而是使用某个词语在句子中的上下文以及统计模型来猜测某个词语代表哪种类型的名词。一个优秀的 NER 系统能够根据上下文线索辨别出人名 “Brooklyn Decker” 和 地名 “Brooklyn”。

这些是经典的 NER 系统能够标记的事物：

- 人名
- 公司名
- 地理位置（物理位置和政治位置）
- 产品名称
- 日期和时间
- 金额
- 事件名称

自从 NER 能够帮助轻易地从文本中获取结构化数据，便被广泛使用。它是从 NLP 管道中获得结果的最便捷途径之一。


#### 第八步：共指解析
在此刻，我们已经对句子有了充分的了解。我们了解了每个词语的词性、词语之间的依存关系以及哪些词语是代表命名实体的。

可是，我们还需要解决一个大问题。英语中存在着大量的代词 —— 比如他、她和它。这些是我们对在句子中反复出现的名称的简化。人们能够根据上下文来得到这些词代表的内容。但是我们的 NLP 模型并不知道这些代词的含义，因为它每次只检查一个句子。

来看看我们的文档中的第三个句子：

    “It was founded by the Romans, who named it Londinium.”

如果我们用 NLP 管道解析这个句子，我们就能知道“它”是由罗马人建立的。但如果能知道“伦敦”是由罗马人建立的那会更有用。

当人们读这个句子时，能够很容易得出“它”代表“伦敦”。共指解析的目的是根据整个句子中的代词来找出这种相同的映射。我们是想要找出所有指向同一实体的词语。

这就是在我们的文档中对“伦敦”使用共指解析的结果：

![](https://i.imgur.com/2nAx9hE.png)


将共指信息、解析树和命名实体信息结合在一起，我们就能够从这个文档中提取出很多信息！

共指解析是我们正在进行工作的管道中的最艰难步骤之一。它甚至比语句解析还要困难。深度学习的最新进展带来更精确的方法，但它还不够完美。


### 用 Python 来构建 NLP 管道

![](https://i.imgur.com/xxqgOTm.png)


共指解析是一项并不总要完成的可选步骤。 

注意：在我们往下看之前，值得一提的是，这些都是构建传统 NLP 管道的步骤，你可以根据你的目的以及如何实现你的 NLP 库来决定是跳过还是重复某些步骤。举个例子，一些像 spaCy 这样的库，是先使用依存语法解析，得出结果后再进行语句分割。
那么，我们该如何构建这个管道？多谢像 spaCy 这样神奇的 python 库，管道的构建工作已经完成！所有的步骤都已完成，时刻准备为你所用。
首先，假设你已经安装了 Python 3，你可以按如下步骤来安装 spaCy：

    # 安装 spaCy 
    pip3 install -U spacy

    # 下载针对 spaCy 的大型英语模型
    python3 -m spacy download en_core_web_lg

    # 安装同样大有用处的 textacy
    pip3 install -U textacy


在一段文档中运行 NLP 管道的代码如下所示：

    import spacy

    # 加载大型英语模型
    nlp = spacy.load('en_core_web_lg')

    # 我们想要检验的文本
    text = """London is the capital and most populous city of England and 
    the United Kingdom.  Standing on the River Thames in the south east 
    of the island of Great Britain, London has been a major settlement 
    for two millennia. It was founded by the Romans, who named it Londinium.
    """

    # 用 spaCy 解析文本. 在整个管道运行.
    doc = nlp(text)

    # 'doc' 现在包含了解析之后的文本。我们可以用它来做我们想做的事！
    # 比如，这将会打印出所有被检测到的命名实体：
    for entity in doc.ents:
    print(f"{entity.text} ({entity.label_})")

如果你运行了这条语句，你就会得到一个关于文档中被检测出的命名实体和实体类型的表：

    London (GPE)  
    England (GPE)  
    the United Kingdom (GPE)  
    the River Thames (FAC)  
    Great Britain (GPE)  
    London (GPE)  
    two millennia (DATE)  
    Romans (NORP)  
    Londinium (PERSON)

需要注意的是，它误将 “Londinium” 作为人名而不是地名。这可能是因为在训练数据中没有与之相似的内容，不过它做出了最好的猜测。如果你要解析具有专业术语的文本，命名实体的检测通常需要做一些微调。

让我们把这实体检测的思想转变一下，来做一个数据清理器。假设你正在尝试执行新的 GDPR 隐私条款并且发现你所持有的上千个文档中都有个人身份信息，例如名字。现在你的任务就是移除文档中的所有名字。

如果将上千个文档中的名字手动去除，需要花上好几年。但如果用 NLP，事情就简单了许多。这是一个移除检测到的名字的数据清洗器：


    import spacy

    # 加载大型英语 NLP 模型
    nlp = spacy.load('en_core_web_lg')

    # 如果检测到名字，就用 "REDACTED" 替换
    def replace_name_with_placeholder(token):
    if token.ent_iob != 0 and token.ent_type_ == "PERSON":
        return "[REDACTED] "
    else:
        return token.string

    # 依次解析文档中的所有实体并检测是否为名字
    def scrub(text):
    doc = nlp(text)
    for ent in doc.ents:
        ent.merge()
    tokens = map(replace_name_with_placeholder, doc)
    return "".join(tokens)

    s = """
    In 1950, Alan Turing published his famous article "Computing Machinery and Intelligence". In 1957, Noam Chomsky’s 
    Syntactic Structures revolutionized Linguistics with 'universal grammar', a rule based system of syntactic structures.
    """

    print(scrub(s))

如果你运行了这个，就会看到它如预期般工作：

    In 1950, [REDACTED] published his famous article "Computing Machinery and Intelligence". In 1957, [REDACTED]   
    Syntactic Structures revolutionized Linguistics with 'universal grammar', a rule based system of syntactic structures.

#### 信息提取
开箱即用的 spaCy 能做的事实在是太棒了。但你也可以用 spaCy 解析的输出来作为更复杂的数据提取算法的输入。这里有一个叫做 textacy 的 python 库，它实现了多种基于 spaCy 的通用数据提取算法。这是一个良好的开端。

它实现的算法之一叫做半结构化语句提取。我们用它来搜索解析树，查找主体为“伦敦”且动词是 “be” 形式的简单语句。这将会帮助我们找到有关伦敦的信息。

来看看代码是怎样的：

    import spacy
    import textacy.extract

    # 加载大型英语 NLP 模型
    nlp = spacy.load('en_core_web_lg')

    # 需要检测的文本
    text = """London is the capital and most populous city of England and  the United Kingdom.  
    Standing on the River Thames in the south east of the island of Great Britain, 
    London has been a major settlement  for two millennia.  It was founded by the Romans, 
    who named it Londinium.
    """

    # 用 spaCy 来解析文档
    doc = nlp(text)

    # 提取半结构化语句
    statements = textacy.extract.semistructured_statements(doc, "London")

    # 打印结果
    print("Here are the things I know about London:")

    for statement in statements:
    subject, verb, fact = statement
    print(f" - {fact}")

打印出这些：

    Here are the things I know about London:

     - the capital and most populous city of England and the United Kingdom.  
     - a major settlement for two millennia.


如果你将这段代码用于维基百科上关于伦敦的整篇文章上，而不只是这三个句子，就会得到令人印象十分深刻的结果：

    Here are the things I know about London:

    - the capital and most populous city of England and the United Kingdom  
    - a major settlement for two millennia  
    - the world's most populous city from around 1831 to 1925  
    - beyond all comparison the largest town in England  
    - still very compact  
    - the world's largest city from about 1831 to 1925  
    - the seat of the Government of the United Kingdom  
    - vulnerable to flooding  
    - "one of the World's Greenest Cities" with more than 40 percent green space or open water  
    - the most populous city and metropolitan area of the European Union and the second most populous in Europe  
    - the 19th largest city and the 18th largest metropolitan region in the world  
    - Christian, and has a large number of churches, particularly in the City of London  
    - also home to sizeable Muslim, Hindu, Sikh, and Jewish communities  
    - also home to 42 Hindu temples  
    - the world's most expensive office market for the last three years according to world property journal (2015) report  
    - one of the pre-eminent financial centres of the world as the most important location for international finance  
    - the world top city destination as ranked by TripAdvisor users  
    - a major international air transport hub with the busiest city airspace in the world  
    - the centre of the National Rail network, with 70 percent of rail journeys starting or ending in London  
    - a major global centre of higher education teaching and research and has the largest concentration of higher education institutes in Europe  
    - home to designers Vivienne Westwood, Galliano, Stella McCartney, Manolo Blahnik, and Jimmy Choo, among others  
    - the setting for many works of literature  
    - a major centre for television production, with studios including BBC Television Centre, The Fountain Studios and The London Studios  
    - also a centre for urban music  
    - the "greenest city" in Europe with 35,000 acres of public parks, woodlands and gardens  
    - not the capital of England, as England does not have its own government


#### 还能做什么？

看看这个 spaCy 文档和 textacy 文档，你会发现很多能够用于解析文本的方法示例。目前我们所看见的只是一个小示例。

这里有另外一个实例：想象你正在构建一个能够向用户展示我们在上一个例子中提取出的全世界城市的信息的网站。

如果你的网站有搜索功能，能像谷歌那样能够自动补全常规的查询就太好了：

![](https://i.imgur.com/nG80L3E.png)


谷歌对于“伦敦”的自动补全建议

如果这么做，我们就需要一个可能提供给用户的建议列表。我们可以使用 NLP 来快速生成这些数据。

这是从文档中提取常用名词块的一种方式：


    import spacy
    import textacy.extract

    # 加载大型英语 NLP 模型
    nlp = spacy.load('en_core_web_lg')

    # 需要检测的文档
    text = """London is the capital and most populous city of England and  the United Kingdom.  
    Standing on the River Thames in the south east of the island of Great Britain, 
    London has been a major settlement  for two millennia.  It was founded by the Romans, 
    who named it Londinium.
    """

    # 用 spaCy 解析文档
    doc = nlp(text)

    # 提取半结构化语句
    statements = textacy.extract.semistructured_statements(doc, "London")

    # 打印结果
    print("Here are the things I know about London:")

    for statement in statements:
    subject, verb, fact = statement
    print(f" - {fact}")


如果你用这段代码来处理维基百科上关于伦敦的文章，就会得到如下结果：

    westminster abbey  
    natural history museum  
    west end  
    east end  
    st paul's cathedral  
    royal albert hall  
    london underground  
    great fire  
    british museum  
    london eye

    .... etc ....