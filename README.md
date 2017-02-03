# Rockrose: Deep Reinforcement Learning Learn.


## Requirements

- [skimage](http://scikit-image.org/)
- [TensorFlow](https://github.com/tensorflow/tensorflow) (Tested with r0.10)
- [Keras](https://github.com/fchollet/keras)
- [Gym](https://github.com/openai/gym)
- [pygame](http://www.pygame.org/wiki/GettingStarted)
- [Bluelake](https://github.com/lancelee82/bluelake) # in this branch, Bluelake is as a sub folder
- [Bluegym](https://github.com/lancelee82/bluegym) # in this branch, Bluegym is as a sub folder


## Algorithms

- DQN
    [V. Mnih, et. al., Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)
    [V. Mnih, et. al., Human-level Control through Deep Reinforcement Learning, Nature, 2015.](http://www.nature.com/nature/journal/v518/n7540/full/nature14236.html)
- A3C
    [Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783)
- UNREAL
    [Reinforcement Learning with Unsupervised Auxiliary Tasks](https://arxiv.org/abs/1611.05397)
    
## Configuration of keras (for ubuntu, this exists in ~/.keras/keras.json)

{
    "image_dim_ordering": "th", 
    "epsilon": 1e-07, 
    "floatx": "float32", 
    "backend": "tensorflow"
}