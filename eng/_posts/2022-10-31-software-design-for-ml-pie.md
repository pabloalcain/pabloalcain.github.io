---
title: "Software engineering for Machine Learning -- Part III: Exploration is production"
category: eng
---


This is part of a series of posts in which we discuss the challenges and strategies for the productionization of machine learning code. In our [previous post]({% post_url 2022-10-17-software-design-for-ml-overeager %})
Reflecting on how we got here, it looks like we've been always one step behind the data scientist ideas. We are extremely coupled with the original solution and we realize that we don't know exactly what model we want. Our main mistake was instantiating the `classifier` in the
