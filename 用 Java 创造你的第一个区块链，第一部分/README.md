## 用 Java 创造你的第一个区块链－第一部分

本系列文章旨在帮助你了解如何使用开发区块链技术。

本文会讲到：

- 创造你的第一个（十分）基础的‘区块链’。
- 实现一个简单的验证性（挖矿）系统。
- 奇迹是有可能发生的.

( 本文假设你对于面向对象编程已经有了基本的了解 )
值得注意的是，文中讲到的并不是一个功能完整，可以上线的区块链系统。相反，这只是一个概念验证性工作，来帮助你理解什么是区块链以便阅读未来的教程.


#### 准备工作
本文准备使用 Java 作为开发语言，但是你应该能够使用任何面向对象语言来跟着一起学习。我会使用 Eclipse，不过你也可以使用任何其他喜欢的编辑器（ 虽然你会错过很多方便的功能）。

你需要：

- 安装 Java 和 JDK
- Eclipse (或者其他 IDE/编辑器)

你的 eclipse 界面也许会看起来和我的不一样，不过没关系，那是因为我使用了深色主题。

你可以安装 GSON library by google (这是什么 ???)，当然这是可选项。它可以让我们将 object 转换成 Json \o/。这是一个超级实用的库，在后面我们也将它用到 peer2peer 上，但你随时可以用一个类似的方法去替换它。

在 Eclipse 中 创建一个 Java 项目(file > new > )。我将我的项目命名为“noobchain”，接着创建一个新的同名 Class （NoobChain）。


