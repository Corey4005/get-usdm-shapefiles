#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 15:16:02 2022

This is a module to unzip all of the downloaded shapefiles in the /shapefiles
directory that is created by get_usdm.py. 

Open a command prompt and run the following command when shapefiles 
exist in the /shapefiles directory.

command: python unzip.py

@author: cwalker
"""

import zipfile
import os

#get the current directory and add it to shapefiles
currentDir = os.getcwd()
shapeDir = currentDir + '/shapefiles'

#if shapefiles is not there, don't unzip anything and exit
if not os.path.exists(shapeDir):
    print('No shapefiles to unzip!')
    os.exit(1)
    
#find all filepaths with .zip and store in list
for root, dirs, files in os.walk(shapeDir):
    for f in files:
        if f.endswith(".zip"):
            zippy = os.path.join(root, f) #zipfile to unzip
            with zipfile.ZipFile(zippy, 'r') as zip_ref:
                zip_ref.extractall(shapeDir)
                print('Unizipped {} from .zipfile into /shapefiles!'.format(f[0:13]))
