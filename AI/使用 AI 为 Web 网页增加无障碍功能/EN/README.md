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


### Artificial Intelligence to the Rescue:

There are numerous ways to caption images; however, most have a few disadvantages in common:

- They aren’t responsive and take a long time to return a caption.
- They are semi-automated (i.e. relying on humans to manually caption images on demand).
- They are expensive to create and maintain.
- 
By creating a neural network, all of these problems can be solved. I recently had started taking a deep dive into machine learning and AI when I came across Tensorflow, an open source library to help with machine learning. Tensorflow enables developers to architect robust models that can be used to complete a variety of tasks from object detection to image recognition.

Doing a bit more research, I came across a paper by Vinyals et al called “[Show and Tell: Lessons learned from the 2015 MSCOCO Image Captioning Challenge](https://arxiv.org/abs/1609.06647)”. These researchers created a deep neural network to describe image content in a semantic manner.


![](https://cdn-images-1.medium.com/max/1600/1*mSvmjcvUbpgB3izigcEi4w.png)

Examples of im2txt in action from the im2txt Github Repository


### Technical Details of im2txt:

The mechanics of the model are fairly detailed, but basically it is an “encoder-decoder” scheme. First, the image is put through a deep convolutional neural network called Inception v3, an image classifier. Next, the encoded image is fed through an LSTM which is a type of neural network that specialized in modeling sequences/time-sensitive information. The LSTM then works through a set vocabulary and constructs a sentence to describe the image. It does this by taking the likelihood of each word from that set vocabulary appearing first in the sentence and then computing the most likely second-word probability distribution given the first-word probability distribution and so on until the most likely character is a “.” indicating the end of the caption.

![](https://cdn-images-1.medium.com/max/1600/1*CW6YVV_zEriaGrxMzN4quA.png)

Overview of the structure of the neural network (from the im2txt Github repository).

Per the Github repository, the training time for this neural network was approximately 1–2 weeks on a Tesla k20m GPU (probably much more for a standard CPU on a laptop which is what I have). Thankfully, a member of the tensorflow community provided a trained model for public download.

### Problems out of the box + Lamdba:
When running the model, I managed to get it to work with Bazel, a tool that is used to pre-package tensorflow models into runnable scripts (among other purposes). However, it took me nearly 15 seconds to get a result from a single image when running on the command line! The only way to solve this issue was to keep the tensorflow graph in memory, but that would require keeping the app up 24/7. I was planning on putting this model on AWS Elasticbeanstalk where compute time is prorated to the hour and keeping an app up all the time was non-ideal (basically leading to situation #3 in the disadvantages of image captioning software). So, I decided to switch over to AWS Lamdba to host everything.

Lambda is a service that provides serverless computing for an incredibly low cost. Furthermore, it charges on a second by second basis when it is actively used. The way Lambda works is simple: once your app gets a request from a user, Lambda will activate an image of your application, serve a response, and deactivate that image. If you have multiple concurrent requests, it just spins up more instances to scale to the load. Additionally, it will keep your app activated as long as there are multiple requests within the hour. This service was a great fit for my use case.


![](https://cdn-images-1.medium.com/max/1600/1*Q4EaQYos3s-67OkhhKzDkg.png)


AWS API Gateway + AWS = heart (src)

The problem with Lambda was that I had to create an API for the im2txt model. Furthermore, Lamdba has memory constraints on the application that can be loaded as a function. When uploading a zip file containing all your application code, including dependencies, the final file cannot be more than ~250 MB. This limit was a problem since the size of the im2txt model was over 180 MB, and the dependencies for it to run was over 350 MB. I tried to get around this issue by uploading some parts into an S3 instance and downloading into my running lambda instance when it was active; however, the total storage size limit on lambda is 512 MB which my application was well over (it was around 530 MB in total).

To reduce the final size of my project, I reconfigured im2txt to accept a pared down model containing only the trained checkpoint and no extraneous metadata. This deletion reduced my model size to 120 MB. I then discovered lambda-packs which contained a minimized version of all the dependencies, albeit with an earlier version of python and tensorflow. After going through the painful process of downgrading any python 3.6 syntax and tensorflow 1.2 code, I finally had a package which was ~480 MB in total, just below the 512 MB limit.

To keep response times quick, I created a CloudWatch function to keep the Lambda instance “hot” and the application active. I added a few helper functions to manipulate images not in JPG format and finally had a working API. All of these reductions led to a blazing fast response time of < 5 seconds in most cases!