## Code your own blockchain mining algorithm in Go!

![](https://cdn-images-1.medium.com/max/800/1*zwlWlWAwTRxaoKkds63rfQ.png)

With all the recent craze in Bitcoin and Ethereum mining it’s easy to wonder what the fuss is all about. For newcomers to this space, they hear wild stories of people filling up warehouses with GPUs making millions of dollars worth of cryptocurrencies a month. What exactly is cryptocurrency mining? How does it work? How can I try coding my own mining algorithm?


We’ll walk you through each of these questions in this post, culminating in a tutorial on how to code your own mining algorithm. The algorithm we’ll be showing you is called Proof of Work, which is the foundation to Bitcoin and Ethereum, the two most popular cryptocurrencies. Don’t worry, we’ll explain how that works shortly.


### What is cryptocurrency mining?
Cryptocurrencies need to have scarcity in order to be valuable. If anyone could produce as many Bitcoin as they wanted at anytime, Bitcoin would be worthless as a currency (wait, doesn’t the Federal Reserve do this? *facepalm*). The Bitcoin algorithm releases some Bitcoin to a winning member of its network every 10 minutes, with a maximum supply to be reached in about 122 years. This release schedule also controls inflation to a certain extent, since the entire fixed supply isn’t released at the beginning. More are slowly released over time.

The process by which a winner is determined and given Bitcoin requires the winner to have done some “work”, and competed with others who were also doing the work. This process is called mining, because it’s analogous to a gold miner spending some time doing work and eventually (and hopefully) finding a bit of gold.

The Bitcoin algorithm forces participants, or nodes, to do this work and compete with each other to ensure Bitcoin aren’t released too quickly.