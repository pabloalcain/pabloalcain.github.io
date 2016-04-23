import numpy as np
import itertools as it

def ssf(x, size, q, pbc=False):
  """
  From a series of positions x in a cubic box of length size we get
  the structure factor for momentum q
  """

  natoms = np.shape(x)[0]
  sf = 0.0
  for i in range(natoms):
    x1 = x[i]
    for j in range(i+1, natoms):
      x2 = x[j]
      dx = x2 - x1
      if pbc:
        for i in range(3):
          if dx[i] >  size/2: dx[i] -= size
          if dx[i] < -size/2: dx[i] += size
      r = np.linalg.norm(dx)
      sf += 2*np.sin(q*r)/(q*r)
  sf /= natoms
  sf += 1
  return sf

def generate_sc(size, n):
  """
  Generate the positions of a simple cubic crystal in a box of
  length size with n atoms in each direction (order parameter =
  size/n)
  """

  natoms = n**3
  pos = range(n)
  x = np.zeros((natoms, 3))
  i = 0
  for px, py, pz in it.product(pos, pos, pos):
    x[i] = (px, py, pz)
    x[i] = x[i] * (size/n)
    i += 1
  return x

if __name__ == '__main__':
  import pylab as pl
  size = 1.0
  x = generate_sc(size, 4)
  q = np.linspace(0, 20.0, 101)[1:]
  sf_pbc = [ssf(x, size, _, True) for _ in q]
  sf_sing = [ssf(x, size, _, False) for _ in q]
  fig, ax  = pl.subplots()
  ax.plot(q, sf_pbc)
  ax.axhline(y=0, c='k', ls='--')
  ax.set_xlabel('Wavenumber')
  ax.set_ylabel('Structure factor')
  fig.tight_layout()
  fig.savefig('ssf_pbc.png')
  pl.close()

  fig, ax  = pl.subplots()
  ax.plot(q, sf_pbc, label='with PBC')
  ax.plot(q, sf_sing, label='without PBC')
  ax.axhline(y=0, c='k', ls='--')
  ax.set_xlabel('Wavenumber')
  ax.set_ylabel('Structure factor')
  ax.legend()
  fig.tight_layout()
  fig.savefig('ssf_comp.png')
  pl.close()
