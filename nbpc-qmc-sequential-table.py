import csv
import pandas as pd
from os import listdir
from fnmatch import fnmatch
import fileinput
from matplotlib import pyplot as plt
from running_helmholtz_monte_carlo.nbpc_percentage_fit import make_fits
import numpy as np
from matplotlib import rc

rc('text', usetex=True) # Found out about this from https://stackoverflow.com/q/54827147


#import pdb; pdb.set_trace()

k_list = [10.0,20.0,30.0]

df_master = pd.DataFrame(index=[int(k) for k in k_list],columns=['num_lu','total_solves','lu_as_percentage','av_gmres','max_gmres'])

for k in k_list:
    
    this_directory = '/home/owen/Documents/running-code/running-nbpc/qmc-nbpc-adaptive/'

    for filename_tmp in listdir(this_directory):
        
        if fnmatch(filename_tmp,'k-'+str(k)+'*csv'):
            filename = this_directory+filename_tmp

    df = pd.read_csv(filename,usecols=[2,3])

    df_master.loc[k,'num_lu'] = df.LU.sum()

    df_master.loc[k,'total_solves'] = df.LU.count()

    df_master.loc[k,'lu_as_percentage'] = 100.0*df.LU.mean()

    df_master.loc[k,'av_gmres'] = df.GMRES.mean()

    df_master.loc[k,'max_gmres'] = df.GMRES.max()

print(df_master)

column_names = [r'\# LU factorisations',r'\makecell{Total \#\\linear systems}',r'\makecell{\# LU factorisations$/$\\\# linear systems}(\%)',r'\makecell{Average \#\\GMRES iterations}',r'\makecell{Max. \#\\GMRES iterations}']

float_format = '{:.2f}'.format # Based on formatting described at https://pyformat.info/#number
# Helped debug using https://stackoverflow.com/a/20937592

column_format = 'Sc Sc Sc Sc Sc'

table_name = 'nbpc-qmc-sequential-table.tex'

with open(table_name,mode='w') as table:
    df_master.to_latex(table,header=column_names,float_format=float_format,column_format=column_format)

# This is a hack to get the table to print like I want

with fileinput.input(files=(table_name),inplace=True) as table:
    for line in table:
        if line.endswith('Sc}\n'):
            print(line[:-2]+' Sc}')        
        elif line.startswith('{}'):
            # This is the column names
            columns = ''
            for name in column_names:
                columns += (' & ' + name)
            print(r'$k$' +columns + r'\\')
        else:
            print(line)

# Also plot a graph

[fit_0,fit_1] = make_fits()

plt.plot(k_list,df_master['lu_as_percentage'],'ok',label='_irrelvanet')

plt.plot(k_list,fit_0 + fit_1*np.array(k_list),'--k',label=r'$'+str(fit_0)[:5]+' + '+str(fit_1)[:4]+r'k$')

plt.xlabel(r'$k$')

plt.legend()

plt.ylabel('Number of LU factorisations/Number of QMC points (%)')

plt.xticks([10,20,30])

plt.savefig('lu-graph.pgf')

#plt.show()
