# Using Linear optimal transport to model plant growth
This Github repository is a replication of the paper [_Registration of spatio-temporal point clouds of plants for 
phenotyping_](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0247243) by Chebrolu et al. 
However, we are creating a modification from the original paper, since the original 
dataset that was used in the paper only contained plant data (point clouds) in only two days for both maize and tomato. 
For a more comprehensive view of working with plant data, we decide to use the 
[Pheno4D Dataset](https://www.ipb.uni-bonn.de/data/pheno4d/index.html), which contains point clouds of both maize and 
tomato in the span of 12 days each, and with more plant variants for each crop. 

For the replication, we aim to model plant growth via Linear Optimal Transport (LOT) embeddings and compare those with 
other machine learning models in classification, such as neural networks. The hope is that the approach via optimal 
transport has a better performance than that of traditional machine learning methods. 

Optimal Transport is a study of trying to measure the difference in probability distributions $\mu$ and $\nu$ (we can 
imagine this as moving a sand pile on the beach and trying to transform it into a castle with minimum 'effort'):

$$
\inf_{T: T_{\\#}\mu = \nu} \int \left| T(x) - x \right| \mu d(x).
$$

The solution to the problem above is exactly the Wasserstein distance between the distibutions $\mu$ and $\nu$:

$$
W_p(\mu, \nu) = \inf_{\gamma \in \Gamma(\mu, \nu)} (\mathbb{E}_{(x, y) \sim \gamma} d(x, y)^p)^{1/p},
$$

where $\Gamma(\mu, \nu)$ is the set of all couplings between the two distributions $\mu$ and $\nu$. 
This is convenient when training point clouds, since we can model data representations in different times as discrete 
probability distributions evolving through time.
Often with real data, we are working in the space $\mathbb{R}^d$, and hence we can use the Euclidean norm as our distance 
metric in the Wasserstein distance:

$$
d(x, y) = \left| x - y \right|_2.
$$

Normally, finding the Wasserstein distance between two probability distributions $\mu$ and $\nu$ above is computationally 
expensive, but there are numerous results which could dramatically reduce the computational complexity (such as entropic 
regularization). Another approach to solving this problem is Linear Optimal Transport (LOT), which is what we will go 
through our replication. We consider the embedding $\mu \mapsto T_{\sigma}^{\mu}$ by choosing a reference distribution 
$\sigma$, and take the tangent plane on the Wasserstein manifold. This produces exactly the $L^2$ space of random 
variables, which we can operate a lot of machine learning algorithms on.


Up till currently, we have been mostly focusing on the theory of optimal transport, as it has proven to be quite 
difficult to understand. Therefore, we do not have much code as we would hope to have for the checkpoint. For the theory, 
here are a list of papers that we tried to understand in the few weeks prior to the checkpoint:

- [Linearized Optimal Transport pyLOT Library: A Toolkit on Machine Learning on 
Point Clouds](https://arxiv.org/abs/2502.03439) by Alexander Cloninger, Jun Linwu, Varun Khurana, & Nicholas Karris
- [Do Neural Optimal Transport Solvers Work? A Continuous Wasserstein-2 Benchmark](https://arxiv.org/abs/2106.01954) 
by Alexander Korotin et al.
- [Linear Optimal Transport Embedding: Provable Wasserstein classification for certain rigid transformations and 
perturbations](https://arxiv.org/abs/2008.09165) by Caroline Moosmuller & Alexander Cloninger
- [Generalized Sliced Wasserstein Distances](https://arxiv.org/abs/1902.00434) by Soheil Kolouri et al.
- [Sinkhorn Distances: Lightspeed Computation of Optimal 
Transport](https://papers.nips.cc/paper_files/paper/2013/hash/af21d0c97db2e27e13572cbf59eb343d-Abstract.html) by 
Marco Cuturi
- [Statistical Optimal Transport](https://arxiv.org/abs/2407.18163) by Sinho Chewi, Jonathan Niles-Weed, & 
Philippe Rigollet

