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


#### Web Server

We assume you’re already familiar with how web servers work and have a bit of experience wiring them up in Go. We’ll walk you through the process now.

We’ll be using the Gorilla/mux package that you downloaded earlier to do the heavy lifting for us.

Let’s create our server in a run function that we’ll call later.


    func run() error {
	mux := makeMuxRouter()
	httpAddr := os.Getenv("ADDR")
	log.Println("Listening on ", os.Getenv("ADDR"))
	s := &http.Server{
		Addr:           ":" + httpAddr,
		Handler:        mux,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}

	if err := s.ListenAndServe(); err != nil {
		return err
	}

	return nil
    }


Note that port we choose comes from our .env file that we created earlier. We give ourselves a quick console message with log.Println to let us know the server is up and running. We configure the server a bit and then ListenAndServe. Pretty standard Go stuff.


Now we need to write the makeMuxRouter function that will define all our handlers. To view and write to our blockchain in a browser, we only need 2 routes and we’ll keep them simple. If we send a GET request to localhost we’ll view our blockchain. If we send a POST request to it, we can write to it.

    func makeMuxRouter() http.Handler {
	muxRouter := mux.NewRouter()
	muxRouter.HandleFunc("/", handleGetBlockchain).Methods("GET")
	muxRouter.HandleFunc("/", handleWriteBlock).Methods("POST")
	return muxRouter
    }


Here’s our GET handler:

    func handleGetBlockchain(w http.ResponseWriter, r *http.Request) {
	bytes, err := json.MarshalIndent(Blockchain, "", "  ")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	io.WriteString(w, string(bytes))
    }

We simply write back the full blockchain, in JSON format, that we can view in any browser by visiting localhost:8080. We have ourADDR variable set as 8080 in our `.env` file so if you change it, make sure to visit your correct port.

Our POST request is a little bit more complicated, but not by much. To start, we’ll need a new Message struct. We’ll explain in a second why we need it.


    type Message struct {
	BPM int
    }

Here’s the code for the handler that writes new blocks. We’ll walk you through it after you’ve read it.

    func handleWriteBlock(w http.ResponseWriter, r *http.Request) {
	var m Message

	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&m); err != nil {
		respondWithJSON(w, r, http.StatusBadRequest, r.Body)
		return
	}
	defer r.Body.Close()

	newBlock, err := generateBlock(Blockchain[len(Blockchain)-1], m.BPM)
	if err != nil {
		respondWithJSON(w, r, http.StatusInternalServerError, m)
		return
	}
	if isBlockValid(newBlock, Blockchain[len(Blockchain)-1]) {
		newBlockchain := append(Blockchain, newBlock)
		replaceChain(newBlockchain)
		spew.Dump(Blockchain)
	}

	respondWithJSON(w, r, http.StatusCreated, newBlock)

    }


The reason we used a separate Message struct is to take in the request body of the JSON POST request we’ll use to write new blocks. This allows us to simply send a POST request with the following body and our handler will fill in the rest of the block for us:

    {"BPM":50}


The 50 is an example pulse rate in beats per minute. Use your own by changing that integer to your own pulse rate.

After we’re done decoding the request body into our var m Message struct, we create a new block by passing in the previous block and our new pulse rate into the generateBlock function we wrote earlier . This is everything the function needs to create a new block. We do a quick check to make sure the new block is kosher using the isBlockValid function we created earlier.


A couple notes

- spew.Dump is a convenient function that pretty prints our structs into the console. It’s useful for debugging.
- for testing POST requests, we like to use Postman. curl works well too, if you just can’t get away from the terminal.


 When our POST requests are successful or unsuccessful, we want to be alerted accordingly. We use a little wrapper function respondWithJSON to let us know what happened. Remember, in Go, never ignore errors. Handle them gracefully.


    func respondWithJSON(w http.ResponseWriter, r *http.Request, code int, payload interface{}) {
	response, err := json.MarshalIndent(payload, "", "  ")
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("HTTP 500: Internal Server Error"))
		return
	}
	w.WriteHeader(code)
	w.Write(response)
    }


#### Almost done!

Let’s wire all these different blockchain functions, web handlers and the web server in a short, clean main function:

    func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal(err)
	}

	go func() {
		t := time.Now()
		genesisBlock := Block{0, t.String(), 0, "", ""}
		spew.Dump(genesisBlock)
		Blockchain = append(Blockchain, genesisBlock)
	}()
	log.Fatal(run())

    }


##### So what’s going on here?

- godotenv.Load() allows us to read in variables like our port number from the.env file we placed at the root of our directory so we don’t have to hardcode them (gross!) throughout our app.
- genesisBlock is the most important part of the main function. We need to supply our blockchain with an initial block, or else a new block will not be able to compare its previous hash to anything, since a previous hash doesn’t exist.
- We isolate the genesis block into its own go routine so we can have a separation of concerns from our blockchain logic and our web server logic. This will work without the go routine but it’s just cleaner this way.