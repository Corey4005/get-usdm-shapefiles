#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 16:03:20 2022

Here I am showing how data can be collected for 20 years for 18 USDA SCAN soil 
moisture stations across alabama from USDM shapefiles collected by get_usdm.py. 


@author: cwalker
"""

import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point
import numpy as np


#scan meta data
print(os.getcwd())
SCAN_META = os.path.join(os.getcwd(), './usdascan/SCAN_METADATA.csv')

#df of points and geodataframe set to the same coordinate reference system as the drought monitor
df = pd.read_csv(SCAN_META)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs='EPSG:4326')

#shapefiles
shapes = os.getcwd() + '/shapefiles'
outdata= os.path.join(os.getcwd(), './outdata/')

#list to store shapefiles
shapefiles = []
#get all of the shapefiles in the directory 
for root, dirs, files in os.walk(shapes):
    for f in files:
        if f.endswith(".shp"):
            shapefiles.append(os.path.join(root, f))
            


#lists to collect information
drought_category = [] #represents drought category
points = [] #represents point location of station
file_names = [] #represents the filename we will loop through
station_names = [] #represents stationname
count = 0 #represents count of file
stations_test = pd.Series(gdf['Station Name']) # a list of station names to compare true intersections against
numshapefiles = len(shapefiles)
for file in shapefiles:
    DM = gpd.read_file(file) #read the drought shapefile
    filename = file[-12:-4] #filename
    numpolygons = len(DM)
    print("\n")
    print('processing {} file count: {}/{}, polygons in file:{}'.format(filename, count, numshapefiles, numpolygons))
    count += 1
    stations_true = [] #used to get if station had a drought category for a particular day. Can be 0, to represent no stations had a drought category
    for p in range(len(DM['geometry'])): #p represents the polygon in each DM file of particular drought category
        poly = DM['geometry'][p] #represents polygon for drought category
        category = DM.iloc[p].DM #provides an integer value between 0-4
        
        for i in range(len(gdf)): #loop through all the points in the gdf
            point = Point(gdf.loc[i].geometry.x, gdf.loc[i].geometry.y) #create a lat lon point object for each point
            stationName = gdf.loc[i]['Station Name'] #station name of point
            pointSeries = gpd.GeoSeries([point]) #creating a geoseries that can be compared to polygon, which is a multipolygon object
            intersects = pointSeries.intersects(poly) #does point intersect polygon?
            if intersects[intersects.index==0].item() == True: #if so, give me the category and tell me that this point was true for a particular day. Point can be "none", which will be handled later
                stations_true.append(stationName)#used to create a series that can be compared to all stations to find non-drought station names for a particular file
                file_names.append(filename)
                points.append(point)
                station_names.append(stationName)
                drought_category.append(category)
                print(stationName, point, category)
    #do some logic here to get the stations that were "None" or contained no drought for a particular file
    
    #if no stations crossed a drought polygon, then just apply none to each station in the station list
    #and append this information to the dataframe lists
    if len(stations_true)==0:
        for s in stations_test:
            stationFrame = gdf[gdf['Station Name']==s]
            point = stationFrame['geometry'].item()
            file_names.append(filename)
            points.append(point)
            station_names.append(s)
            drought_category.append(np.nan)
            print(s, point, "None")
    #else, we will compare the stations that do cross a polygon to the overall stations list and 
    #find those that would be "None" for a particular day
    else:
        stations_true = pd.Series(stations_true)
        stations_none = stations_test[~stations_test.isin(stations_true)] #find the stations that were false in stations list
        for s in stations_none:
            stationFrame = gdf[gdf['Station Name']==s]
            point = stationFrame['geometry'].item()
            file_names.append(filename)
            points.append(point)
            station_names.append(s)
            drought_category.append(np.nan)
            print(s, point, "None")

print("\n")
print("Processing complete!")
#create a dataframe that can be sent to .csv for analyis    
drought_data = pd.DataFrame()
drought_data['date']=file_names
drought_data['point']=points
drought_data['Category']=drought_category
drought_data['station_names']=station_names
drought_data.set_index('date', inplace=True)
drought_data.sort_index(inplace=True)

drought_data.to_csv(outdata+"drought_category_by_scan_site.csv")