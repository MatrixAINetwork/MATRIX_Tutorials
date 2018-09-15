# Facebook 的 AI 万金油：StarSpace 神经网络模型简介


StarSpace 是一个用于解决各种问题、进行高效的实体嵌入（译者注：entity embeddings，一种流行的类别特征处理方法）学习的通用神经网络模型:

学习单词、句子或是文档级别的嵌入。

信息检索：对实体或文档的集合完成排序，例如：Web 文档的排名。

文本分类或是其他打标签形式的任务。

度量学习、相似性学习，例如：对句子或文档的相似性进行学习。

基于内容或是协同过滤进行推荐，例如：推荐音乐和视频。

图嵌入，例如：完成像 Freebase 一样的多关系图。

图片的分类、排名或检索（例如：使用已存在的 ResNet 特性）。


在一般情况下，它会学习如何将不同类型的对象表示为一个常见的矢量嵌入空间，
从名称中的星号（'*'，通配符）和空格开始，并在该空间中将它们相互比较。

它还会学习对给定查询数据的一组实体/文档或对象进行排序，查询所用的数据不一定与该集合中的项目类型相同。

## 最新
- 文件 和 PATENTS 文件 可获得更多信息。
- 我们新增了对实值输入和标签权重的支持：阅读 文件格式 和 ImageSpace 来获取更多有关如何在输入和标签中使用权重的信息。

## 依赖

StarSpace 可在现代的 Mac OS 和 Linux 发行版上构建。鉴于它使用了 C++11 的特性，所以他需要与一个具有良好的 C++11 支持的编译器。包括：

- gcc-4.6.3 以上或是 clang-3.3 以上

编译将会借助一个 Makefile 文件来执行，所以你需要一个能正常工作的 make 命令。
你还需要安装一个 Boost 库并在 makefile 中指定 boost 库的路径译运行 StarSpace。简单地来说就是：

    $wget https://dl.bintray.com/boostorg/release/1.63.0/source/boost_1_63_0.zip
    $unzip boost_1_63_0.zip
    $sudo mv boost_1_63_0 /usr/local/bin



可选步骤：如果你希望能在 src 目录中运行单元测试，你会需要 google test 并将 makefile 中的 'TEST_INCLUDES' 配置为它的路径。


## 构建 StarSpace

想要构建 StarSpace 的话，按顺序执行：

    git clone https://github.com/facebookresearch/Starspace.git
    cd Starspace
    make


## 文档格式

StarSpace 通过以下格式进行文件的输入。 每一行都作为一个输入例子，在最简单的情况下，输入有 k 个单词，后面跟着的每个标签也是一个独立的单词：

    word_1 word_2 ... word_k __label__1 ... __label__r


这种描述格式与 fastText 一样，默认情况下，标签是以字符串 __label__ 为前缀的单词，前缀字符串可以由 -label 参数来设置。

执行这条命令来学习这种嵌入：


    $./starspace train -trainFile data.txt -model modelSaveFile


这里的 data.txt 是一个包含utf-8编码文本的训练文件。在优化结束时，程序将保存两个文件：model 和 modelSaveFile.tsv。

modelSaveFile.tsv 是一个包含实体嵌入向量的标准tsv格式文件，每行一个。modelSaveFile 是一个二进制文件，包含模型的参数以及字典，还包括所有超参数。二进制文件稍后可用于计算实体嵌入的向量或运行评估任务。

在更普遍的情况下，每个标签也会包含单词：

    word_1 word_2 ... word_k <tab> label_1_word_1 label_1_word_2 ... <tab> label_r_word_1 ..


嵌入向量将学习每个单词和标签，并将相似的输入和标签组合在一起。

为了学习更一般情况下的嵌入，每个标签由单词组成，需要指定 -fileFormat 标志为”labelDoc”，如下所示：

    $./starspace train -trainFile data.txt -model modelSaveFile -fileFormat labelDoc

我们还可以通过将参数 -useWeight 设置为 true（默认为 false）来扩展文件格式以支持实值权值（在输入和标签空间中）。如果 -useWeight 为 true，我们支持使用以下格式定义权重。


    word_1:wt_1 word_2:wt_2 ... word_k:wt_k __label__1:lwt_1 ...    __label__r:lwt_r

例如

    dog:0.1 cat:0.5 ...


对于不包括权重的任意单词和标签，其默认权重为 1。


## 训练模式

trainMode = 0:

- 每个实例都包括输入和标签。
- 如果文件格式是‘fastText’，那么标签会有特定的独立特征或是单词（例如，带有 __label__前缀，参见上面的 文件格式 一节。
- 用例：  分类任务，参见后面的 TagSpace 示例。
- 如果文件格式是‘labelDoc’那么这些标签就是特征包，其中一个包被选中（参见上面的 文件格式 一节）。
- 用例：  检索/搜索任务，每个例子包括一个后跟了一组相关文件的查询。


