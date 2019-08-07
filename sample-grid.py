import firedrake as fd
from matplotlib import pyplot as plt
mesh = fd.UnitSquareMesh(10,10)

fd.plot(mesh,colors='k')

plt.savefig('sample-mesh.pgf')
