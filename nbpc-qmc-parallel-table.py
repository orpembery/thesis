import pandas as pd
from os import listdir
from fnmatch import fnmatch
import pickle
import numpy as np
import fileinput

k_list = [10.0,30.0,40.0,50.0,60.0]

df_master = pd.DataFrame(index=[int(k) for k in k_list],columns=['num_lu','total_solves','lu_as_percentage','av_gmres','max_gmres'])

this_directory = './data/data-for-nbpc-qmc/'

for k in k_list:
    print(k)
    # Find the right directory

    for possible_folder in listdir(this_directory):
        
        if fnmatch(possible_folder,'*-k-'+str(k)+'*'):
            filename = this_directory+possible_folder+'/output-h_magnitude-1.0.pickle'

    with open(filename,'rb') as f:
        qmc = pickle.load(f)

    GMRES_its = qmc[3][0]

    df_master.loc[k,'num_lu'] = sum(np.array(GMRES_its)==1)

    df_master.loc[k,'total_solves'] = len(GMRES_its)

    df_master.loc[k,'lu_as_percentage'] = 100.0*df_master.loc[k,'num_lu']/df_master.loc[k,'total_solves']

    df_master.loc[k,'av_gmres'] = np.mean(GMRES_its)

    df_master.loc[k,'max_gmres'] = max(GMRES_its)

column_names = [r'\# LU factorisations',r'\makecell{Total \#\\linear systems}',r'\makecell{\# LU factorisations$/$\\\# linear systems}(\%)',r'\makecell{Average \#\\GMRES iterations}',r'\makecell{Max. \#\\GMRES iterations}']

float_format = '{:.2f}'.format # Based on formatting described at https://pyformat.info/#number
# Helped debug using https://stackoverflow.com/a/20937592

column_format = 'Sc Sc Sc Sc Sc'

table_name = 'nbpc-qmc-parallel-table.tex'

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

            

