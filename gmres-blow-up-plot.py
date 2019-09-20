from matplotlib import pyplot as plt
import pickle
from matplotlib import rc

rc('text', usetex=True) # Found out about this from https://stackoverflow.com/q/54827147

filename = 'GMRES'

txt = []

with open('GMRES.pickle',mode='rb') as file:
    dumped = pickle.load(file)


k_list = dumped[0]

GMRES_its = dumped[1]

plt.plot(k_list,GMRES_its,'s--k')

plt.xlabel('$k$')

plt.ylabel('Number of GMRES iterations')

plt.savefig(filename+'.pgf')
