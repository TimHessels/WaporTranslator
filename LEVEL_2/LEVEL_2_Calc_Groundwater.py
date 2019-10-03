# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Mon Sep 30 19:48:07 2019
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

def Calc_Net_Supply_Drainage(output_folder_L2, Date, example_file):
    
    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
    
    # Create output folder for Net_Supply_Drainage
    output_folder_Net_Supply_Drainage = os.path.join(output_folder_L2, "Net_Supply_Drainage")
    if not os.path.exists(output_folder_Net_Supply_Drainage):
        os.makedirs(output_folder_Net_Supply_Drainage)
   
    # Define output file
    filename_out = os.path.join(output_folder_Net_Supply_Drainage, "Net_Supply_Drainage_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
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
        fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filep = os.path.join(input_folder_L1, "L1_PCP_D", "L1_PCP_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filesmc = os.path.join(output_folder_L2, "Soil_Moisture_Change", "Soil_Moisture_Change_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))  
        
        # Open required files
        destet = RC.reproject_dataset_example(fileet, example_file, 2)
        destp = RC.reproject_dataset_example(filep, example_file, 2)
        destsmc = gdal.Open(filesmc)
        
        # Get georeference
        geo = destet.GetGeoTransform()
        proj = destet.GetProjection()
           
        # Open Arrays
        ET = destet.GetRasterBand(1).ReadAsArray()      
        P = destp.GetRasterBand(1).ReadAsArray()   
        SM_change = destsmc.GetRasterBand(1).ReadAsArray()   
        
        # Calculate Net Supply / Net Drainage     
        Net_Supply_Drainage = (ET - P) * NOD + SM_change
        
        # Save result
        DC.Save_as_tiff(filename_out, Net_Supply_Drainage, geo, proj)   
        
    return()
            
def Calc_Deep_Percolation(output_folder_L2, Date):
    
    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")
    
    # Create output folder for Deep_Percolation
    output_folder_Deep_Percolation = os.path.join(output_folder_L2, "Deep_Percolation")
    if not os.path.exists(output_folder_Deep_Percolation):
        os.makedirs(output_folder_Deep_Percolation)
   
    # Define output file
    filename_out = os.path.join(output_folder_Deep_Percolation, "Deep_Percolation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
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
        filerd = os.path.join(output_folder_L2, "Root_Depth", "Root_Depth_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filetfc = os.path.join(output_folder_L2, "Theta_FC_Subsoil", "Theta_FC_Subsoil.tif")
        filesm = os.path.join(output_folder_L2, "Soil_Moisture", "Soil_Moisture_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))  
        
        # Open required files
        destrd = gdal.Open(filerd)
        desttfc = gdal.Open(filetfc)
        destsm = gdal.Open(filesm)
        
        # Get georeference
        geo = destrd.GetGeoTransform()
        proj = destrd.GetProjection()
           
        # Open Arrays
        Root_Depth = destrd.GetRasterBand(1).ReadAsArray()      
        Theta_FC_Subsoil = desttfc.GetRasterBand(1).ReadAsArray()   
        Soil_Moisture = destsm.GetRasterBand(1).ReadAsArray()   
        
        # Calculate Deep Percolation     
        Deep_Percolation = np.maximum(0, (Soil_Moisture - Theta_FC_Subsoil) * Root_Depth * NOD)
        
        # Save result
        DC.Save_as_tiff(filename_out, Deep_Percolation, geo, proj)   
        
    return() 
    
def Calc_Storage_Coeff_Surface_Runoff(output_folder_L2, Date, example_file):

    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
    
    # Create output folder for Storage_Coeff_Surface_Runoff
    output_folder_Storage_Coeff_Surface_Runoff = os.path.join(output_folder_L2, "Storage_Coeff_Surface_Runoff")
    if not os.path.exists(output_folder_Storage_Coeff_Surface_Runoff):
        os.makedirs(output_folder_Storage_Coeff_Surface_Runoff)
   
    # Define output file
    filename_out = os.path.join(output_folder_Storage_Coeff_Surface_Runoff, "Storage_Coeff_Surface_Runoff_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
    if not os.path.exists(filename_out):
  
        # define required filenames
        filesf = os.path.join(input_folder_L1, "SoilGrids", "Sand_Content", "SandContentMassFraction_sl6_SoilGrids_percentage.tif")
        filelai = os.path.join(output_folder_L2, "LAI", "LAI_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))  
        filetsat = os.path.join(output_folder_L2, "Theta_Sat_Subsoil", "Theta_Sat_Subsoil.tif")
        filesm = os.path.join(output_folder_L2, "Soil_Moisture", "Soil_Moisture_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))  
        
        # Open required files
        destsf = RC.reproject_dataset_example(filesf, example_file, 2)
        destlai = gdal.Open(filelai)
        desttsat = gdal.Open(filetsat)
        destsm = gdal.Open(filesm)
        
        # Get georeference
        geo = destsm.GetGeoTransform()
        proj = destsm.GetProjection()
           
        # Open Arrays
        Sand_Fraction = destsf.GetRasterBand(1).ReadAsArray()      
        LAI = destlai.GetRasterBand(1).ReadAsArray()   
        Theta_Sat_Subsoil = desttsat.GetRasterBand(1).ReadAsArray()   
        Soil_Moisture = destsm.GetRasterBand(1).ReadAsArray() 
        
        # Calculate Storage coefficient for surface runoff     
        Storage_Coeff_Surface_Runoff = 8 * (Sand_Fraction * LAI) * (Theta_Sat_Subsoil - Soil_Moisture)
        
        # Save result
        DC.Save_as_tiff(filename_out, Storage_Coeff_Surface_Runoff, geo, proj)   
        
    return()


    