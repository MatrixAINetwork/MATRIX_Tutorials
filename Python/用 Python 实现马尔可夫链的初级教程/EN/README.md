## Markov Chains in Python: Beginner Tutorial

    Learn about Markov Chains, their properties, transition matrices, and implement one yourself in Python!


A Markov chain is a mathematical system usually defined as a collection of random variables, that transition from one state to another according to certain probabilistic rules. These set of transition satisfies the Markov Property, which states that the probability of transitioning to any particular state is dependent solely on the current state and time elapsed, and not on the sequence of state that preceded it. This unique characteristic of Markov processes render them memoryless.

In this tutorial, you will discover when you can use markov chains, what the Discrete Time Markov chain is. You'll also learn about the components that are needed to build a (Discrete-time) Markov chain model and some of its common properties. Next, you'll implement one such simple model with Python using its numpy and random libraries. You will also learn some of the ways to represent a Markov chain like a state diagram and transition matrix.
Want to tackle more statistics topics with Python? Check out DataCamp's Statistical Thinking in Python course!

Let's transition...

### Why Markov Chains?
Markov Chains have prolific usage in mathematics. They are widely employed in economics, game theory, communication theory, genetics and finance. They arise broadly in statistical specially Bayesian statistics and information-theoretical contexts. When it comes real-world problems, they are used to postulate solutions to study cruise control systems in motor vehicles, queues or lines of customers arriving at an airport, exchange rates of currencies, etc. The algorithm known as PageRank, which was originally proposed for the internet search engine Google, is based on a Markov process. Reddit's Subreddit Simulator is a fully-automated subreddit that generates random submissions and comments using markov chains, so cool!


### Markov Chain
A Markov chain is a random process with the Markov property. A random process or often called stochastic property is a mathematical object defined as a collection of random variables. A Markov chain has either discrete state space (set of possible values of the random variables) or discrete index set (often representing time) - given the fact, many variations for a Markov chain exists. Usually the term "Markov chain" is reserved for a process with a discrete set of times, that is a Discrete Time Markov chain (DTMC).