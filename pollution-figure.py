from helmholtz_firedrake.utils import h_to_num_cells
import firedrake as fd
from matplotlib import pyplot as plt
import numpy as np

k = 1000.0

h = (k**-1.0) * (np.pi/5.0)

d = 1

num_cells = h_to_num_cells(h,d)

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

sin_fn = np.sin(k*coords.dat.data_ro)

filenames = ['pollution-left','pollution-right']

xlims = [[0.0,0.025],[0.975,1.0]]

xticks = [[0,0.01,0.02],[0.98,0.99,1]]

for ii_plot in range(2):

    xlim = xlims[ii_plot]

    filename = filenames[ii_plot]

    fig = plt.figure()
    
    plot1 = plt.plot(coords.dat.data_ro,sin_fn,'-k',label='True solution')

    plt.plot(coords.dat.data_ro,u_h.dat.data_ro,'k--',label='Finite-element approximation')

    # A4 is 8.3 inches wide
    
    fig.set_size_inches((3,3))

    plt.xlim(xlim)

    plt.yticks([-1,0,1])

    plt.xticks(xticks[ii_plot])

    plt.savefig(filename+'.pgf')


