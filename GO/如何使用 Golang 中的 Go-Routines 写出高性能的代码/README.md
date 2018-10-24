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



