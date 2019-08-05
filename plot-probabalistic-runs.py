from os import listdir
from fnmatch import fnmatch
import helmholtz_firedrake.utils as utils
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

this_directory = '/home/owen/Documents/running-code/prob-gmres-examples/output/'

csv_list = []
for filename in listdir(this_directory):
    if fnmatch(filename,'*csv'):
        csv_list.append(this_directory + filename)
        
info_data = utils.read_repeats_from_csv(csv_list[0])

k_list = [10.0,20.0,30.0,40.0]#,50.0,60.0]

betas = [0.0,1.0,2.0]

storage = np.empty(shape=(len(k_list),len(betas)),dtype=object)

for file in csv_list:

    data = utils.read_repeats_from_csv(file)

    k = data[0]['k']

    beta = np.log(1.0/data[0]['scale'])/np.log(k)

    # A bit of a hack
    for new_beta in betas:
        if np.isclose(beta,new_beta):
            beta = new_beta

    ii_k = k_list.index(k)

    ii_beta = betas.index(beta)
    storage[ii_k,ii_beta] = data[1][:,1]

for beta in betas:

    fig = plt.figure()

    filename = 'prob-plot-rate-'+str(beta)

    for k in k_list:

        ii_k = k_list.index(k)

        ii_beta = betas.index(beta)

        data = np.unique(storage[ii_k,ii_beta])

        plt.xlabel('$k$')

        plt.ylabel('Number of GMRES iterations')

        plt.xticks([int(k) for k in k_list])

        # Found out about this from https://www.scivision.dev/matplotlib-force-integer-labeling-of-axis/
        ax = fig.gca()
        
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        plt.plot(k*np.ones((len(data))),data,'ok')

    plt.savefig(filename+'.pgf')

    plt.close()
