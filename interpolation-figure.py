from helmholtz_firedrake.utils import h_to_num_cells
import firedrake as fd
from matplotlib import pyplot as plt
import numpy as np


k_list = [10.0,50.0]

d = 1

filenames = ['interpolation-left','interpolation-right']

for ii_k in range(2):

    k = k_list[ii_k]

    h = (k**-1.0) * (np.pi/5.0)

    h_coarse = (k_list[0]**-1.0) * (np.pi/5.0)

    num_cells_coarse = h_to_num_cells(h_coarse,d)

    num_cells  = h_to_num_cells(h,d)

    mesh_interpolate = fd.UnitIntervalMesh(num_cells_coarse)
    
    mesh_fine = fd.UnitIntervalMesh(10*num_cells)

    V_interpolate = fd.FunctionSpace(mesh_interpolate,"CG",1)

    u_interpolate = fd.Function(V_interpolate)

    x_interpolate = fd.SpatialCoordinate(mesh_interpolate)

    u_interpolate.interpolate(fd.sin(k*x_interpolate[0]))

    coord_interpolate = fd.Function(V_interpolate)

    coord_interpolate.interpolate(x_interpolate[0])

    V_fine = fd.FunctionSpace(mesh_fine,"CG",1)

    coord_fine = fd.Function(V_fine)

    x_fine = fd.SpatialCoordinate(mesh_fine)
    
    coord_fine.interpolate(x_fine[0])

    fig = plt.figure()

    plt.plot(coord_fine.dat.data_ro,np.sin(k*coord_fine.dat.data_ro),'0.7')

    plt.plot(coord_interpolate.dat.data_ro,u_interpolate.dat.data_ro,'k--')

    fig.set_size_inches((3,3))

    plt.yticks([-1,0,1])

    plt.xticks([0,0.5,1])

    filename = filenames[ii_k]

    plt.savefig(filename+'.pgf')

