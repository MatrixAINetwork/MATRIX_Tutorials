###  Keeping up with AI in 2019
### What is the next big thing in AI and ML?

The past year has been rich in events, discoveries and developments in AI. It is hard to sort through the noise to see if the signal is there and, if it is, what is the signal saying. This post attempts to get you exactly that: I’ll try to extract some of the patterns in the AI landscape over the past year. And, if we are lucky, we’ll see how some of the trends extend into the near future.

    Confucius is quoted saying: “The hardest thing of all is to find a black cat in a dark room, especially if there is no cat.” Wise man.


![](https://user-gold-cdn.xitu.io/2019/3/9/16962c7e40bf05c6?imageslim)


See that cat?


Make no mistake: this is an opinion piece. I am not trying to establish some comprehensive record of accomplishments for the year. I am merely trying to outline some of these trends. Another caveat : this review is US-centric. A lot of interesting things are happening, say, in China, but I, unfortunately, am not familiar with that exciting ecosystem.

Who is this post for? If you are still reading, it is probably for you: an engineer, who wants to widen their horizons; an entrepreneur, looking where to direct their energy next; a venture capitalist, looking for their next deal; or just a technology cheerleader, who can’t wait to see where this whirlwind is taking us next.

#### Algorithms

The algorithmic discourse was, undoubtedly, dominated by the Deep Neural Networks. Of course, you would hear about someone deploying a “classical” machine learning model (like Gradient Boosted trees or Multi-armed bandits) here and there. And claiming that it’s the only thing anyone ever needed. There are proclamations, that deep learning is at its death throes. Even top researchers are questioning the efficiency and robustness of some DNN architectures. But, like it or not, DNNs were everywhere: in self-driving cars, natural language systems, robots — you name it. None of the leaps in DNNs were as pronounced as in Natural Language Processing, Generative Adversarial Networks, and deep Reinforcement Learning.

#### Deep NLP: BERT et al.

Though before 2018 there had been several breakthroughs in using DNNs for text (word2vec, GLOVE, LSTM-based models come to mind), one key conceptual element was missing: transfer learning. That is, training a model on a large amount of publicly available data, and then “fine-tuning” it on the specific dataset you are working with. In computer vision, using the patterns discovered on the famous ImageNet dataset to a specific problem was, usually, a part of a solution.


The problem was, the techniques used for transfer learning didn’t really apply well to NLP problems. In some sense, the pre-trained embeddings like word2vec were filling that role, but they work on a single word level and fail to capture the high level structure of language.