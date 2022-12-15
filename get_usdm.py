#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This is an example python file to automate the collection of shapefiles for 20
years from the USDM page using wget and a textfile. 
 
Created on Thu Dec 15 14:59:16 2022

The link for GIS shapefile data: 
    
https://droughtmonitor.unl.edu/DmData/GISData.aspx

Example link string for zip file containing CONUS shapefile
https://droughtmonitor.unl.edu/data/shapefiles_m/USDM_20001226_M.zip

@author: cwalker
"""

#to create the list of datetstamps for 20 years of shapefiles
# we need datestamps being incremented by a timedelta of 7 days
from datetime import datetime, timedelta
import os
import shutil
import sys
#datestamps and desired timedelta until the end date
starting_date = str(sys.argv[1]) #the first date in usdm database entered from command line
ending_date = str(sys.argv[2]) #the last date in usdm database for 2020 entered from command line

if len(starting_date) < 8:
    print('Make sure starting date is yyyymmdd format!')
    os.exit(1)

if len(ending_date) < 8:
    print('Make sure ending date is yyyymmdd format!')

#delta we need to increment time by
day_delta = 7 #days

#convert the start and end date to timestamps
start_stamp = datetime.strptime(starting_date, '%Y%m%d').date()
end_stamp = datetime.strptime(ending_date, '%Y%m%d').date()

#list to collect the data
date_list = []

#while loop to create timestamps and append to list
while start_stamp != (end_stamp+timedelta(days=day_delta)):
    date_list.append(start_stamp)
    start_stamp = start_stamp+timedelta(days=day_delta)
    
#now we will create the link structures
#we will need a standard string and the append each of the 
#correct dates to the end.

#standard string 
standard_string = 'https://droughtmonitor.unl.edu/data/shapefiles_m/USDM_'

#list to collect strings
links = []

for i in range(len(date_list)):
    #dateinformation for each string
    dateyear = str(date_list[i].year)
    datemonth = date_list[i].month
    dateday = date_list[i].day

    #if datemonth is less than 10, we will add a 0 to it so that its correct 
    #in the link
    if datemonth < 10: 
        datemonth = "0" + str(datemonth)
    else: 
        datemonth = str(datemonth)
        
    if dateday < 10:
        dateday = "0"+str(dateday)
    else: 
        dateday = str(dateday)
    #now make each string with correct information
    link = standard_string + dateyear + datemonth + dateday + "_M.zip"
    links.append(link)
#now we will add the strings to the textfile so that we 
#can call wget on it and download all the files


#here we will delete the usdm_links.txt file for every iteration
#that this script is run so that you do not get
#errors where old lines are appended to the new lines
#we will also create a new shapefiles directory 
#for each iteration so that you get the shapefiles for 
#the selected dates only. 
textfile_out = os.getcwd() + '/usdm_links.txt' #textfile for wget to operate on
shapefiles_dir = os.getcwd() + '/shapefiles' #directory for shapefiles 

#delete the shapefiles dir if it exists
if os.path.exists(shapefiles_dir):
    shutil.rmtree(shapefiles_dir)

#delete the textfile if it exists
if os.path.exists(textfile_out):
    os.remove(textfile_out)


#create the usdm.txtfile and write to it
print('\n')
print('Appending HTTP links to download file: ')
with open(textfile_out, 'w') as f:
    for link in links:
        f.write("{}\n".format(link))
        print(link + ' added to {}'.format(textfile_out[-14:]))

#create the data dir to dump USDM shapefiles into for selected dates
os.mkdir(shapefiles_dir)

print('\nDownload file is ready for wget!\n')
print('Run the following command:\n wget -i usdm_links.txt -P shapefiles/ --progress=bar:force:noscroll\n')


