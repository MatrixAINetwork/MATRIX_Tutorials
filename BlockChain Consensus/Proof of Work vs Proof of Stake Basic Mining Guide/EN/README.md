# Proof of Work vs Proof of Stake: Basic Mining Guide

Recently you might have heard about the idea to move from an Ethereum consensus based on the Proof of Work (PoW) system to one based on the so-called Proof of Stake.

In this article, I will explain to you the main differences between Proof of Work vs Proof of Stake and I will provide you a definition of mining, or the process new digital currencies are released through the network.

Also, what will change regarding mining techniques if the Ethereum community decides to do the transition from “work” to “stake”?

This article wants to be a basic guide to understanding the problem above.


![](http://blockgeeks.com/wp-content/uploads/2017/03/infographics2017-01.png)


### What is the Proof of work?

First of all, let’s start with basic definitions.

Proof of work is a protocol that has the main goal of deterring cyber-attacks such as a distributed denial-of-service attack (DDoS) which has the purpose of exhausting the resources of a computer system by sending multiple fake requests.

The Proof of work concept existed even before bitcoin, but Satoshi Nakamoto applied this technique to his/her – we still don’t know who Nakamoto really is – digital currency revolutionizing the way traditional transactions are set.

In fact, PoW idea was originally published by Cynthia Dwork and Moni Naor back in 1993, but the term “proof of work” was coined by Markus Jakobsson and Ari Juels in a document published in 1999.

But, returning to date, Proof of work is maybe the biggest idea behind the Nakamoto’s Bitcoin white paper – published back in 2008 – because it allows trustless and distributed consensus.

### What’s trustless and distributed consensus?
A trustless and distributed consensus system means that if you want to send and/or receive money from someone you don’t need to trust in third-party services.

When you use traditional methods of payment, you need to trust in a third party to set your transaction (e.g. Visa, Mastercard, PayPal, banks). They keep their own private register which stores transactions history and balances of each account.

The common example to better explain this behavior is the following: if Alice sent Bob $100, the trusted third-party service would debit Alice’s account and credit Bob’s one, so they both have to trust this third-party is to going do the right thing.

With bitcoin and a few other digital currencies, everyone has a copy of the ledger (blockchain), so no one has to trust in third parties, because anyone can directly verify the information written.

![](http://blockgeeks.com/wp-content/uploads/2016/09/home.jpg)

### Proof of work and mining
Going deeper, proof of work is a requirement to define an expensive computer calculation, also called mining, that needs to be performed in order to create a new group of trustless transactions (the so-called block) on a distributed ledger called blockchain.

Mining serves as two purposes:

To verify the legitimacy of a transaction, or avoiding the so-called double-spending;

To create new digital currencies by rewarding miners for performing the previous task.

When you want to set a transaction this is what happens behind the scenes:

Transactions are bundled together into what we call a block;

Miners verify that transactions within each block are legitimate;

To do so, miners should solve a mathematical puzzle known as proof-of-work problem;

A reward is given to the first miner who solves each blocks problem;

Verified transactions are stored in the public blockchain

This “mathematical puzzle” has a key feature: asymmetry. The work, in fact, must be moderately hard on the requester side but easy to check for the network. This idea is also known as a CPU cost function, client puzzle, computational puzzle or CPU pricing function.

All the network miners compete to be the first to find a solution for the mathematical problem that concerns the candidate block, a problem that cannot be solved in other ways than through brute force so that essentially requires a huge number of attempts.

When a miner finally finds the right solution, he/she announces it to the whole network at the same time, receiving a cryptocurrency prize (the reward) provided by the protocol.

From a technical point of view, mining process is an operation of inverse hashing: it determines a number (nonce), so the cryptographic hash algorithm of block data results in less than a given threshold.

This threshold, called difficulty, is what determines the competitive nature of mining: more computing power is added to the network, the higher this parameter increases, increasing also the average number of calculations needed to create a new block. This method also increases the cost of the block creation, pushing miners to improve the efficiency of their mining systems to maintain a positive economic balance. This parameter update should occur approximately every 14 days, and a new block is generated every 10 minutes.

Proof of work is not only used by the bitcoin blockchain but also by ethereum and many other blockchains.

Some functions of the proof of work system are different because created specifically for each blockchain, but now I don’t want to confuse your ideas with too technical data.

The important thing you need to understand is that now Ethereum developers want to turn the tables, using a new consensus system called proof of stake.