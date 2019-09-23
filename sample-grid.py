import firedrake as fd
from matplotlib import pyplot as plt
from matplotlib import rc

rc('text', usetex=True) # Found out about this from https://stackoverflow.com/q/54827147

mesh = fd.UnitSquareMesh(10,10)

fd.plot(mesh,colors='k')

fig = plt.gcf()

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')

plt.xticks([])
plt.yticks([])

fig.set_size_inches((5.5,5.5))

plt.savefig('sample-mesh.pgf')
