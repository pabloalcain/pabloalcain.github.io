---
title: "Calculation of the structure factor in computer simulations"
category: physics
---

## Formal definition of the structure factor

We will follow here roughly the derivation by Egami and Billinge in
Ref.[^1], although it can be easily found in many textbooks. We
begin with the *sample scattering amplitude*

$$
\begin{equation}
\Psi(\mathbf{Q}) = \frac{1}{\langle b\rangle} \sum_i b_i \text{e}^{i\mathbf{Q}\cdot\mathbf{R}_i}
\end{equation}
$$

with $$\mathbf{Q}$$ the diffraction vector or momentum
transfer. $$\mathbf{R}_i$$ is the position of the particle $$i$$, and
$$\langle b\rangle$$ is the average of the scattering amplitude of
each particle in the vacuum $$b_i$$. From this moment on, we will
consider that all of the atoms are of the same species, $$b_i = b$$.

From $$\Psi(\mathbf{Q})$$ we define the structure factor
$$S(\mathbf{Q})$$ as[^2]:

$$
\begin{equation}
S(\mathbf{Q}) = \frac{1}{N} |\Psi(\mathbf{Q})|^2
\end{equation}
$$

What follows *immediately* from this expression is that the
structure function must be always positive for every value of
$$\mathbf{Q}$$. We can expand the scattering amplitude and use $$|z| =
z\cdot z^*$$ and, if all the atoms are of the same type,

$$
\begin{align}
    S(\mathbf{Q}) &= \frac{1}{N} \left( \sum_i \text{e}^{i\mathbf{Q}\cdot\mathbf{R}_i} \right)
    \left( \sum_j \text{e}^{-i\mathbf{Q}\cdot\mathbf{R}_j} \right)\\
    &= \frac{1}{N} \sum_{i, j} \text{e}^{i\mathbf{Q}\cdot(\mathbf{R}_i-\mathbf{R}_j)}\\
    &= \frac{1}{N} \left[N + \sum_{i < j}
    \left(\text{e}^{i\mathbf{Q}\cdot(\mathbf{R}_i-\mathbf{R}_j)} +
    \text{e}^{i\mathbf{Q}\cdot(\mathbf{R}_i-\mathbf{R}_j)}\right)\right]\\
    &= 1 + \frac{2}{N}\sum_{i < j}\cos{\mathbf{Q}\cdot\mathbf{R}_{ij}}
\end{align}
$$
  
## Powder average: Debye formula

Usually we are interested in the *powder average* of the structure
factor. This is the structure factor averaged for every possible
orientation of the diffraction vector - because in a powder we have
a lot of structures randomly oriented. We calculate therefore

$$
\begin{equation}
  S(q) = \frac{1}{4\pi}\int\text{d}\phi\text{d}(\cos\theta) S(\mathbf{Q})
\end{equation}
$$

This integral can be performed easily if we put the $$z$$ axis along
with the direction of $$\mathbf{Q}$$ and perform the integration
rotating the distances $$\mathbf{R}_{ij}$$

$$
  \begin{align}
  S(q) &= \frac{1}{4\pi}\int\text{d}\phi\text{d}(\cos\theta)
          \left[1 + 2\sum_{i < j}\cos\left(q\,r_{ij}\,\cos\theta\right)\right]\\
       &= 1 + \frac{1}{2N}\int\text{d}(\cos\theta)
          2\sum_{i < j}\cos\left(q\,r_{ij}\,\cos\theta\right)\\
       &= 1 + \frac{1}{2N} 2 \sum_{i < j} \left.\frac{\sin(q\,r_{ij}u)}{q\,r_{ij}}\right|_{u=-1}^{u=1}\\
       &= 1 + \frac{2}{N} \sum_{i < j}\frac{\sin(q\,r_{ij})}{q\,r_{ij}}
  \end{align}
$$

This is the famous Debye formula and, since its the average of an
always positive quantity, it must be *always positive*.

## Computer simulation

One of the most usual problems when we model and study systems in
computer simulations is that we don't have actual *infinite*
systems. We do, however, use the periodic boundary conditions (PBC)
usually to emulate the behavior of infinite systems. With the
periodic boundary conditions we usually use the minimum image
convention: for the distance between particle $$i$$ and $$j$$, we use
whichever is the closest, considering all the possible positions
through the boundaries. We calculate for a very simple test case (a
simple cubic 3D lattice with 4x4x4=64 atoms) the structure factor
with that prescription
    
![Structure Factor calculated with PBC](/assets/posts/structure-factor/ssf_pbc.png)

