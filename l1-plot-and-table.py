import pandas as pd
import helmholtz_firedrake.utils as utils
from os import listdir
from fnmatch import fnmatch
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import fileinput

this_directory = '/home/owen/Documents/running-code/running-nbpc/nbpc-scaling-l1/output/'

csv_list = []
for filename in listdir(this_directory):
    if fnmatch(filename,'*csv'):
        csv_list.append(this_directory + filename)

num_eps = len(csv_list)

info_data_tmp = utils.read_repeats_from_csv(csv_list[0])

num_k = len(info_data_tmp[1])

k_list = [ii[1] for ii in info_data_tmp[1]]

data = []

eps_list = []
        
for file in csv_list:
        
    info_data = utils.read_repeats_from_csv(file)

    string = file

    # A bit of a hack, because I know the filenames
    #import pdb; pdb.set_trace()
    eps = float(string[(len(this_directory)+17):(len(this_directory)+20)])

    eps_list.append(eps)
    
    this_k_data = [ii[2] for ii in info_data[1]]

    data.append(this_k_data)
    
df = pd.DataFrame(data,columns=k_list,index=eps_list)

df = df.sort_index()



# Put dataframe in a table

# Plot results for 0.0 to 0.3 on one axis 0.4-0.7 on another and 0.8-1.0 on another

def make_plot(locs,filename):

    fig = plt.figure()

    styles = 'ovsd'

    for ii_loc in range(len(locs)):

        loc = locs[ii_loc]

        # special for 0.0 and 1.0


        if loc == 1.0:
            str_loc = '1'
        else:
            str_loc = str(loc)


        if loc == 0.0:
            label = r'$\beta = 0$'
        else:
            label = r'$\beta = '+str_loc+'$'

        
        
        df.loc[loc,:].T.plot(style='k'+styles[ii_loc]+'--',label=label)

    plt.xlabel('$k$')

    plt.ylabel('Number of GMRES iterations')

    plt.xlim([0,110])

    plt.xticks([10,20,30,40,50,60,70,80,90,100])

    # Found out about this from https://www.scivision.dev/matplotlib-force-integer-labeling-of-axis/
    ax = fig.gca()
    
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        
    plt.legend(loc='upper left')


    plt.savefig(filename+'.pgf')

    plt.close() # Why is there an extra figure created when doing two ormore plots, and why does this fix it?

# Make the plots
    
make_plot([0.0,0.1,0.2,0.3],'l1-low')

make_plot([0.4,0.5,0.6,0.7],'l1-med')

make_plot([0.8,0.9,1.0],'l1-high')


# Make the table

float_format = '{:.0f}'.format # Based on formatting described at https://pyformat.info/#number
# Helped debug using https://stackoverflow.com/a/20937592

column_format = 'Sc '*df.shape[1]

df.columns = [int(k) for k in k_list]

l1_table = 'l1-table.tex'


with open(l1_table,mode='w') as table:
    df.to_latex(table,float_format=float_format,column_format=column_format)
    
# This is a hack to get the table to print like I want
with fileinput.input(files=(l1_table),inplace=True) as table:
    for line in table:

        if line.endswith('Sc }\n'):
            print(line[:-3]+'Sc }')        
        elif line.startswith('{}'):
            print(r'$\beta$\textbackslash$k$'+line[2:])
        else:
            print(line)

# Also need to input these files somewhere
