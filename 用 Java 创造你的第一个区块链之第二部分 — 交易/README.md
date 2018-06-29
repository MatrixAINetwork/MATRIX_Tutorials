## 用 Java 创造你的第一个区块链之第二部分 —— 交易

这一系列教程的目的是帮助你们对区块链开发技术有一个大致的蓝图，你可以在这里找到教程的第一部分。

在教程的第二部分我们会：

- 生成一个简单的钱包。
- 使用我们的区块链发送带有签名的交易。
- 自我陶醉。

以上这些最终会造出我们自己的加密货币！


上一篇教程我们说到，我们有了一个基本的可验证区块链。但是现在我们的区块链只能存储相当没用的数据信息。今天我们要将这些无用数据替换为交易数据（我们的区块将能够存储多次交易），这样我们便可以创造一个十分简单的加密货币。我们把这种新币叫做：“菜鸟币”（英文原文：noobcoin）。

### 准备一个钱包

在加密货币中，货币所有权以交易的方式在区块链中转移，交易参与者持有资金的发送方和接收方的地址。如果只是钱包的基本形式，钱包可以只存储这些地址信息。然而，大多数钱包在软件层面上也能够生成新的交易。

不用担心关于交易部分的知识，我们很快会解释这些。

让我们创建一个 Wallet 类来持有我们的公钥和私钥信息：

    package noobchain;
    import java.security.*;

    public class Wallet {
	public PrivateKey privateKey;
	public PublicKey publicKey;
    }

请确保导入了 java.security.* 包 ！

### 这些公钥和私钥是用来干嘛的？
对于我们的“菜鸟币”来说，公钥就是作为我们的地址。你可以与他人分享公钥以便能收到付款。而我们的私钥是用来对我们的交易进行签名，这样除了私钥的主人就没人可以偷花我们的菜鸟币。 用户必须保管好自己的私钥！ 我们在交易的过程中也会发送出我们的公钥，公钥也可以用来验证我们的签名是否合法和数据是否被篡改。

私钥是用来对我们的数据进行签名，防止被篡改。公钥是用来验证这个签名。

我们以一对 KeyPair 的形式生成私钥和公钥。我们会采用椭圆曲线密码学去生成我们的 KeyPairs。 我们在 Wallet 类中添加一个 generateKeyPair() 方法，并且在构造方法中调用它：


    package noobchain;
    import java.security.*;

    public class Wallet {
	
	public PrivateKey privateKey;
	public PublicKey publicKey;
	
	public Wallet(){
		generateKeyPair();	
	}
		
	public void generateKeyPair() {
		try {
			KeyPairGenerator keyGen = KeyPairGenerator.getInstance("ECDSA","BC");
			SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
			ECGenParameterSpec ecSpec = new ECGenParameterSpec("prime192v1");
			// 初始化 KeyGenerator 并且生成一对 KeyPair
			keyGen.initialize(ecSpec, random);   //256 字节大小是可接受的安全等级
	        	KeyPair keyPair = keyGen.generateKeyPair();
	        	// 从 KeyPair中获取公钥和私钥
	        	privateKey = keyPair.getPrivate();
	        	publicKey = keyPair.getPublic();
		}catch(Exception e) {
			throw new RuntimeException(e);
		}
	}
	
    }

关于这个方法你所需要了解的就是它使用了 Java.security.KeyPairGenerator 去生成一个应用椭圆曲线密码学的 KeyPair。这个方法生成公钥和私钥并赋值到对应的公钥私钥对象。它很实用。

既然我们对 Wallet 类有了大致的认识，接下来看一下交易的部分。

