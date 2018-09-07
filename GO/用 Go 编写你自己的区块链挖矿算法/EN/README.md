## Code your own blockchain mining algorithm in Go!

![](https://cdn-images-1.medium.com/max/800/1*zwlWlWAwTRxaoKkds63rfQ.png)

With all the recent craze in Bitcoin and Ethereum mining it’s easy to wonder what the fuss is all about. For newcomers to this space, they hear wild stories of people filling up warehouses with GPUs making millions of dollars worth of cryptocurrencies a month. What exactly is cryptocurrency mining? How does it work? How can I try coding my own mining algorithm?


We’ll walk you through each of these questions in this post, culminating in a tutorial on how to code your own mining algorithm. The algorithm we’ll be showing you is called Proof of Work, which is the foundation to Bitcoin and Ethereum, the two most popular cryptocurrencies. Don’t worry, we’ll explain how that works shortly.


### What is cryptocurrency mining?
Cryptocurrencies need to have scarcity in order to be valuable. If anyone could produce as many Bitcoin as they wanted at anytime, Bitcoin would be worthless as a currency (wait, doesn’t the Federal Reserve do this? *facepalm*). The Bitcoin algorithm releases some Bitcoin to a winning member of its network every 10 minutes, with a maximum supply to be reached in about 122 years. This release schedule also controls inflation to a certain extent, since the entire fixed supply isn’t released at the beginning. More are slowly released over time.

The process by which a winner is determined and given Bitcoin requires the winner to have done some “work”, and competed with others who were also doing the work. This process is called mining, because it’s analogous to a gold miner spending some time doing work and eventually (and hopefully) finding a bit of gold.

The Bitcoin algorithm forces participants, or nodes, to do this work and compete with each other to ensure Bitcoin aren’t released too quickly.

### How does mining work?
A quick Google search of “how does bitcoin mining work?” fills your results with a multitude of pages explaining that Bitcoin mining asks a node (you, or your computer) to solve a hard math problem. While technically true, simply calling it a “math” problem is incredibly hand-wavy and hackneyed. How mining works under the hood is a lot of fun to understand. We’ll need to understand a bit of cryptography and hashing to learn how mining works.

### A brief introduction to cryptographic hashes
One-way cryptography takes in a human readable input like “Hello world” and applies a function to it (i.e. the math problem) to produce an indecipherable output. These functions (or algorithms) vary in nature and complexity. The more complicated the algorithm, the harder it is to reverse engineer. Thus, cryptographic algorithms are very powerful in securing things like user passwords and military codes.

Let’s take a look at an example of SHA-256, a popular cryptographic algorithm. This [hashing website](http://www.xorbin.com/tools/sha256-hash-calculator) lets you easily calculate SHA-256 hashes. Let’s hash “Hello world” and see what we get:

![](https://cdn-images-1.medium.com/max/800/1*_qWZ8MB6pKezY_76qPjEjA.png)

Try hashing “Hello world” over and over again. You get the same hash every time. In programming getting the same result again and again given the same input is called idempotency.

A fundamental property of cryptographic algorithms is that they should be extremely hard to reverse engineer to find the input, but extremely easy to verify the output. For example, using the SHA-256 hash above, it should be trivial for someone else to apply the SHA-256 hash algorithm to “Hello world” to check that it indeed produces the same resultant hash, but it should be very hard to take the resultant hash and get “Hello world” from it. This is why this type of cryptography is called one way.

Bitcoin uses Double SHA-256, which is simply applying SHA-256 again to the SHA-256 hash of “Hello world”. For our examples throughout this tutorial we’ll just use SHA-256.