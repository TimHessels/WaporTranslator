# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:06:37 2019
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


def Calc_Water_Productivity(output_folder_L2, Date, example_file):

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

    # Create output folder for Water Productivity
    output_folder_Water_Productivity = os.path.join(output_folder_L3, "Water_Productivity")
    if not os.path.exists(output_folder_Water_Productivity):
        os.makedirs(output_folder_Water_Productivity)
        
    # Define output files
    filename_out_transpiration_efficiency = os.path.join(output_folder_Water_Productivity, "T_Efficiency", "T_Efficiency_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_aquacrop_water_use_efficiency = os.path.join(output_folder_Water_Productivity, "AquaCrop_Water_Use_Efficiency", "AquaCrop_Water_Use_Efficiency_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_gbwp_decade = os.path.join(output_folder_Water_Productivity, "GBWP_Decade", "GBWP_Decade_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_gbwp_acc = os.path.join(output_folder_Water_Productivity, "GBWP_Accumulated", "GBWP_Accumulated_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_gbwp_target = os.path.join(output_folder_Water_Productivity, "GBWP_Target", "GBWP_Target_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_gbwp_gap = os.path.join(output_folder_Water_Productivity, "GBWP_Gap", "GBWP_Gap_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_gbwp_improvements_required = os.path.join(output_folder_Water_Productivity, "GBWP_Improvements_Required", "GBWP_Improvements_Required_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_normalized_gbwp_max_per_tbp = os.path.join(output_folder_Water_Productivity, "Normalized_GBWP_Max_Per_TBP ", "Normalized_GBWP_Max_Per_TBP_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_normalized_gbwp_min_per_tbp = os.path.join(output_folder_Water_Productivity, "Normalized_GBWP_Min_Per_TBP", "Normalized_GBWP_Min_Per_TBP_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_water_productivity_score = os.path.join(output_folder_Water_Productivity, "Water_Productivity_Score", "Water_Productivity_Score_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_water_productivity = os.path.join(output_folder_Water_Productivity, "Water_Productivity", "Water_Productivity_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    

    if not os.path.exists(filename_out_water_productivity):
   
        # Get georeference
        dest_ex = gdal.Open(example_file)
        geo = dest_ex.GetGeoTransform()
        proj = dest_ex.GetProjection()
        
        # define required filenames
        filet = os.path.join(input_folder_L1, "L2_T_D", "L2_T_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        fileet0 = os.path.join(input_folder_L1, "L1_RET_D", "L1_RET_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))

        # Open required files
        destt = RC.reproject_dataset_example(filet, example_file, 2)
        destet = RC.reproject_dataset_example(fileet, example_file, 2)        
        destet0 = RC.reproject_dataset_example(fileet0, example_file, 2)
        
        # Open Arrays
        T = destt.GetRasterBand(1).ReadAsArray()        
        ET = destet.GetRasterBand(1).ReadAsArray()
        ET0 = destet0.GetRasterBand(1).ReadAsArray()

        # Calculate Transpiration Efficiency
        T_Efficiency = E82/(T * 10)
        
        # Calculate AquaCrop Water Use Efficiency
        AquaCrop_Water_Use_Efficiency = (E90 * 100/(E71 * T/ET0))
        
        # Calculate Gross Biomass Water Productivity - Decade
        GBWP_Decade = E82/(10 * ET)
        
        # Calculate Gross Biomass Water Productivity - Accumulated
        GBWP_Accumulated = (E90 * 1000)/(10 * E72)
        
        # Calculate Gross Biomass Water Productivity - Target
        GBWP_Target = E83/(10 * I8) 
        
        # Calculate Gross Biomass Water Productivity - Gap
        GBWP_Gap = GBWP_Decade - GBWP_Target

        # Calculate Gross Biomass Water Productivity - Improvement Required
        GBWP_Improvements_Required = (GBWP_Target - GBWP_Decade)/GBWP_Decade * 100
        
        # Calculate Normalized Gross Biomass Water Productivity Maximum Per TBP
        Normalized_GBWP_Max_Per_TBP = 5.7 * ET0/H12 
        
        # Calculate Normalized Gross Biomass Water Productivity Minimum Per TBP
        Normalized_GBWP_Min_Per_TBP = 1.7 * ET0/H12
        
        # Calculate Water Productivity Score
        Water_Productivity_Score = 9 * (GBWP_Decade * ET0/H12 - Normalized_GBWP_Min_Per_TBP)/(Normalized_GBWP_Max_Per_TBP - Normalized_GBWP_Min_Per_TBP) + 1

        # Calculate Water Productivity 
        Water_Productivity = (1000 * E91)/(10*E72)       
        
        # Save result
        DC.Save_as_tiff(filename_out_transpiration_efficiency, T_Efficiency, geo, proj)
        DC.Save_as_tiff(filename_out_aquacrop_water_use_efficiency, AquaCrop_Water_Use_Efficiency, geo, proj)
        DC.Save_as_tiff(filename_out_gbwp_decade, GBWP_Decade, geo, proj)
        DC.Save_as_tiff(filename_out_gbwp_acc, GBWP_Accumulated, geo, proj)
        DC.Save_as_tiff(filename_out_gbwp_target, GBWP_Target, geo, proj)
        DC.Save_as_tiff(filename_out_gbwp_gap, GBWP_Gap, geo, proj)
        DC.Save_as_tiff(filename_out_gbwp_improvements_required, GBWP_Improvements_Required, geo, proj)
        DC.Save_as_tiff(filename_out_normalized_gbwp_max_per_tbp, Normalized_GBWP_Max_Per_TBP, geo, proj)
        DC.Save_as_tiff(filename_out_normalized_gbwp_min_per_tbp, Normalized_GBWP_Min_Per_TBP, geo, proj)
        DC.Save_as_tiff(filename_out_water_productivity_score, Water_Productivity_Score, geo, proj)
        DC.Save_as_tiff(filename_out_water_productivity, Water_Productivity, geo, proj)
        
    return()