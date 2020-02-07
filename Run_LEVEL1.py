# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sat Sep 28 10:35:31 2019
"""
import os
import sys
import json
import warnings
import pandas as pd
import WaporTranslator.LEVEL_1 as L1

def main(Start_year_analyses, End_year_analyses, Input_shapefile, Threshold_Mask, output_folder, API_WAPOR_KEY, WAPOR_LVL, Radiation_Data, Albedo_Data, METEO_timestep, LU_Data, Spatial_Resolution):
    
    # Create output folder for LEVEL 1 data
    output_folder_L1 = os.path.join(output_folder, "LEVEL_1")
    if not os.path.exists(output_folder_L1):
        os.makedirs(output_folder_L1)
    
    # Define amount of cores used for downloading
    cores = 4
    
    # Get latlim and lonlim and create a mask of the shapefile
    dest_AOI_MASK, latlim, lonlim = L1.LEVEL_1_AOI.main(Input_shapefile, Threshold_Mask)
    
    # Download ESACCI data
    if LU_Data == "":
        L1.LEVEL_1_Download_ESACCI.main(output_folder_L1, latlim, lonlim)
    
    # Download SoilGrids data
    L1.LEVEL_1_Download_SoilGrids.main(output_folder_L1, latlim, lonlim)
    
    # Download SRTM data
    L1.LEVEL_1_Download_SRTM.main(output_folder_L1, latlim, lonlim)
    
    # Define years
    Years = pd.date_range("%d-01-01" %int(Start_year_analyses), "%d-12-31" %int(End_year_analyses), freq = "AS")
    
    for Year in Years:
        
        year = Year.year
        print("Collect data for the year %s" %year)
        
        # Download WAPOR data
        L1.LEVEL_1_Download_WAPOR.main(output_folder_L1, year, year, latlim, lonlim, WAPOR_LVL, API_WAPOR_KEY, LU_Data)    
        
        # Download GLDAS data
        if METEO_timestep == "Daily":
            L1.LEVEL_1_Download_GLDAS.main(output_folder_L1, year, year, latlim, lonlim, cores, method = "Daily")
            
            # Process MSGCCP data
            if Radiation_Data == "LANDSAF":
                if year >= 2016:
                    L1.LEVEL_1_Process_MSGCCP.main(output_folder_L1, year, latlim, lonlim)
            elif Radiation_Data == "KNMI":
                if year >= 2017:            
                    L1.LEVEL_1_Process_KNMI.main(output_folder_L1, year, latlim, lonlim, cores)
            else:
                print("Choose for Radiation input LANDSAF or KNMI")     
                
        elif METEO_timestep == "Monthly":
            L1.LEVEL_1_Download_GLDAS.main(output_folder_L1, year, year, latlim, lonlim, cores, method = "Monthly")            
        else:
            print("Choose for METEO timestep Daily or Monthly")
            
        # Download MODIS data
        if Albedo_Data == "MODIS":
            L1.LEVEL_1_Download_MODIS.main(output_folder_L1, year, year, latlim, lonlim, Radiation_Data, METEO_timestep)
        
    # Create Mask
    L1.LEVEL_1_Create_Mask.main(output_folder_L1, dest_AOI_MASK, Threshold_Mask, Spatial_Resolution)

if __name__== "__main__":
    
    # Do not show warnings
    warnings.filterwarnings('ignore')    
    
    # open json file
    with open(sys.argv[1]) as f:
        datastore = f.read()
    obj = json.loads(datastore)  
    inputs = obj["Inputs"][0]
    
    # Set Variables
    Start_year_analyses = inputs["Start_year"]
    End_year_analyses = inputs["End_year"]
    Input_shapefile = inputs["Input_shapefile"]
    Threshold_Mask = inputs["Threshold_Mask"]
    output_folder = inputs["Output_folder"]
    API_WAPOR_KEY = inputs["API_WAPOR_KEY"]    
    WAPOR_LVL = inputs["WAPOR_LEVEL"]  
    METEO_timestep = inputs["METEO_timestep"]      
    LU_Data = inputs["LU_Map_Format"]    
    try:
        Spatial_Resolution = inputs["Spatial_Resolution"]    
    except:
        Spatial_Resolution = "None"      
    try:
        Radiation_Data = inputs["Radiation_Source"]   
    except:
        Radiation_Data = "KNMI"     
    try:
        Albedo_Data = inputs["Albedo_Source"]   
    except:
        Albedo_Data = "MODIS"        
    
    # run code
    main(Start_year_analyses, End_year_analyses, Input_shapefile, Threshold_Mask, output_folder, API_WAPOR_KEY, WAPOR_LVL, Radiation_Data, Albedo_Data, METEO_timestep, LU_Data, Spatial_Resolution)