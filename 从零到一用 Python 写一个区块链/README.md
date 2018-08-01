## 从零到一用 Python 写一个区块链


### 背景知识……

要知道区块链是不可变的，有序的记录的链，记录也叫做区块。区块可以包含交易，文件或者任何你能想到的数据。不过至关重要的是，它们由哈希值****链接在一起。

如果你不知道哈希是什么，先看看[这篇文章](https://link.juejin.im/?target=https%3A%2F%2Flearncryptography.com%2Fhash-functions%2Fwhat-are-hash-functions)。


需要什么环境？ Python 版本不低于 3.6，装有 pip。还需要安装 Flask 和绝赞的 Requests 库：

    pip install Flask==0.12.2 requests==2.18.4
哦，你还得有个 HTTP 客户端，比如 Postman 或者 cURL。随便什么都可以。

那代码在哪里？ 源代码在[这里](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fdvf%2Fblockchain)。