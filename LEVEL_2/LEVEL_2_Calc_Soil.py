# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Mon Sep 30 10:38:32 2019
"""

import os
import gdal
import datetime
import numpy as np
import calendar
import pandas as pd

import WaporTranslator.LEVEL_2.LEVEL_2_Calc_Radiation as L2_Rad

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

def Calc_Theta_Sat_Subsoil(output_folder_L2, example_file):
    
    # Create output folder for Theta_Sat_Subsoil
    output_folder_Theta_Sat_Subsoil = os.path.join(output_folder_L2, "Theta_Sat_Subsoil")
    if not os.path.exists(output_folder_Theta_Sat_Subsoil):
        os.makedirs(output_folder_Theta_Sat_Subsoil)

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
             
    # Define output file
    filename_out = os.path.join(output_folder_Theta_Sat_Subsoil, "Theta_Sat_Subsoil.tif")    
    
    if not os.path.exists(filename_out):

        # define required filenames
        fileclay = os.path.join(input_folder_L1, "SoilGrids", "Clay_Content", "ClayContentMassFraction_sl6_SoilGrids_percentage.tif")
        filebulk = os.path.join(input_folder_L1, "SoilGrids", "Bulk_Density", "BulkDensity_sl6_SoilGrids_kg-m-3.tif")
        
        # Open required files
        destclay = RC.reproject_dataset_example(fileclay, example_file, 2)
        destbulk = RC.reproject_dataset_example(filebulk, example_file, 2)
        
        # Get georeference
        geo = destbulk.GetGeoTransform()
        proj = destbulk.GetProjection()
           
        # Open Arrays
        Clay = destclay.GetRasterBand(1).ReadAsArray()      
        Bulk = destbulk.GetRasterBand(1).ReadAsArray()      
        
        # Calculate Land Theta Saturated Subsoil
        Theta_Sat_Subsoil = 0.85 * (1 - Bulk/2650) + 0.13 * Clay * 0.01
        
        # Save result
        DC.Save_as_tiff(filename_out, Theta_Sat_Subsoil, geo, proj)
        
    return()
    

def Calc_Theta_FC_Subsoil(output_folder_L2):
    
    # Create output folder for Theta_FC_Subsoil
    output_folder_Theta_FC_Subsoil = os.path.join(output_folder_L2, "Theta_FC_Subsoil")
    if not os.path.exists(output_folder_Theta_FC_Subsoil):
        os.makedirs(output_folder_Theta_FC_Subsoil)

    # Define output file
    filename_out = os.path.join(output_folder_Theta_FC_Subsoil, "Theta_FC_Subsoil.tif")    
    
    if not os.path.exists(filename_out):

        # define required filenames
        filetsat = os.path.join(output_folder_L2, "Theta_Sat_Subsoil", "Theta_Sat_Subsoil.tif")
        
        # Open required files
        desttsat = gdal.Open(filetsat)
        
        # Get georeference
        geo = desttsat.GetGeoTransform()
        proj = desttsat.GetProjection()
           
        # Open Arrays
        Theta_Sat_Subsoil = desttsat.GetRasterBand(1).ReadAsArray()        
        
        # Calculate Theta Field Capacity Subsoil
        Theta_FC_Subsoil = -2.2 * Theta_Sat_Subsoil**2 + 2.92 * Theta_Sat_Subsoil - 0.59
        
        # Save result
        DC.Save_as_tiff(filename_out, Theta_FC_Subsoil, geo, proj)
        
    return()    
    
def Calc_Theta_WP_Subsoil(output_folder_L2):
    
    # Create output folder for Theta_WP_Subsoil
    output_folder_Theta_WP_Subsoil = os.path.join(output_folder_L2, "Theta_WP_Subsoil")
    if not os.path.exists(output_folder_Theta_WP_Subsoil):
        os.makedirs(output_folder_Theta_WP_Subsoil)

    # Define output file
    filename_out = os.path.join(output_folder_Theta_WP_Subsoil, "Theta_WP_Subsoil.tif")    
    
    if not os.path.exists(filename_out):

        # define required filenames
        filetsat = os.path.join(output_folder_L2, "Theta_Sat_Subsoil", "Theta_Sat_Subsoil.tif")
        
        # Open required files
        desttsat = gdal.Open(filetsat)
        
        # Get georeference
        geo = desttsat.GetGeoTransform()
        proj = desttsat.GetProjection()
           
        # Open Arrays
        Theta_Sat_Subsoil = desttsat.GetRasterBand(1).ReadAsArray()        
        
        # Calculate Theta Wilting Point Subsoil
        Theta_WP_Subsoil =1.7 * Theta_Sat_Subsoil**4
        
        # Save result
        DC.Save_as_tiff(filename_out, Theta_WP_Subsoil, geo, proj)
        
    return()        
    
def Calc_Soil_Water_Holding_Capacity(output_folder_L2):  
    
    # Create output folder for Soil_Water_Holding_Capacity
    output_folder_Soil_Water_Holding_Capacity = os.path.join(output_folder_L2, "Soil_Water_Holding_Capacity")
    if not os.path.exists(output_folder_Soil_Water_Holding_Capacity):
        os.makedirs(output_folder_Soil_Water_Holding_Capacity)

    # Define output file
    filename_out = os.path.join(output_folder_Soil_Water_Holding_Capacity, "Soil_Water_Holding_Capacity.tif")    
    
    if not os.path.exists(filename_out):

        # define required filenames
        filetfc = os.path.join(output_folder_L2, "Theta_FC_Subsoil", "Theta_FC_Subsoil.tif")
        filetwp = os.path.join(output_folder_L2, "Theta_WP_Subsoil", "Theta_WP_Subsoil.tif")

        # Open required files
        desttfc = gdal.Open(filetfc)
        desttwp = gdal.Open(filetwp)
        
        # Get georeference
        geo = desttfc.GetGeoTransform()
        proj = desttfc.GetProjection()
           
        # Open Arrays
        Theta_FC_Subsoil = desttfc.GetRasterBand(1).ReadAsArray()           
        Theta_WP_Subsoil = desttwp.GetRasterBand(1).ReadAsArray()        
        
        # Calculate Theta Wilting Point Subsoil
        Soil_Water_Holding_Capacity = (Theta_FC_Subsoil - Theta_WP_Subsoil) * 1000
        
        # Save result
        DC.Save_as_tiff(filename_out, Soil_Water_Holding_Capacity, geo, proj)
        
    return()      
    
def Calc_Soil_Moisture(output_folder_L2, Date):
    
    # Get dates
    Dates_dek = L2_Rad.Get_Dekads(Date)
    
    # Create output folder for Soil_Moisture
    output_folder_Soil_Moisture = os.path.join(output_folder_L2, "Soil_Moisture")
    if not os.path.exists(output_folder_Soil_Moisture):
        os.makedirs(output_folder_Soil_Moisture)
        
    for Date_one in Dates_dek:
        
        # Define output file
        filename_out = os.path.join(output_folder_Soil_Moisture, "Soil_Moisture_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames
            fileef = os.path.join(output_folder_L2, "Evaporative_Fraction", "Evaporative_Fraction_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))
            filetsat = os.path.join(output_folder_L2, "Theta_Sat_Subsoil", "Theta_Sat_Subsoil.tif")
       
            # Open required files
            destef = gdal.Open(fileef)
            desttsat = gdal.Open(filetsat)
            
            # Get georeference
            geo = destef.GetGeoTransform()
            proj = destef.GetProjection()
               
            # Open Arrays
            Evaporative_Fraction = destef.GetRasterBand(1).ReadAsArray()  
            Theta_Sat_Subsoil = desttsat.GetRasterBand(1).ReadAsArray()  
            
            # Calculate Soil Moisture
            Soil_Moisture = Theta_Sat_Subsoil * np.exp((Evaporative_Fraction - 1)/0.421)
            
            # Save result
            DC.Save_as_tiff(filename_out, Soil_Moisture, geo, proj)
        
    return()     
    
def Calc_Critical_Soil_Moisture(output_folder_L2, Date):    
    
    # Get dates
    Dates_dek = L2_Rad.Get_Dekads(Date)
    
    # Create output folder for Critical Soil_Moisture
    output_folder_Critical_Soil_Moisture = os.path.join(output_folder_L2, "Critical_Soil_Moisture")
    if not os.path.exists(output_folder_Critical_Soil_Moisture):
        os.makedirs(output_folder_Critical_Soil_Moisture)
        
    for Date_one in Dates_dek:
        
        # date in dekad
        day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date_one.day)))[0]), 2)))
        
        # Conversion WAPOR unit to mm/Dekade
        if day_dekad == 2:
            year = Date_one.year
            month = Date_one.month
            NOD = calendar.monthrange(year, month)[1]
            conversion_rate = (NOD - 20)/10
        else:
            NOD = 10
            conversion_rate = 1
        
        # Define output file
        filename_out = os.path.join(output_folder_Critical_Soil_Moisture, "output_folder_Critical_Soil_Moisture_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames
            filecwr = os.path.join(output_folder_L2, "Crop_Water_Requirement", "Crop_Water_Requirement_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))
            filetfc = os.path.join(output_folder_L2, "Theta_FC_Subsoil", "Theta_FC_Subsoil.tif")
            filetwp = os.path.join(output_folder_L2, "Theta_WP_Subsoil", "Theta_WP_Subsoil.tif") 
            
            # Open required files
            destcwr = gdal.Open(filecwr)
            desttfc = gdal.Open(filetfc)
            desttwp = gdal.Open(filetwp)
            
            # Get georeference
            geo = destcwr.GetGeoTransform()
            proj = destcwr.GetProjection()
               
            # Open Arrays
            Crop_Water_Requirement = destcwr.GetRasterBand(1).ReadAsArray()  
            Theta_FC_Subsoil = desttfc.GetRasterBand(1).ReadAsArray()           
            Theta_WP_Subsoil = desttwp.GetRasterBand(1).ReadAsArray()     
            
            # Calculate Soil Moisture
            Critical_Soil_Moisture = Theta_WP_Subsoil + (Theta_FC_Subsoil - Theta_WP_Subsoil) * (0.65+0.04*(5 - Crop_Water_Requirement/NOD))
            
            # Save result
            DC.Save_as_tiff(filename_out, Critical_Soil_Moisture, geo, proj)
            
    return()
    
def Calc_Soil_Moisture_Start_End_Period(output_folder_L2, Date):

    # Get dates
    Dates_dek = L2_Rad.Get_Dekads(Date)
    
    # Create output folder for Soil_Moisture_Start
    output_folder_Soil_Moisture_Start = os.path.join(output_folder_L2, "Soil_Moisture_Start")
    if not os.path.exists(output_folder_Soil_Moisture_Start):
        os.makedirs(output_folder_Soil_Moisture_Start)

    # Create output folder for Soil_Moisture_End
    output_folder_Soil_Moisture_End = os.path.join(output_folder_L2, "Soil_Moisture_End")
    if not os.path.exists(output_folder_Soil_Moisture_End):
        os.makedirs(output_folder_Soil_Moisture_End)

    # Define output file
    filename_out_end = os.path.join(output_folder_Soil_Moisture_Start, "Soil_Moisture_Start_%d.%02d.%02d.tif" %(Dates_dek[1].year, Dates_dek[1].month, Dates_dek[1].day))    
    filename_out_start = os.path.join(output_folder_Soil_Moisture_End, "Soil_Moisture_End_%d.%02d.%02d.tif" %(Dates_dek[1].year, Dates_dek[1].month, Dates_dek[1].day))  
    
    if not os.path.exists(filename_out_end):

        # define required filenames
        filesm = os.path.join(output_folder_L2, "Soil_Moisture", "Soil_Moisture_{yyyy}.{mm:02d}.{dd:02d}.tif")
        
        # Open required files
        destsm1 = gdal.Open(filesm.format(yyyy = Dates_dek[0].year, mm = Dates_dek[0].month, dd = Dates_dek[0].day))
        destsm2 = gdal.Open(filesm.format(yyyy = Dates_dek[1].year, mm = Dates_dek[1].month, dd = Dates_dek[1].day))
        destsm3 = gdal.Open(filesm.format(yyyy = Dates_dek[2].year, mm = Dates_dek[2].month, dd = Dates_dek[2].day))
        
        # Get georeference
        geo = destsm1.GetGeoTransform()
        proj = destsm1.GetProjection()
           
        # Open Arrays
        SM1 = destsm1.GetRasterBand(1).ReadAsArray()      
        SM2 = destsm2.GetRasterBand(1).ReadAsArray()      
        SM3 = destsm3.GetRasterBand(1).ReadAsArray()       
        
        # Calculate Soil Moisture Start and End
        SM_start = (SM2+SM1)/2
        SM_end = (SM3+SM2)/2    
        
        # Save result
        DC.Save_as_tiff(filename_out_start, SM_start, geo, proj)
        DC.Save_as_tiff(filename_out_end, SM_end, geo, proj)   
    
    return()    
    
def Calc_Soil_Water_Storage_Change(output_folder_L2, Date):

    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")
    
    # Create output folder for Soil_Moisture_Change
    output_folder_Soil_Moisture_Change = os.path.join(output_folder_L2, "Soil_Moisture_Change")
    if not os.path.exists(output_folder_Soil_Moisture_Change):
        os.makedirs(output_folder_Soil_Moisture_Change)
   
    # Define output file
    filename_out = os.path.join(output_folder_Soil_Moisture_Change, "Soil_Moisture_Change_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    
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
        filesmstart = os.path.join(output_folder_L2, "Soil_Moisture_Start", "Soil_Moisture_Start_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day)) 
        filesmend = os.path.join(output_folder_L2, "Soil_Moisture_End", "Soil_Moisture_End_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day)) 
        filerd = os.path.join(output_folder_L2, "Root_Depth", "Root_Depth_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day)) 
        
        # Open required files
        destsmstart = gdal.Open(filesmstart)
        destsmend = gdal.Open(filesmend)
        destrd = gdal.Open(filerd)
        
        # Get georeference
        geo = destsmstart.GetGeoTransform()
        proj = destsmstart.GetProjection()
           
        # Open Arrays
        SM_start = destsmstart.GetRasterBand(1).ReadAsArray()      
        SM_end = destsmend.GetRasterBand(1).ReadAsArray()   
        Root_Depth = destrd.GetRasterBand(1).ReadAsArray() 
        
        # Calculate Soil Moisture Change      
        SM_change = Root_Depth * NOD * (SM_end - SM_start)
        
        # Save result
        DC.Save_as_tiff(filename_out, SM_change, geo, proj)   
        
    return()
        


    