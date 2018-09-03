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


#### Let’s get started!

Setup

Since we’re going to write our code in Go, we assume you have had some experience with Go. After [installing](https://golang.org/dl/) and configuring Go, we’ll also want to grab the following packages:

    go get github.com/davecgh/go-spew/spew


Spew allows us to view structs and slices cleanly formatted in our console. This is nice to have.

    go get github.com/gorilla/mux


Gorilla/mux is a popular package for writing web handlers. We’ll need this.

    go get github.com/joho/godotenv

Gotdotenv lets us read from a .env file that we keep in the root of our directory so we don’t have to hardcode things like our http ports. We’ll need this too.


Let’s also create a .env file in the root of our directory defining the port that will serve http requests. Just add one line to this file:

    ADDR=8080


Create a main.go file. Everything from now on will be written to this file and will be less than 200 lines of code. Let’s get coding!


#### Imports

Here are the imports we’ll need, along with our package declaration. Let’s write these to main.go

    package main

    import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/davecgh/go-spew/spew"
	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
     )

#### Data model


Let’s define the struct of each of our blocks that will make up the blockchain. Don’t worry, we’ll explain what all of these fields mean in a minute.


    type Block struct {
	Index     int
	Timestamp string
	BPM       int
	Hash      string
	PrevHash  string
    }

Each Block contains data that will be written to the blockchain, and represents each case when you took your pulse rate (remember you did that at the beginning of the article?).

- Index is the position of the data record in the blockchain

- Timestamp is automatically determined and is the time the data is written
- BPM or beats per minute, is your pulse rate
- Hash is a SHA256 identifier representing this data record
- PrevHash is the SHA256 identifier of the previous record in the chain

Let’s also model out the blockchain itself, which is simply a slice of Block:

    var Blockchain []Block

So how does hashing fit into blocks and the blockchain? We use hashes to identify and keep the blocks in the right order. By ensuring the PrevHash in each Block is identical to Hash in the previous Block we know the proper order of the blocks that make up the chain.