---
title: "Where does the t-distribution come from? Sampling with unknown variance"
category: ds
---


The [Student's t-distribution](https://en.wikipedia.org/wiki/Student%27s_t-distribution) is ubiquitous in statistics, more specifically in the realm of hypothesis testing in continuous variables. What it means conceptually and why it arises in certain contexts with that specific functional form, however, is not always clearly understood. Explanations range from a very basic "like normal distribution but with heavier tails" to a complex interplay of uninformative priors, pivotal quantities, and Bayesian updates. There is a conceptual, easy-to-grasp explanation, that goes along the lines of "Student's t-distribution is defined as the distribution of the random variable $$t$$ which is (very loosely) the "best" that we can do not knowing $$\sigma$$."[^1] In this brief post, we will dive into that sentence and see how the t-distribution arises from considering $$\sigma$$ as unknown and factoring this into a minimal Bayesian framework.

## Estimating mean with a known variance

Let's first recap how we can deal, with Bayesian inference, to the estimation of the parameter of the mean knowing the variance. We will assume that we know for a fact that we will draw samples from an underlying distribution with unknown mean and with standard deviation $$\sigma$$. We draw $$n$$ numbers (which we will call $$x_i$$). How do we estimate the true mean? We can calculate the mean of the sample we just got, but we need a bit more than a point estimate. This question (and questions that are very similar to it) can be answered in many different fashions, one of them is from the Bayesian inference framework:

$$p(\mu | x_i) \propto p(\mu) \cdot p(x_i | \mu)$$

Considering an uninformative prior of $$p(\mu)$$ constant, we can reduce the equation to the well-known result (and a bit misleading!): $$p(\mu \| x_i) \sim \mathcal{N}(\bar{x},\sigma^2/n)$$. When the variance is known, then, we "know" that the true mean is drawn from a normal distribution with those parameters.

## But we don't know the variance

But what happens if we don't have that prior knowledge of the variance? What if we had to estimate it from our measurements? We can estimate the _true_ variance with the variance of the sample we just got, but: you know where we are going, we again need a bit more than a point estimate, we need a _probability distribution for the parameter $$\sigma$$_. To calculate the distribution of the true mean we would need to first draw a $$\sigma$$ from this distribution, and use this draw to get a sample of $$\mu$$. We will repeat this multiple times in order to get a distribution.

Suppose we have drawn 5 samples from a normal distribution, that yielded a mean $$\bar{x} = 15$$ and a sample variance $$s^2 = 45$$. As we said, we want to add here the uncertainty that we have for the variance. We will do it crudely at first, let's simply say that we will let the variance be everywhere between 0 and 90, uniformly distributed.


<script src="https://gist.github.com/pabloalcain/892a2200f96ad66d961d9a95b4d4a4b2.js"></script>

We plot the results and alongside the obtained distribution for $$\mu$$ we also plot the associated normal distribution. By introducing the variance as a distribution instead of a known point estimate, our distribution from $$\mu$$ started to differ from that of a normal distribution: it's much sharper and it has slightly heavier tails.

<figure>
  <img
  src="{{site.url}}/assets/posts/t-distribution/uniform_variance.png"
  alt="Distribution of parameters with uniformly distributed variance"/>
  <figcaption>Distribution of parameters with uniformly distributed variance</figcaption>
</figure>

We know that a complete certainty on the value of $$\sigma$$ (a [Dirac's delta distribution](https://en.wikipedia.org/wiki/Dirac_delta_function)) yields a normal distribution for $$\mu$$, with variance equal to $$\sigma^2/n$$. Modifying the probability density function of $$\sigma$$ to a uniform distribution yielded (unsurprisingly) a different distribution for $$\mu$$, no longer a normal one. Let's think about the differences: as we said, this is analogous to drawing $$\sigma$$ from the uniform distribution and using it to get a sample of $$\mu$$. Since the $$\sigma$$ distribution is uniform, we have a lot of samples that have very small $$\sigma$$ and, therefore, sharpen the definition around $$\mu$$ when those low $$\sigma$$ are drawn. Let's change that a bit, and try to ease the weight of the low $$\sigma$$ in the distribution. For example, let's use a `lognormal` distribution for $$\sigma$$:

<script src="https://gist.github.com/pabloalcain/232a2bbf6a20511c15ba80787d3189f6.js"></script>
<figure>
  <img
  src="{{site.url}}/assets/posts/t-distribution/lognormal_variance.png"
  alt="Distribution of parameters with log-normally distributed variance"/>
  <figcaption>Distribution of parameters with log-normally distributed variance</figcaption>
</figure>

The center peak is still higher than that of a normal distribution, but lower than it was before. And the tails are starting to look much heavier than that of the normal distribution.

We can keep doing this with any distribution for $$\sigma$$ and there is (at least for now) no reason to choose one over the other. And it's clear that the moment we choose a distribution for $$\sigma$$, the distribution for $$\mu$$ will change, so there is an association between the distributions $$\mathcal{F}(\sigma)$$ and $$\mathcal{G}(\mu)$$. We have already discussed $$\mathcal{F}$$ being the uniform and the lognormal distribution, and how it generated specific $$\mathcal{G}$$ distributions (we could give them a name if we wanted). But among all of the possible distributions for $$\mathcal{F}$$ there is a special one.

## Finding the t-distribution

Now we will propose another $$\mathcal{F}$$ distribution for $$\sigma$$: [inverse-chi-squared distribution](https://en.wikipedia.org/wiki/Inverse-chi-squared_distribution), essentially a variation on the $$\Gamma$$ distribution. It takes two parameters: the degrees of freedom $$\nu$$ and the location $$x_0$$. Since the mean of $$\text{Inv-}\chi^2(\nu, x_0)$$ is $$x_0$$ and $$\nu$$ has a very suggestive name, let's check a distribution with $$\nu = n - 1$$ and $$x_0 = s^2$$:


<script src="https://gist.github.com/pabloalcain/e5f78f2c580a516d557bdecd385b077d.js"></script>
<figure>
  <img
  src="{{site.url}}/assets/posts/t-distribution/inv_chi2_variance.png"
  alt="Distribution of parameters with inverse-chi-squared distributed variance"/>
  <figcaption>Distribution of parameters with inverse-chi-squared distributed variance</figcaption>
</figure>

Turns out that this specific $$\mathcal{F}$$ distribution we set for the variance is so important that the generated $$\mathcal{G}$$ function has already been named: it's the Student's t-distribution:

<figure>
  <img
  src="{{site.url}}/assets/posts/t-distribution/t-distribution.png"
  alt="Student's t-distribution"/>
  <figcaption>Student's t-distribution</figcaption>
</figure>

As the sample size increases, we have more certainty on the variance, and the $$\text{Inv-}\chi^2$$ distribution narrows towards the center. Since $$\mathcal{F}$$ becomes better defined in the center (closer to a Dirac's delta), the $$\mathcal{G}$$ distribution becomes closer to a normal distribution:

<figure>
  <img
  src="{{site.url}}/assets/posts/t-distribution/sample_size_evolution.gif"
  alt="Evolution of t-distribution as sample size increases"/>
  <figcaption>Evolution of t-distribution as sample size increases</figcaption>
</figure>

## OK, but why inverse-chi-squared?

As a final note, let's see quickly why inverse-chi-squared is of particular importance. In [Student's original paper](http://www.dcscience.net/Student-t-1908.pdf), Willam Gosset expands the moment coefficients of the distribution of $$\sigma$$ that could have resulted in the observed variance $$s^2$$ and, although not arriving at a formal proof, finds $$\mathcal{F}$$ as the $$\text{Inv-}\chi^2$$ (the derivation is in section I of the paper, only 4 pages long; it looks like he was not aware that he had arrived to a function related to $$\Gamma$$). As we mentioned in the introduction, nowadays the derivation can be greatly simplified through the Bayesian framework, with $$\text{Inv-}\chi^2$$ as a posterior distribution for an uninformative prior for the variance. A derivation of this can be found in section 3.2 of the book [Bayesian Data Analysis](http://www.stat.columbia.edu/~gelman/book/)[^2].

All the calculations done for this article are in the [notebook]({{site.url}}/assets/posts/t-distribution/t-distribution.ipynb).


[^1]: https://mathworld.wolfram.com/Studentst-Distribution.html
[^2]: To dive into the reason behind the $$\sigma^{-2}$$ as an uninformative prior, check section 2.7 as well.
