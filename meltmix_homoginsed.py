# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:30:23 2020

@author: mbexwew4
"""
##This code mixes the deep melt component with various homogeneised lherzolite melt composition and compares the result to sample data using a chi-squared misfit calculation

#import libraries
from pandas import read_csv
from pandas import DataFrame
from pandas import concat


#import data

#deep is the single melt composition determined to represent the homogenised deep melt, replace filename with name of csv file
deep = read_csv('filename.csv')
#lhz is the lherzolite melt compositions to be used in the model, replace filename with name of csv
lhz = read_csv('filename.csv')
#ave is the average melt inclusion composition determined for the area of interest, replace filename with name of csv
ave = read_csv('filename.csv')
#stddev is the standard deviation of the average melt inclusion composition for the area of interest, replace file name with name of csv
stddev = read_csv('filename.csv')
#frace is the proportions of deep and lherzolite melt to be used in the mixture, column headings in csv should be lhz_frac abd deep_frac and proportions between 0 an 1, totally 1 (i.e. 0.2 = 20%)
fracs = read_csv('filename.csv')

#define labels in input csv, max and min values come from homogenising lherzolite melts and selecting the highest and lowest pressure and fractions of melt involved
labels = ['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu', 'P_min', 'P_max', 'F_min', 'F_max']

#define trace elements used, ensure trace elements to be modelled are included
traces = ['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu']

#labels in csv defined, ensure these match in input csvs
#P = pressure, T=temperature, F_deep = fraction of melting of pyroxenite in deep melt
P = ['P']
T = ['TC']
F_deep = ['F_px']
headings = ['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu', 'P(deep)', 'T(deep)', 'F(deep-px)', 'P_max(LHZ)', 'P_min(LHZ)', 'F(LHZ)', 'misfit']

#target composition data, selects target for misfit calculation to attempt to match
data_target = list(ave.iloc[0][traces].T)
stddev = list(stddev.iloc[0][traces].T)


#define data frame trace elements
deep_traces = deep[traces]
lhz_traces = lhz[traces]
lhz_labels = lhz[labels]
deep_P = deep[P]
deep_T = deep[T]
deep_F = deep[F_deep]

#define melt proportions to be used in mixing calculations
frac_lhz = fracs.lhz_frac
frac_deep = fracs.deep_frac


#chisquared function defined
def chisquared (model, target, error):
    total = 0
    for n, el in enumerate(model):
        chi_sq = (target[n] - model[el])/(error[n])**2
        total = total + chi_sq
    return total
    
    
   


# The follow code selects the proportions of each melt source and mixes the compoitions in these proportions, different lhz homogenised melts are mixed with the deep melt component. 
# The mixed compositions are added to a new dataframe and evaluated by the chisquared function with the misfit values
# P in output dataframe refers to pressure and F to the fraction of melting that a lithology has undergone

for p in range(0, len(fracs)):
    possiblefits = DataFrame(columns=['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu', 'P(deep)', 'T(deep)', 'F(deep-px)', 'P_min(LHZ)', 'P_max(LHZ)', 'F_min(LHZ)', 'F_max(LHZ)', 'misfit', 'lhz %', 'deep %'])
    lhz_frac=(frac_lhz.iloc[p])
    deep_frac=(frac_deep.iloc[p])
    print(lhz_frac)
    print(deep_frac)
    #select melt from lhz pressure/temperature step   
    for i in range (0, len(lhz_traces)):
        lhz_position = DataFrame(lhz_labels.iloc[i]).T
        lhz_melt = list(lhz_traces.iloc[i])
        mixed = {}
        for n, el in enumerate(lhz_traces):
            single_mixed_el = (lhz_melt[n]*lhz_frac) + (deep_traces[el]*deep_frac)
            mixed[el] = single_mixed_el
        #creates DataFrame of the results of all pyroxenite melts mixed with each lherzolite melt fraction (inlcudes PT conditions)
        mixed_composition = DataFrame.from_dict(mixed)
        #calculate chi-squared value
        misfit = chisquared(mixed_composition, data_target, stddev)
        #create labelled dataframe
        compiled_mix = mixed_composition
        compiled_mix['P(deep)'] = deep_P
        compiled_mix['T(deep)'] = deep_T
        compiled_mix['F(deep-px)'] = deep_F
        compiled_mix['P_min(LHZ)'] = lhz_labels.iloc[i].P_min
        compiled_mix['P_max(LHZ)'] = lhz_labels.iloc[i].P_max
        compiled_mix['F_min(LHZ)'] = lhz_labels.iloc[i].F_min
        compiled_mix['F_max(LHZ)'] = lhz_labels.iloc[i].F_max
        compiled_mix['misfit'] = misfit
        compiled_mix['lhz %'] = lhz_frac
        compiled_mix['deep %'] = deep_frac
        
   
        #filtered data for acceptable results and add to possible results Data Frame, mixes from peridotite melts from deeper than the deep component is removed
        accepted_fit = compiled_mix[(compiled_mix['P(deep)'] > compiled_mix['P_min(LHZ)'])]
        if not accepted_fit.empty:
            combine = [possiblefits, accepted_fit]
            result = concat(combine)
            possiblefits = result
            print(result)
        else:
            print('no acceptable results')
            
    #outputs results to a csv file, this is not filtered for the misfit value   
    print(possiblefits)
    possiblefits.to_csv('possiblefits_{lhz}lhz_{deep}deep.csv'.format(lhz=lhz_frac, deep=deep_frac))
       