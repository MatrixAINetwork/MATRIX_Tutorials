## 在浏览器里使用 TenserFlow.js 实时估计人体姿态

在与谷歌创意实验室的合作中，我很高兴地宣布 TensorFlow.js 版 PoseNet¹ 的发行，² 它是一个能够在浏览器里对人体姿态进行实时估计的机器学习模型。[点击这里](https://link.juejin.im/?target=https%3A%2F%2Fstorage.googleapis.com%2Ftfjs-models%2Fdemos%2Fposenet%2Fcamera.html)在线体验。



![](https://user-gold-cdn.xitu.io/2018/5/17/1636e48abc1dcc79?imageslim)

![](https://user-gold-cdn.xitu.io/2018/5/17/1636e48520989173?imageslim)

PoseNet 使用单人姿态或多人姿态算法可以检测图像和视频中的人物形象 —— 全部在浏览器中完成。

那么，姿态估计究竟是什么呢？姿态估计是指在图像和视频中检测人物的计算机视觉技术，比如，可以确定某个人的肘部在图像中的位置。需要澄清一点，这项技术并不是识别图像中是谁 —— 姿态估计不涉及任何个人身份信息。该算法仅仅是估计身体关键关节的位置。

好吧，为什么这是令人兴奋的开始？姿态估计有很多用途，从互动装置反馈给身体，到增强现实，动画，健身用途等等。我们希望借助此模型激发更多的开发人员和制造商尝试将姿态检测应用到他们自己的独特项目中。虽然许多同类姿态检测系统也已经开源，但它们都需要专门的硬件和/或相机，以及相当多的系统安装。 借助运行在 TensorFlow.js 上的 PoseNet，任何人只需拥有带摄像头的台式机或者手机即可在浏览器中体验这项技术。而且由于我们已经开源了这个模型，JavaScript 开发人员可以用几行代码来修改和使用这个技术。更重要的是，这实际上可以帮助保护用户隐私。因为基于 TensorFlow.js 的 PoseNet 运行在浏览器中，任何姿态数据都不会离开用户的计算机。






### PoseNet 入门

PoseNet 可以被用来估计单人姿态或多人姿态，这意味着算法有一个检测图像/视频中只有一个人的版本，和检测多人的版本。为什么会有两个版本？因为单人姿态检测更快，更简单，但要求图像中只能有一个主体（后面会详细说明）。我们先说单体姿态，因为它更简单易懂。

姿态估计整体来看主要有两个阶段：

- 输入一个通过卷积神经网络反馈的 RGB 图像。

- 使用单人姿态或多人姿态解码算法从模型输出中解码姿态，姿态置信得分，关键点位置，以及关键点置信得分。

等一下，所有这些关键词指的是什么？我们看看一下最重要的几个：

姿态 - 从最上层来看，PoseNet 将返回一个姿态对象，其中包含每个检测到的人物的关键点列表和实例级别的置信度分数。

![](https://user-gold-cdn.xitu.io/2018/5/17/1636e4850f000924?imageslim)

PoseNet 返回检测到的每个人的置信度值以及检测到的每个姿态关键点。

- 姿态置信度分数 - 决定了对姿态估计的整体置信度。它介于 0.0 和 1.0 之间。它可以用来隐藏分数不够高的姿态。
- 关键点 —— 估计的人体姿态的一部分，例如鼻子，右耳，左膝，右脚等。 它包含位置和关键点置信度分数。PoseNet 目前检测到下图所示的 17 个关键点：



![](https://user-gold-cdn.xitu.io/2018/5/17/1636e485bb9b88f2?imageslim)


PosNet 检测到17个姿态关键点。

- 关键点置信度得分 - 决定了估计关键点位置准确的置信度。它介于 0.0 和 1.0 之间。它可以用来隐藏分数不够高的关键点。
- 关键点位置 —— 检测到关键点的原始输入图像中的二维 x 和 y 坐标。

#### 第 1 部分：导入 TensorFlow.js 和 PoseNet 库
很多工作都是将模型的复杂性抽象化并将功能封装为易于使用的方法。我们看一下构建 PoseNet 项目的基础知识。

该库可以通过 npm 安装：

    npm install @[tensorflow-models/posenet](https://www.npmjs.com/package/@tensorflow-models/posenet)


然后使用 es6 模块导入：

    import * as posenet from '@[tensorflow-models/posenet](https://www.npmjs.com/package/@tensorflow-models/posenet)';

    const net = await posenet.load();

或通过页面中的一个包：

    <html>
      <body>
    <!-- Load TensorFlow.js -->
    <script src="[https://unpkg.com/@tensorflow/tfjs](https://unpkg.com/@tensorflow/tfjs)"></script>
    <!-- Load Posenet -->
    <script src="[https://unpkg.com/@tensorflow-models/posenet](https://unpkg.com/@tensorflow-models/posenet)">
    </script>
    <script type="text/javascript">
      posenet.load().then(function(net) {
        // posenet 模块加载成功
      });
    </script>
      </body>
    </html>


#### 第 2a 部分：单人姿态估计

![](https://user-gold-cdn.xitu.io/2018/5/17/1636e4850f90433c?imageslim)

单人姿态估计算法用于图像的示例


如前所述，单人姿态估计算法更简单，速度更快。它的理想使用场景是当输入图像或视频中心只有一个人。缺点是，如果图像中有多个人，那么来自两个人的关键点可能会被估计成同一个人的姿态的一部分 —— 举个例子，路人甲的左臂和路人乙的右膝可能会由该算法确定为属于相同姿态而被合并。如果输入图像可能包含多人，则应该使用多人姿态估计算法。

我们来看看单人姿态估计算法的输入：

- 输入图像元素 —— 包含要预测图像的 html 元素，例如视频或图像标记。重要的是，输入的图像或视频元素应该是正方形的。

- 图像比例因子 —— 在 0.2 和 1 之间的数字。默认为 0.50。在送入神经网络之前如何缩放图像。将此数字设置得较低以缩小图像，并以精度为代价增加通过网络的速度。

- 水平翻转 —— 默认为 false。表示是否姿态应该水平/垂直镜像。对于视频默认水平翻转（比如网络摄像头）的视频，应该设置为 true，因为你希望姿态能以正确的方向返回。

- 输出步幅 —— 必须为 32，16 或 8。默认 16。在内部，此参数会影响神经网络中图层的高度和宽度。在上层看来，它会影响姿态估计的精度和速度。值越小精度越高，但速度更慢，值越大速度越快，但精度更低。查看输出步幅对输出质量的影响的最好方法是体验这个单人姿态估计演示。

下面让我们看一下单人姿态估计算法的输出：

一个包含姿态置信度得分和 17 个关键点数组的姿态。
每个关键点都包含关键点位置和关键点置信度得分。同样，所有关键点位置在输入图像的坐标空间中都有 x 和 y 坐标，并且可以直接映射到图像上。

这个段代码块显示了如何使用单人姿态估计算法：

    const imageScaleFactor = 0.50;
    const flipHorizontal = false;
    const outputStride = 16;

    const imageElement = document.getElementById('cat');

    // 加载 posenet 模型
    const net = await posenet.load();

    const pose = await net.estimateSinglePose(imageElement, scaleFactor, flipHorizontal, outputStride);


输出姿态示例如下：


    {
     "score": 0.32371445304906,
    "keypoints": [
    { // 鼻子
      "position": {
        "x": 301.42237830162,
        "y": 177.69162777066
      },
      "score": 0.99799561500549
    },
    { // 左眼
      "position": {
        "x": 326.05302262306,
        "y": 122.9596464932
      },
      "score": 0.99766051769257
    },
    { // 右眼
      "position": {
        "x": 258.72196650505,
        "y": 127.51624706388
      },
      "score": 0.99926537275314
    },
     ...
     ]
    }


#### 第 2b 部分：多人姿态估计

![](https://user-gold-cdn.xitu.io/2018/5/17/1636e4850fe5a675?imageslim)

多人姿态估计算法应用于图像的例子


多人姿态估计算法可以估计图像中的多个姿态/人物。它比单人姿态算法更复杂并且稍慢，但它的优点是，如果图片中出现多个人，他们检测到的关键点不太可能与错误的姿态相关联。出于这个原因，即使用例是用来检测单人的姿态，该算法也可能更合乎需要。

此外，该算法吸引人的特性是性能不受输入图像中人数的影响。无论是 15 人还是 5 人，计算时间都是一样的。

让我们看一下它的输入：

- 输入图像元素 —— 与单人姿态估计相同
- 图像比例因子 —— 与单人姿态估计相同
- 水平翻转 —— 与单人姿态估计相同
- 输出步幅 —— 与单人姿态估计相同
- 最大检测姿态 —— 一个整数。默认为 5，表示要检测的姿态的最大数量。
- 姿态置信分数阈值 —— 0.0 至 1.0。默认为 0.5。在更深层次上，这将控制返回姿态的最低置信度分数。
- 非最大抑制（NMS，Non-maximum suppression）半径 —— 以像素为单位的数字。在更深层次上，这控制了返回姿态之间的最小距离。这个值默认为 20，这在大多数情况下可能是好的。可以通过增加/减少，以滤除不太准确的姿态，但只有在调整姿态置信度分数无法满足时才调整它。


让我们看一下它的输出：

- 以一系列姿态为 resolve 的 promise。
- 每个姿态包含与单人姿态估计算法中相同的信息。

这段代码块显示了如何使用多人姿态估计算法：

    const imageScaleFactor = 0.50;
    const flipHorizontal = false;
    const outputStride = 16;
    // 最多 5 个姿态
    const maxPoseDetections = 5;
    // 姿态的最小置信度
    const scoreThreshold = 0.5;
    // 两个姿态之间的最小像素距离
    const nmsRadius = 20;

    const imageElement = document.getElementById('cat');

    // 加载 posenet
    const net = await posenet.load();

    const poses = await net.estimateMultiplePoses(
    imageElement, imageScaleFactor, flipHorizontal, outputStride,    
    maxPoseDetections, scoreThreshold, nmsRadius);