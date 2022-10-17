# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:38:22 2021

@author: mbexwew4
"""

##this code takes output instant melts from REEBOX Pro and homogenises them, outputting to new csv files


#import libraies
from pandas import read_csv
import numpy as np
from pandas import DataFrame


#import data files
#lhz in the instant melt compositions file outpur from REEBOX Pro, replace filename with name of csv
lhz = read_csv('filename.csv')
df = DataFrame(lhz)
#use traces to define the elements you wish to work with
traces = ['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu']

lhz_traces = lhz[traces]
arr = np.array(lhz_traces)


#in the input file label pressure as P and the fraction of melting of the lherzolite as F_lhz
P = lhz.P
F = lhz.F_lhz

#c determines the number of melt compositions to homogenise, this can be altered but ensure the final number is the number of rows in the csv
c= [3, 5, 7, 10, 15, 20, 25, 50, 100, 150, 195]
labelled_mix = DataFrame(columns=['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu', 'P_min', 'P_max', 'F_min', 'F_max'])


#the following code performs the homogenisation and adds the new homogenised composition to a new dataframe, 
#P_max and P_min define the max and min pressure melts in mix are derived from
#F_max and F_min define the max and min fractions of melting melts in mix are derived from
for j in c:
    mixed_lhz = []
    for i in range(0, len(arr)):
        if i < (len(arr)-j):
            mix_arr = arr[i:(i+j)]
            homogenise = sum(mix_arr*(1/j))
            homogenise = list(homogenise)
            P_max = P[i]
            P_min = P[i+(j-1)]
            F_max = F[i]
            F_min = F[i+(j-1)]
            homogenise.append(P_min)
            homogenise.append(P_max)
            homogenise.append(F_min)
            homogenise.append(F_max)
            mixed_lhz.append(homogenise)

        mixed = DataFrame(mixed_lhz, columns=['Nb', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Dy', 'Y', 'Er', 'Yb', 'Lu', 'P_min', 'P_max', 'F_min', 'F_max'])
        mixed.to_csv('homogenised_EVZ_{step}step.csv'.format(step=j))