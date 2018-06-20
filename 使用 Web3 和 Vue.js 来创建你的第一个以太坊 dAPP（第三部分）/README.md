## 使用 Web3 和 Vue.js 来创建你的第一个以太坊 dAPP（第三部分）

##### 上接第二部分


到目前为止，我们的应用程序能够从 metamask 获取并显示帐户数据。但是，在更改帐户时，如果不重新加载页面，则不会更新数据。这并不是最优的，我们希望能够确保响应式地更新数据。
我们的方法与简单地初始化 web3 实例略有不同。Metamask 还不支持 websockets，因此我们将不得不每隔一段时间就去轮询数据是否有修改。我们不希望在没有更改的情况下调度操作，因此只有在满足某个条件（特定更改）时，我们的操作才会与它们各自的有效负载一起被调度。
也许上述方法并不是诸多解决方案中的最优解，但是它在严格模式的约束下工作，所以还算不错。在 util 文件夹中创建一个名为 pollWeb3.js 的新文件。下面是我们要做的：

- 导入 web3，这样我们就不依赖于 Metamask 实例
- 导入我们的 store，这样我们就可以进行数据对比和分发操作
- 创建 web3 实例
- 设置一个间隔来检查地址是否发生了变化，如果没有，检查余额是否发生了变化
- 如果地址或余额有变化，我们将更新我们的 store。因为我们的 hello-metamask 组件具有一个 Computed 属性，这个改变是响应式的

![](https://i.imgur.com/2oQaQC4.png)
   

现在，一旦我们的 web3 实例被初始化，我们就要开始轮询更新。所以，打开 Store/index.js ，导入 pollWeb3.js 文件，并将其添加到我们的 regierWeb3Instance() 方法的底部，以便在状态更改后执行。


    import pollWeb3 from '../util/pollWeb3'

    registerWeb3Instance (state, payload) {
    console.log('registerWeb3instance Mutation being executed', payload)
    let result = payload
    let web3Copy = state.web3
    web3Copy.coinbase = result.coinbase
    web3Copy.networkId = result.networkId
    web3Copy.balance = parseInt(result.balance, 10)
    web3Copy.isInjected = result.injectedWeb3
    web3Copy.web3Instance = result.web3
    state.web3 = web3Copy
    pollWeb3()
    }

由于我们正在调度操作，所以需要将其添加到 store 中，并进行变异以提交更改。我们可以直接提交更改，但为了保持模式一致性，我们不这么做。我们将添加一些控制台日志，以便您可以在控制台中观看精彩的过程。在 actions 对象中添加：

    pollWeb3 ({commit}, payload) {
    console.log('pollWeb3 action being executed')
    commit('pollWeb3Instance', payload)
    }

搞定了！如果我们现在改变 Metamask 的地址，或者余额发生变化，我们将看到在我们的应用程序无需重新加载页面更新。当我们更改网络时，页面将重新加载，我们将重新注册一个新实例。但是，在生产中，我们希望显示一个警告，要求更改到部署协约的正确网络。

在下一节，我们将最终深入到我们的智能协议连接到我们的应用程序。与我们已经做过的相比，这实际上相当容易了。

### 实例化我们的协议

首先，我们将编写代码，然后部署协议并将 ABI 和 Address 插入到应用程序中。为了创建我们期待已久的 casino 组件，需要执行以下操作：

- 需要一个输入字段，以便用户可以输入下注金额
- 需要代表下注数字的按钮，当用户点击某个数字时，它将把输入的金额押在该数字上
- onClick 函数将调用 smart 协议上的 bet() 函数
- 显示一个加载旋转器，以显示事务正在进行中
- 交易完成后，我们会显示用户是否中奖以及中奖金额

但是，首先，我们需要我们的应用程序能够与我们的智能协议交互。我们将用已经做过的同样的方法来处理该问题。在 util 文件夹中创建一个名为 getContract.js 的新文件。

    import Web3 from ‘web3’
    import {address, ABI} from ‘./constants/casinoContract’

    let getContract = new Promise(function (resolve, reject) {
    let web3 = new Web3(window.web3.currentProvider)
    let casinoContract = web3.eth.contract(ABI)
    let casinoContractInstance = casinoContract.at(address)
    // casinoContractInstance = () => casinoContractInstance
    resolve(casinoContractInstance)
    })

    export default getContract

首先要注意的是，我们正在导入一个尚不存在的文件，稍后我们将在部署协议时修复该文件。

首先，我们通过将 ABI(我们将回到)传递到 web3.eth.Contact() 方法中，为稳固性协议创建一个协议对象。然后，我们可以在一地址上初始化该对象。在这个实例中，我们可以调用我们的方法和事件。

然而，如果没有 action 和变体，这将是不完整的。因此，在 casino-component.vue 的脚本标记中添加以下内容。


    export default {
    name: ‘casino’,
    mounted () {
    console.log(‘dispatching getContractInstance’)
    this.$store.dispatch(‘getContractInstance’)
    }
    }

