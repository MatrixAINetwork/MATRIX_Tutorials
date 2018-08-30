## Differentiable Plasticity: A New Method for Learning to Learn


![](https://i.imgur.com/m3Qt3xK.png)

Neural networks, which underlie many of Uber’s machine learning systems, have proven highly successful in solving complex problems, including image recognition, language understanding, and game-playing. However, these networks are usually trained to a stopping point through gradient descent, which incrementally adjusts the connections of the network based on its performance over many trials. Once the training is complete, the network is fixed and the connections can no longer change; as a result, barring any later re-training (again requiring many examples), the network in effect stops learning at the moment training ends.

By contrast, biological brains exhibit plasticity—that is, the ability for connections between neurons to change continually and automatically throughout life, allowing animals to learn quickly and efficiently from ongoing experience. The levels of plasticity of different areas and connections in the brain are the result of millions of years of fine-tuning by evolution to allow efficient learning during the animal’s lifetime. The resultant ability to learn continually over life lets animals adapt to changing or unpredictable environments with very little additional data. We can quickly memorize patterns that we have never seen before or learn new behaviors from just a few trials in entirely novel situations.

To give our artificial agents similar abilities, Uber AI Labs has developed a new method called differentiable plasticity that lets us train the behavior of plastic connections through gradient descent so that they can help previously-trained networks adapt to future conditions. While evolving such plastic neural networks is a longstanding area of research in evolutionary computation, to our knowledge the work introduced here is the first to show it is possible to optimize plasticity itself through gradient descent. Because gradient-based methods underlie many of the recent spectacular breakthroughs in artificial intelligence (including image recognition, machine translation, Atari video games, and Go playing), making plastic networks amenable to gradient descent training may dramatically expand the power of both approaches.


### How differentiable plasticity works

In our method, each connection receives an initial weight, as well as a coefficient that determines how plastic the connection is. More precisely, the activation yi of neuron i is calculated as follows:

![](https://i.imgur.com/DTgUwyt.png)

The first equation is a typical activation function for neural network units, except that the input weights have a fixed component (green) and a plastic component (red). The Hi,j term in the plastic component is automatically updated as a function of ongoing inputs and outputs (as specified in the second equation—note that other formulations are possible).

During an initial training period, gradient descent tunes the structural parameters wi,j and αi,j, which determine how large the fixed and plastic components are. As a result, after this initial training, the agent can learn automatically from ongoing experience because the plastic component of each connection is adequately shaped by neural activity to store information, reminiscent of some forms of learning in animals (including humans).

### Demonstrating differentiable plasticity

To demonstrate the potential of differentiable plasticity, we applied it to several challenging tasks that require fast learning from unpredictable stimuli.

In an image reconstruction task (Figure 1), a network memorizes a set of natural images that it has never seen before; then one of these images is shown, but with one half of it erased, and the network must reconstruct the missing half from memory. We show that differentiable plasticity can effectively train large networks, with millions of parameters, to solve this task. Importantly, traditional networks with non-plastic connections (including state-of-the-art recurrent architectures such as LSTMs) cannot solve this task and take considerably more time to learn a massively simplified version of it.

![](https://i.imgur.com/4Qf4Tl6.png)


    Figure 1: An image completion task (each row indicates a separate episode). After being shown three images, the network is given a partial image and must reconstruct the missing part from memory. Non-plastic networks (including LSTMs) cannot solve this task. Source images from the CIFAR10 dataset.


We also trained plastic networks to solve the Omniglot task (a standard ”learning to learn” task), which requires learning to recognize a set of novel handwritten symbols from a single demonstration of each one. Furthermore, the method can also be applied to reinforcement learning problems: plastic networks outperform non-plastic ones in a maze exploration task in which the agent must discover, memorize, and repeatedly reach the location of a reward within a maze (Figure 2). In this way, the simple idea of adding plasticity coefficients to neural networks offers a genuinely novel approach—sometimes the best available—to solving a wide breadth of problems requiring continuous learning from ongoing experience.

![](https://i.imgur.com/E1BHPAv.png)


    Figure 2: A maze exploration task. The agent (yellow square) is rewarded for hitting the reward location (green square) as many times as possible (the agent is teleported to a random location each time it finds the reward). In Episode 1 (left), the agent’s behavior is essentially random. After 300,000 episodes (right), the agent has learnt to memorize the reward location and navigate towards it.

### Looking forward
In effect, differentiable plasticity offers a new, biologically-inspired approach to the classical problem of “Learning to Learn,” or “meta-learning.” The approach is also highly flexible, providing gradient descent with an elementary building block (the plastic connection) that it can harness in a variety of powerful ways, as demonstrated in the diverse tasks described above.

Furthermore, it opens the door to multiple new avenues of research. For example, can we improve existing complex network architectures, such as LSTMs, by making their connections plastic? What if the plasticity of the connections was under the control of the network itself, as it seems to be in biological brains through the influence of neuromodulators? Can plasticity offer a more efficient form of memory than recurrence alone (note that recurrence stores incoming information in neural activity, while plasticity stores it in connections, which are much more numerous)?

We intend to investigate these and other exciting questions in our future work in differentiable plasticity and hope others will join us in this exploration. 