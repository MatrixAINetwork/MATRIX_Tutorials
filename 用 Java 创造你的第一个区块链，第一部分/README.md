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

测试

我们在主类 NoobChain 中新建一些区块对象并将其 hash 值打印到屏幕上，来确保一切工作正常有序