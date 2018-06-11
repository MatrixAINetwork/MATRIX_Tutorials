### 用 Java 代码实现区块链

让我们来看看用 Java 代码实现区块链的可能性。我们从基本原理出发，开发一些代码来演示它们是如何融合在一起的。

比特币（Bitcoin）炙手可热 —— 多么的轻描淡写。虽然数字加密货币的前景尚不明确，但区块链 —— 用于驱动比特币的技术 —— 却非常流行。
区块链的应用领域尚未探索完毕。它也有可能会破坏企业自动化。关于区块链的工作原理，有很多可用的信息。我们有一个深度区块链的[免费白皮书](https://link.juejin.im/?target=https%3A%2F%2Fkeyholesoftware.com%2Fwp-content%2Fuploads%2FBlockchain-For-The-Enterprise-Keyhole-White-Paper.pdf)（无需注册）。

本文将重点介绍区块链体系结构，特别是通过简单的代码示例演示“不可变，仅附加”的分布式账本是如何工作的。

作为开发者，阅读代码会比阅读技术文章更容易理解。至少对我来说是这样。那么我们开始吧！

### 简述区块链

首先我们简要总结下区块链。区块包含一些头信息和任意一组数据类型或一组交易。该链从第一个（初始）区块开始。随着交易被添加/扩展，将基于区块中可以存储多少交易来创建新区块。

当超过区块阀值大小时，将创建一个新的交易区块。新区块与前一个区块连接，因此称为区块链。


### 不可变性

因为交易时会计算 SHA-256 哈希值，所以区块链是不可变的。区块链的内容也被哈希则提供了唯一的标识符。此外，相连的前一个区块的哈希也会被在区块的头信息中散列并储存。

这就是为什么试图篡改区块基本上是不可能的，至少以目前的计算能力是这样的。下面是一个展示区块属性的 Java 类的部分定义。

     ...
     public class Block&lt;T extends Tx>; {
     public long timeStamp;
     private int index;
     private List<T> transactions = new ArrayList<T>();
     private String hash;
     private String previousHash;
     private String merkleRoot;
     private String nonce = "0000";

     // 缓存事务用 SHA256 哈希
    public Map<String,T> map = new HashMap<String,T>();

注意，注入的泛型类型为 Tx 类型。这允许交易数据发生变化。此外，previousHash 属性将引用前一个区块的哈希值。稍后将描述 merkleRoot 和 nonce 属性。

### 区块哈希值

每个区块可以计算一个哈希。这实际上是链接在一起的所有区块属性的哈希，包括前一个区块的哈希和由此计算而得的 SHA-256 哈希。

下面是在 Block.java 类中定义的计算哈希值的方法。

        ...
     public void computeHash() {
        Gson parser = new Gson(); // 可能应该缓存这个实例
        String serializedData = parser.toJson(transactions);  
        setHash(SHA256.generateHash(timeStamp + index + merkleRoot + serializedData + nonce + previousHash));
     }
        ...


交易被序列化为 JSON 字符串，因此可以在哈希之前将其追加到块属性中。

### 链

区块链通过接受交易来管理区块。当到达预定阀值时，就创建一个区块。下面是 SimpleBlockChain.java 的部分实现：

     ...
     ...
     public class SimpleBlockchain<T extends Tx> {
     public static final int BLOCK_SIZE = 10;
     public List<Block<T>> chain = new ArrayList<Block<T>>();

     public SimpleBlockchain() {
     // 创建初始区块
     chain.add(newBlock());
     }

     ...

注意，chain 属性维护了一个类型为 Tx 的区块列表。此外，无参构造器 会在创建初始链表时初始化“初始”区块。下面是 newBlock() 方法源码。

     ...
     public Block<T> newBlock() {
     int count = chain.size();
     String previousHash = "root";

     if (count > 0)
     previousHash = blockChainHash();

     Block<T> block = new Block<T>();

     block.setTimeStamp(System.currentTimeMillis());
     block.setIndex(count);
     block.setPreviousHash(previousHash);
     return block;
     }
     ...

