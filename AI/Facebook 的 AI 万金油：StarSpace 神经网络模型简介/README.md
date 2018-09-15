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