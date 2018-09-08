## 30 分钟 Python 爬虫教程

一直想用 Python 和 Selenium 写一个网页爬虫，但一直都没去实现。写代码从 Unsplash 网站上抓取一些漂亮的图片，这看起来好像是非常艰巨的事情，但实际上却是极其简单。

#### 简单图片爬虫的原料

- Python (3.6.3 或以上)
- Pycharm (社区版就已经足够了)
- pip install requests Pillow selenium
- geckodriver (具体见下文)
- Mozlla Firefox (如果你没有安装过的话)
- 正常的网络连接（显然需要的）
- 时间


#### 简单图片爬虫的菜谱

以上的所有都安装好了后，在我们继续开始写代码前，我先来解释一下以上这些原料都是用来干什么的。

我们首先要做的是利用 Selenium webdriver 和 geckodriver 来为我们打开一个浏览器窗口。首先，在 Pycharm 中新建一个项目，根据你的操作系统下载最新版的 geckodriver，将其解压并把 geckodriver 文件拖到项目文件夹中。Geckodriver 本质上就是一个能让 Selenium 控制 Firefox 的工具，因此我们的项目需要它来让浏览器帮我们做一些事。

接下来我们要做的事就是从 Selenium 中导入 webdriver 到我们的代码中，然后连接到我们想爬取的 URL 地址。说做就做：


    from selenium import webdriver
    # 我们想要浏览的 URL 链接
    url = "https://unsplash.com"
    # 使用 Selenium 的 webdriver 来打开这个页面
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)

打开浏览器窗口到指定的 URL。

![](https://i.imgur.com/LMIH5sR.png)

一个远程控制的 Firefox 窗口。

相当容易对吧？如果以上所说你都正确完成了，你已经攻克了最难的那部分了，此时你应该看到一个类似于以上图片所示的浏览器窗口。

接下来我们就应该向下滚动以便更多的图片可以加载出来，然后我们才能够将它们下载下来。我们还想再等几秒钟，以便万一网络连接太慢了导致图片没有完全加载出来。由于 Unsplash 网站是使用 React 构建的，等个 5 秒钟似乎已经足够”慷慨”了，那就使用 Python 的 time 包等个 5 秒吧，我们还要使用一些 Javascript 代码来滚动网页——我们将会用到 [window.scrollTo()](https://developer.mozilla.org/en-US/docs/Web/API/Window/scrollTo) 函数来实现这个功能。将以上所说的合并起来，最终你的代码应该像这样：

    import time
    from selenium import webdriver

    url = "https://unsplash.com"

    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)
    # 向下滚动页面并且等待 5 秒钟
    driver.execute_script("window.scrollTo(0,1000);")
    time.sleep(5)