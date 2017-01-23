import numpy as np
import math

""" Anlyze module for - Homogeneous gridding of inhomogeneous point swarms """

def add_grid_ll_vals(a,lgs):
    """ adds DKN cell Lower Left (LL) values to each record, as new fields
    input a (numpy array), with col0=East, col1=North, nothing else...
    input lgs "lst grid size" (list of integers): like [100000,50000,10000,5000,1000,500,100]
    output npa_data, with some added columns. """
    
    lgs.sort() # Sort ascending, as each new col is inserted _before_ col 2, and therefore ends up reversed
    for n in lgs:
        factor = str(n).count('0')+2 # how many digits to clip
        # Northing
        vals_n = [n*math.floor(v/n) for v in a[:,0]] # floor down to nearest n
        vals_n = [int(str(v)[:-factor]) for v in vals_n] # clip digits from the floored value
        a = np.insert(a, 2, values=vals_n, axis=1) # insert values before column 2
        # Easting
        vals_e = [n*math.floor(v/n) for v in a[:,1]] # floor down to nearest n
        vals_e = [int(str(v)[:-factor]) for v in vals_e] # clip digits from the floored value
        a = np.insert(a, 2, values=vals_e, axis=1) # insert values before column 2
    return a

def gridsize_to_kmlable(n):
    if n>=1000: # several kms
        return str(int(n/1000))+"km"
    else:
        return str(n)+"m"
    
def grid_stat(a,lgs):
    """ For each grid size, make a dic of the occurrences of each km_N_E lable
    input a (numpy array), with col0=East, col1=North, nothing else...
    input lgs "lst grid size" (list of integers): like [100000,50000,10000,5000,1000,500,100] """
    dic_stat = dict()
    for s in enumerate(sorted(lgs, reverse=True)):
        ##print s
        vals_lab = [gridsize_to_kmlable(s[1])+"_"+str(int(l[0]))+"_"+str(int(l[1])) for l in zip(a[:,2+(s[0]*2)],a[:,2+(s[0]*2)+1])]
        unique, counts = np.unique(vals_lab, return_counts=True)
        dic_stat[s[1]] = dict(zip(unique, counts))
    return dic_stat

def best_grid_cell(tup_coor,all_coor,dic_stat,max_cnt=1000):
    """ Find the lable for the largest cell, not containing more than max_cnt. """
    if isinstance(tup_coor, tuple):
        if len(tup_coor)==2:
            # maybe check if all_coor is <type 'numpy.ndarray'>?
            if isinstance(dic_stat, dict):
                if max_cnt > 0:
                    key_s = dic_stat.keys()
                    key_s.sort(reverse=True)
                    for n in range(len(key_s)):
                        lable_a = gridsize_to_kmlable(key_s[n])
                        lable_b = int(all_coor[2+(n*2)])
                        lable_c = int(all_coor[2+(n*2)+1])
                        lable = lable_a+"_"+str(lable_b)+"_"+str(lable_c)
                        cnt = dic_stat[key_s[n]][lable]
                        if  tup_coor == (863191.346501,6129949.6485):
                            print "Catch136", lable, cnt
                        if cnt<=max_cnt:
                            return lable
                    return lable
                else:
                    print "NOT positive integer:", str(type(max_cnt)), max_cnt
            else:
                print "NOT dict:", str(type(dic_stat)), dic_stat
        else:
            print "tuple NOT length 2:", str(type(tup_coor)), tup_coor
    else:
        print "NOT tuple:", str(type(tup_coor)), tup_coor
    return ""
    
    
