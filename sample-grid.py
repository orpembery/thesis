import firedrake as fd
from matplotlib import pyplot as plt
from matplotlib import rc

rc('text', usetex=True) # Found out about this from https://stackoverflow.com/q/54827147

mesh = fd.UnitSquareMesh(10,10)

fd.plot(mesh,colors='k')

plt.savefig('sample-mesh.pgf')
