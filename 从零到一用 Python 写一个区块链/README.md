## 从零到一用 Python 写一个区块链


### 背景知识……

要知道区块链是不可变的，有序的记录的链，记录也叫做区块。区块可以包含交易，文件或者任何你能想到的数据。不过至关重要的是，它们由哈希值****链接在一起。

如果你不知道哈希是什么，先看看[这篇文章](https://link.juejin.im/?target=https%3A%2F%2Flearncryptography.com%2Fhash-functions%2Fwhat-are-hash-functions)。


需要什么环境？ Python 版本不低于 3.6，装有 pip。还需要安装 Flask 和绝赞的 Requests 库：

    pip install Flask==0.12.2 requests==2.18.4
哦，你还得有个 HTTP 客户端，比如 Postman 或者 cURL。随便什么都可以。

那代码在哪里？ 源代码在[这里](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fdvf%2Fblockchain)。

### 第一步：创建 Blockchain 类
用你喜欢的编辑器或者 IDE，新建 blockchain.py 文件，我个人比较喜欢 PyCharm。本文全文都使用这一个文件，但是如果你搞丢了，可以参考源代码。

表示区块链

创建 Blockchain 类，其构造函数会创建两个初始为空的列表，一个存储区块链，另一个存储交易信息。类设计如下：


    class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass
    
    def new_transaction(self):
        # Adds a new transaction to the list of transactions
        pass
    
    @staticmethod
    def hash(block):
        # Hashes a Block
        pass

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

Blockchain 类的设计

Blockchain 类负责管理链。它用来存储交易信息，也有一些帮助方法用来将新区块添加到链中。我们接着来实现一些方法