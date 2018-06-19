## 使用 Web3 和 Vue.js 来创建你的第一个以太坊 dAPP（第二部分）

欢迎回到这个很棒的系列教程的第二部分，在个教程中我们要亲身实践，创建我们的第一个去中心化应用（decentralized application）。在第二部分中，我们将介绍 VueJS 和 VueX 的核心概念以及 web3js 与 metamask 的交互。


进入正题：VueJS

VueJS 是一个用于构建用户界面的 JavaScript 框架。初看起来，它类似传统的 mustache（译者注：原文为 moustache）模板，但其实 Vue 在后面做了很多工作。

    <div id=”app”>
    {{ message }}
    </div>
    
    var app = new Vue({
    el: '#app',
    data: {
    message: 'Hello Vue!'
    }
    })

这是一个很基本的 Vue 应用的结构。数据对象中的 message 属性会被渲染到屏幕上 id 为「app」的元素中，当我们改变 message 时，屏幕上的值也会实时更新。你可以去这个 jsfiddle 上查看（开启自动运行）：jsfiddle.net/tn1mfxwr/2/

VueJS 的另一个重要特征是组件。组件是小的、可复用的并且可嵌套的小段代码。本质上，一个 Web 应用是由较小组件组成的组件树构成的。当我们着手编写我们前端应用时，我们会愈加清楚。

![](https://i.imgur.com/bGJEgn6.png)


这个页面示例是由组件构成的。页面由三个组件组成的，其中的两个有子组件。

### 状态的整合: Vuex
我们使用 Vuex 管理应用的状态。类似于 Redux，Vuex 实现了一个对于我们应用数据「单一数据源」的容器。Vuex 允许我们使用一种可预见的方法操作和提供应用程序使用的数据。

它工作的方式是非常直观的。当组件需要数据进行渲染时，它会触发（dispatch）一个 action 获取所需的数据。Action 中获取数据的 API 调用是异步的。一旦取得数据，action 会将数据提交（commit）给一个变化（mutation）。然后，Mutation 会使得我们容器（store）的状态发生改变（alert the state）。当组件使用的容器中的数据改变时，它会重新进行渲染。

![](https://i.imgur.com/doJqM9z.png)


Vuex 的状态管理模式。

在我们继续之前...

在第一部分中，我们已经通过 vue-cli 生成了一个 Vue 应用，我们也安装了所需的依赖。如果你没有这样做的话，请查看上面第一部分的链接。

如果你正确完成了各项的话，你的目录看起来应该是这样的：


![](https://i.imgur.com/wicjT55.png)

新生成的 vue 应用。

小提示：如果你要从这里复制粘贴代码段的话，请在你的 .eslintignore 文件中添加 /src/，以免出现缩进错误。

你可以在终端中输入 npm start 运行这个应用。首先我们需要清理它包含的这个默认的 Vue 应用。

注解：尽管只有一个路由，但是我们还是会使用 Vue Router，虽然我们并不需要，但是因为这个教程相当简单，我想将其保留会更好。

贴士：在你的 Atom 编辑器右下角中将 .vue 文件设置为 HTML 语法（高亮）

现在处理这个刚生成的应用：

- 在 app.vue 中删除 img 标签和 style 标签中的内容。

- 删除 components/HelloWorld.vue，创建两个名为 casino-dapp.vue（我们的主组件）和 hello-metamask.vue（将包含我们的 Metamask 数据）的两个新文件。

- 在我们的新 hello-metamask.vue 文件中粘贴下面的代码，它现在只显示了在一个 p 标签内的「hello」文本。


    <template>
    <p>Hello</p>
    </template>

    <script>
    export default {
    name: 'hello-metamask'
    }
    </script>

    <style scoped>

    </style>

现在我们首先导入 hello-metamask 组件文件，通过导入文件将其加载到主组件 casino-app 中，然后在我们的 vue 实例中，引用它作为模板中一个标签。在 casino-dapp.vue 中粘贴这些代码：

    <template>
    <hello-metamask/>
    </template>

    <script>
    import HelloMetamask from '@/components/hello-metamask'
    export default {
    name: 'casino-dapp',
    components: {
    'hello-metamask': HelloMetamask
    }
    }
    </script>

    <style scoped>

    </style>

现在如果你打开 router/index.js 你会看到 root 下只有一个路由，它现在仍指向我们已删除的 HelloWorld.vue 组件。我们需要将其指向我们主组件 casino-app.vue。

    import Vue from 'vue'
    import Router from 'vue-router'
    import CasinoDapp from '@/components/casino-dapp'

    Vue.use(Router)

    export default new Router({
    routes: [
    {
    path: '/',
    name: 'casino-dapp',
    component: CasinoDapp
    }
    ]
    })


关于 Vue Router：你可以增加额外的路径并为其绑定组件，当你访问定义的路径时，在 App.vue 文件中的 router-view 标签中，对应的组件会被渲染，并进行显示。

- 在 src 中创建一个名为 util 的新文件夹，在这个文件夹中创建另一个名为 constants 的新文件夹，并创建一个名为 networks.js 的文件，粘贴下面的代码。我们用 ID 来代替以太坊（Ethereum）网络名称显示，这样做会保持我们代码的整洁。

    export const NETWORKS = {
    '1': 'Main Net',
    '2': 'Deprecated Morden test network',
    '3': 'Ropsten test network',
    '4': 'Rinkeby test network',
    '42': 'Kovan test network',
    '4447': 'Truffle Develop Network',
    '5777': 'Ganache Blockchain'
     }


- 最后的但同样重要的（实际上现在用不到）是，在 src 中创建一个名为 store 的新文件夹。我们将在下一节继续讨论。

如果你在终端中执行 npm start，并在浏览器中访问 localhost:8000，你应该可以看到「Hello」出现在屏幕上。如果是这样的话，就表示你准备好进入下一步了。

### 设置我们的 Vuex 容器

在这一节中，我们要设置我们的容器（store）。首先从在 store 目录（上一节的最后一部分）下创建两个文件开始：index.js 和 state.js；我们先从 state.js 开始，它是我们所检索的数据一个空白表示（Blank representation）。

    let state = {
    web3: {
    isInjected: false,
    web3Instance: null,
    networkId: null,
    coinbase: null,
    balance: null,
    error: null
    },
    contractInstance: null
    }
    export default state


好了，现在我们要对 index.js 进行设置。我们会导入 Vuex 库并且告诉 VueJS 使用它。我们也会把 state 导入到我们的 store 文件中。

    import Vue from 'vue'
    import Vuex from 'vuex'
    import state from './state'

    Vue.use(Vuex)

    export const store = new Vuex.Store({
    strict: true,
    state,
    mutations: {},
    actions: {}
    })


最后一步是编辑 main.js ，以包含我们的 store 文件：

    import Vue from 'vue'
    import App from './App'
    import router from './router'
    import { store } from './store/'

    Vue.config.productionTip = false

    /* eslint-disable no-new */
    new Vue({
    el: '#app',
    router,
    store,
    components: { App },
    template: '<App/>'
    })


