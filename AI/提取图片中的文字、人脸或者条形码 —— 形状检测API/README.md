### 提取图片中的文字、人脸或者条形码 —— 形状检测API


#### 什么是形状检测 API？

借助 API navigator.mediaDevices.getUserMedia 和新版安卓的 chrome photo picker，从移动设备上的相机获取图像或者实时上传视频数据或本地图像变得相当容易。在此之前，这些动态的图像数据以及页面上的静态图像一直都是个我们无法操作的黑盒，即使图像实际上可能包含许多有趣的特征，如人脸、条形码和文本。

过去，如果开发人员想要在客户端提取这些特征，例如构建一个二维码识别器，他们必须借助外部的 JavaScript 库。从性能的角度来看代价是昂贵的，并且会增加整体页面的资源体积。另一方面，诸如 Android、iOS 和 macOS 这些操作系统，以及他们的相机模块中的硬件芯片，通常已经具有高性能和高度优化的特征检测器，例如 Android 的 FaceDetector 或者 iOS 自带的特征检测器 CIDetector。

而 Shape Detection API 做的便是调用这些原生实现，并将其转化为一组 JavaScript 接口。目前，这个 API 支持的功能是通过 FaceDetector 接口进行人脸检测，通过 BarcodeDetector 接口进行条形码检测以及通过 TextDetector 接口进行文本检测（光学字符识别，OCR）。

    小提示：尽管文本检测是一个有趣的领域，但在目前要标准化的计算平台或字符集中，文本检测还不够稳定，这也使文本检测已经有一套单独的信息规范的原因。


#### Shape Detection API 实践用例


如上所述，Shape Detection API 目前支持检测人脸、条形码和文本。以下列表包含了所有三个功能的用例示例：

- 人脸检测

在线社交网络或照片共享网站通常会让用户在图像中标记出人物。通过边缘检测识别人脸，能使这项工作更为便捷。

内容网站可以根据可能检测到的面部动态裁剪图像，而不是依赖于其他启发式方法，或者使用 Ken Burns 提出的通过平移或者缩放检测人脸。

多媒体消息网站可以允许其用户在检测到的面部的不同位置上添加太阳镜或胡须之类的有趣贴图。

- 条形码检测

能够读取二维码的 Web 应用程序可以实现很多有趣的用例，如在线支付或 Web 导航，或使用条形码在应用程序上分享社交连接。

购物应用可以允许其用户扫描实体店中物品的 EAN 或者 UPC 条形码，以在线比较价格。

机场可以设立网络信息亭，乘客可以在那里扫描登机牌的 Aztec codes 以显示与其航班相关的个性化信息。


- 文字检测

当没有提供其他描述时，在线社交网站可以通过将检测到的文本添加为 img[alt] 属性值来改善用户生成的图像内容的体验。

内容网站可以使用文本检测来避免将标题置于包含文本的主要图像之上。

Web 应用程序可以使用文本检测来翻译文本，例如，翻译餐馆菜单。
#### 如何使用 Shape Detection API

三个检测器向外暴露的接口 FaceDetector、BarcodeDetector 和 TextDetector 都非常相似，它们都提供了一个异步方法 detect，它接受一个 ImageBitmapSource 输入（或者是一个 CanvasImageSource、[Blob] 对象([w3c.github.io/FileAPI/#df…](https://link.juejin.im/?target=https%3A%2F%2Fw3c.github.io%2FFileAPI%2F%23dfn-Blob)) 或者 ImageData）。

在使用 FaceDetector 和 BarcodeDetector 的情况下，可选参数可以被传递到所述检测器的构造函数中，其允许向底层原生检测器发起调用指示。

    小提示：如果你的 ImageBitmapSource 来自一个 独立的脚本源 并且与 document 的源不同，那么 detect 将会调用失败并抛出一个名为 SecurityError 的 DOMException 。如果你的图片对跨域设置了 CORS，那么你可以使用 crossorigin 属性来请求 CORS 访问。


#### 在项目里使用 FaceDetector

    const faceDetector = new FaceDetector({
    // (Optional) Hint to try and limit the amount of detected faces
    // on the scene to this maximum number.
    maxDetectedFaces: 5,
    // (Optional) Hint to try and prioritize speed over accuracy
    // by, e.g., operating on a reduced scale or looking for large features.
    fastMode: false
    });
    try {
    const faces = await faceDetector.detect(image);
    faces.forEach(face => console.log(face));
    } catch (e) {
    console.error('Face detection failed:', e);
    }

#### 在项目里使用 BarcodeDetector

    const barcodeDetector = new BarcodeDetector({
    // (Optional) A series of barcode formats to search for.
    // Not all formats may be supported on all platforms
    formats: [
    'aztec',
    'code_128',
    'code_39',
    'code_93',
    'codabar',
    'data_matrix',
    'ean_13',
    'ean_8',
    'itf',
    'pdf417',
    'qr_code',
    'upc_a',
    'upc_e'
     ]
    });
    try {
     const barcodes = await barcodeDetector.detect(image);
     barcodes.forEach(barcode => console.log(barcode));
    } catch (e) {
    console.error('Barcode detection failed:', e);
    }


#### 在项目里使用 TextDetector

    const textDetector = new TextDetector();
    try {
    const texts = await textDetector.detect(image);
    texts.forEach(text => console.log(text));
    } catch (e) {
    console.error('Text detection failed:', e);
    }

#### 可用性检验

在使用 Shape Detection API 接口之前检查构造函数是否存在是必须的，因为虽然 Linux 和 Chrome OS 上的 Chrome 目前已经开放了检测器的接口，但它们却没法正常使用（bug）。作为临时措施，我们建议在使用这些 API 之前应当这么做：

    const supported = await (async () => 'FaceDetector' in window &&
    await new FaceDetector().detect(document.createElement('canvas'))
    .then(_ => true)
    .catch(e => e.name === 'NotSupportedError' ? false : true))();

#### 最佳做法