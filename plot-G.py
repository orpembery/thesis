from calc_G import G
from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np

eps = 1e-5

C = 0.1

diffs = np.linspace(0.01,1.0,10000)

# Found out how to do this from https://tex.stackexchange.com/a/391078
pgf_latex_dict  = { 'pgf.preamble' : [r'\usepackage{amssymb}',r'\usepackage{mleftright}']}

rcParams.update(pgf_latex_dict)

filename = 'G'

lines = ['--','-.',':']

k_list = [20.0,40.0,100.0]

for ii_k in range(len(k_list)):

    k = k_list[ii_k]

    N = k**3.0

    Gs = np.array([G(diff,eps,C,k,N) for diff in diffs])

    plt.semilogy(diffs,Gs,'k'+lines[ii_k],label=r'$k = '+str(int(k))+r'$')

    plt.xlabel(r'$\|n_{1} - n_{2}\|_{L^{\infty}\mleft(D_{R},\mathbb{R}\mright)}$')

    plt.ylabel(r'$G_{\varepsilon}$')

plt.legend()

plt.savefig(filename+'.pgf')
