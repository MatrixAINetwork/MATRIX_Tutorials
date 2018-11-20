## 构建流畅的交互界面

### 如何在 iOS 上创建自然的交互手势及动画

在 WWDC 2018 上，苹果设计师进行了一次题为 “[设计流畅的交互界面](https://link.juejin.im/?target=https%3A%2F%2Fdeveloper.apple.com%2Fvideos%2Fplay%2Fwwdc2018%2F803%2F)” 的演讲，解释了 iPhone X 手势交互体系背后的设计理念。

![](https://user-gold-cdn.xitu.io/2018/8/23/16564d9022f03791?imageslim)

苹果 WWDC18 演讲 “设计流畅的交互界面”

这是我最喜欢的 WWDC 分享 —— 我十分推荐它

这次分享提供了一些技术性指导，这对一个设计演讲来说是很特殊的，但它只是一些伪代码，留下了太多的未知。


![](https://user-gold-cdn.xitu.io/2018/8/23/16564d9022bcee95?imageslim)

演讲中一些看起来像 Swift 的代码。

如果你想尝试实现这些想法，你可能会发现想法和实现是有差距的。

我的目的就是通过提供每个主要话题的可行的代码例子，来减少差距。

![](https://user-gold-cdn.xitu.io/2018/8/23/16564d9030ef256f?imageslim)


我们会创建 8 个界面。 按钮，弹簧动画，自定义界面和更多！

这是我们今天会讲到的内容概览：

- “设计流畅的交互界面”演讲的概要。
- 8 个流畅的交互界面，背后的设计理念和构建的代码。
- 设计师和开发者的实际应用

### 什么是流畅的交互界面？
一个流畅交互界面也可以被描述为“快”，“顺滑”，“自然”或是“奇妙”。它是一种光滑的，无摩擦的体验，让你只会感觉到它是对的。

WWDC 演讲认为流畅的交互界面是“你思想的延伸”或是“自然世界的延伸”。当一个界面是按照人们的想法做事，而不是按照机器的想法时，他就是流畅的。

### 是什么让它们流畅？
流畅的交互界面是响应式的，可中断的，并且是可重定向的。这是一个 iPhone X 滑动返回首页的手势案例：

![](https://user-gold-cdn.xitu.io/2018/8/23/16564d9058822b59?imageslim)

应用在启动动画中是可以被关闭的。

交互界面即时响应用户的输入，可以在任何进程中停止，甚至可以中途改变动画方向。

### 我们为什么关注流畅的交互界面？

- 流畅的交互界面提升了用户体验，让用户感觉每一个交互都是快的，轻量和有意义的。
- 它们给予用户一种掌控感，这为你的应用与品牌建立了信任感。
- 它们很难被构建。一个流畅的交互界面是很难被仿造，这是一个有力的竞争优势。


### 交互界面
这篇文章剩下的部分，我会为你们展示怎样来构建 WWDC 演讲中提到的 8 个主要的界面。

![](https://user-gold-cdn.xitu.io/2018/8/23/16564d9022c608ec?imageslim)

图标代表了我们要构建的 8 个交互界面

![](https://user-gold-cdn.xitu.io/2018/8/23/16564d9021d4e466?imageslim)


### 交互界面 #1：计算器按钮
这个按钮模仿了 iOS 计算器应用中按钮的表现行为

![](https://user-gold-cdn.xitu.io/2018/8/23/16564d91b81f5702?imageslim)

### 核心功能
- 被点击时马上高亮。
- 即便处于动画中也可以被立即点击。
- 用户可以在按住手势结束时或手指脱离按钮时取消点击。
- 用户可以在按住手势结束时，手指脱离按钮和手指重回按钮来确认点击。


### 设计理念
我们希望按钮感觉是即时响应的，让用户知道它们是有功能的。另外，我们希望操作是可以被取消的，如果用户在按下按钮时决定撤销操作。这允许用户更快的做决定，因为他们可以在考虑的同时进行操作。

![](https://user-gold-cdn.xitu.io/2018/8/23/16564d916989b63a?imageslim)

WWDC 演讲上的幻灯片，展示了手势是如何与想法同时进行的，以此让操作更迅速。

### 关键代码

第一步是创建一个按钮，继承自 UIControl，不是继承自 UIButton。UIButton 也可以正常工作，但我们既然要自定义交互，那我们就不需要它的任何功能了。

    CalculatorButton: UIControl {
        public var value: Int = 0 {
            didSet { label.text = “\(value)” }
        }
        private lazy var label: UILabel = { ... }()
    }

下一步，我们会使用 UIControlEvents 来为各种点击交互事件分配响应的功能。


    addTarget(self, action: #selector(touchDown), for: [.touchDown, .touchDragEnter])
    addTarget(self, action: #selector(touchUp), for: [.touchUpInside, .touchDragExit, .touchCancel])