import numpy as np
from scipy.optimize import bisect
from matplotlib import pyplot as plt
from scipy.stats import expon

def G(diff,eps,C,k,N):
    """Defines the probabalistic GMRES bound function.

    diff - L^\infty norm of n^(1) - n^(2)

    eps - in (0,1), the tolerance

    C - C_2 in the GMRES result

    k - the wavenumber

    N - the number of dofs

    Returns the bound. Uses natural logs
    """    
    alpha = C * k * diff

    if alpha >= 1.0:
        val = N

    elif alpha == 0.0:
        val = 1

    else:
    
        complicated = np.log(eps) / np.log( (2.0*alpha**0.5) / ((1.0+alpha)**2.0) )

        val = min([N,complicated+1.0])

    return val

def calc_prob(R,eps,C,k,N,scale):
    """Calculates the probability that GMRES converges in fewer than R
    iterations when the L^\infty norm of the difference is
    exp(scale)"""
    
    if R >= N:
        total_prob = 1.0
    else:

        def G_single(x):
            return G(x,eps,C,k,N)

        def G_single_R(y):
            return G_single(y) - R

        # Find the point at which we revert to the worst-case GMRES estimate
        endpoint = 1.0/(C*k)

        # Find the point at which the gradient is zero
        # And therefore the maximum on the part alpha < 1
        # One can calculate this by hand
        gradpoint = 1.0/(3.0*C*k)

        total_prob = 0.0
        
        if G_single(gradpoint) < R:
            # integrate [0,end]
            total_prob += expon.cdf(endpoint,scale=scale)

        else:

            if G_single(0.0) < R:
                lower_point = bisect(G_single_R,0.0,gradpoint)

                # integrate [0,lower_point]
                total_prob += expon.cdf(lower_point,scale=scale)

            nearly_end = endpoint - 10.0**-10.0

            if G_single(nearly_end) < R:
                higher_point = bisect(G_single_R,gradpoint,nearly_end)

                # integrate [higher_point,end]
                total_prob += (expon.cdf(endpoint,scale=scale)-expon.cdf(higher_point,scale=scale))

    return total_prob

