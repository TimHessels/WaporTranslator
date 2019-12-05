# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:06:01 2019
"""

import os
import gdal
import numpy as np
import warnings

import WaporTranslator.LEVEL_1.Input_Data as Inputs
import WaporTranslator.LEVEL_1.DataCube as DataCube
import WaporTranslator.LEVEL_2.Functions as Functions

def main(Start_year_analyses, End_year_analyses, output_folder):  

    # Do not show non relevant warnings
    warnings.filterwarnings("ignore")
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    # Define dates
    Dates = Functions.Get_Dekads(Start_year_analyses, End_year_analyses)
    
    # Get path and formats
    Paths = Inputs.Input_Paths()
    Formats = Inputs.Input_Formats()
    Conversions = Inputs.Input_Conversions()
    
    # Set example file
    example_file = os.path.join(output_folder, "LEVEL_1", "MASK", "MASK.tif")
    
    # Open Mask
    dest_mask = gdal.Open(example_file)
    MASK = dest_mask.GetRasterBand(1).ReadAsArray()
    
    # Define output folder LEVEL 3
    output_folder_L3 = os.path.join(output_folder, "LEVEL_3", "Drought")
    if not os.path.exists(output_folder_L3):
        os.makedirs(output_folder_L3)
    
    ################################# Dynamic maps #################################
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET), Formats.ET, Dates, Conversion = Conversions.ET, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = 'mm/day')
    Pcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_P), Formats.Cumulative_P, Dates, Conversion = Conversions.Cumulative_P, Variable = 'Pcum', Product = '', Unit = 'mm')
    ETcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_ET), Formats.Cumulative_ET, Dates, Conversion = Conversions.Cumulative_ET, Variable = 'ETcum', Product = '', Unit = 'mm')
    Soil_Moisture = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Soil_Moisture), Formats.Soil_Moisture, Dates, Conversion = Conversions.Soil_Moisture, Variable = 'Soil Moisture', Product = '', Unit = 'cm3/cm3')
    Crop_Water_Requirement = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Crop_Water_Requirement), Formats.Crop_Water_Requirement, Dates, Conversion = Conversions.Crop_Water_Requirement, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Crop Water Requirement', Product = '', Unit = 'mm/decade')
    Soil_Moisture_Long_Term = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Soil_Moisture_Long_Term), Formats.Soil_Moisture_Long_Term, Dates, Conversion = Conversions.Soil_Moisture_Long_Term, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Long Term Soil Moisture', Product = '', Unit = 'cm3/cm3')
   
    ######################## Calculate days in each dekads #################################
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)    

    ######################## Calculate Evapotranspiration deficit ########################
    ET_Deficit_Data = Crop_Water_Requirement.Data - ET.Data * Days_in_Dekads[:, None, None]

    # Write in DataCube
    ET_Deficit = DataCube.Rasterdata_Empty()
    ET_Deficit.Data = ET_Deficit_Data * MASK
    ET_Deficit.Projection = ET.Projection
    ET_Deficit.GeoTransform = ET.GeoTransform
    ET_Deficit.Ordinal_time = ET.Ordinal_time
    ET_Deficit.Size = ET_Deficit_Data.shape
    ET_Deficit.Variable = "Evapotranspiration Deficit"
    ET_Deficit.Unit = "mm-dekad-1"       

    del ET_Deficit_Data
    
    ET_Deficit.Save_As_Tiff(os.path.join(output_folder_L3, "ET_Deficit"))     
    
    ######################## Calculate Accumulated Rainfall Deficit over Season ########################
    Accumulated_Rainfall_Deficit_Data = Pcum.Data - ETcum.Data

    # Write in DataCube
    Accumulated_Rainfall_Deficit = DataCube.Rasterdata_Empty()
    Accumulated_Rainfall_Deficit.Data = Accumulated_Rainfall_Deficit_Data * MASK
    Accumulated_Rainfall_Deficit.Projection = ET.Projection
    Accumulated_Rainfall_Deficit.GeoTransform = ET.GeoTransform
    Accumulated_Rainfall_Deficit.Ordinal_time = ET.Ordinal_time
    Accumulated_Rainfall_Deficit.Size = Accumulated_Rainfall_Deficit_Data.shape
    Accumulated_Rainfall_Deficit.Variable = "Accumulated Rainfall Deficit"
    Accumulated_Rainfall_Deficit.Unit = "mm"       

    del Accumulated_Rainfall_Deficit_Data
    
    Accumulated_Rainfall_Deficit.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_Rainfall_Deficit"))     
    
    ######################## Calculate Soil Moisture Anomaly ########################
    Soil_Moisture_Anomaly_Data = (Soil_Moisture.Data - Soil_Moisture_Long_Term.Data)/Soil_Moisture_Long_Term.Data * 100 
 
    # Write in DataCube
    Soil_Moisture_Anomaly = DataCube.Rasterdata_Empty()
    Soil_Moisture_Anomaly.Data = Soil_Moisture_Anomaly_Data * MASK
    Soil_Moisture_Anomaly.Projection = ET.Projection
    Soil_Moisture_Anomaly.GeoTransform = ET.GeoTransform
    Soil_Moisture_Anomaly.Ordinal_time = ET.Ordinal_time
    Soil_Moisture_Anomaly.Size = Soil_Moisture_Anomaly_Data.shape
    Soil_Moisture_Anomaly.Variable = "Soil Moisture Anomaly"
    Soil_Moisture_Anomaly.Unit = "Percentage"       

    del Soil_Moisture_Anomaly_Data
    
    Soil_Moisture_Anomaly.Save_As_Tiff(os.path.join(output_folder_L3, "Soil_Moisture_Anomaly"))     
        
    ######################## Calculate Lake Reservoir Level Anomaly ########################
    #Lake_Reservoir_Level_Anomaly = 
    
    ######################## Calculate Open Water Anomaly ########################
    #Open_Water_Anomaly = 
    
    ######################## Calculate Integrated Drought Alert Level ########################
    Alert_limits = Alert_dict()
    
    Integrated_Drought_Alert_Level_ET_Deficit = np.ones(ET.Size) * np.nan
    Integrated_Drought_Alert_Level_P_Deficit = np.ones(ET.Size) * np.nan    
    Integrated_Drought_Alert_Level_Soil_Anomalies = np.ones(ET.Size) * np.nan
        
    for values in Alert_limits['et_deficit'].items():
        Integrated_Drought_Alert_Level_ET_Deficit = np.where(np.logical_and(ET_Deficit.Data > values[1][0], ET_Deficit.Data <= values[1][1]), values[0], Integrated_Drought_Alert_Level_ET_Deficit)
    for values in Alert_limits['p_deficit'].items():
        Integrated_Drought_Alert_Level_P_Deficit = np.where(np.logical_and(Accumulated_Rainfall_Deficit.Data > values[1][0], Accumulated_Rainfall_Deficit.Data <= values[1][1]), values[0], Integrated_Drought_Alert_Level_P_Deficit)
    for values in Alert_limits['soil_anomalies'].items():
        Integrated_Drought_Alert_Level_Soil_Anomalies = np.where(np.logical_and(Soil_Moisture_Anomaly.Data < values[1][0], Soil_Moisture_Anomaly.Data >= values[1][1]), values[0], Integrated_Drought_Alert_Level_Soil_Anomalies)

    Integrated_Drought_Alert_Level_Data = np.nanmax(np.stack((Integrated_Drought_Alert_Level_ET_Deficit, Integrated_Drought_Alert_Level_P_Deficit, Integrated_Drought_Alert_Level_Soil_Anomalies)),axis = 0)    

    # Write in DataCube
    Integrated_Drought_Alert_Level = DataCube.Rasterdata_Empty()
    Integrated_Drought_Alert_Level.Data = Integrated_Drought_Alert_Level_Data * MASK
    Integrated_Drought_Alert_Level.Projection = ET.Projection
    Integrated_Drought_Alert_Level.GeoTransform = ET.GeoTransform
    Integrated_Drought_Alert_Level.Ordinal_time = ET.Ordinal_time
    Integrated_Drought_Alert_Level.Size = Integrated_Drought_Alert_Level_Data.shape
    Integrated_Drought_Alert_Level.Variable = "Integrated Drought Alert Level"
    Integrated_Drought_Alert_Level.Unit = "Percentage"       

    del Integrated_Drought_Alert_Level_Data
    
    Integrated_Drought_Alert_Level.Save_As_Tiff(os.path.join(output_folder_L3, "Integrated_Drought_Alert_Level"))   
     
    return()
    
def Alert_dict(version = '1.0'):
    
    Alert_V1 = {
    'et_deficit':    {1: [-100, 9999],
               2: [-200, -100],
               3: [-300, -200],
               4: [-400, -300],
               5: [-9999, -400]},
    
    'p_deficit':    {1: [-9999, 5],
               2: [5, 10],
               3: [10, 15],
               4: [15, 20],
               5: [20, 9999]},
               
    'soil_anomalies': {1: [-10, 9999],
               2: [-20, -10],
               3: [-30, -20],
               4: [-40, -30],
               5: [-50, -9999]}}
                         
    Alert_dict = dict()
    Alert_dict['1.0'] = Alert_V1
    Alert_dict['2.0'] = Alert_V1
    
    return Alert_dict[version]    
    