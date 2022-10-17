# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 10:59:45 2020

@author: mbexwew4
"""

##this code filters the output csvs from the melt mix model to identify those results that are less than or equal to the acceptable chi misfit value

#import libraries
import glob
import pandas as pd

#selects all csv files in a folder, have all the files for filtering in one place
extension = 'csv'
result = glob.glob('*.{}'.format(extension))

print(result)

#defines column names in output dataframe
column_names = ["lhz_frac", "deep_frac", "min_misfit", "no_results"]

#new dataframe for results of filter
summary = pd.DataFrame(columns = column_names)

#filters data to ensure onlu lhz melts produced at lower pressures than the deep melt are mixed
#for each input csv the minium misfit in that file
#results are output to a summary csv highlighting the proportions of each lithology in the mix and the minimum misfit that resulted from the mixing proportions
for file in result:
    df = pd.read_csv(file)
    df_logic = df[df['P(LHZ)']<=df['P(deep)']]
    if not df_logic.empty:
        no_results = len(df_logic)
        min_misfit = df_logic['misfit'].min()
        lhz = df_logic.iloc[0]['lhz %']
        deep = df_logic.iloc[0]['deep %']
        new_data = pd.Series([lhz, deep, min_misfit, no_results], index=["lhz_frac", "deep_frac", "min_misfit", "no_results"])
        new_row = pd.DataFrame(new_data).T
        result =[summary, new_row]
        addition = pd.concat(result)
        summary = addition
print (summary)

#outputs the summary of the filter to a new csv labelled 'summary.csv'
summary.to_csv('summary.csv')
