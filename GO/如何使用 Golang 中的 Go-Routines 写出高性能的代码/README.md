## 如何使用 Golang 中的 Go-Routines 写出高性能的代码


为了用 Golang 写出快速的代码，你需要看一下 Rob Pike 的视频 - Go-Routines。

他是 Golang 的作者之一。如果你还没有看过视频，请继续阅读，这篇文章是我对那个视频内容的一些个人见解。我感觉视频不是很完整。我猜 Rob 因为时间关系忽略掉了一些他认为不值得讲的观点。不过我花了很多的时间来写了一篇综合全面的关于 go-routines 的文章。我没有涵盖视频中涵盖的所有主题。我会介绍一些自己用来解决 Golang 常见问题的项目。

好的，为了写出很快的 Golang 程序，有三个概念你需要完全了解，那就是 Go-Routines，闭包，还有管道。


### Go-Routines

让我们假设你的任务是将 100 个盒子从一个房间移到另一个房间。再假设，你一次只能搬一个盒子，而且移动一次会花费一分钟时间。所以，你会花费 100 分钟的时间搬完这 100 个箱子。

现在，为了让加快移动 100 个盒子这个过程，你可以找到一个方法更快的移动这个盒子（这类似于找一个更好的算法去解决问题）或者你可以额外雇佣一个人去帮你移动盒子（这类似于增加 CPU 核数用于执行算法）

这篇文章重点讲第二种方法。编写 go-routines 并利用一个或者多个 CPU 核心去加快应用的执行。

任何代码块在默认情况下只会使用一个 CPU 核心，除非这个代码块中声明了 go-routines。所以，如果你有一个 70 行的，没有包含 go-routines 的程序。它将会被单个核心执行。就像我们的例子，一个核心一次只能执行一个指令。因此，如果你想加快应用程序的速度，就必须把所有的 CPU 核心都利用起来。


所以，什么是 go-routine。如何在 Golang 中声明它？

让我们看一个简单的程序并介绍其中的 go-routine。


### 示例程序 1

假设移动一个盒子相当于打印一行标准输出。那么，我们的实例程序中有 10 个打印语句（因为没有使用 for 循环，我们只移动 10 个盒子）。

    package main

    import "fmt"

    func main() {
    fmt.Println("Box 1")
    fmt.Println("Box 2")
    fmt.Println("Box 3")
    fmt.Println("Box 4")
    fmt.Println("Box 5")
    fmt.Println("Box 6")
    fmt.Println("Box 7")
    fmt.Println("Box 8")
    fmt.Println("Box 9")
    fmt.Println("Box 10")
    }


因为 go-routines 没有被声明，上面的代码产生了如下输出。

#### 输出

    Box 1
    Box 2
    Box 3
    Box 4
    Box 5
    Box 6
    Box 7
    Box 8
    Box 9
    Box 10

所以，如果我们想在在移动盒子这个过程中使用额外的 CPU 核心，我们需要声明一个 go-routine。


### 包含 Go-Routines 的示例程序 2

    package main

    import "fmt"

    func main() {
    go func() {
        fmt.Println("Box 1")
        fmt.Println("Box 2")
        fmt.Println("Box 3")
    }()
    fmt.Println("Box 4")
    fmt.Println("Box 5")
    fmt.Println("Box 6")
    fmt.Println("Box 7")
    fmt.Println("Box 8")
    fmt.Println("Box 9")
    fmt.Println("Box 10")
    }


这儿，一个 go-routine 被声明且包含了前三个打印语句。意思是处理 main 函数的核心只执行 4-10 行的语句。另一个不同的核心被分配去执行 1-3 行的语句块。


### 输出

    Box 4
    Box 5
    Box 6
    Box 1
    Box 7
    Box 8
    Box 2
    Box 9
    Box 3
    Box 10


### 分析输出

