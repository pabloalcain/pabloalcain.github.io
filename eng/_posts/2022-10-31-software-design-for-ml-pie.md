---
title: "Software engineering for Machine Learning -- Part III: Production-is-exploration"
category: eng
---


This is part of a series of posts in which we discuss the challenges and strategies for the productionization of machine learning code. If you haven't, make sure to check [part I]({% post_url 2022-10-03-software-design-for-ml-motivation %}) and [part II]({% post_url 2022-10-17-software-design-for-ml-overeager %}) before diving into this one. In part II we got an exploration code and started working on it to get to production, splitting the code into "application" and "library". While trying to do this, we ended up with a code that was too brittle and hard to modify in typical exploration settings. You can check on that specific commit on the repo what the [`model.py`](https://github.com/pabloalcain/software-design-for-ml/blob/14ea162f1ce222b412dfc7e96cd41dd9258f1bd8/model.py) file ended looking like, which tempted us to fall back to the *deploy as a service* approach.

Reflecting on how we got there, we've been always one step behind the data scientist's ideas, chasing them one solution at a time. Let's recall, just for context, what the `model.py` file looked like when we first started down this path:

<script src="https://gist.github.com/pabloalcain/49266d30928da163c918a6db5902533b.js"></script>

The problem is that we are extremely coupled to the specific solution we are setting inside the `Model` constructor. Fortunately, we know the solution to this problem from Software Designs principles: the I in SOLID is for dependency injection, which is (ultimately) just a fancy name for *parametrization*. We want to parametrize the classifier altogether:

<script src="https://gist.github.com/pabloalcain/e54830eca4cde63540159ea977ee2eb6.js"></script>

Two things to note here: first, we call the `classifier` the "backend model". This comes with a realization of what we are building on the "library" code: it is a specific interface to scikit learn classifiers. The other thing is that the `fit` and the `predict` model are essentially delegations to the backend. We use this delegation to implement a well-known pattern in object oriented design: the [*strategy*](https://en.wikipedia.org/wiki/Strategy_pattern) pattern. The `train.py` file has to be modified as well to take into account this change

<script src="https://gist.github.com/pabloalcain/dc916c73f9c5d4e2556eb0dd6860e709.js"></script>

Through dependency injection, we have effectively decoupled the `Model` object from the classifier solution itself and crawled out of the hole we dug for ourselves.

Let's go for another proposed modification and see how we can generalize our technique. Suppose that now we want to experiment on what would happen if we were to remove all instances with very long sepals, and keep only those with sepal length less than 5.0. It looks like doing a dependency injection might help (for example, we could load the dataset with `pandas`, do the modifications we want and then inject it into the dataset during the construction), but we can pause a bit and reflect on the approach we have just taken for the `Model`.

When doing the dependency injection, one of the side effects was to _expose_ the `scikit learn` code that was on the "library" space to the "application" space, and all that belongs to the "application" space is easy to modify quickly (remember that the application space is the area of influence for the DS code modifications). Exposing this known library to the DS is what simplifies the exploration process. The price we are paying for it will become clear when we apply this concept to the `Dataset` object (see [commit](https://github.com/pabloalcain/software-design-for-ml/tree/31478a12d93285689099841fa1b7b1d1cf232c73)). The `dataset.py` and `train.py` files now look like this:

<script src="https://gist.github.com/pabloalcain/db67f7c029548c9b9cb0c2733d96a88a.js"></script>

<script src="https://gist.github.com/pabloalcain/35197721b5450964c3e584f58207e84e.js"></script>

There are some quirks in the implementation, but let's analyze how our abstractions affect the exploration workflow. Of all the possible definitions of "abstraction", my favorite is the one by Joel Spolsky: _an abstraction is a simplification of something much more complicated that is going on under the covers_. I like this definition because clearly shows the subjective nature of an abstraction: different people will regard different things as "too complicated" that should belong "under the covers". When we regarded the model itself as something that belongs under the covers (in our terminology, the "library" code), the exploration phase was a force that consistently tried to uncover the implementation. It makes total sense: while from a software design perspective we can say "what matters is that we are _classifying_, the way we do it is an implementation detail", from the DS perspective the implementation is everything but a detail: it's the most important part.

In the same [article](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/) (and please, oh please! read it if you haven't yet) in which Spolsky defines the abstraction, he coined the Law of Leaky Abstractions: _all non-trivial abstractions, to some degree, are leaky_. While this is a general law, and Spolsky lays out several examples, in this case the situation is even more extreme: we have a constant drive (the exploration) to leak the abstractions. Our strategy for the *production-is-exploration* approach is to own this reality and instead of fighting the leakage, we try to channel it. We know that the abstractions will leak sooner rather than later, so we choose how to. This is the price we are paying: by leaking the abstractions the API will be too wide and relatively shallow when interfacing with `pandas`, `scikit-learn` or whichever backend library we use.

Let's see how this approach allows us to fulfill our four pillars:

### Fast and easy exploration

We have already seen how easy it is to change the classifier itself. Let's try out now our current challenge: what we have now is production code and we want to explore training the model without flowers with long sepals. The implementation is trivial for the data scientist, modifying only application code:

<script src="https://gist.github.com/pabloalcain/988d45f5661f71f2508fc387510a905f.js"></script>

Not only for this change but for any other one they want to make, they will be able to use all the knowledge they already have of libraries that are well known and established in the domain.

### Declarative and intention-revealing

After the exploration, the DS decides to put this into production. When the code gets to production, we want it to be intention-revealing and probably the line we have just added is too verbose and cumbersome. Therefore, we reify the implementation of the long sepal filter to the `Dataset` object:

<script src="https://gist.github.com/pabloalcain/ad2bc96a4130e7cd1406411d9149124e.js"></script>

<script src="https://gist.github.com/pabloalcain/7e73c56ffbf7b25a8eccc592eee71a8a.js"></script>

### Sensible checkpoints

Along this development, we rolled back the interfaces of our methods. Instead of using our own class `Dataset` to fit the model, we decided to use `pandas` dataframes directly. This is a somewhat controversial decision that unlocks needed flexibility in the checkpoints: we can bring to the model any `pandas` dataframe created through any means, even loading a crude CSV file from disk. This is a slippery slope, and probably the decision depends both on the team and the problem we are solving. We should, at least, consider exposing to the application code "basic" types[^1] instead of custom abstractions. But be weary of overdoing it and falling into the [**Primitive Obsession**](https://wiki.c2.com/?PrimitiveObsession) antipattern.

### Seamless tracking and monitoring

Being an intermediate layer between the application and the backend, the "library" space is a perfect place to put the logging code and other monitoring hooks, for example:

<script src="https://gist.github.com/pabloalcain/488541478bb3d9947cd3985953aeeab1.js"></script>

<script src="https://gist.github.com/pabloalcain/63fae4d7a8e6e7c95eef30f242bfcebd.js"></script>

---

In the *production-is-exploration* approach, we used that **what constitutes an implementation detail lies in the eye of the beholder**, and leverage this concept to allow flexibility in the user experience by **allowing the application code to speak the language of the developer**. We came to terms with the idea that abstractions will leak and, instead of fighting it, we channel it and used it to our advantage. While we are aware of some of the challenges that come with this solution, in some cases the benefits might outweigh them: the removal of code duplication and rewriting and the ease of exploring and modifying based on well-known and maintained production code relieves a lot of the "maintenance" pressure that developers typically have in the "deploy as a service" and in the "exploration is production" setting.


[^1]: Basic types in this context include `pandas` dataframes and alike
