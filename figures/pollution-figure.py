from helmholtz_firedrake.problems import HelmholtzProblem
from helmholtz_firedrake.utils import h_to_num_cells
import firedrake as fd
from matplotlib import pyplot as plt
import numpy as np

k = 1000.0

h = (k**-1.0) * 0.1

d = 1

num_cells = h_to_num_cells(h,d)

print(num_cells,h**-1)

mesh = fd.UnitIntervalMesh(num_cells)

V = fd.FunctionSpace(mesh,"CG",1)

u = fd.TrialFunction(V)

v = fd.TestFunction(V)

a = (fd.inner(fd.grad(u), fd.grad(v))\
     - k**2 * fd.inner(u,v)) * fd.dx#\
#     - (1j* k * fd.inner(u,v)) * fd.ds(2)

bc = fd.DirichletBC(V, 0.0, 1)

L = fd.inner(k*np.cos(k),v)*fd.ds(2)

u_h = fd.Function(V)

fd.solve(a==L,u_h,solver_parameters = {'ksp_type': 'preonly', 'pc_type': 'lu'},bcs=[bc])

u_true = fd.Function(V)

x = fd.SpatialCoordinate(mesh)

u_true.interpolate(fd.sin(k*x[0]))

coords = fd.Function(V)

coords.interpolate(x[0])

#fd.plot(u_h)

sin_fn = np.sin(k*coords.dat.data_ro)

for xlim in ([0.0,0.025],[0.975,1.0]):

    fig = plt.figure()

    plt.plot(coords.dat.data_ro,sin_fn,'-k',label='True solution')

    plt.plot(coords.dat.data_ro,u_h.dat.data_ro,'k--',label='Finite-element approximation')

    plt.xlim(xlim)

    plt.legend(loc='upper right')

    plt.show()



