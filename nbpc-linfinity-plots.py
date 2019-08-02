import helmholtz_firedrake.utils as utils
from os import listdir
from fnmatch import fnmatch
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator


this_directory = '/home/owen/Documents/running-code/running-nbpc/nbpc-scaling-linfinity/output/output02/'

noise_level = 0.2

csv_list = []
for filename in listdir(this_directory):
    if fnmatch(filename,'*csv'):
        csv_list.append(this_directory+filename)

info_data = utils.read_repeats_from_csv(csv_list[0])

names_list = list(info_data[0].keys())

names_list.remove('num_pieces')
names_list.remove('h_tuple')
names_list.remove('Git hash')
names_list.remove('Date/Time')
names_list.remove('A_pre_type')
names_list.remove('num_repeats')
        
all_csvs_df = utils.csv_list_to_dataframe(csv_list,names_list)


def plt_gmres(n_pre_type,noise_master,ks,modifier,filename):

    fig = plt.figure()
    
    for k in ks:
        data = all_csvs_df.xs((n_pre_type,noise_master,modifier,k),level=('n_pre_type','noise_master','modifier','k'),drop_level=False)
        for jj in data.columns:
            plt.scatter(data.reset_index().loc[0,'k'],data.iloc[0,jj],c='k')

    plt.xlabel(r'$k$')
    plt.ylabel('Number of GMRES Iterations')

    plt.xticks([20,40,60,80,100]) # told by http://stackoverflow.com/questions/12608788/ddg#12608937

    # Integers only on y axis
    # Found out about this from https://www.scivision.dev/matplotlib-force-integer-labeling-of-axis/
    ax = fig.gca()   
    ax.yaxis.set_major_locator(MaxNLocator(integer=True)) # Maybe add an argument to MaxNLocator to give the number of intervals on the x axis
    plt.savefig(filename+'.pgf')

#----- Should only need to edit below here ------


n_pre_type = 'constant'

noise_masters = ['('+str(noise_level)+', 0.0)','(0.0, '+str(noise_level)+')']

ks = [20.0,40.0,60.0,80.0,100.0]

modifierss = [['(0.0, -1.0, 0.0, 0.0)','(0.0, -0.5, 0.0, 0.0)','(0.0, 0.0, 0.0, 0.0)'],['(0.0, 0.0, 0.0, -1.0)','(0.0, 0.0, 0.0, -0.5)','(0.0, 0.0, 0.0, 0.0)']]

# ------ An example -------
for ii_An in range(2):
    noise_master = noise_masters[ii_An]
    modifiers = modifierss[ii_An]
    filename = 'nbpc-linfinity-plot-'
    if ii_An == 0:
        filename += 'n'
    else:
        filename += 'A'
    filename += '-'
    
    for ii in range(len(modifiers)):
        filename_tmp = filename + str(ii)
        plt_gmres(n_pre_type,noise_master,ks,modifiers[ii],filename_tmp)

                              



