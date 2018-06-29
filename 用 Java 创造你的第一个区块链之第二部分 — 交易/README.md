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

### 交易和签名

每一个交易都包含一定大小的数据：

- 资金发送方的公钥（地址）。
- 资金接受方的公钥（地址）。
- 要转账的资金数额。
- 输入，是上一次交易的引用，证明发送方有资金可以发送出去。
- 输出，是在交易中接收方收到的金额。 （在新交易中这些输出也会被当作是输入）
- 一个加密的签名，证明地址的所有者是发送这个交易的人并且发送的数据没有被篡改。（例如，阻止第三方更改发送出去的数额）

让我们写一个新的 Transaction 类：

    import java.security.*;
    import java.util.ArrayList;

    public class Transaction {
	
	public String transactionId; // 这个也是交易的哈希值
	public PublicKey sender; // 发送方地址/公钥
	public PublicKey reciepient; // 接受方地址/公钥
	public float value;
	public byte[] signature; // 用来防止他人盗用我们钱包里的资金
	
	public ArrayList<TransactionInput> inputs = new ArrayList<TransactionInput>();
	public ArrayList<TransactionOutput> outputs = new ArrayList<TransactionOutput>();
	
	private static int sequence = 0; // 对已生成交易个数的粗略计算 
	
	// 构造方法： 
	public Transaction(PublicKey from, PublicKey to, float value,  ArrayList<TransactionInput> inputs) {
		this.sender = from;
		this.reciepient = to;
		this.value = value;
		this.inputs = inputs;
	}
	
	// 用来计算交易的哈希值（可作为交易的 id）
	private String calulateHash() {
		sequence++; //increase the sequence to avoid 2 identical transactions having the same hash
		return StringUtil.applySha256(
				StringUtil.getStringFromKey(sender) +
				StringUtil.getStringFromKey(reciepient) +
				Float.toString(value) + sequence
				);
	}
    }

我们应该也写一个空的 TransactionInput 类和 TransactionOutput 类，我们之后会把它们补上。

我们的交易类也包含了生成/验证签名和验证交易的相关方法。

### 这些签名的目的和工作方式是什么？


签名在我们区块链中起到的两个很重要的工作就是： 第一，它们允许所有者去花他们的钱，第二，防止他人在新的一个区块被挖出来之前（进入到整个区块链），篡改他们已提交的交易。

    私钥用来对数据进行签名，公钥用来验证它的合法性。

    例如：Bob 想给 Sally 两个菜鸟币，所以他们的钱包客户端生成这个交易并且递交给矿工，使其成为下一个区块的一部分。有一个矿工尝试把这两个币的接受人篡改为 John。然而，很幸运地是，Bob 已经用他的私钥把交易数据签名了，任何人使用 Bob 的公钥就能验证这个交易的数据是否被篡改了（其他人的公钥无法校验此交易）。

（从之前的代码中）我们可以看到我们的签名会包含很多字节的信息，所以我们创建一个生成这些信息的方法。首先我们在 StringUtil 类中写几个辅助方法：


    //采用 ECDSA 签名并返回结果（以字节形式）
		public static byte[] applyECDSASig(PrivateKey privateKey, String input) {
		Signature dsa;
		byte[] output = new byte[0];
		try {
			dsa = Signature.getInstance("ECDSA", "BC");
			dsa.initSign(privateKey);
			byte[] strByte = input.getBytes();
			dsa.update(strByte);
			byte[] realSig = dsa.sign();
			output = realSig;
		} catch (Exception e) {
			throw new RuntimeException(e);
		}
		return output;
	}
	
	//验证一个字符串签名
	public static boolean verifyECDSASig(PublicKey publicKey, String data, byte[] signature) {
		try {
			Signature ecdsaVerify = Signature.getInstance("ECDSA", "BC");
			ecdsaVerify.initVerify(publicKey);
			ecdsaVerify.update(data.getBytes());
			return ecdsaVerify.verify(signature);
		}catch(Exception e) {
			throw new RuntimeException(e);
		}
	}

	public static String getStringFromKey(Key key) {
		return Base64.getEncoder().encodeToString(key.getEncoded());
	}