在这段代码中，有两个 CPU 核心同时运行，试图执行他们的任务，并且这两个核心都依赖标准输出来完成它们相应的任务（因为这个示例中我们使用了 print 语句）换句话来说，标准输出（运行在它自己的一个核心上）一次只能接受一个任务。所以，你在这儿看到的是一种随机的排序，这取决于标准输出决定接受 core1 core2 哪个的任务。



### 如何声明 go-routine？

为了声明我们自己的 go-routine，我们需要做三件事。

- 我们创建一个匿名函数
- 我们调用这个匿名函数
- 我们使用 「go」关键字来调用

所以，第一步是采用定义函数的语法，但忽略定义函数名（匿名）来完成的。


    func() {
    fmt.Println("Box 1")
    fmt.Println("Box 2")
    fmt.Println("Box 3")
    }

第二步是通过将空括号添加到匿名方法后面来完成的。这是一种叫命名函数的方法。


    func() {
     fmt.Println("Box 1")
    fmt.Println("Box 2")
    fmt.Println("Box 3")
    } ()


步骤三可以通过 go 关键字来完成。什么是 go 关键字呢，它可以将功能块声明为可以独立运行的代码块。这样的话，它可以让这个代码块被系统上其他空闲的核心所执行。


    #细节 1：当 go-routines 的数量比核心数量多的时候会发生什么？
    单个核心通过上下文切换并行执行多个go程序来实现多个核心的错觉。
    #自己试试之1：试着移除示例程序2中的 go 关键字。输出是什么呢？
    答案：示例程序2的结果和1一模一样。
    #自己试试之 2：将匿名函数中的语句从 3 增加至 8 个。结果改变了吗？
    答案：是的。main 函数是一个母亲 go-routine（其他所有的 go-routine 都在它里面被声明和创建）。所以，当母亲 go-routine 执行结束，即使其他 go-routines 执行到中途，它们也会被杀掉然后返回。


我们现在已经知道 go-routines 是什么了。接下来让我们来看看闭包。

如果之前没有在 Python 或者 JavaScript 中学过闭包，你可以现在在 Golang 中学习它。学到的人可以跳过这部分来节省时间，因为 Golang 中的闭包和 Python 或者 JavaScript 中是一样的。

在我们深入理解闭包之前。让我们先看看不支持闭包属性的语言比如 C，C++ 和 Java，在这些语言中，

函数只访问两种类型的变量，全局变量和局部变量（函数内部的变量）。

没有函数可以访问声明在其他函数里的变量。

一旦函数执行完毕，这个函数中声明的所有变量都会消失。

对 Golang，Python 或者 JavaScript 这些支持闭包属性的语言，以上都是不正确的，原因在于，这些语言拥有以下的灵活性。

函数可以声明在函数内。

函数可以返回函数。



    推论 #1：因为函数可以被声明在函数内部，一个函数声明在另一个函数内的嵌套链是这种灵活性的常见副产品


为了了解为什么这两个灵活性完全改变了运作方式，让我们看看什么是闭包。


### 所以什么是闭包？

除了访问局部变量和全局变量，函数还可以访问函数声明中声明的所有局部变量，只要它们是在之前声明的（包括在运行时传递给闭包函数的所有参数），在嵌套的情况下，函数可以访问所有函数的变量（无论闭包的级别如何）。

为了理解的更好，让我们考虑一个简单的情况，两个函数，一个包含另一个。


    package main

    import "fmt"

    var zero int = 0

    func main() {
    var one int = 1
    child := func() {
        var two int = 3
        fmt.Println(zero)
        fmt.Println(one)
        fmt.Println(two)
        fmt.Println(three) // causes compilation Error
    }
    child()
    var three int = 2
    }


这儿有两个函数 - 主函数和子函数，其中子函数定义在主函数中。子函数访问

- zero 变量 - 它是全局变量
- one 变量 - 闭包属性 - one 属于主函数，它在主函数中且定义在子函数之前。
- two 变量 - 它是子函数的局部变量

