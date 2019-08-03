import pickle
import numpy as np
import sys
from running_helmholtz_monte_carlo.name_writing import make_quants, name_writing
#from name_writing import name_writing, make_quants
from helmholtz_monte_carlo.calculate import mean_and_error
from glob import glob
from matplotlib import pyplot as plt

"""This script plots (and calculates) how the quasi-monte carlo error depends on the wavenumber k."""

"""The script takes a number of command-line arguments, in order, as follows:

number of h levels - the number of grids used, where they were obtained by uniform refinement from a grid with mesh size k**-3/2. A value of 1 indicates that the finest grid had mesh size k**-3/2.

M - where the number of integration points was (for QMC) 2**M

nu - the number of shifts used for a shifted QMC rule

J - the stochastic dimension of the stochastic coefficient

delta - the parameter controlling the decay rate in the KL-like coefficients

lambda_mult - the parameter controlling the absolute value of the KL-like coefficients

j_scaling - the amount of scaling applied to the oscillatory nature of the spatial parts of the KL-like coefficients.

dim - the physical dimension of the problem

h_coarse_magnitude - the (absolute) magnitude of how h on the coarsest space scales with k.

h_coarse_scaling - how h on the coarsest space scales with k - the power of k.

The script computes results for all the qois that are available

The remaining arguments are the values of k to use.
"""

h_levels = 1#sys.argv[1]

M = 11#int(sys.argv[2])

nu = 20#int(sys.argv[3])

J = 10#int(sys.argv[4])

delta = 1.0#float(sys.argv[5])

lambda_mult = 1.0#float(sys.argv[6])

j_scaling = 4.0#float(sys.argv[7])

dim = 2#int(sys.argv[8])

h_coarse_magnitude = 0.002#float(sys.argv[9])

h_coarse_scaling = 0.0#float(sys.argv[10])

nearby_preconditioning = 0

nearby_preconditioning_proportion = 1.0

#next_number = 11

# If altered, don't forget to change entry to make_quants

on_balena = '*' # This doesn't matter, but needs to go in for completeness

qois = '*' # As above

k_list = [10.0,20.0,30.0,40.0,50.0,60.0]#[ float(k) for k in sys.argv[next_number:]]

markers = 'ovsdp*'

lines = ['--','--','-.','-.',':',':']

for ii_k in range(len(k_list)):

    k = k_list[ii_k]

    # Make the dict
    quants = make_quants([k,h_levels,M,nu,J,delta,lambda_mult,j_scaling,dim,on_balena,h_coarse_magnitude,h_coarse_scaling,nearby_preconditioning,nearby_preconditioning_proportion,qois])

    folder_name_start = name_writing(quants)

    h_magnitude = quants['h_coarse_mag']

    test_filename = './data/data-for-num-qmc-points/' + folder_name_start + '*/*' + str(h_magnitude) + '*' + '.pickle'
    
    filenames = glob(test_filename)

    if len(filenames) == 0:
        raise Exception('No file exists with filename beginning {0}.'.format(test_filename))
    elif len(filenames) > 1:
        raise Exception('More than one file exists with filename beginning {0}.'.format(test_filename))
    else:
        filename = filenames[0]
    
        with open(filename,'rb') as f:
            qmc = pickle.load(f)
    # The following is a bit of string hackery to get the names of the qois
    try:
        names_list_old = qoi_names_list
    except NameError:
        # First time we run through the loop
        names_list_old = 42
        
    qoi_names_list = filename[filename.find('qois-'):filename.find('-git-hash')].split('-')[1:]

    # Sanity check that the order of the qois hasn't changed
    assert (qoi_names_list == names_list_old) or names_list_old == 42

    # Second entry of QMC is a list
    # Each entry of the list corresponds to a shift
    # And each is itself a list of length num_qois
    # Each entry of which corresponds to a different QoI
    # And each is itself a list of length (number of samples), containing ????floats

    num_qois = len(qmc[1][0])

    # Create storage on first iteration through loop
    if k == k_list[0]:
        error_store = [np.zeros((len(k_list),M+1)) for ii in range(num_qois)]
        
    for this_M in range(M+1):
        # Select the samples for this M

        # qmc_tmp has a similar structure to qmc, but only records
        # values for this_M. Third entry of qmc_tmp is the samples
        # themselves, although they're currently not used.
        qmc_tmp = []

        qmc_tmp.append(qmc[0])

        qmc_tmp.append([])

        qmc_tmp.append([])

        # For each shift, and for each QoI, pick up the first 2**this_M samples
        for ii_nu in range(nu):
            samples_tmp = []
            n_tmp = []
            for ii_qoi in range(num_qois):
                samples_tmp.append(qmc[1][ii_nu][ii_qoi][:(2**this_M)])
                n_tmp.append(qmc[2][ii_nu][ii_qoi][:(2**this_M)])
            qmc_tmp[1].append(samples_tmp)
            qmc_tmp[2].append(n_tmp)

        computed_mean_err = mean_and_error(qmc_tmp,'qmc')

        for ii_qoi in range(num_qois):
            error_store[ii_qoi][ii_k,this_M] = np.abs(computed_mean_err[1][ii_qoi])