不用过分地去弄懂这些方法具体怎么工作的。你真正要了解的是： applyECDSASig 方法接收发送方的私钥和字符串输入，进行签名并返回一个字节数组。verifyECDSASig 方法接收签名，公钥和字符串，根据签名的有效性返回 true 或 false。getStringFromKey 方法就是接受任何一种私钥，返回一个加密的字符串。

现在我们在 Transaction 类中使用这些签名相关的方法，添加 generateSignature() 和 verifiySignature() 方法。

    //对所有我们不想被篡改的数据进行签名
    public void generateSignature(PrivateKey privateKey) {
	String data = StringUtil.getStringFromKey(sender) + StringUtil.getStringFromKey(reciepient) + Float.toString(value)	;
	signature = StringUtil.applyECDSASig(privateKey,data);		
    }
    //验证我们已签名的数据
    public boolean verifiySignature() {
	String data = StringUtil.getStringFromKey(sender) + StringUtil.getStringFromKey(reciepient) + Float.toString(value)	;
	return StringUtil.verifyECDSASig(sender, data, signature);
    }


实际上，你可能想对更多信息加入签名，像输出/输入或是时间戳（但现在我们只想对最基本的信息进行签名）。

签名可以由矿工进行验证，就像一个新交易被验证后添加到一个区块中。

当检查区块链的合法性的时候，我们同样也可以检查签名。

### 测试钱包和签名

现在我们快完成一半的工作量了，去测试一下吧。在 NoobChain 类中，添加一些新变量并替换掉 main 方法中的相应内容：

    import java.security.Security;
    import java.util.ArrayList;
    import java.util.Base64;
    import com.google.gson.GsonBuilder;

    public class NoobChain {
	
	public static ArrayList<Block> blockchain = new ArrayList<Block>();
	public static int difficulty = 5;
	public static Wallet walletA;
	public static Wallet walletB;

	public static void main(String[] args) {	
		//设置 Bouncey castle 作为 Security Provider
		Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider()); 
		//创建新的钱包 
		walletA = new Wallet();
		walletB = new Wallet();
		//测试公钥和私钥
		System.out.println("Private and public keys:");
		System.out.println(StringUtil.getStringFromKey(walletA.privateKey));
		System.out.println(StringUtil.getStringFromKey(walletA.publicKey));
		//生成从 WalletA 到 walletB 的测试交易 
		Transaction transaction = new Transaction(walletA.publicKey, walletB.publicKey, 5, null);
		transaction.signature = transaction.generateSignature(walletA.privateKey);
		//验证签名是否起作用并结合公钥验证
		System.out.println("Is signature verified");
		System.out.println(transaction.verifiySignature());
		
	}

请务必记得把 boncey castle 添加为 security provider。

我们创建了两个钱包，walletA 和 walletB，然后打印出 walletA 的私钥和公钥。生成了一个 Transaction 并使用 walletA 的公钥对其签名。然后就是希望一切能正常工作吧。

你的输出应该像这样子：

