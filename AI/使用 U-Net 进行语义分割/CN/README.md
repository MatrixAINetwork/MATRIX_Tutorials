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

![](https://user-gold-cdn.xitu.io/2018/10/16/1667af9fea9c411b?imageslim)

图 6. 细胞核遮罩（左）和原始图像（右）

尽管这个任务起初听起来像是个语义分割任务，但其实需要实例分割。我们需要独立地处理图像中的每个核，并将它们识别为 nuclei 1、nuclei 2、nuclei 3 等等，这就类似于前面那个实例中的 Car 1、Car 2、Person 1 等等。也许这项任务的动机是跟踪记录细胞样本中细胞核的大小、数量和特征。这样的自动化跟踪记录过程非常重要，有助于进一步加速各种疾病治疗实验的研究进程。

你现在可能想，如果这篇文章是关于语义分割的，但如果 Data Science Bowl 2018 是实例分割任务样例，那么我为什么一直要讨论这个特定的比赛。如果你在考虑这些，绝对是正确，这次比赛的最终目标并不能作为语义分割的样例。但是，如何将这个实例分割问题转化为多分类的语义分割任务。这是我尝试过的方法，虽然在实践过程中失败了但是也对最后成功有一定帮助。

在这三个月的竞赛中，在整个论坛中分享或至少明确讨论的只有两种模型（或它们的变体）：Mask-RCNN 和 U-Net。正如前面所述，Mask-RCNN 是目前最优秀的对象检测算法，它同实例分割中一样能检测出单个对象并预测它们的遮罩。但由于 Mask-RCNN 使用了两阶段的方式，需要先优化一个 RPN（Region Proposal Network）然后同时预测边界框、类别和遮罩，所以部署与训练都会非常困难。

另一方面，U-Net 是种非常流行的用于语义分割的端到端编解码网络[9]。最初它也是创建并应用在生物医学图像分割领域，和这次 Data Science Bowl 非常类似的任务。在这种竞赛中没有银弹，这两种架构如果不做后处理或预处理亦或结构上细微的调整，都不能得到较好的预测值。我在这次比赛中并没有机会尝试 Mask-RCNN，所以我就围绕着 U-Net 进行试验，学习到很多东西。

另外，由于我们的主题是语义分割，Mask-RCNN 就留给其他博客来解释。但如果你想在自己的 CV 应用上尝试它们，这里有两个已实现功能并受欢迎的 github 库：Tensorflow 和 PyTorch。[10, 11]

现在，我们继续讲解 U-Net，并深入研究它的细节...

下面先以它的体系结构开始：

![](https://user-gold-cdn.xitu.io/2018/10/16/1667af9feb1b9a24?imageslim)

图 7. 原生 U-Net

对于熟悉传统卷积神经网络的朋友来说，第一部分（表示为下降）的结构非常眼熟。第一部分可以称作下降或你可以认为它是编码器部分，你在这里用卷积模块处理，然后再使用最大池化下采样，将输入图像编码为不同层级的特征表示。

网络的第二部分则包括上采样和级联，然后是普通的卷积运算。对于一些读者来说，在 CNN 中使用上采样可能是个新概念，但其思路很简单：扩展特征维度，以达到与左侧的相应级联块的相同大小。这里的灰色和绿色的箭头表示将两个特征映射在一起。与其他 FCN 分割网络相比，U-Net 在这方面的主要贡献在于，在上采样和深入网络过程中，我们将下采样中的高分辨率特征与上采样特征连接起来以便在后续的卷积过程中更好地定位和学习实体的表征。由于上采样是稀疏操作，我们需要在早期处理过程中获取良好的先验，以更好的表示位置信息。在 FPN（Feature Pyramidal Networks） 中也有类似的连接匹配分级的思路。

![](https://user-gold-cdn.xitu.io/2018/10/16/1667af9feaea3cf9?imageslim)
图 7. 原生 U-Net 张量图解

我们可以将在下降部分中的一个操作模块定义为“卷积 → 下采样”。

    # 一个采样下降模块
    def make_conv_bn_relu(in_channels, out_channels, kernel_size=3, stride=1, padding=1):
    return [
        nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size,  stride=stride, padding=padding, bias=False),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True)
    ]
    self.down1 = nn.Sequential(
     *make_conv_bn_relu(in_channels, 64, kernel_size=3, stride=1, padding=1 ),
     *make_conv_bn_relu(64, 64, kernel_size=3, stride=1, padding=1 ),
    )

    # 卷积然后最大池化
    down1 = self.down1(x)
    out1   = F.max_pool2d(down1, kernel_size=2, stride=2)


U-Net 下采样模块

同样我们可以在上升部分中定义一个操作模块：“上采样 → 级联 → 卷积”。


    # 一个采样上升模块
    def make_conv_bn_relu(in_channels, out_channels, kernel_size=3, stride=1, padding=1):
    return [
        nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size,  stride=stride, padding=padding, bias=False),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(inplace=True)
    ]
    self.up4 = nn.Sequential(
     *make_conv_bn_relu(128,64, kernel_size=3, stride=1, padding=1 ),
     *make_conv_bn_relu(64,64, kernel_size=3, stride=1, padding=1 )
    )
    self.final_conv = nn.Conv2d(32, num_classes, kernel_size=1, stride=1, padding=0 )

    # 对 out_last 上采样，并与 down1 级联，然后卷积
    out   = F.upsample(out_last, scale_factor=2, mode='bilinear')  
    out   = torch.cat([down1, out], 1)
    out   = self.up4(out)

    # 用于最后预测的 1 * 1 卷积
    final_out = self.final_conv(out)


