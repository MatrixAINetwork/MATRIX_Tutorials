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

### Mining

Now that we understand what cryptography is, we can get back to cryptocurrency mining. Bitcoin needs to find some way to make participants who want to earn Bitcoin “work” so Bitcoins aren’t released too quickly. Bitcoin achieves this by making the participants hash many combinations of letters and numbers until the resulting hash contains a specific number of leading “0”s.

For example, go back to the [hash website](http://www.xorbin.com/tools/sha256-hash-calculator) and hash “886”. It produces a hash with 3 zeros as a prefix.

![](https://cdn-images-1.medium.com/max/800/1*5l3FgMIR5Gn_AUZ1X5mW9Q.png)

But how did we know that “886” produced something with 3 zeros? That’s the point. Before writing this blog, we didn’t. In theory, we would have had to work through a whole bunch combinations of letters and numbers and tested the results until we got one that matched the 3 zeros requirement. To give you a simple example, we already worked in advance to realize the hash of “886” produced 3 leading zeros.

The fact that anyone can easily check that “886” produces something with 3 leading zeros proves that we did the grunt work of testing and checking a large combination of letters and numbers to get to this result. So if I’m the first one who got this result, I would have earned the Bitcoin by proving I did this work — the proof is that anyone can quickly check that “886” produces the number of zeros I claim it does. This is why the Bitcoin consensus algorithm is called Proof-of-Work.


But what if I just got lucky and I got the 3 leading zeros on my first try? This is extremely unlikely and the occasional node that successfully mines a block (proves that they did the work) on their first try is outweighed by millions of others who had to work extra to find the desired hash. Go ahead and try it. Type in any other combination of letters and numbers in the hash website. We bet you won’t get 3 leading zeros.

Bitcoin’s requirements are a bit more complex than this (many more leading zeros!) and it is able to adjust the requirements dynamically to make sure the work required isn’t too easy or too hard. Remember, it aims to release Bitcoin every 10 minutes so if too many people are mining, it needs to make the proof of work harder to compensate. This is called adjusting the difficulty. For our purposes, adjusting the difficulty will just mean requiring more leading zeros.

So you can see the Bitcoin consensus algorithm is much more interesting than just “solving a math problem”!


### Enough background. Let’s get coding!
Now that we have the background we need, let’s build our own Blockchain program with a Proof-of-Work algorithm. We’ll write it in Go because we use it here at Coral Health and frankly, it’s awesome.

Before proceeding, we recommend reading our original blog post, Code your own blockchain in less than 200 lines of Go! It’s not a requirement but some of the examples below we’ll be running through quickly. Refer to the original post if you need more detail. If you’re already familiar with this original post, skip to the “Proof of Work” section below.

#### Architecture

![](https://cdn-images-1.medium.com/max/800/1*z0fgOU0iYm7Pjc5Zn5nCjA.png)


We’ll have a Go server, where for simplicity we’ll put all our code in a single main.go file. This file will provide us all the blockchain logic we need (including Proof of Work) and will contain all the handlers for our REST APIs. This blockchain data is immutable; we only need GET and POST requests. We’ll make requests through the browser to view the data through GET and we’ll use Postman to POST new blocks (curl works fine too).

#### Imports

Let’s start with our standard imports. Make sure to grab the following packages with go get

github.com/davecgh/go-spew/spew pretty prints your blockchain in Terminal

github.com/gorilla/mux a convenience layer for wiring up your web server

github.com/joho/godotenv read your environmental variables from a .env file in your root directory

Let’s create a .env file in our root directory that just stores one environment variable that we’ll need later. Put one line in your .env file:ADDR=8080

Make your package declaration and define your imports in main.go in your root directory:

    package main

    import (
        "crypto/sha256"
        "encoding/hex"
        "encoding/json"
        "fmt"
        "io"
        "log"
        "net/http"
        "os"
        "strconv"
        "strings"
        "sync"
        "time"

        "github.com/davecgh/go-spew/spew"
        "github.com/gorilla/mux"
        "github.com/joho/godotenv"
    )

