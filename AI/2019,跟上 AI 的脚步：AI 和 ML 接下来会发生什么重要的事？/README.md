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


In 2018, however, this has changed. ELMo, contextualized embeddings became the first significant step to improved transfer learning in NLP. ULMFiT went even further: not satisfied with the semantic capturing capability of embeddings, the authors figured out a way to do a transfer learning for the entire model.


But the most interesting development was, definitely, the introduction of BERT. By letting the language model learn from the entire collection of articles from English Wikipedia, the team was able to achieve state-of-the-art results on 11 NLP tasks — quite a feat! Even better, both the code and the pre-trained modes were published online — so you can apply this breakthrough to your own problem.


#### Many Faces of GANs


CPU speeds are not growing exponentially any more, but the number of academic papers on Generative Adversarial Networks surely seems to be continuing to grow. GANs have been an academic darling for many years now. The real life applications seem to be few and far between though, and it changed very little in 2018. Still GANs have amazing potential waiting to be realized.


A new approach, that emerged, was an idea of progressively growing GANs: getting the generator to increase the resolution of its output progressively throughout the training process. One of the more impressive papers that used this approach was employing style transfer techniques to generate realistic looking photos. How realistic? You tell me:



 How and why do the GANs really work though? We haven’t had deep insight into that yet, but there are important steps being made: a team at MIT has done a a high quality study of that problem.

Another interesting development, though not technically a GAN, was Adversarial Patch. The idea was to use both black-box (basically, not looking at the internal state of a neural network) and white-box methods to craft a “patch”, that would deceive a CNN-based classifier. This is an important result: it guided us towards better intuition about how DNNs work and how far we are still from a human-level conceptual perception.



#### We need Reinforcement

Reinforcement learning has been in the spotlight since AlphaGo defeated Lee Sedol in 2016. With AI dominating the last “classic” game though, what else there is to conquer? Well, the rest of the world! Specifically, computer games and robotics.

For it’s training, reinforcement learning relies on the “reward” signal, a scoring of how well it did in it’s last attempt. Computer games provide a natural environment, where such signal is readily available, as opposed to the real life. Hence all the attention RL researches are giving to teaching AI how to play Atari games.

Talking about DeepMind, their new creation, AlphaStar just made news again. This new model has defeated one of the top StarCraft II professional players. StarCraft is much more complex than chess or Go, with a huge action space and crucial information hidden from a player, unlike in most board games. This victory is a very significant leap for the field as a whole.

OpenAI, another important player in the space or RL, did not sit idle either. Their claim to fame is OpenAI Five, a system that in August defeated a team of 99.95th percentile players in Dota 2, an extremely complex esports game.

Though OpenAI has been giving a lot of attention to computer games, they haven’t ignored a real potential application for RL: robots. In real world, the feedback one might give to a robot is rare and expensive to create: you basically need a human babysitting your R2D2, while it’s trying to take its first “steps”. And you need millions of these data points. To bridge that gap, the recent trend was to learn to simulate an environment and run a large number of those scenarios in parallel to teach a robot basic skills, before moving on to the real world. Both OpenAI and Google are working on that approach..


#### Honorable mention: Deepfakes

Deepfakes are images or videos that show (usually) a public figure doing or saying something they never did or said. They are created by training a GAN on a large amount of footage of the “target” person, and then generating new media with desired actions performed in it. A desktop application called FakeApp released in January 2018 allows anyone with a computer and zero computer science knowledge to create deepfakes. And while the videos it produces can be easily spotted as non genuine, the technology has progressed very far. Just watch this video to see how much.