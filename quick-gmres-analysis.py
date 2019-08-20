import numpy as np
import pickle

filename = 'output-h_magnitude-1.0.pickle'

with open(filename,'rb') as f:
    qmc = pickle.load(f)

gmres = np.array(qmc[3][0])

num_samples = gmres.shape[0]

print('number of samples',num_samples)

num_pcs = (gmres==1).sum()

print('number of pcs',num_pcs)

print('fraction of pcs',float(num_pcs)/float(num_samples))
    
print('max GMRES iterations',np.max(qmc[3][0]))
