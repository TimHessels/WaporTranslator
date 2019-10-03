# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 09:12:46 2019

The output unit is mW m^-2 sr^-1 (cm^-1)^-1.
To get W/m2 divide the tiff file by 10^-6

"""

import os
import gdal
import bz2
import datetime
import pandas as pd
import shutil

def main(output_folder_L1, End_year_analyses, latlim, lonlim):

    # Get Date range
    Startdate = "2016-01-01"
    Enddate = "%s-12-31" %End_year_analyses
    Dates = pd.date_range(Startdate, Enddate, freq = "D")
    
    # Select input folder LANDSAF data
    input_folder = os.path.join(output_folder_L1, "LANDSAF")
    os.chdir(input_folder)
    
    # Set formats of bz files
    LSASAF_bz2_format_DLSF = "HDF5_LSASAF_MSG_DIDSLF_MSG-Disk_{yyyy}{mm:02d}{dd:02d}0000.bz2"
    LSASAF_bz2_format_DSSF = "HDF5_LSASAF_MSG_DIDSSF_MSG-Disk_{yyyy}{mm:02d}{dd:02d}0000.bz2"    
    
    for One_Date in Dates:
        
        # Process Downward Long Wave  
        filename_in = LSASAF_bz2_format_DLSF.format(yyyy = One_Date.year, mm = One_Date.month, dd = One_Date.day)
        if os.path.exists(filename_in):
            Process_LSASAF(input_folder, filename_in, latlim, lonlim, Parameter = "DSLF")
        else:
            print("ERROR: filename %s does not exists!!!" % filename_in)      
            
        # Process Downward Shortwave   
        filename_in = LSASAF_bz2_format_DSSF.format(yyyy = One_Date.year, mm = One_Date.month, dd = One_Date.day)   
        if os.path.exists(filename_in):
            Process_LSASAF(input_folder, filename_in, latlim, lonlim, Parameter = "DSSF")
        else:
            print("ERROR: filename %s does not exists!!!" % filename_in)
            
    # remove trash folder        
    trash_folder = os.path.join(input_folder, "Trash")    
    shutil.rmtree(trash_folder)      
        
    return()
    

def Process_LSASAF(input_folder, filename_in, latlim, lonlim, Parameter = "DSLF"):
    
    # Create output folder
    output_folder = os.path.join(input_folder, Parameter)
    if not os.path.exists(output_folder):
       os.makedirs(output_folder)
    
    # Create input path
    filename_path_in = os.path.join(input_folder, filename_in)
    
    # Get Filename
    filename_without_ext = os.path.splitext(filename_path_in)[0]  
    
    # Get date
    Date_str = filename_without_ext.split("_")[-1]
    Date = datetime.datetime.strptime(Date_str, "%Y%m%d0000")
    
    # unzip
    filename_HDF5 = ''.join([filename_without_ext, '.HDF5'])
    with open(filename_HDF5, 'wb') as new_file, bz2.BZ2File(filename_path_in, 'rb') as file:
        for data in iter(lambda : file.read(100 * 1024), b''):
            new_file.write(data)
    
    # Create Trash Bin
    trash_folder = os.path.join(input_folder, "Trash")
    if not os.path.exists(trash_folder):
        os.makedirs(trash_folder)
        
    # Get Filename
    filename_basename = os.path.basename(filename_path_in)
    filename_basename_without_ext = os.path.splitext(filename_basename)[0]
    filename_basename_tiff = ''.join([filename_basename_without_ext, '.tif'])
    
    # give projection to MSG disk
    output_filename = os.path.join(trash_folder, filename_basename_tiff)
    input_filename = ''.join(['HDF5:"', "%s" %filename_HDF5, '"://%s' %Parameter])        
    Set_MSGdisk_Projection(input_filename, output_filename)
    
    # Clip array to area of interest
    input_filename = output_filename
    output_format = "%s_LSASAF_MSG_{yyyy}.{mm:02}.{dd:02}.tif" %Parameter
    output_filename = os.path.join(output_folder, output_format.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
    Clip_Reproject_Tiff(input_filename, output_filename, latlim, lonlim)
    return()

def Set_MSGdisk_Projection(input_filename, output_filename):        
    
    options_list = ['-a_srs "+proj=geos +a=6378169 +b=6356583.8 +lon_0=0 +h=35785831"',
               '-a_ullr -5570248.832537 5570248.832537 5570248.832537 -5570248.832537']
    options_string = " ".join(options_list)
    
    gdal.Translate(output_filename, input_filename, options = options_string)
    return()
    
def Clip_Reproject_Tiff(input_filename, output_filename, latlim, lonlim):    

    options_list = [ '-s_srs "+proj=geos +lon_0=0 +h=35785831 +x_0=0 +y_0=0 +a=6378169 +b=6356583.8 +units=m +no_defs"',
                    '-t_srs EPSG:4326',
                    '-te %f %f %f %f' %(lonlim[0], latlim[0], lonlim[1], latlim[1])]
    options_string = " ".join(options_list)    
    gdal.Warp(output_filename, input_filename, options = options_string) 
    return()