from helmholtz_firedrake.utils import h_to_num_cells
import firedrake as fd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import rc

rc('text', usetex=True) # Found out about this from https://stackoverflow.com/q/54827147


k = 1000.0

h = (k**-1.0) * (np.pi/5.0)

d = 1

num_cells = h_to_num_cells(h,d)

mesh = fd.UnitIntervalMesh(num_cells)

mesh_fine = fd.UnitIntervalMesh(20*num_cells)

V = fd.FunctionSpace(mesh,"CG",1)

V_fine = fd.FunctionSpace(mesh_fine,"CG",1)

u = fd.TrialFunction(V)

v = fd.TestFunction(V)

a = (fd.inner(fd.grad(u), fd.grad(v))\
     - k**2 * fd.inner(u,v)) * fd.dx#\
#     - (1j* k * fd.inner(u,v)) * fd.ds(2)

bc = fd.DirichletBC(V, 0.0, 1)

L = fd.inner(k*np.cos(k),v)*fd.ds(2)

u_h = fd.Function(V)

fd.solve(a==L,u_h,solver_parameters = {'ksp_type': 'preonly', 'pc_type': 'lu'},bcs=[bc])

u_fine = fd.Function(V_fine)

x = fd.SpatialCoordinate(mesh)

x_fine = fd.SpatialCoordinate(mesh_fine)

u_fine.interpolate(fd.sin(k*x_fine[0]))

coords = fd.Function(V)

coords.interpolate(x[0])

coords_fine = fd.Function(V_fine)

coords_fine.interpolate(x_fine[0])

sin_fn = np.sin(k*coords_fine.dat.data_ro)

filenames = ['pollution-left','pollution-right']

xlims = [[0.0,0.025],[0.975,1.0]]

xticks = [[0,0.01,0.02],[0.98,0.99,1]]

for ii_plot in range(2):

    xlim = xlims[ii_plot]

    filename = filenames[ii_plot]

    fig = plt.figure()
    
    plot1 = plt.plot(coords_fine.dat.data_ro,sin_fn,'-k',label='True solution')

    plt.plot(coords.dat.data_ro,u_h.dat.data_ro,'k--',label='Finite-element approximation')

    # A4 is 8.3 inches wide
    
    fig.set_size_inches((3,3))

    plt.xlim(xlim)

    plt.yticks([-1,0,1])

    plt.xticks(xticks[ii_plot])

    plt.savefig(filename+'.pgf')


