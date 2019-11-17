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

def main(Start_year_analyses, End_year_analyses, Input_shapefile, Threshold_Mask, output_folder, API_WAPOR_KEY, Radiation_Data):
    
    # Create output folder for LEVEL 1 data
    output_folder_L1 = os.path.join(output_folder, "LEVEL_1")
    if not os.path.exists(output_folder_L1):
        os.makedirs(output_folder_L1)
    
    # Define amount of cores used for downloading
    cores = 4
    
    # Get latlim and lonlim and create a mask of the shapefile
    dest_AOI_MASK, latlim, lonlim = L1.LEVEL_1_AOI.main(Input_shapefile)
    
    # Download ESACCI data
    L1.LEVEL_1_Download_ESACCI.main(output_folder_L1, latlim, lonlim)
    
    # Download SoilGrids data
    L1.LEVEL_1_Download_SoilGrids.main(output_folder_L1, latlim, lonlim)
    
    # Download SRTM data
    L1.LEVEL_1_Download_SRTM.main(output_folder_L1, latlim, lonlim)
    
    # Define years
    Years = pd.date_range(Start_year_analyses, End_year_analyses, "AS")
    
    for Year in Years:
        
        year = Year.year
        print("Collect data for the year %s" %year)
        
        # Download WAPOR data
        L1.LEVEL_1_Download_WAPOR.main(output_folder_L1, year, year, latlim, lonlim, API_WAPOR_KEY)    
        
        # Download GLDAS data
        L1.LEVEL_1_Download_GLDAS.main(output_folder_L1, year, year, latlim, lonlim, cores)
        
        # Download MODIS data
        L1.LEVEL_1_Download_MODIS.main(output_folder_L1, year, year, latlim, lonlim, Radiation_Data)
        
        # Process MSGCCP data
        if Radiation_Data == "LANDSAF":
            if year >= 2016:
                L1.LEVEL_1_Process_MSGCCP.main(output_folder_L1, year, latlim, lonlim)
            
        elif Radiation_Data == "KNMI":
            if year >= 2017:            
                L1.LEVEL_1_Process_KNMI.main(output_folder_L1, year, latlim, lonlim, cores)
        else:
            print("Choose for Radiation input LANDSAF or KNMI")
    
    # Create Mask
    L1.LEVEL_1_Create_Mask.main(output_folder_L1, dest_AOI_MASK, Threshold_Mask)

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
    try:
        Radiation_Data = inputs["Radiation_Source"]   
    except:
        Radiation_Data = "KNMI"
    
    # run code
    main(Start_year_analyses, End_year_analyses, Input_shapefile, Threshold_Mask, output_folder, API_WAPOR_KEY, Radiation_Data)