trainMode = 1:

- 每个示例都包含一组标签。在训练时，随机选取集合中的一个标签作为标签量，其余标签作为输入。
- 用例：  基于内容或协同过滤进行推荐，参见后面的 PageSpace 示例。


trainMode = 2:

- 每个示例都包含一组标签。在培训的时候，随机选取一个来自集合的标签作为输入量，集合中其余的标签成为标签量。
- 用例： 学习从一个对象到它所属的一组对象的映射，例如，从句子（文档内的）到文档。


trainMode = 3:

- 每个示例都包含一组标签。在训练时，随机选取集合中的两个标签作为输入量和标签量。
- 用例： 从类似对象的集合中学习成对的相似性，例如：句子的相似性。


trainMode = 4:

- 每个示例都包含两个标签。在训练时，集合中的第一个标签将被选为输入量，第二个标签将被选为标签量。
- 用例： 从多关系图中学习。


trainMode = 5:

- 每个示例只包含输入量。在训练期间，它会产生多个训练样例：从输入的每个特征被选为标签量，其他特征（到距离 ws（译者注：单词级别训练的上下文窗口大小，一个可选的输入参数））被挑选为输入特征。
- 用例： 通过无监督的方式学习单词嵌入。


## 典型用例

### TagSpace 单词、标签的嵌入

模型： 通过学习两者的嵌入，学习的映射从单词集到标签集。
例如，输入“restaurant has great food <\tab> #restaurant <\tab> #yum”将被翻译成下图。（图中的节点是要学习嵌入的实体，图中的边是实体之间的关系。


![](https://user-gold-cdn.xitu.io/2018/2/14/1619267e5b2c272d?imageslim)


输入文件的格式:

    $./starspace train -trainFile input.txt -model tagspace -label '#'

### 示例脚本：

我们将该模型应用于 AG的新闻主题分类数据集 的文本分类问题。在这一问题中我们的标签是新闻文章类别，我们使用 hit@1 度量来衡量分类的准确性。这个示例脚本 下载数据并在示例目录下运行StarSpace模型：

    $bash examples/classification_ag_news.sh



### PageSpace 用户和页面的嵌入

用途： 在Facebook上，用户可以粉（关注）他们感兴趣的公共页面。当用户浏览页面时，用户可以在 Facebook 上收到所有页面发布的内容。 我们希望根据用户的喜爱数据学习页面嵌入，并用它来推荐用户可能感兴趣（可能关注）的新页面。 这个用法可以推广到其他推荐问题：例如，根据过去观看的电影记录学习嵌入，向用户推荐电影; 根据过去用户登录的餐厅学习嵌入，向用户推荐餐馆等。

模型： 用户被表示为他们关注的页面（粉了）。也就是说，我们不直接学习用户的嵌入，相反，每个用户都会有一个嵌入，这个嵌入就是用户煽动的页面的平均嵌入。页面直接嵌入（在字典中具有独特的功能）。在用户数量大于页面数量的情况下，这种设置可以更好地工作，并且每个用户喜欢的页面平均数量较少（即用户和页面之间的边缘相对稀疏）。它也推广到新用户而无需再重新训练。 也可以使用更传统的推荐设置。

![](https://user-gold-cdn.xitu.io/2018/2/14/16192685d36b0062?imageslim)

每个用户都由用户展开的集合表示，每个训练实例都是单个用户。

输入文件格式：

    page_1 page_2 ... page_M


在训练时，在每个实例（用户）的每个步骤中，选择一个随机页面作为标签量，并且剩余的页面被选择为输入量。 这可以通过将标志 -trainMode 设置为 1 来实现。

命令：

    $./starspace train -trainFile input.txt -model pagespace -label 'page' -trainMode 1


## DocSpace 文档推荐

用途： 我们希望根据用户的历史喜好和点击数据为用户生成嵌入和推荐网络文档。

模型： 每个文件都由文件的一个集合来表示。 每个用户都被表示为他们过去喜欢/点击过的文档（集合）。 在训练时，在每一步选择一个随机文件作为标签量，剩下的文件被选为输入量。


![](https://user-gold-cdn.xitu.io/2018/2/14/1619268ba6ede311?imageslim)

输入文件格式：

    roger federer loses <tab> venus williams wins <tab> world series ended
    i love cats <tab> funny lolcat links <tab> how to be a petsitter  

每行是一个用户，每个文档（由标签分隔的文档）是他们喜欢的文档。 所以第一个用户喜欢运动，而第二个用户对这种情况感兴趣。

命令：

    ./starspace train -trainFile input.txt -model docspace -trainMode 1 -fileFormat labelDoc