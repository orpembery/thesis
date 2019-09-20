from os import listdir
from fnmatch import fnmatch
import helmholtz_firedrake.utils as utils
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import rcParams
from matplotlib import rc

rc('text', usetex=True) # Found out about this from https://stackoverflow.com/q/54827147


# Found out how to do this from https://tex.stackexchange.com/a/391078
pgf_latex_dict  = { 'pgf.preamble' : [r'\usepackage{mleftright}']}

rcParams.update(pgf_latex_dict)

this_directory = '/home/owen/Documents/running-code/prob-gmres-examples/output/'

csv_list = []
for filename in listdir(this_directory):
    if fnmatch(filename,'*csv'):
        csv_list.append(this_directory + filename)
        
info_data = utils.read_repeats_from_csv(csv_list[0])

k_list = [10.0,20.0,30.0,40.0]#,50.0,60.0]

betas = [0.0,1.0,2.0]

threshold = 12

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

    fig.set_size_inches((6,2.5))

    ax = fig.gca()
        
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    filename = 'prob-plot-rate-'+str(beta)

    ii_beta = betas.index(beta)

    frac_under_threshold = []
    
    for ii_k in range(len(k_list)):
    
        data = storage[ii_k,ii_beta]

        frac_under_threshold.append(float(np.sum(data <= threshold))/float(len(data)))

    plt.xlabel('$k$')

    plt.ylabel('Empirical probability that\n$\mathrm{GMRES}\mleft(\epsilon, n^{(1)} n^{(2)}\mright) \leq 12$')

    plt.xticks([int(k) for k in k_list])

    # Found out about this from https://www.scivision.dev/matplotlib-force-integer-labeling-of-axis/
    ax = fig.gca()

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.plot(k_list,frac_under_threshold,'ok--')

    if beta == 0.0:
        plt.yticks([0.0,0.1,0.2,0.3,0.4])
    elif beta == 1.0:
        plt.yticks([0.992,0.994,0.996,0.998,1.0])
    elif beta == 2.0:
        plt.yticks([1.0])

    plt.savefig(filename+'.pgf')

    plt.close()
