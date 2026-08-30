---
title: "You don't like Bayesian Statistics, you like Modeling"
category: ds
---

I'm not saying that you _dislike_ Bayesian Statistics (disclaimer: I like it), I'm saying that many (not all) of the niceties that appear in Bayesian Statistics are actually in parametric statistics. Let us take, for example, the simple linear regression. You can model it in this classical fashion:

$$y_i = \beta \cdot x_i + \alpha + \varepsilon_i$$

We can estimate this paramaters by using the [Ordinary Least Squares estimator](https://en.wikipedia.org/wiki/Ordinary_least_squares) (OLS), which minimises the quantity $$C = \sum_{i=1}{n}(y_i - \beta x_i - \alpha)^2$$, the sum of squares of the differences between $$y_i$$ and the "inference" of $$\hat{\beta} \cdot x_i + \hat{\alpha}$$. The result is well known:

$$\hat{\beta} = \frac{\sum_{i=1}^n(x_i-\bar{x})(y_i-\bar{y})}{\sum_{i=1}^n(x_i-\bar{x})^2}$$

$$\hat{\alpha} = \bar{y} - \hat{\beta}\bar{x}$$

It is relatively simple to prove the [Gauss--Markov theorem](https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem), that says that under some conditions on the errors $$\varepsilon_i$$ (namely that they i. are uncorrelated, ii. have equal variance, and iii. have expectation value of zero) the Ordinary Least Squares estimator is the best linear unbiased estimator (BLUE).

## But can't we model a bit more?

A bit hidden in the first expression is the fact that $$y_i$$ can be split in two parts: the first one depends on $$x_i$$ ($$\beta \cdot x_i + \alpha$$) and the second one is completely random noise ($$\varepsilon_i$$).
So we can rewrite that expression to:

$$y_i = \mu_i + \varepsilon_i$$

$$\mu_i = \beta \cdot x_i + \alpha$$

And now it becomes a bit more clear that we were modeling the relationship between $$y_i$$ and $$x_i$$ through $$\mu_i$$, but not the errors themselves, $$\varepsilon_i$$. A simple way to model it that fulfills the conditions for Gauss--Markov is to say that they come from a zero-centered normal distribution: $$\varepsilon \sim \mathcal{N}(0, \sigma^2)$$. We can rearrange a bit the previous equations into 

$$y_i \sim \mathcal{N}(\mu_i, \sigma^2)$$

$$\mu_i = \beta \cdot x_i + \alpha$$

We modeled explicitly the _sample generation process_: once you know everything there is to know about the relationship between the variables, how are samples actually generated? That's the $$y_i \sim \mathcal(\mu_i, \sigma^2)$$[^1]. From this point onwards you can very simply go down the Bayesian statistics path: pick a prior, sample with MCMC and calculate a posterior for $$\beta$$ and $$\alpha$$. My guess is that since this _sample generation process_ is necessary to start the Bayesian machinery, modeling and Bayesian models start to get tightly coupled in practicioners views[^2]. Something (very crudely simplified) like frequentist -> OLS, bayesian -> modeling.

Let us use the frequentist machinery to estimate $$\alpha$$ and $$\beta$$ from this last set of equations.
There are many possible frequentist estimators to do this, and one of the most extended ones due to its theoretical niceties is the [Maximum Likelihood Estimator](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation) (MLE). In a nutshell, a likelihood function $$\mathcal{L}(\theta | x) = f(\theta; x)$$ measures how compatible the observed data $$x$$ are with the possible parameters $$\theta$$. In our case, the likelihood would look like

$$\mathcal{L}(\theta | x) = \prod_{i=1}^n \frac{1}{\sqrt{2\pi\sigma^2}}\text{exp}\left(-\frac{(y_i - \beta x_i - \alpha)^2}{2\sigma^2}\right)$$

$$\mathcal{L}(\theta | x) = \frac{1}{\sqrt{2\pi\sigma^2}^n}\text{exp}\left(-\frac{\sum_{i=1}^{n}(y_i - \beta x_i - \alpha)^2}{2\sigma^2}\right)$$


From this expression you can see that to maximise the likelihood $$\mathcal{L}$$ we need to maximise the exponent, which is the same as mimimising:

$$\sum_{i=1}^{n}(y_i - \beta x_i - \alpha)^2$$

returning again the OLS estimator.

## What have we won?

After all this, we got to the same result. Even further, the OLS estimator is the BLUE under conditions much less strict than the one we used to find the MLE in this case (remember, we've only shown that the results match when the generation process is normally distributed). Staying in the realm of frequentist statistics, have we achieved anything?

I think that we have gained a lot more interpretation of the problem. And, although this cannot be seen directly in the simple linear regression model, the key is playing with the estimators. The [Ridge regression](https://en.wikipedia.org/wiki/Ridge_regression) or Tikhonov regularisation is usually seen as a penalty term in the OLS. Instead of minimising $$C = \sum_{i=1}{n}(y_i - \beta x_i - \alpha)^2$$, you minimise  $$C' = \sum_{i=1}{n}(y_i - \beta x_i - \alpha)^2 + \lambda \beta^2$$. This new term will penalise large $\beta$ and will therefore have smaller estimates than the OLS. The goal is that, although these estimators will be biased, they can compensate the overal error by [reducing variance](https://en.wikipedia.org/wiki/Bias%E2%80%93variance_tradeoff).

This regression is usually explained in a conceptually very crisp way in the Bayesian framework through the [usage of priors are regularisers](https://en.wikipedia.org/wiki/Ridge_regression#Bayesian_interpretation). In the frequentist framework we could say that instead of using the Maximum Likelihood Estimator we are using an estimator of a modified likelihood $$ \mathcal{L}' = \mathcal{L}(\theta) \cdot \text{exp}(-C * \beta^2) $$.

## The value in modeling

In the vanilla linear regression we analysed we saw that thanks to the model we used our MLE method is easy to interpret, but we needed to constrain the error generation process. OLS is a bit more obscure, but errors can be much more general and still maintain theoretical niceties. This value in modeling is also seen in this Ridge regression case: in OLS it's a very obscure (almost out of the blue) penalisation. Through the likelihood it becomes clearer, and switching to the Bayesian framework, everything fit nicely through the concept of priors.

It is helpful to understand how much of the interpretation (in any given problem) we acheive thanks to modeling and how much is due to the framework we choose. After all, we only have data and models. With the proper translation[^3], results in Bayesian and Frequentist framework should also be the same.


[^1]: Why stop there? We could also model the sampling of $$x_i$$ if we wanted to!
[^2]: If you ask any hardcore Bayesian or any hardcore Frequentist about this, they would certainly be aware and clear that this is not the case. I am talking more about a "sentiment" that I think is floating around.
[^3]: This "proper translation" can be very hard!