# Now move on to convergence rates with respect to k and plotting

            
for ii_qoi in range(num_qois):

    M_list = list(range(0,M+1))

    N_list = 2.0**np.array(M_list)

    qoi_C_alpha = [[],[]]

    qoi = qoi_names_list[ii_qoi]

    # Assume QMC error is CN^alpha. We first fit C and alpha to the data (for each k) and then investigate their dependence on k.
    for ii_k in range(len(k_list)):
    
        error_list = error_store[ii_qoi][ii_k,:]

        # Expect error = C*N^{-alpha}, so log(error) = log(C) -alpha*log(N)

        fit = np.polyfit(np.log10(N_list),np.log10(error_list),deg=1)

        C = 10.0**fit[1]
        alpha = -fit[0]

        qoi_C_alpha[0].append(C)

        qoi_C_alpha[1].append(alpha)

        fig = plt.figure()
        
        # Do a loglog plot of the error
        loglog = plt.loglog(N_list,error_list,'ok')

        # Draw line of best fit, based on values of C and alpha calculated above
        
        big_N = max(N_list)

        small_N = min(N_list)

        x_for_fit = [small_N,big_N]

        y_for_fit = C*np.array([small_N,big_N])**-alpha

        num_sig_fig = 6

        k = k_list[ii_k]

        plt.loglog(x_for_fit,y_for_fit,'--',color=loglog[-1].get_color(),label= r'$' + str(C)[:num_sig_fig] + r'N_{\mathrm{QMC}}^{-' + str(alpha)[:num_sig_fig] + r'}$')

        plt.xlabel(r'$N_\mathrm{QMC}$')

        plt.ylabel('QMC Error')

        #plt.title(qoi+', k = '+str(int(k)))

        plt.legend()
    
        #plt.show()

        fig_name = qoi+'-'+str(int(k))+'-error-plot'

        fig.set_size_inches((3,3))
        
        plt.savefig(fig_name+'.pgf')

        plt.close(fig)
        
    # Now investigate dependence of C and alpha on k

    fig = plt.figure()
    
    plt.loglog(k_list,qoi_C_alpha[0],'ko')
    #plt.title('C against k, for qoi = '+ qoi)
    plt.xlabel('k')
    plt.ylabel('C')
    #plt.show()

    fig_name = qoi+'-C-plot'

    fig.set_size_inches((3,3))
    
    plt.savefig(fig_name+'.pgf')

    plt.close(fig)
    
    # Now fit alpha = alpha_0 - alpha_1 log(k)

    log_k = np.log10(k_list)

    alpha = qoi_C_alpha[1]

    # Numpy.polyfit uses different notation to us. So entry [0] corresponds to -alpha_1 and entry [1] corresponds to alpha_0
    
    alpha_logk_fit = np.polyfit(log_k,alpha,deg=1)

    alpha_0 = alpha_logk_fit[1]

    alpha_1 = -alpha_logk_fit[0]

    # Add best fit line
    alpha_logk_best_fit = alpha_0 - alpha_1 * log_k


    fig = plt.figure()

    plt.semilogx(k_list,alpha_logk_best_fit,'k--',label=r'$\alpha = '+str(alpha_0)[:num_sig_fig]+r' - '+str(alpha_1)[:num_sig_fig]+r'\log(k)$')
    # ; alpha_1/alpha_0 = '+str(alpha_1/alpha_0)[:num_sig_fig]
    #plt.title('alpha against k for qoi = '+qoi)
    plt.xlabel(r'$k$')
    plt.ylabel(r'$\alpha$')
    plt.legend()
    plt.semilogx(k_list,qoi_C_alpha[1],'ko')

    fig_name = qoi+'-alpha-plot'

    fig.set_size_inches((3,3))
    
    plt.savefig(fig_name+'.pgf')

    plt.close(fig)
    
    #plt.show()


    


# Need to get qoi strings, and check that they always come in the same order

# Also need to think about how to plot variation in n
