from helmholtz_firedrake.problems import HelmholtzProblem
from helmholtz_firedrake.utils import h_to_num_cells
import firedrake as fd
import pickle


k_list = [10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0,100.0]

GMRES_its = []

for k in k_list:
    
    if fd.COMM_WORLD.rank == 0:
        print(k,flush=True)
        
    h = k**-1.5

    num_cells = h_to_num_cells(h,2)

    mesh = fd.UnitSquareMesh(num_cells,num_cells)

    V = fd.FunctionSpace(mesh,"CG",1)

    prob = HelmholtzProblem(k,V)

    prob.solve()

    GMRES_its.append(prob.GMRES_its)

if fd.COMM_WORLD.rank == 0:
    
    print(GMRES_its)

    with open('GMRES.pickle',mode='wb') as file:
        pickle.dump([k_list,GMRES_its],file)

