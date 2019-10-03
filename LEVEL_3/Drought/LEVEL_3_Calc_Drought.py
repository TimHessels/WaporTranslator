# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:06:01 2019
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


def Calc_Drought(output_folder_L2, Date, example_file):

    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")
    
    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")

    # Get folder L3
    output_folder_L3 = output_folder_L2.replace("LEVEL_2", "LEVEL_3")   

    # date in dekad
    day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date_datetime.day)))[0]), 2)))
        
    # Conversion WAPOR unit to mm/Dekade
    if day_dekad == 2:
        year = Date_datetime.year
        month = Date_datetime.month
        NOD = calendar.monthrange(year, month)[1]
    else:
        NOD = 10

    # Create output folder for Drought
    output_folder_Drought = os.path.join(output_folder_L3, "Drought")
    if not os.path.exists(output_folder_Drought):
        os.makedirs(output_folder_Drought)
        
    # Define output files
    filename_out_et_deficit = os.path.join(output_folder_Drought, "ET_Deficit", "ET_Deficit%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_accumulated_rainfall_deficit = os.path.join(output_folder_Drought, "Accumulated_Rainfall_Deficit", "Accumulated_Rainfall_Deficit_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_soil_moisture_anomaly = os.path.join(output_folder_Drought, "Soil_Moisture_Anomaly", "Soil_Moisture_Anomaly_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_lake_reservoir_level_anomaly = os.path.join(output_folder_Drought, "Lake_Reservoir_Level_Anomaly", "Lake_Reservoir_Level_Anomaly_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_open_water_anomaly = os.path.join(output_folder_Drought, "Open_Water_Anomaly", "Open_Water_Anomaly_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_integrated_drought_alert_level = os.path.join(output_folder_Drought, "Integrated_Drought_Alert_Level", "Integrated_Drought_Alert_Level_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    

    if not os.path.exists(filename_out_soil_moisture_anomaly):
   
        # Get georeference
        dest_ex = gdal.Open(example_file)
        geo = dest_ex.GetGeoTransform()
        proj = dest_ex.GetProjection()
        
        # define required filenames
        fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filecwr = os.path.join(output_folder_L2, "Crop_Water_Requirement", "Crop_Water_Requirement_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filecump = os.path.join(output_folder_L2, "Cumulative", "Precipitation", "P_cum_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
        filecumet = os.path.join(output_folder_L2, "Cumulative", "Evapotranspiration", "ET_cum_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filesm = os.path.join(output_folder_L2, "Soil_Moisture", "Soil_Moisture_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
         
        # Open required files
        destet = RC.reproject_dataset_example(fileet, example_file, 2)
        destcwr = gdal.Open(filecwr)
        destcump = gdal.Open(filecump)
        destcumet = gdal.Open(filecumet)
        destsm = gdal.Open(filesm)

        # Open Arrays
        ET = destet.GetRasterBand(1).ReadAsArray()        
        Crop_Water_Requirement = destcwr.GetRasterBand(1).ReadAsArray()
        P_cumulated = destcump.GetRasterBand(1).ReadAsArray()
        ET_cumulated = destcumet.GetRasterBand(1).ReadAsArray()
        Soil_Moisture = destsm.GetRasterBand(1).ReadAsArray()         

        # Calculate Evapotranspiration deficit
        ET_Deficit = Crop_Water_Requirement - ET * NOD
        
        # Calculate Accumulated Rainfall Deficit over Season
        Accumulated_Rainfall_Deficit = P_cumulated - ET_cumulated
        
        # Calculate Soil Moisture Anomaly
        Soil_Moisture_Anomaly = (Soil_Moisture - E68)/E68 * 100 #!!!
        
        # Calculate Lake Reservoir Level Anomaly
        #Lake_Reservoir_Level_Anomaly = 
        
        # Calculate Open Water Anomaly
        #Open_Water_Anomaly = 
        
        # Calculate Integrated Drought Alert Level
        #Integrated_Drought_Alert_Level =
            
        # Save result
        DC.Save_as_tiff(filename_out_et_deficit, ET_Deficit, geo, proj)
        DC.Save_as_tiff(filename_out_accumulated_rainfall_deficit, Accumulated_Rainfall_Deficit, geo, proj)
        #DC.Save_as_tiff(filename_out_soil_moisture_anomaly, Soil_Moisture_Anomaly, geo, proj)
        #DC.Save_as_tiff(filename_out_lake_reservoir_level_anomaly, Lake_Reservoir_Level_Anomaly, geo, proj)
        #DC.Save_as_tiff(filename_out_open_water_anomaly, Open_Water_Anomaly, geo, proj)
        #DC.Save_as_tiff(filename_out_integrated_drought_alert_level, Integrated_Drought_Alert_Level, geo, proj)
        
    return()