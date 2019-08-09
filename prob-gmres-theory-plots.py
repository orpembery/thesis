import numpy as np
import calc_G
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

def plot_k(threshold,beta):
    """threshold is GMRES its threshold. beta is power in k-dependence."""
    eps = 10.0**-5.0

    filename = 'prob-gmres-theory-'+str(beta)

    probs = []

    k_range = np.linspace(10.0,40.0,101)

    to_use = []
    
    for k in k_range:

        d = 2.0

        N = np.ceil(k**(d*1.5))

        C = 0.1 # Would need to estimate this?

        scale = 1.0/k**beta

        probs.append(calc_G.calc_prob(float(threshold),eps,C,k,N,scale))

    fig = plt.figure()

    fig.set_size_inches((6,2.5))
    
    plt.xlabel(r'$k$')

    plt.ylabel('Probability that number of\nGMRES iterations is at most 12')

    if beta == 2.0:
        plt.yticks([0.97,0.98,0.99,1.0])
    elif beta == 0.0:
        plt.yticks([0.01,0.02,0.03])
    elif beta == 1.0:
        # Found out about this from https://www.scivision.dev/matplotlib-force-integer-labeling-of-axis/
        ax = fig.gca()
        ax.yaxis.set_major_locator(MaxNLocator(4))
        #plt.yticks([0.28,0.29,0.3])
        
    plt.plot(k_range,probs,'.k')

    plt.savefig(filename + '.pgf')


plot_k(12,0.0)
plot_k(12,1.0)
plot_k(12,2.0)

    
