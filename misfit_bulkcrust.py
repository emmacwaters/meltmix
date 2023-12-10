# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:30:23 2020

@author: mbexwew4
"""

##this code compares the bulk crust/ aggregate melt compositions calculate by REEBOX Pro and compares them to sample data to determine a chi-sqaured misfit

#import libraries to run code
from pandas import read_csv
from pandas import DataFrame


#import compositional data

#bc is column accumulate data file output by REEBOX Pro, replace filename with name of file
bc = read_csv('filename.csv')

#for data input a csv with the average composition determined for the area of interest, replace filename with name of file
data = read_csv('filename.csv')

#for standard deviation input a cvs with the standard deviation of element from elements in an area of interest, replace filename with name of file
stddev = read_csv('filename.csv')



#define trace elements used, ensure the labels match those in the input files
labels = ['P', 'TC', 'Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu']
#select trace elements to model
traces = ['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu']
##P = pressure, T = temperature, F_per = fraction of melting of peridotite, F_px = fraction of melting of pyroxenite
# X_per = proportion of peridotite melt in agregate, #X_pxproportion of pyroxenite melt in aggregate
P = ['P']
T = ['TC']
F_per = ['F anhydrous peridotite']
X_per = ['X_per_dry']
F_px = ['F KG1']
X_px = ['X_KG1']
headings = ['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu', 'P(KG1)', 'T(KG1)', 'P(bc)', 'T(bc)', 'misfit']

#target composition data, determines the average composition the model is trying to match
data_target = list(data.iloc[0][traces].T)
stddev = list(stddev.iloc[0][traces].T)



#define bulk crust aggregate data frame trace elements, ensure labels are the same as csv

#P = pressure, T = temperature, F_per = fraction of melting of lherzolite, F_px = fraction of melting of pyroxenite
# X_per = proportion of lherzolite melt in agregate, #X_px proportion of pyroxenite melt in aggregate
bc_traces = bc[traces]
bc_labels = bc[labels]
bc_P = bc[P]
bc_T = bc[T]
bc_F_per = bc[F_per]
bc_X_per = bc[X_per]
bc_F_px = bc[F_px]
bc_X_px = bc[X_px]

#chisquared function
def chisquared (model, target, error):
    total = 0
    for n, el in enumerate(model):
        chi_sq = ((target[n] - model[el])/(error[n]))**2
        total = total + chi_sq
    return total
    #print (total)
    
   
#the following code runs the misfit calculation and stores the results in a new dataframe called compare
   
misfit = chisquared(bc_traces, data_target, stddev)
compare = DataFrame(bc_traces)
compare['P(bc)']=bc_P
compare['T(bc)']=bc_T
compare['F_per']=bc_F_per
compare['F_px']=bc_F_px
compare['X_per']=bc_X_per
compare['X_px']=bc_X_px
compare['misfit']=misfit
 
#defines what the accepatble chi-squared misfit is, adjust his to suit the number of elements being calculated  
accepted_fit = compare[(compare.misfit <= 21.026)]
compiled_mix_traces = accepted_fit[traces]


        
#outputs files with those in acceptable misfit range and all the possible results to 2 csv files
print(accepted_fit)
accepted_fit.to_csv('result.csv')
compare.to_csv('all_model_results.csv')
