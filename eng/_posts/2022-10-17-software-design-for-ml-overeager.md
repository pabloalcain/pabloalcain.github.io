---
title: "Software engineering for Machine Learning -- Part II: An overeager implementation"
category: eng
---

This is part of a series of posts in which we discuss the challenges and strategies for the productionization of machine learning code. In our [previous post]({% post_url 2022-10-03-software-design-for-ml-motivation %}) we introduced the problem and arrived at the four pillars that the production ML code should have:

1. **Fast** and **easy** exploration
2. **Declarative** and **Intention revealing**
3. Useful **checkpoints**
4. **Seamless** tracking and monitoring

We will do an attempt to productionize the playground code we wrote earlier and show _step by step_ the rationale behind each of our decisions. We will see how some attempts to implement a *production-is-exploration* approach eventually fall back to *deploy as a service* when we disregard the typical exploration workflow. To follow the evolution of the code, you can check the [repository](https://github.com/pabloalcain/software-design-for-lm). Remember that we began with the [original playground file](https://github.com/pabloalcain/software-design-for-ml/tree/e17264e310d8b82e0e79a469a4b3ad05ff136efa)

<script src="https://gist.github.com/pabloalcain/4aaf66b3f7ca3593cf97f6619a2c511b.js"></script>

The first thing we realize with this code is that there is no way in which we can put it into production: the model only leaves within this python file scope. We need to persist it somehow, and for that we choose [`pickle`](https://docs.python.org/3/library/pickle.html). Instead of calculating the accuracy score, once we train the model we save it (check the code at [that commit in the repo](https://github.com/pabloalcain/software-design-for-ml/tree/592b342c84c83da090b3b27d6bebb4a0608e64c7)):

<script src="https://gist.github.com/pabloalcain/8f4814ea1ea4e183267b71bce8a5b27b.js"></script>

We can then use this saved model to predict on a completely new dataset. In this scenario we will simplify this by reading the unseen dataset from disk, but keep in mind that we can use this to serve a model over any API with, for example, [fastAPI](https://fastapi.tiangolo.com/).


<script src="https://gist.github.com/pabloalcain/285417b5928019b2d3c8de9d6dc2fb43.js"></script>

From the _exploration-is-production_ perspective (see [part I]({% post_url 2022-10-03-software-design-for-ml-motivation %}) we could say our work is done: we have a model and it's going into production. However, there are some things that can be improved in this code. Take for example the calls to `pickle`. If eventually we wanted to save it in any other format, we'd have to manually change all these files. And it's something that Data Scientists are usually not interested in. Essentially we are saying that there are *implementation details* being exposed in the code. We know how to solve it -- we abstract the implementation details away into functions! So we create the module `model.py` that will be in charge of knowing how to persist and load the model (check the diff from the previous step in the [repo](https://github.com/pabloalcain/software-design-for-ml/commit/c581cb699db6931a56497d4c6c938dc089a95aa8)):

<script src="https://gist.github.com/pabloalcain/4f106da2835ca4050bb3c368c49b5434.js"></script>

<script src="https://gist.github.com/pabloalcain/46d2384412874ccf6a510ec6d0d2966d.js"></script>

<script src="https://gist.github.com/pabloalcain/e3bdc0c7ab0f972b4be79eaa28f578d1.js"></script>

See that, when creating this new file we have also split the code in two spaces: the file `model.py` is part of a "library" code, while `predict.py` and `train.py` are "application" code. See that now if, for some reason, we decided to change the tool we use to save the model (for example using `joblib` instead of `pickle`), we'd have to change only the library code and the user of the application code would not be impacted by this at all. This difference is important in order to understand how and when we are going to abstract implementation details, and we'll use this distinction throughout this post.

Now we turn our attention to the model fitting itself, this section of the `train.py` file:

<script src="https://gist.github.com/pabloalcain/5564cbb10c54088a9703d8c5a6baaea9.js"></script>

In a similar fashion to what we've done before, we will abstract the fitting of the model into a function. And, spoiler alert: this will turn out badly right away. When we abstract the `fit_model` into a function, we end up with `train.py` file and the `model.py` file looking like this ([diff](https://github.com/pabloalcain/software-design-for-ml/commit/d31652dc81301b2776f3bf190c08d313ca8cb16b)):


<script src="https://gist.github.com/pabloalcain/040ceac5b19768cd695cfcda8410493e.js"></script>


<script src="https://gist.github.com/pabloalcain/c7b76f7679bf47c077319b6f1b54a5a0.js"></script>

See that we have the `_model` as a repeating suffix in all of the functions. As Sandi Metz put it in her wonderful talk [All the Little Things](https://www.youtube.com/watch?v=8bZh5LMaSmE), when we see functions that have a repeating prefix or a repeating suffix, there's a tortured object there that's screaming trying to get out. So we do a very quick code refactor and "upgrade" the collection of functions with `_model` to a wellformed `Model` object, which you can also [check in the repo](https://github.com/pabloalcain/software-design-for-ml/tree/604bff99265be6c98d9ebf2fab89bc006c6f6d5e).

<script src="https://gist.github.com/pabloalcain/49266d30928da163c918a6db5902533b.js"></script>


Emboldened by the success and how clean the `Model` object looks like, we now turn our attention to the dataset loading in the `train.py` file

<script src="https://gist.github.com/pabloalcain/dc8af34879334eed3d2120b3f473fd1d.js"></script>

Similarly, we can build the `Dataset` object that abstracts the information about the `features` and the `target`:

<script src="https://gist.github.com/pabloalcain/133a97523bf56e060cdfdc2b98063d98.js"></script>

We can also leverage this new object to modify slightly the signature of the `fit` method in `Model` and use this new structure:

<script src="https://gist.github.com/pabloalcain/9909d6355c3079138cd9946458242f67.js"></script>

With these small changes, the `train.py` file now is much more concise (check the full code in the [repo](https://github.com/pabloalcain/software-design-for-ml/tree/e9a12a8efee1ab6cc3f05ce01757c4919e557444)):

<script src="https://gist.github.com/pabloalcain/67e5187cde35d3cf0c6b9a7bfae5a532.js"></script>

It is now only a handful of lines, and it is intention-revealing: each of the lines in the application code is clear about what it's doing. But, as we said earlier, this story doesn't end well: immersed in our search for abstracting implementation details, we simply **went too far**.

Remember that one of our goals is to have fast and easy exploration. Suppose that a data scientist in our team wants to try out (even completely offline!) how the model would perform if we select 3 instead of 2 features in the `SelectKBest`. It's OK, we know how to solve it: we get the hardcoded `2` in the `__init__` method and parametrize it away! ([diff](https://github.com/pabloalcain/software-design-for-ml/commit/4a28fd4e9d2373bcb5a2b16c089ccad5b9e75f43))


<script src="https://gist.github.com/pabloalcain/7401282614eaf6692a8ee9a5cd560197.js"></script>

Done! We live to see another day. But that "another day", the data scientists that are exploring the model realize that sometimes they don't want to pick anything, just want to go directly to the logistic regression step. Rushed by the needs of the data scientist to be able to explore this quickly, then, we come up with a maybe questionable (but very widespread in Python) design decision: we will use `None` as a special value in `number_of_selected` so that, in this case, we will skip the selection step ([diff](https://github.com/pabloalcain/software-design-for-ml/commit/3c71fde369a349a49740f3e543b15c11fa458bdf)):


<script src="https://gist.github.com/pabloalcain/571c6208fe0d9fc5ece5e755188d1ddb.js"></script>

Phew! Bullet dodged, we are not super happy with the solution but it works. But right away (remember, the Data Science job here is to explore different solutions) people want to try out what would happen if we don't use a logistic regression as the classifier, and they want to try out a fancy multilayer perceptron. Reluctantly, we do whatever-gets-this-thing-solved, and we come up with this idea ([diff](https://github.com/pabloalcain/software-design-for-ml/commit/14ea162f1ce222b412dfc7e96cd41dd9258f1bd8)):


<script src="https://gist.github.com/pabloalcain/bf4c63431839ccc78c49134ea912b2e0.js"></script>

This was super fast to implement, but it's clearly not good code: we are comparing with a string, raising an error that can be hard to understand, and the user needs to remember what are possible values for the `classifier_type` parameter, among other problems. We can see how this is a slippery slope: we did a lot of modifications to our production code for things that are only going to be part of the exploration step, they might never get into production. The price that we have to pay is both degradation of the quality of production code and also an exploration workflow with a lot of friction. At this point, we are extremely tempted to tell the data scientist to try whatever modification they want on their own and, if it turns out to be production-worthy, we will code it in production, falling back to the *deploy as a service* approach.

We finish this post on a sad note, but the solution is right around the corner. As some tips about how to solve it: see that we are extremely coupled with the original solution and that we actually don't know what model we want. In the following posts, we will provide an alternative path to solve this problem.
