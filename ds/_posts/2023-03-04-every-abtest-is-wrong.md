---
title: "Every AB test is wrong"
category: ds
---

The industry, through concepts like agility and Lean Startups, has taken on rapidly the practice of performing AB
tests. In a nutshell, the AB tests are controlled scenarios that help us decide which of two alternatives is better.
One approach to make this decision is considering that we have a current state of a system and asking the question: _what
would happen if we inflict a treatment?_ The AB test way of answering the question is to split the population randomly
in two groups (A and B, or _control_ and _treatment_), measure both and then decide. But does an AB test really answer
our question? In this post, we will see the core assumptions of AB tests into two dimensions (time and space) and whether
they hold or not, following a real-life scenario.

In 2022, Twitter started the release of
[Twitter Circles](https://www.theverge.com/2022/5/3/23055515/twitter-circle-close-friends-private-tweets-150-people).
The main idea of Circles was to segregate the audience of tweets, allowing someone to decide whether they wanted the
tweet to be "for everyone" or for a handpicked audience known as "circle", in a similar fashion to the Close Friends on
Instagram. We don't know if the Circles functionality was actually AB-tested or not (although its rollout was
definitely staged, meaning not everyone got it at the same time), but let's try to see the challenges that would arise
if we wanted to.

## Time Stability

### Novelty Effect

The effect of seeing a change for the first time is massive. Suppose that the whole interface of the news
site you check every morning changed all of a sudden: you'd probably feel lost, not finding the sections you actually
want to see, missclicking a lot. It will take some time for you to get used to the novelty. Similarly, in the case of
Twitter Circles, you might receive the novel feature with an enthusiasm that won't last. But we are not interested in
these transient scenarios, since they don't relate purely to the treatment effect: they also relate to the effect
of *having done a treatment*. To measure the treatment effect itself we'd need to wait until this novelty effect
fades out, but this is both hard to determine (because of the typical variance that comes with the metrics) and can take
a lot of precious time that we might not have. Approaches that allocate the population dynamically to different treatments (like multi-armed bandits) are very exposed to this issue.

### Time extrapolation

Even if you wait until the novelty effect fades out, you don't know what the future holds. If you do an AB test during a
period of time T and find that B is better than A (according to some significance criteria) you know only that: that B
was better than A during T, and the future can be very different from T. Take, for example, seasonality: although you
can
probably sometimes account for weekly or even monthly seasonality, you won't be able to do so for every AB test if you
want to be fast-paced. Even beyond seasonality, you can have some events (like holidays season) that are very relevant
for the business but during which you cannot test. What if B is *much worse* than A during that very important event?
There is, unfortunately, no way to know. And finally, you have simply environmental conditions: people in the future can
behave in a multitude of ways and, in some of them, B won't perform better than A. The bottom line is that you won't be able to
*know* what will happen between B and A in the future.

## Spatial Stability

When we try different settings for populations A and B we want both of them to be representative of the whole
population: the effect on any of them represents the effect on every possible user. This is why A and B are chosen
randomly, but it's *not enough*. Consider an AB test in which we want to test the effect of circles. Twitter is a highly
cohesive social network, in which interactions drive the behavior of users.

If you give users in population B the possibility of using circles, how do you handle the interaction with group A?
There is no solution to this problem: if you allow people in group A to see that group B is using circles, then group A
would *not* be representative of "what would happen if nobody had circles?". On the other hand, if you don't allow
people in group A to see the tweets from B's circles, then it's group B that wouldn't be representative. Of course, you
can do some clever manipulation and try to choose groups A and B so that the interactions between them are minimized and
therefore the effect is diminished. But it won't go away, and it's very hard to model. This is known in the literature
as Stable Unit Treatment Validity Assumption (SUTVA) violation and, whenever people can communicate with each other
beyond your application (fortunately always) you are exposed to it. Even if your treatment is a change in the background
color of your webpage, someone from group B can call someone from group A and tell them: "Oh, I really dislike the new
color" and you're done.

## What is the impact?

We all know that AB tests come with uncertainty, and we do our best to measure it (through p-values, significance
levels, expected loss, and alike). But the main consequence of these effects is uncertainty of the worst kind: the one
that is
not quantifiable. All of our uncertainty measurements are built on top of these shaky grounds that we have already
mentioned. And as if this was not
enough, this variance also helps inflate our AB tests result. Suppose that there was no effect between A and B other
than seasonality: on Jan-Jun B performs 2% better than A, and on Jul-Dec A performs 2% better than B (in our target KPI). In
January we do an AB test and measure that B is definitely better than A, so we roll out B. If by the end of the year, we
were to measure the impact of our AB tests (for example, suppose that we froze a portion of the traffic with the
configuration of the beginning of the year), we'll find that instead of improving by 2% it decreased by the same amount!
Our AB tests effect would appear to be inflated in 4% and would be actually inflated in 2%.

As a general rule, every time we add variance to a metric that we are selecting, we will introduce selection bias. This
is known as the [winner's curse](https://en.wikipedia.org/wiki/Winner%27s_curse).

## So... should we stop doing AB tests?

These unavoidable problems stack the odds against us, they make it harder for us to be confident in our results. But
that's OK: we don't do AB tests because they will give us absolute confidence that one model is better than the other,
but because they give us more confidence than choosing randomly. In the parts in which we have control, we have to be as
rigorous as possible, and this implies (most of the time) doing AB tests. But their pitfalls are there, and if we
cannot avoid them we need to find a way to measure them or, at least, their impact. Even if we are confident that all of
our statistical techniques are correct, doing a meta-analysis on AB tests, along with techniques
like long-term hold-out groups (see, for
example, [this post from Pinterest eng](https://medium.com/pinterest-engineering/how-holdout-groups-drive-sustainable-growth-35a4786c3801))
can help us see how good our AB tests are and measure our exposure to these problems. Sure, all experiments are wrong.
But some are useful.
