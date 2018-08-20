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

区块长什么样？

每个区块都有其索引，时间戳（Unix 时间），交易列表，证明（稍后解释），以及前序区块的哈希值。

下面是一个单独区块


    block = {
    'index': 1,
    'timestamp': 1506057125.900785,
    'transactions': [
        {
            'sender': "8527147fe1f5426f9dd545de4b27ee00",
            'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
            'amount': 5,
        }
    ],
    'proof': 324984774000,
    'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    }


区块链中的区块的例子

到这里链的概念就介绍清楚了：每个新区块都包含上一个区块的哈希。这一重要概念使得区块链的不可变性成为可能：如果攻击者篡改了链中的前序区块，所有的后续区块的哈希都是错的。

理解了吗？如果没有想明白，花点时间思考一下，这是区块链的核心思想。


### 在区块中添加交易信息
此外，还需要在区块中添加交易信息的方法。用 new_transaction() 方法来做这件事吧，代码写出来非常直观：


    class Blockchain(object):
    ...
    
    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

new_transaction() 在列表中添加新交易之后，会返回该交易被加到的区块的索引，也就是指向下一个要挖的区块。稍后会讲到这对于之后提交交易的用户会有用。


### 创建新区块

实例化 Blockchain 类之后，需要新建一个创始区块，它没有任何前序区块。此外还要在创始区块中加入证明，证明来自挖矿（或者工作量证明）。稍后再来讨论挖矿这件事。

除了要在构造函数中创建创始区块，我们还要实现 new_block()，new_transaction() 和 hash()。


    import hashlib
    import json
    from time import time
 

    class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

上面的代码还是比较直观的，还有一些注释和文档字符串做进一步解释。这样就差不多可以表示区块链了。但是到了这一步，你一定好奇新区块是怎样被创建，锻造或者挖出来的。
