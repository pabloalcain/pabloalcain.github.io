---
title: "Python and C interaction: Part III - Advanced use of Ctypes"
category: hpc 
tags: [python, ctypes, python-c]
---

We will discuss in this topic a completely Pythonic way to communicate C and Python and make the end result completely Object Oriented, not usually explained.

So far, we have discussed about how to connect Python and C through [ctypes](https://docs.python.org/2/library/ctypes.html) to speed up Python code[^1].
The main goal was not only to be able to run C code, but also to do so transparently.
This way, we could call C code and wrap it properly so the library user would never know she or he is actually using C code.
Both with values and references we were able to do so, but we actually accomplished the transparency of Python *functions*.
We know that, though Python is multi-paradigm, its use is heavily focused in Object Oriented Programming.
[Wouldn't it be nice](https://www.youtube.com/watch?v=lD4sxxoJGkA) if we could somehow mimic the object oriented behaviour through ctypes?

## Structures
Among the many types that ctypes exposes to Python, it exposes the structure.
So, let's say we have a `Rectangle` structure in C and a functions that takes a rectangle as an argument as follows:

{% highlight c %}
{% include_relative ctypes-struct/rectangle.c %}
{% endhighlight %}
and build it as a dynamic library
```
$ gcc -c -fPIC rectangle.c
$ gcc -shared rectangle.o -o libgeometry.so 
```

A C structure in Python is an object that inherits from the `Structure` in ctypes, and the variables of the structure (in this case, `height` and `width`) are called `_fields_` in the ctypes structure.
So a minimal Python library can be:

{% highlight python %}
{% include_relative ctypes-struct/geometry_minimal.py %}
{% endhighlight %}
were we encapsulated the area function from the C library.

We can use now this library completely seamlessly from python:
```python
>>> import geometry_minimal
>>> r = geometry_minimal.Rectangle()
>>> r.width = 10
>>> r.height = 30
>>> geometry_minimal.area(r)
300.0
```
## Object Oriented Python and C through Ctypes

### Memory Layout
When we set the fields of the ctypes structure, we have to be very cautious: the order has to be the same as the order in the original C structure.
Studying the reason behind this, we will answer an actual larger question: Why *on Earth* does this work?
First of all: a structure in C is actually a fancy way to name relative memory positions[^3].
In this case, `height` is a float (that takes 4 bytes) that is located 0 bytes relative to the memory location of `Rectangle`.
Similarly, `width` is a float that is located 4 bytes relative to the memory location of `Rectangle` (since the first 4 bytes are taken by `height`)[^2].
So actually the C function `area` just takes the first 4 bytes starting from `rect` and the second 4 bytes starting from `rect`, interpret the data as floats and then multiply each other.
How do we take advantage of this behaviour from Python?
When we define a Python class inheriting from a C structure, we are saying that the first bytes will be occupied by the `_fields_` and the class itself.
Every other method or attribute we add, will be added below.
So the C function `area`, when going to the locations we named earlier, will actually find `height` and `width`.
This is, obviously, as long as we put both the C structure and the ctypes fields in the same order.


### Implementation of the Library
If we modify the Python class that inherits from the ctypes structure adding methods or new attributes, the first bytes will remain unchanged.
This means that, for the C functions, adding methods and attributes will not change the structure (at least, in the memory positions that were originally available in the C structure).
This is what we will use in order to completely encapsulate the C structure as a Python object.
As a first example, we can add a simple `__init__` function[^4].
But the most interesting example is adding methods that were originally C functions.
From the explanation above, it is quite evident that we can encapsulate the C `area` function as a method of the Python object, and the argument that we will use to call the `area` function has to be the structure itself.
So now we can create a more advanced Python library:

{% highlight python %}
{% include_relative ctypes-struct/geometry.py %}
{% endhighlight %}

How do we use this library from Python?

```python
>>> import geometry
>>> r = geometry.Rectangle(10, 20)
>>> r.area()
200.0
>>> r.width = 400
>>> r.area()
4000.0
```

And, finally, the C structure and functions are completely encapsulated.
For the end user, there is no difference between this library and a pure Python library, but we are actually running C code.

## Conclusions

We were able to encapsulate completely the behaviour of C functions that act on structures as methods of a Python object.
Therefire, we have a completely object oriented code, that looks completely pythonic, yet does, in the background, all its calculations in C.


[^1]: Remember, we are not actually speeding up Python code, we are calling a much faster C code from Python.

[^2]: We cannot generally add directly the sizes of the elements, since [data alignment](https://en.wikipedia.org/wiki/Data_structure_alignment#Typical_alignment_of_C_structs_on_x86) is slightly more tricky.

[^3]: Actually, since a structure is a memory position and these are integers, it is not *technically* a requisite to add the `argtype` as a `C.Structure`.

[^4]: There is a default `__init__` function for the ctypes Structure, that initializes the values of the fields to the arguments passed in the constructor.
