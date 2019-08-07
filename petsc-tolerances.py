# I found out how to use the petsc4py commands by taking some of this from https://github.com/firedrakeproject/petsc4py/blob/16675da20ac64ed690db3633850f2573f54d0d8a/test/test_ksp.py
from petsc4py import PETSc
ksp = PETSc.KSP()
ksp.create(PETSc.COMM_SELF)

# I know what the labels are from https://www.mcs.anl.gov/petsc/petsc-current/docs/manualpages/KSP/KSPGetTolerances.html#KSPGetTolerances
labels = ['Relative Convergence Tolerance','Absolute Convergence Tolerance','Divergence Tolerance','Maximum number of iterations']
tols = ksp.getTolerances()

for ii in range(4):
    print(labels[ii],tols[ii])

