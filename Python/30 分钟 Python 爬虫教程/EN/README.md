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

    import time
    from selenium import webdriver

    url = "https://unsplash.com"

    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)

    driver.execute_script("window.scrollTo(0,1000);")
    time.sleep(5)
    # Select image elements and print their URLs
    image_elements = driver.find_elements_by_css_selector("#gridMulti img")
    for image_element in image_elements:
    image_url = image_element.get_attribute("src")
    print(image_url)

Now, to actually get the images we found. For this, we will use requests and part of the PIL package, namely Image. We also want to use BytesIO from io to write the images to a ./images/ folder that we will create inside our project folder. So, to put this all together, we need to send an HTTP GET request to the URL of each image and then, using Image and BytesIO, we will store the image that we get in the response. Here’s one way to do this:

    import requests
    import time
    from selenium import webdriver
    from PIL import Image
    from io import BytesIO

    url = "https://unsplash.com"

    driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
    driver.get(url)

    driver.execute_script("window.scrollTo(0,1000);")
    time.sleep(5)
    image_elements = driver.find_elements_by_css_selector("#gridMulti img")
    i = 0

    for image_element in image_elements:
    image_url = image_element.get_attribute("src")
    # Send an HTTP GET request, get and save the image from the response
    image_object = requests.get(image_url)
    image = Image.open(BytesIO(image_object.content))
    image.save("./images/image" + str(i) + "." + image.format, image.format)
    i += 1

That’s pretty much all you need to get a bunch of free images downloaded. Obviously, unless you want to prototype a design and you just need random images, this little scraper isn’t of much use. So, I took some time to improve it, by adding a few more features:

- Command line arguments that allow the user to specify a search query, as well as a numeric value for scrolling, which allows the page to display more images for downloading.
- Customizable CSS selector.
- Customized result folders, based on search queries.
- Full HD images by cropping the URL of the thumbnails, as necessary.
- Named images, based on their URLs.
- Closing the browser window at the end of the process.


You can (and probably should) try implementing some of these features on your own. The full-featured version of the web scraper is available here. Remember to download geckodriver separately and connect it to your project, as instructed at the start of the article.


### Limitations, Considerations and Future Improvements
This whole project was a very simple proof-of-concept to see how web scraping is done, meaning there are a lot of things one can do to improve upon this little tool:

- Not crediting the original uploaders of the images is a pretty bad idea. Selenium is definitely capable of working around this, so that each image comes with the name of the author.
Geckodriver shouldn’t be placed in the project folder, but rather installed globally and be part of the PATH system variable.
- The search functionality could be easily extended to include multiple queries, so that the process of downloading lots of images can be simplified.
- The default browser could be changed from Firefox to Chrome or even PhantomJS, which would be a lot better for this kind of project.