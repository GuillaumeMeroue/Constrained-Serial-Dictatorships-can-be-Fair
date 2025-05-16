# Constrained Serial Dictatorship

## Abstract

When allocating indivisible items to agents, it is known that the only strategyproof mechanisms that satisfy a set of rather mild conditions are {\em constrained serial dictatorships}: given a fixed order over agents, at each step the designated agent chooses a given number of items (depending on her position in the sequence).  
Agents who come earlier in the sequence have a larger choice of items; however, this advantage can be compensated by a higher number of items received by those who come later. How to balance priority in the sequence and number of items received is a nontrivial question. 
We use a previous model, parameterized by a mapping from ranks to scores, a social welfare functional, and a distribution over preference profiles. For several meaningful choices of parameters, we show that the optimal sequence can be computed exactly in polynomial time  or approximated using sampling.  
Our results hold for several probabilistic models on preference profiles, with an emphasis on the Plackett-Luce model. 
We conclude with experimental results showing how the optimal sequence is impacted by various parameters.

## Source Files Overview

### Sampling

These files allow for the sampling of preference profiles based on different distributions:

- `sample_luce.py`: Samples preferences according to the Luce model.
- `sample_mallows.py`: Samples preferences using the Mallows model.
- `sample_IC.py`: Samples preferences assuming an Impartial Culture (IC) model.

### Classic Allocation

These files implement the standard method of performing allocations step by step, calculating utilities, and iterating to find the best possible allocation:

- `Allocation.py`: Allocates objects to agents based on a given policy.
- `Utility.py`: Handles all utility-related computations, such as calculating an agent's utility and overall social welfare.
- `Bruteforce.py`: Tries all possible allocations, computes the social welfare for each, and retains the one that maximizes the objective.

### Dynamic Programming

These files implement dynamic programming approaches to optimize the allocation process:

- `Approx_prog_dyn.py`: Implements Equation 2 when condition C1 is met, with expected utilities approximated via sampling.
- `Prog_dyn.py`: Implements Equation 2 when condition C1 is met, using Equation 1 to compute expected utilities.

### Greedy Algorithms

- `Greedy_esw.py`: Implements Algorithm 1, along with an enhanced version that maximizes the leximin.

### Social Welfare Functions and Vector Scoring

Please note that there are two coexisting implementations of social welfare functions and vector scoring functions—one set used in the dynamic programming files and another in the rest of the source files.

### Tests

Functions have been tested in this folder, primarily through unit tests, to ensure consistent results across the same input data.

### Plotting

The functions used to generate data for the paper and the visualization can be found in this section.

## Visualization

To launch the visualization, open the `index.html` file in a web browser or try the [Web-App](https://guillaumemeroue.github.io/IJCAI25/index.html). This visualization is not the core focus of our paper, nor is it an industrial-grade application with full features. However, it provides reviewers with visual insights into the optimal allocation process, the distribution of objects, and utilities among agents. This interactive visualization is designed to aid understanding and provide intuitive support for the concepts discussed in the paper.

Several allocations have been precomputed for specific values of `n` (number of agents) and `m` (number of objects). The corresponding data has been hardcoded into the HTML file, so no local or online server deployment is required to view the visualization.


## Citation

If you found this codebase or our work useful please cite us:

```
@misc{bouveret2025constrainedserialdictatorshipsfair,
      title={Constrained Serial Dictatorships can be Fair}, 
      author={Sylvain Bouveret and Hugo Gilbert and Jérôme Lang and Guillaume Méroué},
      year={2025},
      eprint={2301.06086},
      archivePrefix={arXiv},
      primaryClass={cs.GT},
      url={https://arxiv.org/abs/2301.06086}, 
}

```
