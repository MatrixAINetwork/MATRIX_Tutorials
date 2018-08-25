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