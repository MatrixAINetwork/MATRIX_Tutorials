### Swift 5 强制独占性原则

    Swift 5 允许在 Release 构建过程中默认启用关于「独占访问内存」的运行时检查，进一步增强了 Swift 作为安全语言的能力。在 Swift 4 中，这种运行时检查仅允许在 Debug 构建过程中启用。在这篇文章中，首先我将解释这个变化对 Swift 开发人员的意义，然后再深入研究为什么它对 Swift 的安全和性能策略至关重要。


### 背景

为了实现 内存安全，Swift 需要对变量进行独占访问时才能修改该变量。本质上来说，当一个变量作为 inout 参数或者 mutating 方法中的 self 被修改时，不能通过不同的名称被访问的。

在以下示例中，通过将 count 作为 inout 参数传递来对 count 变量进行修改。出现独占性违规情况是因为 modifier 闭包对捕获的 count 变量同时进行了读取操作，并且在同一变量修改的范围内进行了调用。在 modifyTwice 函数中，count 变量只能通过 inout 修饰的 value 参数来进行安全访问而在 modified 闭包内，它只能以 $0 来进行安全访问。


    func modifyTwice(_ value: inout Int, by modifier: (inout Int) -> ()) {
    modifier(&value)
    modifier(&value)
    }
    
    func testCount() {
    var count = 1
    modifyTwice(&count) { $0 += count }
    print(count)
    }


违反独占性的情况通常如此，程序员的意图此时显得有些模糊。他们希望 count 打印的值是「3」还是「4」呢？无论哪种结果，编译器都无法保证。更糟糕的是，编译器优化会在出现此类错误时产生微妙的不可预测行为。为了防止违反独占性并允许引入依赖于安全保证的语言特性，强制独占性最初在 Swift 4.0 中引入的：[SE-0176：实施对内存的独占访问](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fapple%2Fswift-evolution%2Fblob%2Fmaster%2Fproposals%2F0176-enforce-exclusive-access-to-memory.md)。

编译时（静态）检测可以捕获许多常见的独占性违规行为，但是还需要运行时（动态）检测来捕获涉及逃逸闭包，类类型的属性，静态属性和全局变量的违规情况。Swift 4.0 同时提供了编译时和运行时的强制性检测，但运行时的强制检测仅在 Debug 构建过程中启用。


在 Swift 4.1 和 4.2 中，编译器检查能力逐渐得到加强，可以捕获到越来越多程序员绕过独占性规则的情况 —— 最明显的是在非逃逸闭包中捕获变量，或者将非逃逸闭包转换为逃逸闭包。Swift 4.2 宣称，[在 Swift 4.2 中将独占访问内存警告升级为错误](https://link.juejin.im/?target=https%3A%2F%2Fforums.swift.org%2Ft%2Fupgrading-exclusive-access-warning-to-be-an-error-in-swift-4-2%2F12704)，并解释了一些受新强制独占性检测影响的常见案例。

Swift 5 修复了语言模型中剩余的漏洞，并完全执行了该模型。 由于在 Release 编译过程中默认启用了对内存独占情况的强制性运行时检查，一些以前表现得很好的但未在 Debug 模式下被充分测试的 Swift 程序可能会受到一些影响

一些罕见的还无法被编译器检测出来的涉及非法代码的情况（[SR-8546](https://link.juejin.im/?target=https%3A%2F%2Fbugs.swift.org%2Fbrowse%2FSR-8546)，[SR-9043](https://link.juejin.im/?target=https%3A%2F%2Fbugs.swift.org%2Fbrowse%2FSR-9043)）。

### 对 Swift 项目的影响

Swift 5 中的强制独占性检查对现有项目可能会产生以下两种影响：


如果项目源码违反了 Swift 的独占性规则（具体查看 [SE-0176：实施对内存的独占访问](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fapple%2Fswift-evolution%2Fblob%2Fmaster%2Fproposals%2F0176-enforce-exclusive-access-to-memory.md)），Debug 调试测试时未能执行无效代码，然后，在构建 Release 二进制文件时可能会触发运行时陷阱。产生崩溃并抛出一个包含字符串的诊断消息：
「Simultaneous accesses to …, but modification requires exclusive access」
源代码级别修复通常很简单。后面的章节会展示常见的违规和修复示例。


内存访问检查的开销可能会影响的 Release 二进制包的性能。在大多数情况下，这种影响应该很小；如果你发现某个明显的性能下降情况，请提交 bug，以便我们了解需要改进的内容。作为一般性准则，应当避免在大多数性能关键循环中执行类属性访问，特别是在每个循环迭代中的不同对象上。如果必须如此，那么你可以将类属性修饰为 private 或 internal 来帮助告知编译器没有其他代码访问循环内的相同属性。


你可以通过 Xcode 的「Exclusive Access to Memory」构建设置来禁用这些运行时检查，该设置还有「Run-time Checks in Debug Builds Only」和「Compile-time Enforcement Only」两个选项：

![](https://user-gold-cdn.xitu.io/2019/2/28/16932f8a6b530db2?imageslim)