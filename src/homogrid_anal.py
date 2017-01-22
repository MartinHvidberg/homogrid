import numpy as np
import math

""" Anlyze module for - Homogeneous gridding of inhomogeneous point swarms """

def add_gridvals(npa_data,lst_grid_size):
    """ adds DKN cell names to each record, as new fields
    input npa_data (numpy array), with col0=id, col1=East, col2=North, other columns ignored, but preserved
    input lst_grid_size (list of integers): like [100000,50000,10000,5000,1000,500,100]
    output npa_data, with some added columns. """
    
    lst_grid_size.sort() # Sort assending, as each new col is inserted _before_ col 3, and therefore ends up reversed
    a = npa_data
    for n in lst_grid_size:
        # Northing
        vals = [n*math.floor(v/n) for v in a[:,1]] # floor down to nearest n
        factor = str(n).count('0')+2 # how many digits to clip
        vals = [int(str(v)[:-factor]) for v in vals] # clip digits from the floored value
        a = np.insert(a, 3, values=vals, axis=1) # insert values before column 3
        # Easting
        vals = [n*math.floor(v/n) for v in a[:,2]] # floor down to nearest n
        factor = str(n).count('0')+2 # how many digits to clip
        vals = [int(str(v)[:-factor]) for v in vals] # clip digits from the floored value
        a = np.insert(a, 3, values=vals, axis=1) # insert values before column 3
    return a

def grid_stat(npa_data,lst_grid_size):
    """ For each grid size, make a dic of the occurences of each N and E value """
    dic_stat = dict()
    for s in enumerate(sorted(lst_grid_size, reverse=True)):
        dic_stat[s[1]] = dict()
        unique, counts = np.unique(npa_data[:,3+(2*s[0])], return_counts=True)
        dic_stat[s[1]]['N'] = dict(zip(unique, counts))
        print s[1], "zip Nor", dic_stat[s[1]]['N']
        unique, counts = np.unique(npa_data[:,4+(2*s[0])], return_counts=True)
        dic_stat[s[1]]['E'] = dict(zip(unique, counts))
        print s[1], "zip Eas:", dic_stat[s[1]]['E']
    return dic_stat

def add_lable(npa_data,dic_stat,max_cnt=1000):
    """ Find the lable for the largest cell, not containing more than max_cnt. """
    