![](https://i.imgur.com/l0bm0RO.png)


#### 创造区块链

一个区块链只是一个个区块的链接/列表。区块链中的每一个区块都会有自己的数字签名，前一个区块的数字签名和一些数据（例如一些交易数据）。

![](https://i.imgur.com/PPmUqSX.png)

    Hash = Digital Signature.

每一个区块不仅仅包含前一个区块的 hash 值，其自己的 hash 值，有一部分是根据前一个区块的 hash 值计算出来的。如果前一个区块的数据发生了变化，那么前一个区块的 hash 值也会随之变化（因为它有一部分是根据区块的数据进行计算的），并会依次影响所有区块的 hash 值。通过计算和比较 hash 值，我们可以判断区块链是否合法。

这意味着什么？修改链中的任意数据，都会改变数字签名，进而破坏整个区块链。

那么首先让我们来创建组成区块链的 Block 类：

    import java.util.Date;

    public class Block {

	public String hash;
	public String previousHash;
	private String data; //我们的数据是一条简单的消息
	private long timeStamp; //从 1/1/1970 起至现在的总毫秒数.

	//Block 类的构造方法.
	public Block(String data,String previousHash ) {
		this.data = data;
		this.previousHash = previousHash;
		this.timeStamp = new Date().getTime();
	}
    }

你可以看到，我们的基础 Block 类包含一个 String hash，它代表了数字签名。previousHash 变量为前一个区块的 hash 值，它和 String data 组成了这个区块的数据。

接着我们需要一种方法去生成数字签名，

有很多加密算法可供我们选择，当然 SHA256 算法正好适合我们这个例子。我们可以通过 import java.security.MessageDigest; 来使用 SHA256 算法。

我们在 StringUtil ‘工具’ 类 中创建了一个方便使用的方法，以便在接下来去使用 SHA256 算法：

    import java.security.MessageDigest;

    public class StringUtil {
	//使用 Sha256 算法加密一个字符串，返回计算结果
	public static String applySha256(String input){		
		try {
			MessageDigest digest = MessageDigest.getInstance("SHA-256");	        
			//对输入使用 sha256 算法
			byte[] hash = digest.digest(input.getBytes("UTF-8"));	        
			StringBuffer hexString = new StringBuffer(); // 它会包含16进制的 hash 值
			for (int i = 0; i < hash.length; i++) {
				String hex = Integer.toHexString(0xff & hash[i]);
				if(hex.length() == 1) hexString.append('0');
				hexString.append(hex);
			}
			return hexString.toString();
		}
		catch(Exception e) {
			throw new RuntimeException(e);
		}
	}	
    }


如果你不理解这个辅助方法的内容，也不用担心。 你只需要知道，它接受一个字符串作为输入，并对其使用 SHA256 算法，最后将返回的字符串作为数字签名。

现在让我们在 Block class 中的一个新方法里使用 applySha256 辅助方法来计算 hash 值。我们必须根据区块中那些不想被篡改的数据来计算 hash 值。对于本文中的区块，我们会包含 previousHash、data 和 timeStamp。


    public String calculateHash() {
	String calculatedhash = StringUtil.applySha256( 
			previousHash +
			Long.toString(timeStamp) +
			data 
			);
	return calculatedhash;
    }

让我们把这个方法加入到 Block 构造方法中去...

	public Block(String data,String previousHash ) {
		this.data = data;
		this.previousHash = previousHash;
		this.timeStamp = new Date().getTime();
		this.hash = calculateHash(); //Making sure we do this after we set the other values.
	}

开始测试...

我们在主类 NoobChain 中新建一些区块对象并将其 hash 值打印到屏幕上，来确保一切工作正常有序。

第一个区块被命名为起始区块，由于它前面没有区块，所以我们用 “0” 作为其前一个区块的 hash 值。


    public class NoobChain {

	public static void main(String[] args) {
		
		Block genesisBlock = new Block("Hi im the first block", "0");
		System.out.println("Hash for block 1 : " + genesisBlock.hash);
		
		Block secondBlock = new Block("Yo im the second block",genesisBlock.hash);
		System.out.println("Hash for block 2 : " + secondBlock.hash);
		
		Block thirdBlock = new Block("Hey im the third block",secondBlock.hash);
		System.out.println("Hash for block 3 : " + thirdBlock.hash);
		
	}
    }

这段程序的输出应该类似于：

![](https://i.imgur.com/5873sg8.png)

由于时间戳不一样，你的 hash 值和我的应该会不同。

现在，每一个区块应该拥有自己的基于区块数据和前一个区块签名计算出来的数字签名

目前，这还并不是区块链，所以让我们将区块存储在一个 ArrayList 中并导入 gson 库来将其输出为 Json 字符串


    import java.util.ArrayList;
    import com.google.gson.GsonBuilder;

    public class NoobChain {
	
	public static ArrayList<Block> blockchain = new ArrayList<Block>(); 

	public static void main(String[] args) {	
		//将我们的区块加入到区块链 ArrayList 中：
		blockchain.add(new Block("Hi im the first block", "0"));		
		blockchain.add(new Block("Yo im the second block",blockchain.get(blockchain.size()-1).hash)); 
		blockchain.add(new Block("Hey im the third block",blockchain.get(blockchain.size()-1).hash));
		
		String blockchainJson = new GsonBuilder().setPrettyPrinting().create().toJson(blockchain);		
		System.out.println(blockchainJson);
	}

    }


#### 现在我们需要一种方法来检查区块链的完整合法性

让我们在 NoobChain 类 中新建一个返回值为 Boolean 的 isChainValid() 方法，它会循环链中所有的区块并比较其 hash 值。这个方法需要能够检查当前区块的 hash 值和计算出来的 hash 值是否相等以及前一个区块的 hash 值是否等于当前区块存储的 previousHash 值。

    public static Boolean isChainValid() {
	Block currentBlock; 
	Block previousBlock;
	
	//循环区块链并检查 hash 值：
	for(int i=1; i < blockchain.size(); i++) {
		currentBlock = blockchain.get(i);
		previousBlock = blockchain.get(i-1);
		//比较当前区块存储的 hash 值和计算出来的 hash 值：
		if(!currentBlock.hash.equals(currentBlock.calculateHash()) ){
			System.out.println("Current Hashes not equal");			
			return false;
		}
		//比较前一个区块存储的 hash 值和当前区块存储的 previousHash 值：
		if(!previousBlock.hash.equals(currentBlock.previousHash) ) {
			System.out.println("Previous Hashes not equal");
			return false;
		}
	}
	return true;
    }

对链中的区块做任何改变都会导致这个方法返回 false。

在比特币网络中，区块链被每个节点所共享，最长的合法链会被接受。那么靠什么去阻止某人篡改旧区块中的数据，然后创建一个全新的更长的区块链并将其分享到网络中？答案是区块链的合法性验证工作量。 hashcash 的验证工作意味着计算机需要大量的时间和计算能力来创建新的区块。

因此，攻击者需要比其他同行拥有更多的计算能力。

hashcash, 那需要很大的工作量

#### 开始挖矿
我们要求 miners 去做验证性工作，通过在区块中尝试不同的参数值直到其 hash 值以若干个 0 开头。

让我们新增一个 int 类型的 nonce 变量，并将其使用到 calculateHash() 方法和十分重要的 mineBlock() 方法中：

