import os, sys
import numpy as np
import homogrid_anal

# set the working directory
str_dir = r"/home/martin/Work"  # home
str_dir = r"C:/Martin/Work/qc_kilde_mat_jst_kf_pos" # work
os.chdir(str_dir)
str_fn = r"qc_kilde_mat_jst_kf_pos_Bornholm.txt"
str_dirdel = "/" # Unix style
str_dirdel = "/" # win style

# Build list of input data (id, E, N, ...)
lst_data = list()
print "opening:", str_dir, str_dirdel, str_fn
with open(str_dir+str_dirdel+str_fn, 'r') as f:
    for line in f:
        lst_line = [l for l in line.strip().split(" ")]
        tup_line = (int(lst_line[0]), float(lst_line[1]), float(lst_line[2]), int(lst_line[3]))
        #print tup_line
        lst_data.append(tup_line)
print "length( list of tuples):", len(lst_data)

# make numpy array, of coordinates only
col_north = 2
col_east = 1
lst_data_coor = [(d[col_east], d[col_north]) for d in lst_data]
print "A", lst_data_coor[:3]
npa_data_coor = np.asarray(lst_data_coor)
print "B", npa_data_coor[:3]

lst_grid_size = [100000,50000,10000,5000,1000,500,100]
# Append DKN LL-values
npa_data_coor = homogrid_anal.add_grid_ll_vals(npa_data_coor,lst_grid_size)
print "C", npa_data_coor[:3]

# Build dic of stat
dic_stat = homogrid_anal.grid_stat(npa_data_coor,lst_grid_size)
for keyn in dic_stat.keys()[:4]:
    print "dic_stat", keyn, str(type(dic_stat[keyn]))
    for keynn in dic_stat[keyn].keys()[:4]:
        print "  two:", keynn, dic_stat[keyn][keynn]
sys.exit(0)

# Append Final lable, given a specific 'max points per cell' value
npa_data = homogrid_anal.add_lable(npa_data,dic_stat,1000)

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
print "first", npa_data[12345]

print "Done..."