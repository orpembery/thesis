import numpy as np
import calc_G
from matplotlib import pyplot as plt

def plot_k(threshold,beta):
    """threshold is GMRES its threshold. beta is power in k-dependence."""
    eps = 10.0**-5.0

    probs = []

    k_range = np.linspace(10.0,40.0,1001)

    to_use = []
    
    for k in k_range:

        d = 2.0

        N = np.ceil(k**(d*1.5))

        C = 0.1 # Would need to estimate this?

        scale = 1.0/k**beta

        probs.append(calc_G.calc_prob(float(threshold),eps,C,k,N,scale))

    plt.plot(k_range,probs,'.')
    
    plt.show()

if __name__ == '__main__':

    plot_k(12,0.0)
    plot_k(12,1.0)
    plot_k(12,2.0)

    
