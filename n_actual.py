import numpy as np
from running_helmholtz_monte_carlo.calculate_m import calc_M, alpha
from pandas import DataFrame
import fileinput

k = np.array([10,20,30,40,50,60])

Ctilde = alpha(10) * np.log(2048.0)

N = np.round(np.exp(Ctilde / alpha(k)))

M_actual = (np.array([calc_M(kk) for kk in k]))

N_actual = 2.0**M_actual

column_names = [r'$\NQMC$',r'$\NQMCactual$']

df = DataFrame(index = k,columns=column_names)

for ii_k in range(len(k)):
    kk = int(k[ii_k])
    df.loc[kk,:] = [N[ii_k],N_actual[ii_k]]

column_format = 'Sc Sc Sc '

table_name = 'num-qmc-points-table.tex'

float_format = '{:.2f}'.format # Based on formatting described at https://pyformat.info/#number
# Helped debug using https://stackoverflow.com/a/20937592

with open(table_name,mode='w') as table:
    df.to_latex(table,header=column_names,float_format=float_format,column_format=column_format)

# This is a hack to get the table to print like I want

with fileinput.input(files=(table_name),inplace=True) as table:
    for line in table:
        if line.startswith('{}'):
            # This is the column names
            columns = ''
            for name in column_names:
                columns += (' & ' + name)
            print(r'$k$' +columns + r'\\')
        else:
            print(line)

