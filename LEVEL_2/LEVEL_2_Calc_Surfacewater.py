# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Mon Sep 30 19:57:54 2019
"""

import os
import gdal
import datetime
import pandas as pd
import calendar
import numpy as np

import WaporTranslator.LEVEL_2.LEVEL_2_Calc_Radiation as L2_Rad

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

def Calc_Surface_Runoff_P(output_folder_L2, Date, example_file):

    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
    
    # Create output folder for Surface_Runoff_P
    output_folder_Surface_Runoff_P = os.path.join(output_folder_L2, "Surface_Runoff_P")
    if not os.path.exists(output_folder_Surface_Runoff_P):
        os.makedirs(output_folder_Surface_Runoff_P)
   
    # Define output file
    filename_out = os.path.join(output_folder_Surface_Runoff_P, "Surface_Runoff_P_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
    if not os.path.exists(filename_out):
        
         # date in dekad
        day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date_datetime.day)))[0]), 2)))
        
        # Conversion WAPOR unit to mm/Dekade
        if day_dekad == 2:
            year = Date_datetime.year
            month = Date_datetime.month
            NOD = calendar.monthrange(year, month)[1]
        else:
            NOD = 10
        
        # define required filenames
        filei = os.path.join(input_folder_L1, "L2_I_D", "L2_I_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filep = os.path.join(input_folder_L1, "L1_PCP_D", "L1_PCP_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filecsr = os.path.join(output_folder_L2, "Storage_Coeff_Surface_Runoff","Storage_Coeff_Surface_Runoff_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
        
        # Open required files
        desti = RC.reproject_dataset_example(filei, example_file, 2)
        destp = RC.reproject_dataset_example(filep, example_file, 2)
        destcsr = gdal.Open(filecsr)
        
        # Get georeference
        geo = destcsr.GetGeoTransform()
        proj = destcsr.GetProjection()
           
        # Open Arrays
        I = desti.GetRasterBand(1).ReadAsArray()      
        P = destp.GetRasterBand(1).ReadAsArray()   
        Storage_Coeff_Surface_Runoff = destcsr.GetRasterBand(1).ReadAsArray()   
        
        # Calculate Surface Runoff P  
        Surface_Runoff_P = (NOD * (P - I))**2/(NOD * (P - I) + Storage_Coeff_Surface_Runoff)
        
        # Save result
        DC.Save_as_tiff(filename_out, Surface_Runoff_P, geo, proj)   
        
    return()
    
def Calc_Surface_Runoff_Coefficient(output_folder_L2, Date, example_file):

    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
    
    # Create output folder for Surface_Runoff_Coefficient
    output_folder_Surface_Runoff_Coefficient = os.path.join(output_folder_L2, "Surface_Runoff_Coefficient")
    if not os.path.exists(output_folder_Surface_Runoff_Coefficient):
        os.makedirs(output_folder_Surface_Runoff_Coefficient)
   
    # Define output file
    filename_out = os.path.join(output_folder_Surface_Runoff_Coefficient, "Surface_Runoff_Coefficient_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
    if not os.path.exists(filename_out):
        
         # date in dekad
        day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date_datetime.day)))[0]), 2)))
        
        # Conversion WAPOR unit to mm/Dekade
        if day_dekad == 2:
            year = Date_datetime.year
            month = Date_datetime.month
            NOD = calendar.monthrange(year, month)[1]
        else:
            NOD = 10
        
        # define required filenames
        filep = os.path.join(input_folder_L1, "L1_PCP_D", "L1_PCP_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filesrp = os.path.join(output_folder_L2, "Surface_Runoff_P", "Surface_Runoff_P_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        
        # Open required files
        destp = RC.reproject_dataset_example(filep, example_file, 2)
        destsrp = gdal.Open(filesrp)
        
        # Get georeference
        geo = destsrp.GetGeoTransform()
        proj = destsrp.GetProjection()
           
        # Open Arrays    
        P = destp.GetRasterBand(1).ReadAsArray()   
        Surface_Runoff_P = destsrp.GetRasterBand(1).ReadAsArray()   
        
        # Calculate Surface Runoff P  
        Surface_Runoff_Coefficient = np.maximum(0.1, Surface_Runoff_P/(P * NOD))
        
        # Save result
        DC.Save_as_tiff(filename_out, Surface_Runoff_Coefficient, geo, proj)   
        
    return()




    
    