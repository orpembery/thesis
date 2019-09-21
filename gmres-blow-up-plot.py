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

fig = plt.figure()

plt.plot(k_list,GMRES_its,'s--k')

ax = plt.gca()

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.xlabel('$k$')

plt.ylabel('Number of GMRES iterations')

fig.set_size_inches((5,5))

plt.savefig(filename+'.pgf')
