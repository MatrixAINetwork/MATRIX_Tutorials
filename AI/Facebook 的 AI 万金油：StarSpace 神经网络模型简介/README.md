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
