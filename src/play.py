import numpy as np

a = np.array([[1,2,3],[2,3,4]])
print a

b = np.insert(a, 3, values=7*(a[:,2]), axis=1) # insert values before column 3
print b