import os, sys
#import ogr
import numpy as np
import homogrid_anal

# set the working directory
str_dir = r"/home/martin/Work" 
os.chdir(str_dir)
str_fn = r"qc_kilde_mat_jst_kf_pos_Bornholm.txt"
str_dirdel = r"/"

# Build list of input data (id, E, N, ...)
lst_data = list()
with open(str_dir+str_dirdel+str_fn, 'r') as f:
    for line in f:
        lst_line = [l for l in line.strip().split(" ")]
        tup_line = (int(lst_line[0]), float(lst_line[1]), float(lst_line[2]), int(lst_line[3]))
        #print tup_line
        lst_data.append(tup_line)
print "length( list of tuples):", len(lst_data)

# make numpy array
npa_data = np.asarray(lst_data)
del lst_data

lst_grid_size = [100000,50000,10000,5000,1000,500,100]

# Append DKN lables
npa_data = homogrid_anal.add_gridvals(npa_data,lst_grid_size)
# Build dic of stat
dic_stat = homogrid_anal.grid_stat(npa_data,lst_grid_size)
print "dic_stat", dic_stat
# Append Final lable, given a specific 'max points per cell' value
npa_data = homogrid_anal.add_lable(npa_data,dic_stat,1000)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
print "first", npa_data[12345]

print "Done..."