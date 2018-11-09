## Making the Web More Accessible With AI

According to the World Health Organization, approximately 285 million people are visually impaired worldwide, and in the United States alone, 8.1 million internet users have a visual impairment.

What most non-disabled individuals consider to be the internet, a place full of text, images, videos, and more, is something completely different for the visually impaired. Screen readers, tools that can read text and metadata on a web page, are very limited and can only expose one part of a webpage, namely the text of the site. While some developers take the time to go through their sites and add descriptive captions to their images for visually disabled users, the vast majority of programmers do not take the time to do this admittedly tedious task.

So, I decided to make a tool to help visually impaired individuals “see” the internet with the power of AI. It’s called Auto Alt Text and is a chrome extension that allows users to right click and get a description of the scene in an image — the first to do so.

Check out the video below to see how it works and [download it to try it out](http://abhinavsuri.com/aat)!

### Why I made Auto Alt Text:
I used to be one of those developers who didn’t take the time to add descriptions to images on my page. For me, accessibility was always a second thought until I got an email from a user of one of my projects.


![](https://cdn-images-1.medium.com/max/1600/1*uYx_pi9vAI17mQ20D81ykw.png)


    Email Text: “Hi Abhinav, I found your flask-base project and think it is definitely going to be a great fit for my next project. Thanks for working on it. I also just wanted to let you know that you should put some alt descriptions on your readme images. I’m legally blind and had a tough time making out what was in them :/ From REDACTED”


At that point, my development process put accessibility at the bottom of the list, basically an afterthought. However, this email was a wakeup call for me. There are many individuals on the internet who need accessibility features to understand the original intent of websites, apps, projects, and more.


    “The web is replete with images that have missing, incorrect, or poor alternative text” — WebAIM (Center for Persons with Disabilities at Utah State University)