![](https://i.imgur.com/qXFTzcx.png)

签名按照预想应该被验证为 true。

现在我们只需创建/验证输出和输入，然后把交易存储在区块链中。

### 输入和输出 1：自己是怎么持有加密货币的

如果你想拥有一个比特币，那你要先收到一个比特币。交易账单不会真的把一个比特币加给你，也不会从发送方那里减去一个比特币。发送方有标识证明他/她之前收到过一个比特币，然后交易输出就会生成，显示一个比特币已经发送到你的地址（交易中的输入来源于之前交易的输出）。

    你的钱包余额是你所有的未花费的交易输出。

在这点上我们会跟比特币的叫法一样，把未花费的交易输出称为：UTXO。

我们再写一个 TransactionInput 类：

    public class TransactionInput {
	public String transactionOutputId; //把 TransactionOutputs 标识为对应的transactionId
	public TransactionOutput UTXO; //包括了所有未花费的交易输出
	
	public TransactionInput(String transactionOutputId) {
		this.transactionOutputId = transactionOutputId;
	}
    }

这个类会被用作未花费的 TransactionOutputs 的引用。transactionOutputId 被用来查找相关的 TransactionOutput，允许矿工检查你的所有权。

还有 TransactionOutputs 类：

    import java.security.PublicKey;

    public class TransactionOutput {
	public String id;
	public PublicKey reciepient; //这些币的新持有者
	public float value; //他们持有币的总额
	public String parentTransactionId; //生成这个输出的之前交易的 id
	
	//构造方法
	public TransactionOutput(PublicKey reciepient, float value, String parentTransactionId) {
		this.reciepient = reciepient;
		this.value = value;
		this.parentTransactionId = parentTransactionId;
		this.id = StringUtil.applySha256(StringUtil.getStringFromKey(reciepient)+Float.toString(value)+parentTransactionId);
	}
	
	//检查币是否属于你
	public boolean isMine(PublicKey publicKey) {
		return (publicKey == reciepient);
	}
	
    }

交易输出会显示最终发送给各接收方的金额。这些输出，在新交易中会被当作输入，作为你有资金可以发送出去的凭据。


### 输入和输出 2：处理交易

区块可能收到很多交易并且区块链长度可能会很长，这样会花非常长时间去处理一个新的交易，因为需要去查找和检查它的输入。为了处理这个问题，我们要再写一个可用作输出的未花费交易集合。在 NoobChain 类中，加入 UTXOs 集合：


    public class NoobChain {
	
	public static ArrayList<Block> blockchain = new ArrayList<Block>();
	public static HashMap<String,TransactionOutputs> UTXOs = new HashMap<String,TransactionOutputs>(); //未花费交易的 list 
	public static int difficulty = 5;
	public static Wallet walletA;
	public static Wallet walletB;

	public static void main(String[] args) {

HashMaps 通过 key 去找到 value，但你需要引入 java.util.HashMap。

好，接下来就是重点了。

把处理交易的方法 processTransaction 放到 Transaction 类里面：

    //如果新交易可以生成，返回 true	
    public boolean processTransaction() {
		
		if(verifiySignature() == false) {
			System.out.println("#Transaction Signature failed to verify");
			return false;
		}
				
		//整合所有交易输入（确保是未花费的）
		for(TransactionInput i : inputs) {
			i.UTXO = NoobChain.UTXOs.get(i.transactionOutputId);
		}

		//检查交易是否合法
		if(getInputsValue() < NoobChain.minimumTransaction) {
			System.out.println("#Transaction Inputs to small: " + getInputsValue());
			return false;
		}
		
		//生成交易输出
		float leftOver = getInputsValue() - value; //获取剩余的零钱
		transactionId = calulateHash();
		outputs.add(new TransactionOutput( this.reciepient, value,transactionId)); //send value to recipient
		outputs.add(new TransactionOutput( this.sender, leftOver,transactionId)); //把剩下的“零钱“发回给发送方		
				
		//添加输出到未花费的 list 中
		for(TransactionOutput o : outputs) {
			NoobChain.UTXOs.put(o.id , o);
		}
		
		//从 UTXO list里面移除已花费的交易输出
		for(TransactionInput i : inputs) {
			if(i.UTXO == null) continue; //if Transaction can't be found skip it 
			NoobChain.UTXOs.remove(i.UTXO.id);
		}
		
		return true;
	}
	
    //返回输入(UTXOs) 值的总额
	public float getInputsValue() {
		float total = 0;
		for(TransactionInput i : inputs) {
			if(i.UTXO == null) continue; //if Transaction can't be found skip it 
			total += i.UTXO.value;
		}
		return total;
	}

    //返回输出总额
	public float getOutputsValue() {
		float total = 0;
		for(TransactionOutput o : outputs) {
			total += o.value;
		}
		return total;
	}

同样再添加一个 getInputsValue 方法。

通过这个方法进行一些检查，去验证交易合法性，然后整合输入并生成输出（看看代码里的注释会清楚点）。

重要的一点，在最后，我们把 Inputs 从 UTXO list里面移除了，说明一个交易输出作为一个输入只能使用一次。因此，输入的总数值必须都花出去，这样发送方才有剩余“零钱”可拿回来。

红色箭头是输出。注意绿色的输入来自之前的输出。

最后更新我们的钱包：

- 收集我们的余额（通过循环 UTXO list并检查一个交易输出是否是自己的钱币）
- 为我们生成交易