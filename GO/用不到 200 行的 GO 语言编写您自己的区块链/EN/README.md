### Code your own blockchain in less than 200 lines of Go!

![](https://cdn-images-1.medium.com/max/800/1*Elzguv8ycXYcphhD7M95hQ.jpeg)


This tutorial is adapted from this excellent post about writing a basic blockchain using Javascript. We’ve ported it over to Go and added some extra goodies like viewing your blockchain in a web browser. If you have any questions about the following tutorial, make sure to join our Telegram chat. Ask us anything!

The data examples in this tutorial will be based on your resting heartbeat. We are a healthcare company after all :-) For fun, count your pulse for a minute (beats per minute) and keep that number in mind throughout the tutorial.

Almost every developer in the world has heard of the blockchain but most still don’t know how it works. They might only know about it because of Bitcoin and because they’ve heard of things like smart contracts. This post is an attempt to demystify the blockchain by helping you write your own simple blockchain in Go, with less than 200 lines of code! By the end of this tutorial, you’ll be able to run and write to a blockchain locally and view it in a web browser.

What better way to learn about the blockchain than to create your own?



#### What you will be able to do

- Create your own blockchain
- Understand how hashing works in maintaining integrity of the blockchain
- See how new blocks get added
- See how tiebreakers get resolved when multiple nodes generate blocks
- View your blockchain in a web browser
- Write new blocks
- Get a foundational understanding of the blockchain so you can decide where your journey takes you from here!


#### What you won’t be able to do

To keep this post simple, we won’t be dealing with more advanced consensus concepts like proof of work vs. proof of stake. Network interactions will be simulated so you can view your blockchain and see blocks added, but network broadcasting will be reserved for a future post.


