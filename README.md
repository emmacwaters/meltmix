# meltmix

This files in melt mix contain code used in the manuscript "Mantle source and melting processes beneath Iceland’s Flank and Rift Zones: Forward Modelling of Heterogeneous Mantle Melting beneath Iceland" by E. Waters et al.

The code can be used with outputs from the program REEBOX Pro to model melt mixing from a heterogeneous mantle and compare the results of this modelling to sample compositional data to find potential matches

There are 4 files in the project:

lherzolite_homogenisation.py - for homogenising lherzolite instanateous melts calculated by REEBOX Pro.

misfit_bulkcrust.py - compares modelled column accumulate melts from REEBOX Pro to sample compositional data to find potential matches.

meltmix_homogenised.py - mixes a deep melt component with variuos lherzolite melt compositions and compares the output compositions to sample data to find potential matches

meltmix_filter.py - filters the outputs from meltmix_homogenised.py to identfy the best fit to sample data