U-Net 上采样模块

仔细看下结构图，你会发现输出尺寸（388 * 388）与原始输入（572 * 572）并不一致。如果你希望输出保持一致的尺寸，你可以使用填充卷积来保持跨级联的维度一致，就像我们在上面的示例代码中所做的那样。

当提到这种上采样时，您可能会遇到以下术语之一：转置卷积、上卷积、反卷积或上采样。很多人，包括我在内的很多人以及PyTorch技术文档都不喜欢反卷积这个术语，因为在上采样阶段，我们实际上是在做常规的卷积运算，并没有字面上所谓的“反”。在进一步讨论之前，如果你不熟悉基本卷积运算及其算术，我强烈建议你访问查看here.。[12]

我将解释从简单到复杂的上采样方法。这里有三种在 PyTorch 中对二维张量进行上采样的方法：

最近邻插值

这是在将张量调整(转换)为更大张量(例如2x2到4x4、5x5或6x6)时寻找缺失像素值的最简单方法。

我们使用 Numpy 逐步实现这个基础的计算机视觉算法：

    def nn_interpolate(A, new_size):
    """
    逐步实现最近邻插值
    """
    # 获取大小
    old_size = A.shape
    
    # 计算扩充后的行与列
    row_ratio, col_ratio = new_size[0]/old_size[0], new_size[1]/old_size[1]
    
    # 定义新的行与列位置 
    new_row_positions = np.array(range(new_size[0]))+1
    new_col_positions = np.array(range(new_size[1]))+1
    
    # 按照比例标准化新行与列的位置
    new_row_positions = new_row_positions / row_ratio
    new_col_positions = new_col_positions / col_ratio
    
    # 对新行与列位置应用 ceil （计算大于等于该值的最小整数）
    new_row_positions = np.ceil(new_row_positions)
    new_col_positions = np.ceil(new_col_positions)
    
    # 计算各点需要重复的次数
    row_repeats = np.array(list(Counter(new_row_positions).values()))
    col_repeats = np.array(list(Counter(new_col_positions).values()))
    
    # 在矩阵的各列执行列向插值
    row_matrix = np.dstack([np.repeat(A[:, i], row_repeats) 
                            for i in range(old_size[1])])[0]
    
    # 在矩阵的各列执行列向插值
    nrow, ncol = row_matrix.shape
    final_matrix = np.stack([np.repeat(row_matrix[i, :], col_repeats)
                             for i in range(nrow)])

    return final_matrix
    
    
    def nn_interpolate(A, new_size):
    ""向量化最近邻插值"""

    old_size = A.shape
    row_ratio, col_ratio = np.array(new_size)/np.array(old_size)

    # 行向插值
    row_idx = (np.ceil(range(1, 1 + int(old_size[0]*row_ratio))/row_ratio) - 1).astype(int)

    # 列向插值
    col_idx = (np.ceil(range(1, 1 + int(old_size[1]*col_ratio))/col_ratio) - 1).astype(int)

    final_matrix = A[:, row_idx][col_idx, :]

    return final_matrix

