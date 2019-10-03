# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Mon Sep 30 10:46:36 2019
"""

import os
import gdal
import datetime
import calendar
import numpy as np
import pandas as pd

import WaporTranslator.LEVEL_2.LEVEL_2_Calc_Radiation as L2_Rad

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

def Calc_Crop_Water_Requirement(output_folder_L2, Date, example_file):
    
    # Get dates
    Dates_dek = L2_Rad.Get_Dekads(Date)

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
    
    # Create output folder for Crop_Water_Requirement
    output_folder_Crop_Water_Requirement = os.path.join(output_folder_L2, "Crop_Water_Requirement")
    if not os.path.exists(output_folder_Crop_Water_Requirement):
        os.makedirs(output_folder_Crop_Water_Requirement)

    for Date_datetime in Dates_dek:
    
        # date in dekad
        day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date_datetime.day)))[0]), 2)))
            
        # Conversion WAPOR unit to mm/Dekade
        if day_dekad == 2:
            year = Date_datetime.year
            month = Date_datetime.month
            NOD = calendar.monthrange(year, month)[1]
            conversion_rate = (NOD - 20)/10
        else:
            NOD = 10
            conversion_rate = 1
        
        # Define output file
        filename_out = os.path.join(output_folder_Crop_Water_Requirement, "Crop_Water_Requirement_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames
            fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
            fileet0 = os.path.join(input_folder_L1, "L1_RET_D", "L1_RET_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
            filecropcoef = os.path.join(output_folder_L2, "Crop_Coef_Dry_Soil", "Crop_Coef_Dry_Soil_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
            
            # Open required files
            destet = RC.reproject_dataset_example(fileet, example_file, 2)
            destet0 = RC.reproject_dataset_example(fileet0, example_file, 2)
            destcropcoef  = gdal.Open(filecropcoef)
                    
            # Get georeference
            geo = destcropcoef.GetGeoTransform()
            proj = destcropcoef.GetProjection()
               
            # Open Arrays
            ET = destet.GetRasterBand(1).ReadAsArray()      
            ET0 = destet0.GetRasterBand(1).ReadAsArray()     
            Crop_Coef_Dry_Soil = destcropcoef.GetRasterBand(1).ReadAsArray()     
            
            # Fill ET0
            ET0 = RC.gap_filling(ET0, 0.0)
            
            # Calculate LAI
            Crop_Water_Requirement = np.maximum(conversion_rate * ET, Crop_Coef_Dry_Soil * ET0 * conversion_rate)
            
            # Save result
            DC.Save_as_tiff(filename_out, Crop_Water_Requirement, geo, proj)
        
    return()     
    
def Calc_Crop_Coef_Update(output_folder_L2, Date, example_file):

    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
    
    # Create output folder for Calc_Crop_Coef_Update
    output_folder_Calc_Crop_Coef_Update = os.path.join(output_folder_L2, "Calc_Crop_Coef_Update")
    if not os.path.exists(output_folder_Calc_Crop_Coef_Update):
        os.makedirs(output_folder_Calc_Crop_Coef_Update)
   
    # Define output file
    filename_out = os.path.join(output_folder_Calc_Crop_Coef_Update, "Calc_Crop_Coef_Update_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
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
        fileet0 = os.path.join(input_folder_L1, "L1_RET_D", "L1_RET_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filecwr = os.path.join(output_folder_L2, "Crop_Water_Requirement", "Crop_Water_Requirement_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        
        # Open required files
        destet0 = RC.reproject_dataset_example(fileet0, example_file, 2)
        destcwr = gdal.Open(filecwr)
        
        # Get georeference
        geo = destcwr.GetGeoTransform()
        proj = destcwr.GetProjection()
           
        # Open Arrays    
        ET0 = destet0.GetRasterBand(1).ReadAsArray()   
        Crop_Water_Requirement = destcwr.GetRasterBand(1).ReadAsArray()   

        # Fill ET0
        ET0 = RC.gap_filling(ET0, 0.0)
        
        # Calculate updated crop coefficient 
        Calc_Crop_Coef_Update = Crop_Water_Requirement/(NOD * ET0)
        
        # Save result
        DC.Save_as_tiff(filename_out, Calc_Crop_Coef_Update, geo, proj)   
        
    return()    