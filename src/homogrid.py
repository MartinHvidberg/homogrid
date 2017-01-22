import os, sys
import ogr
import numpy as np

""" Homogeneous gridding of inhomogeneous point swarms """

# set the working directory
os.chdir(r"/home/martin/Work")

# open the output text file for writing
file = open('qc_kilde_mat_jst_kf_pos.txt', 'w')

# get the shapefile driver
driver = ogr.GetDriverByName('ESRI Shapefile')

# open the data source
datasource = driver.Open(r"qc_kilde_mat_jst_kf_pos.shp", 0)
if datasource is None:
    print 'Could not open file'
    sys.exit(1)

# get the data layer
layer = datasource.GetLayer()

# Get Shapefile Fields and Types
layerDefinition = layer.GetLayerDefn()

print "Name  -  Type  Width  Precision"
for i in range(layerDefinition.GetFieldCount()):
    fieldName =  layerDefinition.GetFieldDefn(i).GetName()
    fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
    fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
    fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
    GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()
    print fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision)

# loop through the features in the layer, write selected fields to an output text file, and save them in a list of tuples
feature = layer.GetNextFeature()
lst_data = list()
h1, h0 = (0,0)
while feature:
    # get the attributes
    id = feature.GetFieldAsString('feat_id')
    komm = feature.GetFieldAsString('komkode')

    # get the x,y coordinates for the point
    geom = feature.GetGeometryRef()
    x = geom.GetX()
    y = geom.GetY()
    
    # lus                                                                             # lus Bornholm
    if x>800000:
        h1 += 1
        # write info out to the text file
        file.write(str(id) + ' ' + str(x) + ' ' + str(y) + ' ' + str(komm) + '\n')
        # add to list
        lst_data.append((int(id),float(x),float(y),int(komm)))
    else:
        h0 += 1
    
    # destroy the feature and get a new one
    feature.Destroy()
    feature = layer.GetNextFeature()

# close the data source and text file
datasource.Destroy()
file.close()

print "hit:", h1, "nay:", h0

# make numpy array
npa_data = np.asarray(lst_data)
print "npa:", npa_data

print "Done..."