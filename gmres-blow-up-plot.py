from matplotlib import pyplot as plt
import pickle

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
