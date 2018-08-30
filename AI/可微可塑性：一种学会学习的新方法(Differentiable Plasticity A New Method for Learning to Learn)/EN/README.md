## Differentiable Plasticity: A New Method for Learning to Learn


![](https://i.imgur.com/m3Qt3xK.png)

Neural networks, which underlie many of Uber’s machine learning systems, have proven highly successful in solving complex problems, including image recognition, language understanding, and game-playing. However, these networks are usually trained to a stopping point through gradient descent, which incrementally adjusts the connections of the network based on its performance over many trials. Once the training is complete, the network is fixed and the connections can no longer change; as a result, barring any later re-training (again requiring many examples), the network in effect stops learning at the moment training ends.

By contrast, biological brains exhibit plasticity—that is, the ability for connections between neurons to change continually and automatically throughout life, allowing animals to learn quickly and efficiently from ongoing experience. The levels of plasticity of different areas and connections in the brain are the result of millions of years of fine-tuning by evolution to allow efficient learning during the animal’s lifetime. The resultant ability to learn continually over life lets animals adapt to changing or unpredictable environments with very little additional data. We can quickly memorize patterns that we have never seen before or learn new behaviors from just a few trials in entirely novel situations.

To give our artificial agents similar abilities, Uber AI Labs has developed a new method called differentiable plasticity that lets us train the behavior of plastic connections through gradient descent so that they can help previously-trained networks adapt to future conditions. While evolving such plastic neural networks is a longstanding area of research in evolutionary computation, to our knowledge the work introduced here is the first to show it is possible to optimize plasticity itself through gradient descent. Because gradient-based methods underlie many of the recent spectacular breakthroughs in artificial intelligence (including image recognition, machine translation, Atari video games, and Go playing), making plastic networks amenable to gradient descent training may dramatically expand the power of both approaches.


### How differentiable plasticity works

In our method, each connection receives an initial weight, as well as a coefficient that determines how plastic the connection is. More precisely, the activation yi of neuron i is calculated as follows:

![](https://i.imgur.com/DTgUwyt.png)

The first equation is a typical activation function for neural network units, except that the input weights have a fixed component (green) and a plastic component (red). The Hi,j term in the plastic component is automatically updated as a function of ongoing inputs and outputs (as specified in the second equation—note that other formulations are possible, as discussed in the paper).

During an initial training period, gradient descent tunes the structural parameters wi,j and αi,j, which determine how large the fixed and plastic components are. As a result, after this initial training, the agent can learn automatically from ongoing experience because the plastic component of each connection is adequately shaped by neural activity to store information, reminiscent of some forms of learning in animals (including humans).

### Demonstrating differentiable plasticity

To demonstrate the potential of differentiable plasticity, we applied it to several challenging tasks that require fast learning from unpredictable stimuli.

In an image reconstruction task (Figure 1), a network memorizes a set of natural images that it has never seen before; then one of these images is shown, but with one half of it erased, and the network must reconstruct the missing half from memory. We show that differentiable plasticity can effectively train large networks, with millions of parameters, to solve this task. Importantly, traditional networks with non-plastic connections (including state-of-the-art recurrent architectures such as LSTMs) cannot solve this task and take considerably more time to learn a massively simplified version of it.