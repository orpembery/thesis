from os import listdir
from fnmatch import fnmatch
import helmholtz_firedrake.utils as utils
#import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

this_directory = './'

csv_list = []
for filename in listdir():
    if fnmatch(filename,'*csv'):
        csv_list.append(this_directory + filename)

info_data = utils.read_repeats_from_csv(this_directory+csv_list[0])

k_list = [10.0,20.0,30.0,40.0]#,50.0,60.0]

betas = [0.0,1.0,2.0]

storage = np.empty(shape=(len(k_list),len(betas)),dtype=object)

for file in csv_list:

    data = utils.read_repeats_from_csv(this_directory+file)

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

    plt.figure()

    for k in k_list:

        ii_k = k_list.index(k)

        ii_beta = betas.index(beta)

        data = storage[ii_k,ii_beta]

        plt.xlabel('$k$')

        plt.ylabel('Number of GMRES iterations')

        plt.xticks([10,20,30,40])

        plt.plot(k*np.ones((len(data))),data,'.k')

    print(beta)
        
    plt.show()
