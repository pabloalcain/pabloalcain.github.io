---
title: "Software engineering for Machine Learning -- Part I: Motivation"
category: eng
---

Machine Learning and Data Science code has its own set of challenges and peculiarities. When we write code to be used by Data Scientists or Machine Learning Developers we have to keep in mind constantly that every abstraction we use has to a) be compatible with a fast and easy exploration playground; b) allow for sensible checkpoints and optimizations; c) implement in a declarative fashion repeated queries and functions; and d) provide an abstraction level over all of the production code so it can be tracked and monitored seamlessly.

In this series of blog posts we will provide general guidelines to approach this problem from a software design perspective, defining what should our entities be, how deep should our abstraction go, and how to avoid some usual design pitfalls.

We will study specifically a very well-known problem from multilabel classification: the [iris species problem](https://www.kaggle.com/datasets/uciml/iris). Our goal is to be able to classify different species of iris flowers (versicolor, setosa, and virginica) from the length and width of both the sepal and the petal. So let's assume we begin with a dataset saved as a CSV file and we want to use [scikit learn](https://scikit-learn.org/) and [pandas](https://pandas.pydata.org/) to classify the flowers. The first approach to this problem could be to analyze the data in what we will call a _playground_, an offline analysis of the dataset. This is, for example, a solution to the classification problem through a pipeline: we first select the 2 best features (according to the f-value, as is the default behavior in scikit learn) and then we use a logistic regression as the classifier step. We fit this pipeline to the target and calculate the accuracy of the predictions:

<figure>
  <img
  style="width:60%"
  src="{{site.url}}/assets/posts/software-design-for-ml/iris_eda.png"
  alt="Iris features distributions"/>
  <figcaption>Iris features distribution</figcaption>
</figure>

<script src="https://gist.github.com/pabloalcain/4aaf66b3f7ca3593cf97f6619a2c511b.js"></script>

Eventually, we will want to put this model into production. This involves a lot of different stuff, among them: data preparation, model deployment, serving capabilities, infrastructure provisioning, monitoring, and model tracking. There is a very interesting and well-known paper (although maybe a bit dated now) from 2015 about different challenges in all of these, [Hidden Technical Debt in Machine Learning Systems](https://proceedings.neurips.cc/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf). The main thesis of the paper is that the Machine Learning code itself, although fundamental, is a very small part of a robust ML system. 

<figure>
  <img src="{{site.url}}/assets/posts/software-design-for-ml/htdiml.png" alt="Hidden Technical Debt in ML Systems"/>
  <figcaption>Hidden Technical Debt in ML Systems</figcaption>
</figure>


Keeping this general landscape in mind, we will focus now on what happens with the machine learning code itself. In our case, the playground code we wrote earlier. How does it go into production?

### Exploration-is-production

One very extended approach is what we will call _exploration-is-production_. In this approach, the Data Scientist has direct access to production code, and she usually moves the exploration code to the production environment. If a next data scientist comes, he will have to read the production code and understand it in order to do some changes. This scenario is fast for exploration and productionization, but it's extremely fragile: naturally production and exploration are different tasks and have different requirements.

Suppose, for example, we wanted to log things on production: all of the logging will end up polluting the exploration code as well. Code quality can also suffer a lot since usually exploration is done without readability and modularity in mind. Therefore the production space very quickly ends up having hard-to-understand, duplicated, and non-informative code. This, as we said, makes total sense: it's not the task of the DS to write _good_ code (for whatever that means) and they are not trained to do that (and it's OK; probably they shouldn't).

<figure>
  <img src="{{site.url}}/assets/posts/software-design-for-ml/eip.png" alt="Exploration-is-production approach"/>
  <figcaption>Exploration-is-production approach</figcaption>
</figure>

### Deploy as a Service

On the other extreme, we attempt to solve the shortcomings of this approach by putting a barrier between the Data Scientists and production code, the _Machine Learning Engineering_ team. The data scientist focuses on the exploration and development of models conceptually and we remove the burden of code quality and deploy to the MLE. The cost of this approach is having more people on the team and exposing the solution to "translation" bugs, in which the production code doesn't do exactly what the exploration code does. This makes the production code fundamentally **unreliable**. On the bright side, (at first at least) it makes it easier for the DS to develop code, and apparently decouples them from production.

However, keep in mind that the moment a new DS (or even the same one) wants to modify or even analyze production code, they will have to understand code that was written by an engineer, focusing on the code and not on the model. It also isolates knowledge: some implementation details done by the engineers will not mimic completely the intention in the production code. Very quickly we end up having (at least) two code bases being developed in parallel, and no reliable source of truth.

<figure>
  <img src="{{site.url}}/assets/posts/software-design-for-ml/daas.png" alt="Deploy as a Service approach"/>
  <figcaption>Deploy as a Service approach</figcaption>
</figure>

## What do we want from our solution?

The attempt to decouple data scientists from production code generates a lot of problems that can be solved in many different ways (having engineers more familiar with the models themselves, helping data scientists understand production code, etc). We will propose here a solution in the realm of Software Design techniques that attempts to simplify this productionization. For it, we will focus on four pillars:

1\. **Fast** and **easy** exploration: the nature of the machine learning models is speculative and they change way too often. We need to be sure that data scientists are able to work with new ideas starting from 100% reliable production code.

2\. **Declarative** and **Intention revealing**: as Martin Fowler put it in [CodeAsDocumentation](https://martinfowler.com/bliki/CodeAsDocumentation.html), the code is the only source of documentation that is "sufficiently detailed and precise to act in that role". This, of course, doesn't mean that we don't have to write any documentation, rather that we have to seize the opportunity of the production code to act as documentation.

3\. Useful **checkpoints**: if we have a workflow with many different steps in production (like feature extraction, transformation, model training), we want to be able to hook into and out of this workflow in a way in which we can reuse previous or future steps. Sometimes this reutilization is fundamental for fast exploration since the steps can take a very long time to run.

<figure>
  <img src="{{site.url}}/assets/posts/software-design-for-ml/checkpoints.png" alt="Hooking into and out of the production process in specific checkpoints"/>
  <figcaption>Hooking into and out of the production process in specific checkpoints</figcaption>
</figure>

4\. **Seamless** tracking and monitoring: we have to track the goal, but we should not track it in a way that pollutes the declarative and intention revealing code we have just described. Suppose, for example, we take the playground code we wrote in the beginning and add to it tens of lines that call functions that are pure logging: it will be very hard for us to find, among all of these lines, where is actually the **model**. And in the playground, we are usually not interested in the same loggings we want in production. 

With these four pillars, we will see in the following posts how to write production code that also serves as exploration, subverting the *exploration-is-production* idea into what we will call *production-is-exploration*. 

