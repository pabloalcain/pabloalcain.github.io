---
title: "Python and C interaction: Part I - An Introduction"
category: hpc
---

Too much is said of
[Python as a glue](https://www.google.com.ar/search?q=python+as+a+glue).
Although many Python advocates use this to value Python over other
languages, the truth is that any high-level scripting language (think
of perl, ruby or incipient Julia). However, and despite the Global
Interpreter Lock,
[Python's Hardest Problem](https://jeffknupp.com/blog/2012/03/31/pythons-hardest-problem/),
Python (especially v2.7+) is the main scripting language in scientific
applications due mostly to the high availiability of scientific
libraries: NumPy, SciPy, SciKitLearn, *et al*. The advantage over a
compiled language becomes evident once we compare a simple code for
calculating averages in Python and in C:

## Python
{% highlight python %}
{% include_relative python-c/add_numbers.py %}
{% endhighlight %}

## C
{% highlight c %}
{% include_relative python-c/add_numbers.c %}
{% endhighlight %}

Not only the Python syntax is much cleaner, but also keep in mind that
the C code has to be compiled previous to execution, say to
`add_numbers.e`. The question now is, why do we use C then? The answer
is obvious: both codes do the exact same thing, but while the Python
code takes `8.047 s` [^1], the C code takes `0.284 s`: 28 times
faster[^2]. So, how can we overcome these issues? Anyone who has used
NumPy, knows that this is problem goes exactly to its
locker. Let's take a look at the Python code with NumPy:

## Python (with NumPy)
{% highlight python %}
{% include_relative python-c/add_numbers_fast.py %}
{% endhighlight %}

With this new code we get a time of `0.266 s`, comparable with
C. However, we also know that numpy is quite strict: we have to
use vectors and try to write our implementation so we use only NumPy
functions. Hence, we've lost Python versatility. The question is then:
can we get the versatility of the scripting language and the speed of
a compiled language? There are two ways to do this:

1. **We implement a scripting language in C:** Much as Python is
   written in C, we can write our program in C and also code a
   scripting language surrounding it. The main problem is that you
   have to reimplement a lot of things in C that are not time critical
   and might end up with a quite shaky and not straightforward
   scripting language. A good example of a rewrite of a full fledged
   scripting language from C code is
   [LAMMPS](http://lammps.sandia.gov/).

2. **We write Python and C code separately and we link them:** If
   every language deep down has to be machine code, we *have to* be
   able to communicate any languages we want. In this case, we can
   write **a)** Python code; **b)** C code; and **c)** a C/Python API
   that takes care of the communication. We only write the time
   consuming part in C and we can use the Python flexibility,
   scriptability, duck-typability and
   everything-that-is-good-in-this-worldability. The infamous NumPy
   library actually does this in order to get its speedup[^3].

We will focus, of course in this last option. But the C/Python API
itself has many sub-choices:

1. **Write the whole module in C, Python-like:** If Python was written
   in C, we can write any Python module in C. This is, for example,
   the [`Python.h` API](https://docs.python.org/2/c-api/). I have done
   this a couple of times, and can assure it can be rather painful,
   since you have to rewrite many of the Python parsing in C, and also
   take into account memory management. The biggest advantage,
   however, is that you write the C code that is going to be executed,
   and consequently you can make fine tuning choices that can be
   critical in performance.
   
2. **Write the module in Python and generate C code from it:** This is
   the [Cython](http://cython.org/) way. As you can see from the
   examples in the webpage, we write pure Python code, and then
   convert it to C code This translation tween langauges of similar
   level languages is call *transpilation* (portmanteau of translation
   and compilation). Cython is, therefore, a
   *transpiler*[^4]. Although this looks very good on paper, the truth
   is that, as in any compiler, a lot of work needs to be done in
   order to get good optimizations[^5]. The fine tuning you could do
   with the Python C-API now cannot be done.
   
3. **Write the module in C and interface it with Python:** If we could
   make Python aware of the crude, low-level C data structures (`int`,
   `float`), we can call the functions from C shared library with
   them. This is the idea behind
   [ctypes](https://docs.python.org/2/library/ctypes.html). You write
   your C function as you would if you were only writing C code, but
   then call it from Python with the proper data types. This way, we
   can write C code as in case **1**, but it has the great advantage
   that the interface and memory management is done in Python.
   
I would like to discuss briefly option **2** Cython and other close
relatives like [Numba](http://numba.pydata.org/): although they can
give relatively good speedups with very little work from already
written Python code, they do not go *the extra mile*. They are
obviously the choice if you know nothing of C. Or, if you are looking to
get that creeping Python script to take 10 minutes instead of waiting
an hour, maybe give them a chance first. But if you are writing with
HPC in mind from the beginning, they will definitely fall short[^6].

Options **1** and **3** are very similar and, in my opinion, option
**3** actually supersedes option **1**. This is just an introduction
and aims to give a wide view of the possibilities. In part II we
will show some examples of **ctypes** and its basic usage (nothing
that cannot be found just searching online). Part III will be
dedicated to an advanced and not often discussed use.


[^1]: Obviously all performance measures are highly hardware dependent.

[^2]: This means that a one hour simulation takes one day if we use
    Python. While 28x is obviously a huge boost, I remember discussing
    once with a (*really good*) colleague, who did not work on HPC,
    about 2x-5x speedups. I am still quite amazed by the fact that he
    was not amazed by a 5x speedup. The point of this being that you
    have to think whether its worth it to perform a full-fledged
    optimization.

[^3]: Bonus points: since you are actually running a shared library,
    you release the Global Interpreter Lock, and in the running shared
    library you can thread.


[^4]: We can argue whether it's a *transpiler* or a compiler. But it's
    not worth it

[^5]: The same goes for writing C code. No matter how good the
    compiler is, you won't get better performance than good, hand-written
    assembly code.

[^6]: [F2PY](http://docs.scipy.org/doc/numpy-dev/f2py/) actually does
    the inverse. From pure FORTRAN code, it automatically generates
    the Python interface; therefore we get the fine tuning in the
    compiled language and the eventually non-optimized autogenerated
    code is on the already slow, not time critical Python side.
