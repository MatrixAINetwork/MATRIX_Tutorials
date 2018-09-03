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

![](https://cdn-images-1.medium.com/max/800/1*VwT5d8NPjUpI7HiwPa--cQ.png)


#### Hashing and Generating New Blocks

So why do we need hashing? We hash data for 2 main reasons:

- To save space. Hashes are derived from all the data that is on the block. In our case, we only have a few data points but imagine we have data from hundreds, thousands or millions of previous blocks. It’s much more efficient to hash that data into a single SHA256 string or hash the hashes than to copy all the data in preceding blocks over and over again.

- Preserve integrity of the blockchain. By storing previous hashes like we do in the diagram above, we’re able to ensure the blocks in the blockchain are in the right order. If a malicious party were to come in and try to manipulate the data (for example, to change our heart rate to fix life insurance prices), the hashes would change quickly and the chain would “break”, and everyone would know to not trust that malicious chain.


Let’s write a function that takes our Block data and creates a SHA256 hash of it.

    func calculateHash(block Block) string {
	record := string(block.Index) + block.Timestamp + string(block.BPM) + block.PrevHash
	h := sha256.New()
	h.Write([]byte(record))
	hashed := h.Sum(nil)
	return hex.EncodeToString(hashed)
    }

This calculateHash function concatenates Index, Timestamp, BPM, PrevHash of the Block we provide as an argument and returns the SHA256 hash as a string. Now we can generate a new Block with all the elements we need with a new generateBlock function. We’ll need to supply it the previous block so we can get its hash and our pulse rate in BPM. Don’t worry about the BPM int argument that’s passed in. We’ll address that later.


    func generateBlock(oldBlock Block, BPM int) (Block, error) {

	var newBlock Block

	t := time.Now()

	newBlock.Index = oldBlock.Index + 1
	newBlock.Timestamp = t.String()
	newBlock.BPM = BPM
	newBlock.PrevHash = oldBlock.Hash
	newBlock.Hash = calculateHash(newBlock)

	return newBlock, nil
    }

Notice that the current time is automatically written in the block with time.Now(). Also notice that our prior calculateHash function was called. PrevHash is copied over from the hash of the previous block. Index is incremented from the Index of the previous block.

#### Block Validation

Now we need to write some functions to make sure the blocks haven’t been tampered with. We do this by checking Index to make sure they’ve incremented as expected. We also check to make sure our PrevHash is indeed the same as the Hash of the previous block. Lastly, we want to double check the hash of the current block by running the calculateHash function again on the current block. Let’s write a isBlockValid function that does all these things and returns a bool. It’ll return true if it passes all our checks:

    func isBlockValid(newBlock, oldBlock Block) bool {
	if oldBlock.Index+1 != newBlock.Index {
		return false
	}

	if oldBlock.Hash != newBlock.PrevHash {
		return false
	}

	if calculateHash(newBlock) != newBlock.Hash {
		return false
	}

	return true
    }


What if we run into an issue where two nodes of our blockchain ecosystem both added blocks to their chains and we received them both. Which one do we pick as the source of truth? We choose the longest chain. This is a classic blockchain issue and has nothing to do with nefarious actors.


Two well meaning nodes may simply have different chain lengths, so naturally the longer one will be the most up to date and have the latest blocks. So let’s make sure the new chain we’re taking in is longer than the current chain we have. If it is, we can overwrite our chain with the new one that has the new block(s).


![](https://cdn-images-1.medium.com/max/800/1*H1fCp0NLun0Kn0wIy0dyEA.png)

We simply compare the length of the slices of the chains to accomplish this:

    func replaceChain(newBlocks []Block) {
	if len(newBlocks) > len(Blockchain) {
		Blockchain = newBlocks
	}
    }

If you’ve made it this far, pat yourself on the back! We’ve basically written up the guts of our blockchain with all the various functions we need.

Now we want a convenient way to view our blockchain and write to it, ideally in a web browser so we can show our friends!