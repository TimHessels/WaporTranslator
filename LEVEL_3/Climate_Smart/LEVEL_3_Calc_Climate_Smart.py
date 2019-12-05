# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:05:39 2019
"""

import os
import gdal
import warnings
import numpy as np

def main(Start_year_analyses, End_year_analyses, output_folder):

    import WaporTranslator.LEVEL_1.Input_Data as Inputs
    import WaporTranslator.LEVEL_1.DataCube as DataCube
    import WaporTranslator.LEVEL_2.Functions as Functions
    import WaporTranslator.LEVEL_3.Food_Security.LEVEL_3_Calc_Food_Security as L3_Food
        
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
    output_folder_L3 = os.path.join(output_folder, "LEVEL_3", "Climate_Smart")
    if not os.path.exists(output_folder_L3):
        os.makedirs(output_folder_L3)
    
    ################################# Dynamic maps #################################
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET), Formats.ET, Dates, Conversion = Conversions.ET, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = 'mm/day')
    NPP = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.NPP), Formats.NPP, Dates, Conversion = Conversions.NPP, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'NPP', Product = 'WAPOR', Unit = 'g/m2/d')
    CropType = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.LU_END), Formats.LU_END, Dates, Conversion = Conversions.LU_END, Variable = 'LU_END', Product = '', Unit = '-')
    CropSeason = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.CropSeason), Formats.CropSeason, Dates, Conversion = Conversions.CropSeason, Variable = 'CropSeason', Product = '', Unit = '-')
    Fractional_Vegetation_Cover = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Fractional_Vegetation_Cover), Formats.Fractional_Vegetation_Cover, Dates, Conversion = Conversions.Fractional_Vegetation_Cover, Variable = 'Fractional Vegetation Cover', Product = '', Unit = '-')
    Deep_Percolation = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Deep_Percolation), Formats.Deep_Percolation, Dates, Conversion = Conversions.Deep_Percolation, Variable = 'Deep Percolation', Product = '', Unit = 'mm/decade')
    Surface_Runoff_P = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Surface_Runoff_P), Formats.Surface_Runoff_P, Dates, Conversion = Conversions.Surface_Runoff_P, Variable = 'Surface Runoff Precipitation', Product = '', Unit = 'mm/decade')
    Net_Radiation = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Net_Radiation), Formats.Net_Radiation, Dates, Conversion = Conversions.Net_Radiation, Variable = 'Net Radiation', Product = '', Unit = 'W/m2')
    Evaporative_Fraction = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.EF), Formats.EF, Dates, Conversion = Conversions.EF, Variable = 'Evaporative Fraction', Product = '', Unit = '-')
    Wind = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Wind), Formats.Wind, Dates, Conversion = Conversions.Wind, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Wind Speed', Product = '', Unit = 'm/s')
    
    ################################# Static maps #################################     
    Soil_Organic_Carbon_Stock2 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.SOCS), Formats.SOCS.format(level = 2), Dates = None, Conversion = Conversions.SOCS, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Soil Organic Carbon Stock level 2', Product = '', Unit = 'ton/ha')
    Soil_Organic_Carbon_Stock3 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.SOCS), Formats.SOCS.format(level = 3), Dates = None, Conversion = Conversions.SOCS, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Soil Organic Carbon Stock level 2', Product = '', Unit = 'ton/ha')
    Soil_Organic_Carbon_Stock4 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.SOCS), Formats.SOCS.format(level = 4), Dates = None, Conversion = Conversions.SOCS, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Soil Organic Carbon Stock level 2', Product = '', Unit = 'ton/ha')
    Soil_Organic_Carbon_Content1 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.SOCC), Formats.SOCC.format(level = 1), Dates = None, Conversion = Conversions.SOCC, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Soil Organic Carbon Content level 1', Product = '', Unit = 'gr/kg')
    PH10 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.PH10), Formats.PH10.format(level = 1), Dates = None, Conversion = Conversions.PH10, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'PH10 for level 1', Product = '', Unit = 'ton/ha')
    Clay =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Clay), Formats.Clay.format(level=6), Dates = None, Conversion = Conversions.Clay, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Clay', Product = 'SoilGrids', Unit = 'Percentage')
    Silt =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Silt), Formats.Silt.format(level=6), Dates = None, Conversion = Conversions.Silt, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Silt', Product = 'SoilGrids', Unit = 'Percentage')
    Sand =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Sand), Formats.Sand.format(level=6), Dates = None, Conversion = Conversions.Sand, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Sand', Product = 'SoilGrids', Unit = 'Percentage')
    DEM =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.DEM), Formats.DEM, Dates = None, Conversion = Conversions.DEM, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'DEM', Product = 'SRTM', Unit = 'm')

    ######################## Calculate days in each dekads #################################
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)
    
    ################################# Calculate Crop Season and LU #################################
    Season_Type = L3_Food.Calc_Crops(CropType, CropSeason, MASK)
    
    ################################# Calculate Carbon Root Zone  #################################
    # Calculate Carbon Root Zone Cropland       
    Carbon_Root_Zone_Cropland = (Soil_Organic_Carbon_Stock2.Data + Soil_Organic_Carbon_Stock3.Data + Soil_Organic_Carbon_Stock4.Data) * 1000
    
    # Calculate Carbon Root Zone Pasture
    Carbon_Root_Zone_Pasture =(Soil_Organic_Carbon_Stock2.Data + Soil_Organic_Carbon_Stock3.Data) * 1000
    
    # Carbon Root Zone
    Carbon_Root_Zone_Data = np.where(Season_Type.Data==5, Carbon_Root_Zone_Pasture[None, :, :], Carbon_Root_Zone_Cropland[None, :, :])

    # Write in DataCube
    Carbon_Root_Zone = DataCube.Rasterdata_Empty()
    Carbon_Root_Zone.Data = Carbon_Root_Zone_Data * MASK
    Carbon_Root_Zone.Projection = ET.Projection
    Carbon_Root_Zone.GeoTransform = ET.GeoTransform
    Carbon_Root_Zone.Ordinal_time = ET.Ordinal_time
    Carbon_Root_Zone.Size = Carbon_Root_Zone_Data.shape
    Carbon_Root_Zone.Variable = "Carbon Root Zone"
    Carbon_Root_Zone.Unit = "kg-ha-1"       

    del Carbon_Root_Zone_Data
    
    Carbon_Root_Zone.Save_As_Tiff(os.path.join(output_folder_L3, "Carbon_Root_Zone"))    
    
    ################################# Calculate Carbon Sequestration #################################
    # Calculate Sequestration Cropland    
    Carbon_Sequestration_Cropland =10 * NPP.Data * (1 - 4/(4 + 1)) * Days_in_Dekads[:, None, None] * 0.3
    
    # Calculate Sequestration Pasture
    Carbon_Sequestration_Pasture =10 * NPP.Data * (1 - 1.5/(1.5 + 1)) * Days_in_Dekads[:, None, None] * 0.7
    
    # Carbon Root Zone
    Carbon_Sequestration_Data = np.where(Season_Type.Data==5, Carbon_Sequestration_Pasture, Carbon_Sequestration_Cropland)

    # Write in DataCube
    Carbon_Sequestration = DataCube.Rasterdata_Empty()
    Carbon_Sequestration.Data = Carbon_Sequestration_Data * MASK
    Carbon_Sequestration.Projection = ET.Projection
    Carbon_Sequestration.GeoTransform = ET.GeoTransform
    Carbon_Sequestration.Ordinal_time = ET.Ordinal_time
    Carbon_Sequestration.Size = Carbon_Sequestration_Data.shape
    Carbon_Sequestration.Variable = "Carbon Sequestration"
    Carbon_Sequestration.Unit = "kg-ha-1-dekad-1"       

    del Carbon_Sequestration_Data
    
    Carbon_Sequestration.Save_As_Tiff(os.path.join(output_folder_L3, "Carbon_Sequestration"))       
    
    ################################# Calculate Climatic Cooling #################################
    Climatic_Cooling_Data =((0.7 * Net_Radiation.Data - (1 - Evaporative_Fraction.Data) * Net_Radiation.Data) * (208/Wind.Data))/(1.15 * 1004)

    # Write in DataCube
    Climatic_Cooling = DataCube.Rasterdata_Empty()
    Climatic_Cooling.Data = Climatic_Cooling_Data * MASK
    Climatic_Cooling.Projection = ET.Projection
    Climatic_Cooling.GeoTransform = ET.GeoTransform
    Climatic_Cooling.Ordinal_time = ET.Ordinal_time
    Climatic_Cooling.Size = Climatic_Cooling_Data.shape
    Climatic_Cooling.Variable = "Climatic Cooling"
    Climatic_Cooling.Unit = "Celcius-dekad-1"       

    del Climatic_Cooling_Data
    
    Climatic_Cooling.Save_As_Tiff(os.path.join(output_folder_L3, "Climatic_Cooling"))       
    
    ################################# Calculate Water Generation #################################
    Water_Generation_Data =(Surface_Runoff_P.Data + Deep_Percolation.Data) * 10

    # Write in DataCube
    Water_Generation = DataCube.Rasterdata_Empty()
    Water_Generation.Data = Water_Generation_Data * MASK
    Water_Generation.Projection = ET.Projection
    Water_Generation.GeoTransform = ET.GeoTransform
    Water_Generation.Ordinal_time = ET.Ordinal_time
    Water_Generation.Size = Water_Generation_Data.shape
    Water_Generation.Variable = "Water Generation"
    Water_Generation.Unit = "m3-ha-1-dekad-1"       

    del Water_Generation_Data
    
    Water_Generation.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Generation"))       

    ################################# Calculate Soil Erodibility #################################
    Soil_Erodibility_Data =(0.043 * PH10.Data + 0.062/(Soil_Organic_Carbon_Content1.Data * 10) + 0.0082 * Sand.Data - 0.0062 * Clay.Data) * Silt.Data/10
    
    # Write in DataCube
    Soil_Erodibility = DataCube.Rasterdata_Empty()
    Soil_Erodibility.Data = Soil_Erodibility_Data * MASK
    Soil_Erodibility.Projection = ET.Projection
    Soil_Erodibility.GeoTransform = ET.GeoTransform
    Soil_Erodibility.Ordinal_time = None
    Soil_Erodibility.Size = Soil_Erodibility_Data.shape
    Soil_Erodibility.Variable = "Soil Erodibility"
    Soil_Erodibility.Unit = "-"       

    del Soil_Erodibility_Data
    
    Soil_Erodibility.Save_As_Tiff(os.path.join(output_folder_L3, "Soil_Erodibility"))         
    
    ################################# Calculate Combating Soil Erosion #################################
    Combating_Soil_Erosion_Data =50 * Water_Generation.Data * Soil_Erodibility.Data * 1 * DEM.Data[None, :, :] * Fractional_Vegetation_Cover.Data * 0.5

    # Write in DataCube
    Combating_Soil_Erosion = DataCube.Rasterdata_Empty()
    Combating_Soil_Erosion.Data = Combating_Soil_Erosion_Data * MASK
    Combating_Soil_Erosion.Projection = ET.Projection
    Combating_Soil_Erosion.GeoTransform = ET.GeoTransform
    Combating_Soil_Erosion.Ordinal_time = ET.Ordinal_time
    Combating_Soil_Erosion.Size = Combating_Soil_Erosion_Data.shape
    Combating_Soil_Erosion.Variable = "Combating Soil Erosion"
    Combating_Soil_Erosion.Unit = "kg-ha-1-dekad-1"       

    del Combating_Soil_Erosion_Data
    
    Combating_Soil_Erosion.Save_As_Tiff(os.path.join(output_folder_L3, "Combating_Soil_Erosion"))      

    ################################# Calculate Sustaining Rainfall #################################
    Sustaining_Rainfall_Data = 0.2 * ET.Data * Days_in_Dekads[:, None, None]
    
    # Write in DataCube
    Sustaining_Rainfall = DataCube.Rasterdata_Empty()
    Sustaining_Rainfall.Data = Sustaining_Rainfall_Data * MASK
    Sustaining_Rainfall.Projection = ET.Projection
    Sustaining_Rainfall.GeoTransform = ET.GeoTransform
    Sustaining_Rainfall.Ordinal_time = ET.Ordinal_time
    Sustaining_Rainfall.Size = Sustaining_Rainfall_Data.shape
    Sustaining_Rainfall.Variable = "Sustaining Rainfall"
    Sustaining_Rainfall.Unit = "m3-ha-1-dekad-1"       

    del Sustaining_Rainfall_Data
    
    Sustaining_Rainfall.Save_As_Tiff(os.path.join(output_folder_L3, "Sustaining_Rainfall"))          

    ################################# Calculate NPP Change In Time #################################
    
    # Set time
    T = np.arange(len(Dates)) 
    
    # Calculate trend
    trend_dekad = ((np.sum(np.where(np.isnan(NPP.Data),0,1),axis = 0) * np.nansum(NPP.Data * T[:,None,None], axis = 0)) - (np.nansum(NPP.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(NPP.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    trend_year = trend_dekad * 36 
    NPP_Change_In_Time_Data = trend_year / np.nanmean(NPP.Data, axis = 0) * 100
        
    # Write in DataCube
    NPP_Change_In_Time = DataCube.Rasterdata_Empty()
    NPP_Change_In_Time.Data = NPP_Change_In_Time_Data * MASK
    NPP_Change_In_Time.Projection = ET.Projection
    NPP_Change_In_Time.GeoTransform = ET.GeoTransform
    NPP_Change_In_Time.Ordinal_time = None
    NPP_Change_In_Time.Size = NPP_Change_In_Time_Data.shape
    NPP_Change_In_Time.Variable = "NPP Change In Time Data"
    NPP_Change_In_Time.Unit = "Percentage-year-1"       

    del NPP_Change_In_Time_Data
    
    NPP_Change_In_Time.Save_As_Tiff(os.path.join(output_folder_L3, "NPP_Change_In_Time"))    
        
    return()