# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 18:08:02 2019
"""

import os
import gdal
import datetime
import numpy as np

import WaporTranslator.LEVEL_2.LEVEL_2_Calc_Radiation as L2_Rad

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC


def Calc_LAI(output_folder_L2, Date, example_file):
    
    # Get dates
    Dates_dek = L2_Rad.Get_Dekads(Date)
    
    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
    
    # Create output folder for LAI
    output_folder_LAI = os.path.join(output_folder_L2, "LAI")
    if not os.path.exists(output_folder_LAI):
        os.makedirs(output_folder_LAI)
        
    for Date_datetime in Dates_dek:    
        
        # Define output file
        filename_out = os.path.join(output_folder_LAI, "LAI_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
        
        # Get georeference
        dest_ex = gdal.Open(example_file)
        geo = dest_ex.GetGeoTransform()
        proj = dest_ex.GetProjection()
        
        if not os.path.exists(filename_out):
            
            # define required filenames
            fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
            filet = os.path.join(input_folder_L1, "L2_T_D", "L2_T_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
            
            # Open required files
            destet = RC.reproject_dataset_example(fileet, example_file)
            destt = RC.reproject_dataset_example(filet, example_file)
            
            # Open Arrays
            ET = destet.GetRasterBand(1).ReadAsArray()
            T = destt.GetRasterBand(1).ReadAsArray()        
            LU = dest_ex.GetRasterBand(1).ReadAsArray() 
            
            # Calculate LAI
            LAI = np.log((1-T/ET))/(-0.45)
            LAI = LAI.clip(0, 8.0)
            
            # Improve LAI
            LAI[T==0] = -9999
            LAI = RC.gap_filling(LAI, -9999)
            LAI[LU==80] = 0.0
            
            # Save result
            DC.Save_as_tiff(filename_out, LAI, geo, proj)
        
    return()
    
def Calc_Root_Depth(output_folder_L2, Date):
    
    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")
    
    # Create output folder for Root_Depth
    output_folder_Root_Depth = os.path.join(output_folder_L2, "Root_Depth")
    if not os.path.exists(output_folder_Root_Depth):
        os.makedirs(output_folder_Root_Depth)
        
    # Define output file
    filename_out = os.path.join(output_folder_Root_Depth, "Root_Depth_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
    if not os.path.exists(filename_out):

        # define required filenames
        filelai = os.path.join(output_folder_L2, "LAI", "LAI_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        
        # Open required files
        destlai = gdal.Open(filelai)
 
        # Get georeference
        geo = destlai.GetGeoTransform()
        proj = destlai.GetProjection()
           
        # Open Arrays
        LAI = destlai.GetRasterBand(1).ReadAsArray()      
        
        # Calculate LAI
        Root_Depth = 0.7 * 100 * np.maximum(0,-0.0326 * LAI**2 + 0.4755 * LAI - 0.0411)
        Root_Depth = Root_Depth.clip(0, 500)
        
        # Save result
        DC.Save_as_tiff(filename_out, Root_Depth, geo, proj)
        
    return()     
    
    
def Calc_Fractional_Vegt_Cover(output_folder_L2, Date):
    
    # Get dates
    Dates_dek = L2_Rad.Get_Dekads(Date)
    
    # Create output folder for Fractional Vegetation Cover
    output_folder_Frac_Vegt = os.path.join(output_folder_L2, "Fractional_Vegetation_Cover")
    if not os.path.exists(output_folder_Frac_Vegt):
        os.makedirs(output_folder_Frac_Vegt)
    
    for Date_datetime in Dates_dek:
        
        # Define output file
        filename_out = os.path.join(output_folder_Frac_Vegt, "Fractional_Vegetation_Cover_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames
            filelai = os.path.join(output_folder_L2, "LAI", "LAI_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
            
            # Open required files
            destlai = gdal.Open(filelai)
     
            # Get georeference
            geo = destlai.GetGeoTransform()
            proj = destlai.GetProjection()
               
            # Open Arrays
            LAI = destlai.GetRasterBand(1).ReadAsArray()      
            
            # Calculate LAI
            Fract_vegt = 1-np.exp(-0.65 * LAI)
            Fract_vegt = Fract_vegt.clip(0, 1.0)
            
            # Save result
            DC.Save_as_tiff(filename_out, Fract_vegt, geo, proj)
        
    return()   

def Calc_Crop_Coeff_Dry_Soil(output_folder_L2, Date):

    # Get dates
    Dates_dek = L2_Rad.Get_Dekads(Date)
    
    # Create output folder for Crop coefficient for dry soil
    output_folder_Crop_Coef_Dry_Soil= os.path.join(output_folder_L2, "Crop_Coef_Dry_Soil")
    if not os.path.exists(output_folder_Crop_Coef_Dry_Soil):
        os.makedirs(output_folder_Crop_Coef_Dry_Soil)  

    for Date_datetime in Dates_dek:
        
        # Define output file
        filename_out = os.path.join(output_folder_Crop_Coef_Dry_Soil, "Crop_Coef_Dry_Soil_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames
            filefrvegt = os.path.join(output_folder_L2, "Fractional_Vegetation_Cover", "Fractional_Vegetation_Cover_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
            
            # Open required files
            destfrvegt = gdal.Open(filefrvegt)
     
            # Get georeference
            geo = destfrvegt.GetGeoTransform()
            proj = destfrvegt.GetProjection()
               
            # Open Arrays
            Fract_vegt = destfrvegt.GetRasterBand(1).ReadAsArray()      
            
            # Calculate LAI
            Crop_Coef_Dry_Soil = np.minimum(1.4 ,0.95 * Fract_vegt + 0.2)
            Crop_Coef_Dry_Soil = Crop_Coef_Dry_Soil.clip(0, 500)
            
            # Save result
            DC.Save_as_tiff(filename_out, Crop_Coef_Dry_Soil, geo, proj)
        
    return()     

