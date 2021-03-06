from calc_G import G
from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np
from matplotlib import rc, rcParams

rc('text', usetex=True) # Found out about this from https://stackoverflow.com/q/54827147

rcParams.update({'text.latex.preamble':[r'\usepackage[urw-garamond]{mathdesign}',r'\usepackage[T1]{fontenc}'],'font.size':11})

eps = 1e-5

C = 0.1

diffs = np.linspace(0.01,1.0,10000)

# Found out how to do this from https://tex.stackexchange.com/a/391078
pgf_latex_dict  = { 'pgf.preamble' : [r'\usepackage{amssymb}',r'\usepackage{mleftright}']}

rcParams.update(pgf_latex_dict)

filename = 'G'

lines = ['--','-.',':']

k_list = [20.0,40.0,100.0]

fig = plt.figure()

fig.set_size_inches((5.5,5.5))

for ii_k in range(len(k_list)):

    k = k_list[ii_k]

    N = k**3.0

    Gs = np.array([G(diff,eps,C,k,N) for diff in diffs])

    plt.semilogy(diffs,Gs,'k'+lines[ii_k],label=r'$k = '+str(int(k))+r'$')

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    plt.xlabel(r'$\|n_{1} - n_{2}\|_{L^{\infty}\mleft(D_{R},\mathbb{R}\mright)}$')

    plt.ylabel(r'$G_{\varepsilon}$')

plt.legend()

plt.savefig(filename+'.pgf')
