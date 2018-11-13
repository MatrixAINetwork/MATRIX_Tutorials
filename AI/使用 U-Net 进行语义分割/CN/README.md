## 使用 U-Net 进行语义分割

从定义上讲，语义分割是将图像分割为连续部件的过程。例如，对属于一个人、一辆车、一棵树或数据集里的任何其它实体的每个像素进行分类。

### 语义分割 VS 实例分割

语义分割相比与它的老哥实例分割来说容易很多。

实例分割中，我们的目标不仅要对每个人，每辆车做出像素级的预测，同时还要将实体区分为 person 1、person 2、tree 1、tree 2、car 1、car 2 等等。目前最优秀的分割算法是 Mask-RCNN：一种使用 RPN（Region Proposal Network）、FPN（Feature Pyramid Network）和 FCN（Fully Convolutional Network）[5, 6, 7, 8] 多子网协作的两阶段方法。

![](https://user-gold-cdn.xitu.io/2018/10/16/1667af9fec62e0ea?imageslim)

图 4. 语义分割

![](https://user-gold-cdn.xitu.io/2018/10/16/1667af9feac1a2b6?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

![](https://user-gold-cdn.xitu.io/2018/10/16/1667af9feac1a2b6?imageslim)

图 5. 实例分割


### 研究案例：Data Science Bowl 2018


Data Science Bowl 2018 刚刚结束，在比赛中我学习到很多。其中最重要的一点可能就是，即使有了相较于传统机器学习自动化程度更高的深度学习，预处理与后处理可能才是取得优异成绩的关键。这些都是从业人员需要掌握的重要技能，它们决定了为问题搭建网络结构与模型化的方式。

因为在 Kaggle 上已经有大量对这个任务以及竞赛过程中所用方法的讨论和解释，所以我不会详尽的评述这次竞赛中的每个细节。但由于冠军方案和这篇博文的基础有关联，所以会简要讲解它。

Data Science Bowl 2018 和往届比赛一样都是由 Booz Allen Foundation 组织。今年的任务是在给定的显微镜图像中识别出细胞核，并为其绘制单独的分割遮罩。

现在，先花一两分钟猜下这个任务需要哪种类型的分割：语义还是实体？

这是一个样本遮罩图片和原始显微图像。