A surprising result! We insisted several times that the structure
factor should be always positive, yet we get, using *the very same
definition*, a negative structure factor for wavenumbers
near 10. Where did these negative values come from? From the
construction that used to help us a lot, the minimum image
convention. The pair distance now isn't always $$r_{ij} = r_j - r_i$$,
but depends on whether we use the original particles or their
images. Therefore, this "new" structure factor isn't the product of
two conjugate complex numbers[^3]. What if we avoid the
periodic boundary conditions? We have a comparision of the structure
factor with and without boundary conditions (i. e., with the 64 atoms
in a void):

![Comparison of structure factor with and without PBC](/assets/posts/structure-factor/ssf_comp.png)

This shows that the structure factor, when we use its definition
*without minimum image convention*, is (as expected) always
positive.

## A bit further

We can also use the pair distribution function and calculate the
structure factor as the Fourier Transform. But keep in mind that if
you calculate the pair distribution function with PBC, when you get
the structure factor related to it you *might* get negative
numbers.

## How can we simulate an infinite medium?

The question then, remains: how can we simulate an infinite medium
when calculating structure factor? The first answer is that it is not
that obvious that we would actually need this *infinite* medium, since
the periodic images of the cell would be aligned in a crystal that
might interfere with the structure within the cell --- the one we
actually do want to study. However, a couple of replicas should be
enough to smear out some of the finite size effects. One of the
possibilities is to replicate explicitly the box, creating the
particles in the neighboring cells by duplication of the original
ones. This, though, implies a calculation much harder, since the sum
is over $$N^2$$ particles, and replicating only one cell right and left
in each direction would imply a computational time of $$(3^3\cdot N)^2
\approx 700\cdot N^2$$. In general, the complexity $$\mathcal{O}(N^2)$$
makes structure factor calculation very expensive for large systems.

There is an alternative to add the boundary conditions. We begin with
the definition of the *sample scattering amplitude*, but writing explicitly the periodic boundary
images we want to consider:

$$
\begin{equation}
  \Psi(\mathbf{Q}) = \sum_i \sum_j
  \text{e}^{i\mathbf{Q}\cdot(\mathbf{R}_i+\mathbf{\Delta L}_j})
\end{equation}
$$

where $$\mathbf{\Delta L}_j$$ is the distance between a particle and its
$$j$$-th periodic replica. Since the sums are independent, we can
write:

$$
\begin{equation}
  \Psi(\mathbf{Q}) = \left(\sum_i
    \text{e}^{i\mathbf{Q}\cdot\mathbf{R}_i}\right)
  \left(\sum_j\text{e}^{i\mathbf{Q}\cdot\mathbf{\Delta L}_j}\right)
\end{equation}
$$

Multiplying by the conjugate gives us the structure factor

$$
\begin{align}
  S(\mathbf{Q}) &= \left|\sum_i
    \text{e}^{i\mathbf{Q}\cdot\mathbf{R}_i}\right|^2 \left|\sum_j
    \text{e}^{i\mathbf{Q}\cdot\mathbf{\Delta L}_j}\right|^2\\
  &= S_{\text{cell}}(\mathbf{Q})\,S_{\text{PBC}}(\mathbf{Q})
\end{align}
$$

The advantage of this calculation is that it is linear in the sum of
the number of particles $$N$$ and the number of replicas $$M$$
consider, $$\mathcal{O}(N+M)$$, much lower than the previous
$$\mathcal{O}(N^2M^2)$$. Consequently, if we want to focus in a region
of $$\mathbf{Q}$$, this new approach will be useful[^4]. We are left
with only one detail, respecting to the *powder average*. It is not
trivial how to calculate this integral, since we need to give proper
weights to each angle. One of the alternatives are to use the Lebedev
quadrature[^5], although other methods like Importance Sampling
Montecarlo can be useful in this situation.

## Code
Here is the code with which we generated the figures above:

{% highlight python %}
{% include_relative ssf.py %}
{% endhighlight %}

[^1]: Egami T, Billinge, S. *Underneath the Bragg Peaks: Structural
    Analysis of Complex Materials*. Amsterdam: Pergamon, 2003
    

[^2]: This definition already uses that all particles are equal. For
    the general definition, see Egami and Billinge.

[^3]: Even further, now the imaginary part of $$S(q)$$ is no longer
    zero!

[^4]: We should consider though that in this approach, we will need
    $$\mathcal{O}(N+M)$$ calculations for each $$\mathbf{Q}$$, so we
    can't use it to sweep the whole $$\mathbf{Q}$$ spectrum.

[^5]: Lebedev, V. I. (1975) *Zh. Vȳchisl. Mat. Mat. Fiz.* **15** (1):
    48–54. doi:10.1016/0041-5553(75)90133-0.
