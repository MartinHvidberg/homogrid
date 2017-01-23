import os, sys
import numpy as np
import homogrid_anal

### Hardcoded values ###
# set the working directory
str_dir = r"/home/martin/Work"  # home
str_dir = r"C:/Martin/Work/qc_kilde_mat_jst_kf_pos" # work
os.chdir(str_dir)
str_fn = r"qc_kilde_mat_jst_kf_pos_DK.txt" #                                    -- Lus (qc_kilde_mat_jst_kf_pos_Bornholm.txt/qc_kilde_mat_jst_kf_pos_DK.txt)
str_out_fn = r"qc_kilde_mat_jst_kf_posDK_hg1000.txt" #                         -- Lus (qc_kilde_mat_jst_kf_pos_Bornholm_hg1000.txt/qc_kilde_mat_jst_kf_pos_DK_hg1000.txt)
str_dirdel = "/" # Unix style
str_dirdel = "/" # win style
# assumed order of each line, first column being 0
num_north = 2
num_east = 1
csv_delim = " " # file is 'space delimited'
# set grid sizes to use
lst_grid_size = [100000,50000,10000,5000,1000,500,100]
# criteria: max points per grid-cell
num_max_points = 1000

# Build list of input data (id, E, N, ...)
lst_data = list()
print "opening:", str_dir, str_dirdel, str_fn
with open(str_dir+str_dirdel+str_fn, 'r') as f:
    lst_lines = f.readlines()
    
for line in lst_lines:
    lst_line = [l for l in line.strip().split(" ")]
    tup_line = (int(lst_line[0]), float(lst_line[1]), float(lst_line[2]), int(lst_line[3]))
    #print tup_line
    lst_data.append(tup_line)

print "length( list of tuples):", len(lst_data)

# make numpy array, of coordinates only
col_north = 2
col_east = 1
lst_data_coor = [(d[col_east], d[col_north]) for d in lst_data]
print "\nA", lst_data_coor[:3]
npa_data_coor = np.asarray(lst_data_coor)
print "\nB", npa_data_coor[:3]

# Append DKN LL-values
npa_data_coor = homogrid_anal.add_grid_ll_vals(npa_data_coor,lst_grid_size)
print "\nC", npa_data_coor[:3]

# Build dic of stat
print "\nD"
dic_stat = homogrid_anal.grid_stat(npa_data_coor,lst_grid_size)

print "\nE"
for keyn in dic_stat.keys():
    print "dic_stat", keyn, str(type(dic_stat[keyn]))
    for keynn in dic_stat[keyn].keys()[:4]:
        print "  two:", keynn, dic_stat[keyn][keynn]
        
# Write output file, appending Final lable, given a specific 'max points per cell' value
print "\nF"
finest_grid = sorted(lst_grid_size)[0:1]
print "finest_grid",finest_grid 
if len(lst_lines) == len(npa_data_coor):
    print "length match between raw file read and numpy matrix:", len(npa_data_coor)
with open(str_out_fn, "w") as outfile:
    for n in range(len(lst_lines)-1): # Count through raw file read and numpy matrix
        lst_line = lst_lines[n].split(csv_delim)
        num_coor_n = float(lst_line[num_north].strip()) # if lats in line, may include '\n', just being causious...
        num_coor_e = float(lst_line[num_east].strip())
        all_coor = npa_data_coor[n]
        best_cell = homogrid_anal.best_grid_cell((num_coor_e,num_coor_n),all_coor,dic_stat,num_max_points)
        if n == 136:
            print "\ng:case..."
            print "line", lst_line
            print "num_coor:", num_coor_e, num_coor_n
            print "allcoor:", str(type(all_coor)), all_coor
            print "bestcell:", best_cell
        outfile.write(lst_lines[n].strip()+csv_delim+best_cell+"\n")
print "closed out file:", outfile

print "Done..."
sys.exit(0)
