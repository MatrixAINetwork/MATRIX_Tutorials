## 30-minute Python Web Scraper

I’ve been meaning to create a web scraper using Python and Selenium for a while now, but never gotten around to it. A few nights ago, I decided to give it a spin. Daunting as it may have seemed, it was extremely easy to write the code to grab some beautiful images from Unsplash.


![](https://i.imgur.com/KyCWyxl.jpg)


### Ingredients for a simple Image Scraper
- Python (3.6.3 or newer)
- Pycharm (Community edition is just fine)
- pip install requests Pillow selenium
- geckodriver (read below for instructions)
- Mozlla Firefox (as if you didn’t have it installed)
- Working internet connection (obviously)
- 30 minutes of your time (possibly less)


### Recipe for a simple Image Scraper

Got everything installed and ready? Good! I’ll explain what each of these ingredients does, as we move forward with our code.

The first thing we’ll be utilizing is the Selenium webdriver combined with geckodriver to open a browser window that does our job for us. To get started, create a project in Pycharm, download the latest version of geckodriver for you operation system, open the compressed file and drag & drop the geckodriver file into your project’s folder. Geckodriver is basically what lets Selenium get control of Firefox, so we need it in our project folder to be able to utilize the browser.

Next thing we want to be doing is to actually import the webdriver from Selenium into our code and connect to the URL we want. So let’s do just that:

    from selenium import webdriver
    # The URL we want to browse to
    url = "https://unsplash.com"
    # Using Selenium's webdriver to open the page
    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)

Opening a new browser window to a specific URL

![](https://i.imgur.com/WD9e7NW.png)

Pretty easy, huh? If you’ve done everything correctly, you are over the hard part already and you should see a browser window similar to the one shown in the above image.

Next up, we should scroll down so that more images can be loaded before we get to download them. We also want to wait a few seconds, just in case the connection is slow and the images have not fully loaded. As Unsplash is built with React, waiting for about 5 seconds seems like a generous timeframe, so we should do just that, using the time package. We also want to use some Javascript code to scroll the page — we will be using window.scrollTo() to accomplish this. Putting it all together, you should end up with something like this:


    import time
    from selenium import webdriver

    url = "https://unsplash.com"

    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)
    # Scroll page and wait 5 seconds
    driver.execute_script("window.scrollTo(0,1000);")
    time.sleep(5)

After testing the above code, you should see the browser scroll down the page a little bit. The next thing we need to be doing is finding the images we want to downalod from the website. After digging around in the code React generates, I figured out that we can use a CSS selector to specifically target the images in the gallery of the page. The specific layout and code of the page might change in the future, but at the time of writing I could use a #gridMulti img selector to get all the <img> elements that were appearing on my screen.

We can get a list of these elements using find_elements_by_css_selector(), but what we want is the src attribute of each element. So, we can iterate over the list and grab those: