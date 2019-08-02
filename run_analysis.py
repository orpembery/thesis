import pickle
import numpy as np
import sys
from name_writing import name_writing, make_quants
from helmholtz_monte_carlo.calculate import mean_and_error
from glob import glob
from matplotlib import pyplot as plt

"""This script plots (and calculates) how the quasi-monte carlo error depends on the wavenumber k.

The script takes a number of command-line arguments, in order, as follows:

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

h_levels = sys.argv[1]

M = int(sys.argv[2])

nu = int(sys.argv[3])

J = int(sys.argv[4])

delta = float(sys.argv[5])

lambda_mult = float(sys.argv[6])

j_scaling = float(sys.argv[7])

dim = int(sys.argv[8])

h_coarse_magnitude = float(sys.argv[9])

h_coarse_scaling = float(sys.argv[10])

next_number = 11

# If altered, don't forget to change entry to make_quants

on_balena = '*' # This doesn't matter, but needs to go in for completeness

qois = '*' # As above

k_list = [ float(k) for k in sys.argv[next_number:]]

for ii_k in range(len(k_list)):

    k = k_list[ii_k]

    # Make the dict

    quants = make_quants([k,h_levels,M,nu,J,delta,lambda_mult,j_scaling,dim,on_balena,h_coarse_magnitude,h_coarse_scaling,qois])

    folder_name_start = name_writing(quants)

    h_magnitude = 2.0**-(float(quants['h_levels'])-1.0)*h_coarse_magnitude

    test_filename = folder_name_start + '*/*' + str(h_magnitude) + '*' + '.pickle'
    
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

for ii_qoi in range(num_qois):

    M_list = list(range(0,M+1))

    N_list = 2.0**np.array(M_list)

    qoi_C_alpha = [[],[]]

    for ii_k in range(len(k_list)):
    
        error_list = error_store[ii_qoi][ii_k,:]

        # Expect error = C*N^{-alpha}, so log(error) = log(C) -alpha*log(N)

        fit = np.polyfit(np.log10(N_list),np.log10(error_list),deg=1)

        C = 10.0**fit[1]
        alpha = -fit[0]

        qoi_C_alpha[0].append(C)

        qoi_C_alpha[1].append(alpha)

        # Do a loglog plot of the error
        loglog = plt.loglog(N_list,error_list,'.')    

        big_N = max(N_list)

        small_N = min(N_list)

        x_for_fit = [small_N,big_N]

        y_for_fit = C*np.array([small_N,big_N])**-alpha

        num_sig_fig = 6

        k = k_list[ii_k]

        # Add the best fit line
        plt.loglog(x_for_fit,y_for_fit,'--',color=loglog[-1].get_color(),label='k='+str(k)+': C = '+str(C)[:num_sig_fig] + ', alpha = '+str(alpha)[:num_sig_fig])
        

    plt.xlabel('N')

    plt.ylabel('QMC Error')

    plt.title(qoi_names_list[ii_qoi])

    plt.legend()
    
    plt.show()

    qoi_name = qoi_names_list[ii_qoi]

    plt.loglog(k_list,qoi_C_alpha[0],'rx')
    plt.title('C against k, for qoi = '+ qoi_name)
    plt.xlabel('k')
    plt.ylabel('C')
    plt.show()

    # Now fit alpha = alpha_0 - alpha_1 log(k)

    log_k = np.log10(k_list)

    alpha = qoi_C_alpha[1]

    alpha_logk_fit = np.polyfit(log_k,alpha,deg=1)

    alpha_0 = alpha_logk_fit[0]

    alpha_1 = alpha_logk_fit[1]

    # Add best fit line
    alpha_logk_best_fit = alpha_1 + alpha_0 * log_k
    

    plt.semilogx(k_list,alpha_logk_best_fit,'r','--',label='alpha = '+str(alpha_0)[:num_sig_fig]+' - '+str(alpha_1)[:num_sig_fig]+'log(k); alpha_1/alpha_0 = '+str(-alpha_1/alpha_0)[:num_sig_fig])
    plt.title('alpha against k for qoi = '+qoi_name)
    plt.xlabel('k')
    plt.ylabel('alpha')
    plt.legend()
    plt.semilogx(k_list,qoi_C_alpha[1],'rx')
    plt.show()


    


# Need to get qoi strings, and check that they always come in the same order

# Also need to think about how to plot variation in n
