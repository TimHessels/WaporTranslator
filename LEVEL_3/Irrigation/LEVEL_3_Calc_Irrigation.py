# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:06:20 2019
"""

import os
import gdal
import warnings
import pandas as pd
import numpy as np

import WaporTranslator.LEVEL_1.Input_Data as Inputs
import WaporTranslator.LEVEL_1.DataCube as DataCube
import WaporTranslator.LEVEL_2.Functions as Functions

def main(Start_year_analyses, End_year_analyses, output_folder):

    # Do not show non relevant warnings
    warnings.filterwarnings("ignore")
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    Startdate = "%s-01-01" %Start_year_analyses
    Enddate = "%s-12-31" %End_year_analyses
    
    # Define dates
    Dates = Functions.Get_Dekads(Start_year_analyses, End_year_analyses)
    Dates_Years = pd.date_range(Startdate, Enddate, freq = "AS")
    
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
    output_folder_L3 = os.path.join(output_folder, "LEVEL_3", "Irrigation")
    if not os.path.exists(output_folder_L3):
        os.makedirs(output_folder_L3)
    
    ################################# Dynamic maps #################################
    Crop_Water_Requirement = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Crop_Water_Requirement), Formats.Crop_Water_Requirement, Dates, Conversion = Conversions.Crop_Water_Requirement, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Crop Water Requirement', Product = '', Unit = 'mm/decade')
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET), Formats.ET, Dates, Conversion = Conversions.ET, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = 'mm/day')
    E = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.E), Formats.E, Dates, Conversion = Conversions.E, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'E', Product = 'WAPOR', Unit = 'mm/day')
    I = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.I), Formats.I, Dates, Conversion = Conversions.I, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'I', Product = 'WAPOR', Unit = 'mm/day')
    P = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.P), Formats.P, Dates, Conversion = Conversions.P, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'P', Product = 'WAPOR', Unit = 'mm/day')
    Critical_Soil_Moisture = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Critical_Soil_Moisture), Formats.Critical_Soil_Moisture, Dates, Conversion = Conversions.Critical_Soil_Moisture, Variable = 'Critical Soil Moisture', Product = 'SoilGrids', Unit = 'cm3/cm3')
    Soil_Moisture = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Soil_Moisture), Formats.Soil_Moisture, Dates, Conversion = Conversions.Soil_Moisture, Variable = 'Soil Moisture', Product = '', Unit = 'cm3/cm3')
    Net_Supply_Drainage  = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Net_Supply_Drainage), Formats.Net_Supply_Drainage, Dates, Conversion = Conversions.Net_Supply_Drainage, Variable = 'Net Supply Drainage', Product = '', Unit = 'mm/decade')
    Deep_Percolation = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Deep_Percolation), Formats.Deep_Percolation, Dates, Conversion = Conversions.Deep_Percolation, Variable = 'Deep Percolation', Product = '', Unit = 'mm/decade')
    Surface_Runoff_Coefficient = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Surface_Runoff_Coefficient), Formats.Surface_Runoff_Coefficient, Dates, Conversion = Conversions.Surface_Runoff_Coefficient, Variable = 'Surface Runoff Coefficient', Product = '', Unit = '-')
    Surface_Runoff_P = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Surface_Runoff_P), Formats.Surface_Runoff_P, Dates, Conversion = Conversions.Surface_Runoff_P, Variable = 'Surface Runoff Precipitation', Product = '', Unit = 'mm/decade')
    AEZ = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.AEZ), Formats.AEZ, Dates, Conversion = Conversions.AEZ, Variable = 'Surface Runoff Coefficient', Product = '', Unit = '-')  
    ETcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_ET), Formats.Cumulative_ET, Dates, Conversion = Conversions.Cumulative_ET, Variable = 'Cumulated Evapotranspiration', Product = '', Unit = 'mm/decade')      
    Irrigation = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Irrigation), Formats.Irrigation, Dates, Conversion = Conversions.Irrigation, Variable = 'Irrigation', Product = '', Unit = '-')  
    
    ################################# Static maps #################################     
    Theta_FC_Subsoil = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Theta_FC_Subsoil), Formats.Theta_FC_Subsoil, Dates = None, Conversion = Conversions.Theta_FC_Subsoil, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Theta Field Capacity Subsoil', Product = 'SoilGrids', Unit = 'cm3/cm3')

    ######################## Calculate days in each dekads #################################
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)

    ######################## Calculate Irrigation Water Requirement ########################
    Irrigation_Water_Requirement_Data = (Crop_Water_Requirement.Data - 0.7 * P.Data * Days_in_Dekads[:, None, None])/(0.65)
 
    # Write in DataCube
    Irrigation_Water_Requirement = DataCube.Rasterdata_Empty()
    Irrigation_Water_Requirement.Data = Irrigation_Water_Requirement_Data * MASK
    Irrigation_Water_Requirement.Projection = ET.Projection
    Irrigation_Water_Requirement.GeoTransform = ET.GeoTransform
    Irrigation_Water_Requirement.Ordinal_time = ET.Ordinal_time
    Irrigation_Water_Requirement.Size = Irrigation_Water_Requirement_Data.shape
    Irrigation_Water_Requirement.Variable = "Irrigation Water Requirement"
    Irrigation_Water_Requirement.Unit = "mm-dekad-1"
    
    del Irrigation_Water_Requirement_Data
    
    Irrigation_Water_Requirement.Save_As_Tiff(os.path.join(output_folder_L3, "Irrigation_Water_Requirement"))    

    ######################## Calculate ETblue ########################
    ETblue_Data = np.where(ET.Data > 0.7 * P.Data, Days_in_Dekads[:, None, None] * (ET.Data - 0.7 * P.Data), 0)
    
    # Write in DataCube
    ETblue = DataCube.Rasterdata_Empty()
    ETblue.Data = ETblue_Data * MASK
    ETblue.Projection = ET.Projection
    ETblue.GeoTransform = ET.GeoTransform
    ETblue.Ordinal_time = ET.Ordinal_time
    ETblue.Size = ETblue_Data.shape
    ETblue.Variable = "Blue Evapotranspiration"
    ETblue.Unit = "mm-dekad-1"
    
    del ETblue_Data
    
    ETblue.Save_As_Tiff(os.path.join(output_folder_L3, "ETblue"))    
    
    ######################## Calculate Gross Irrigation Water Supply ########################
    Gross_Irrigation_Water_Supply_Data = np.maximum(0, (Net_Supply_Drainage.Data + Deep_Percolation.Data + Surface_Runoff_P.Data) * (1 + Surface_Runoff_Coefficient.Data))
    Gross_Irrigation_Water_Supply_Data = np.minimum(1/0.95 * ETblue.Data, Gross_Irrigation_Water_Supply_Data)
    
    # Write in DataCube
    Gross_Irrigation_Water_Supply = DataCube.Rasterdata_Empty()
    Gross_Irrigation_Water_Supply.Data = Gross_Irrigation_Water_Supply_Data * MASK
    Gross_Irrigation_Water_Supply.Projection = ET.Projection
    Gross_Irrigation_Water_Supply.GeoTransform = ET.GeoTransform
    Gross_Irrigation_Water_Supply.Ordinal_time = ET.Ordinal_time
    Gross_Irrigation_Water_Supply.Size = Gross_Irrigation_Water_Supply_Data.shape
    Gross_Irrigation_Water_Supply.Variable = "Gross Irrigation Water Supply"
    Gross_Irrigation_Water_Supply.Unit = "mm-dekad-1"
    
    del Gross_Irrigation_Water_Supply_Data
    
    Gross_Irrigation_Water_Supply.Save_As_Tiff(os.path.join(output_folder_L3, "Gross_Irrigation_Water_Supply"))    
    
    ######################## Calculate Adequacy Relative Water Supply ########################
    Adequacy_Relative_Water_Supply_Data = (Gross_Irrigation_Water_Supply.Data + P.Data * Days_in_Dekads[:, None, None])/Crop_Water_Requirement.Data
    
    # Write in DataCube
    Adequacy_Relative_Water_Supply = DataCube.Rasterdata_Empty()
    Adequacy_Relative_Water_Supply.Data = Adequacy_Relative_Water_Supply_Data * MASK
    Adequacy_Relative_Water_Supply.Projection = ET.Projection
    Adequacy_Relative_Water_Supply.GeoTransform = ET.GeoTransform
    Adequacy_Relative_Water_Supply.Ordinal_time = ET.Ordinal_time
    Adequacy_Relative_Water_Supply.Size = Adequacy_Relative_Water_Supply_Data.shape
    Adequacy_Relative_Water_Supply.Variable = "Adequacy Relative Water Supply"
    Adequacy_Relative_Water_Supply.Unit = "-"
    
    del Adequacy_Relative_Water_Supply_Data
    
    Adequacy_Relative_Water_Supply.Save_As_Tiff(os.path.join(output_folder_L3, "Adequacy_Relative_Water_Supply"))    
       
    ######################## Calculate Adequacy Relative Irrigation Water Supply ########################
    Adequacy_Relative_Irrigation_Water_Supply_Data = Gross_Irrigation_Water_Supply.Data/Irrigation_Water_Requirement.Data
    
    # Write in DataCube
    Adequacy_Relative_Irrigation_Water_Supply = DataCube.Rasterdata_Empty()
    Adequacy_Relative_Irrigation_Water_Supply.Data = Adequacy_Relative_Irrigation_Water_Supply_Data * MASK
    Adequacy_Relative_Irrigation_Water_Supply.Projection = ET.Projection
    Adequacy_Relative_Irrigation_Water_Supply.GeoTransform = ET.GeoTransform
    Adequacy_Relative_Irrigation_Water_Supply.Ordinal_time = ET.Ordinal_time
    Adequacy_Relative_Irrigation_Water_Supply.Size = Adequacy_Relative_Irrigation_Water_Supply_Data.shape
    Adequacy_Relative_Irrigation_Water_Supply.Variable = "Adequacy Relative Irrigation Water Supply"
    Adequacy_Relative_Irrigation_Water_Supply.Unit = "-"
    
    del Adequacy_Relative_Irrigation_Water_Supply_Data
    
    Adequacy_Relative_Irrigation_Water_Supply.Save_As_Tiff(os.path.join(output_folder_L3, "Adequacy_Relative_Irrigation_Water_Supply"))    

     
    ######################## Calculate Non Consumptive Use Due To Irrigation ########################
    Non_Consumptive_Use_Due_To_Irrigation_Data = np.maximum(0, Gross_Irrigation_Water_Supply.Data - ETblue.Data)

    # Write in DataCube
    Non_Consumptive_Use_Due_To_Irrigation = DataCube.Rasterdata_Empty()
    Non_Consumptive_Use_Due_To_Irrigation.Data = Non_Consumptive_Use_Due_To_Irrigation_Data * MASK
    Non_Consumptive_Use_Due_To_Irrigation.Projection = ET.Projection
    Non_Consumptive_Use_Due_To_Irrigation.GeoTransform = ET.GeoTransform
    Non_Consumptive_Use_Due_To_Irrigation.Ordinal_time = ET.Ordinal_time
    Non_Consumptive_Use_Due_To_Irrigation.Size = Non_Consumptive_Use_Due_To_Irrigation_Data.shape
    Non_Consumptive_Use_Due_To_Irrigation.Variable = "Non Consumptive Use Due To Irrigation"
    Non_Consumptive_Use_Due_To_Irrigation.Unit = "mm-dekad-1"
    
    del Non_Consumptive_Use_Due_To_Irrigation_Data
    
    Non_Consumptive_Use_Due_To_Irrigation.Save_As_Tiff(os.path.join(output_folder_L3, "Non_Consumptive_Use_Due_To_Irrigation"))    
    
    ######################### Calculate Onfarm Irrigation Efficiency ########################
    Onfarm_Irrigation_Efficiency_Data = ETblue.Data/Gross_Irrigation_Water_Supply.Data * 100
    
    # Write in DataCube
    Onfarm_Irrigation_Efficiency = DataCube.Rasterdata_Empty()
    Onfarm_Irrigation_Efficiency.Data = Onfarm_Irrigation_Efficiency_Data * MASK
    Onfarm_Irrigation_Efficiency.Projection = ET.Projection
    Onfarm_Irrigation_Efficiency.GeoTransform = ET.GeoTransform
    Onfarm_Irrigation_Efficiency.Ordinal_time = ET.Ordinal_time
    Onfarm_Irrigation_Efficiency.Size = Onfarm_Irrigation_Efficiency_Data.shape
    Onfarm_Irrigation_Efficiency.Variable = "Onfarm Irrigation Efficiency"
    Onfarm_Irrigation_Efficiency.Unit = "Percentage"
    
    del Onfarm_Irrigation_Efficiency_Data
    
    Onfarm_Irrigation_Efficiency.Save_As_Tiff(os.path.join(output_folder_L3, "Onfarm_Irrigation_Efficiency"))    
    
    ########################## Calculate Degree Of Over Irrigation #########################
    Degree_Of_Over_Irrigation_Data = Soil_Moisture.Data/Theta_FC_Subsoil.Data[None, :, :]
 
    # Write in DataCube
    Degree_Of_Over_Irrigation = DataCube.Rasterdata_Empty()
    Degree_Of_Over_Irrigation.Data = Degree_Of_Over_Irrigation_Data * MASK
    Degree_Of_Over_Irrigation.Projection = ET.Projection
    Degree_Of_Over_Irrigation.GeoTransform = ET.GeoTransform
    Degree_Of_Over_Irrigation.Ordinal_time = ET.Ordinal_time
    Degree_Of_Over_Irrigation.Size = Degree_Of_Over_Irrigation_Data.shape
    Degree_Of_Over_Irrigation.Variable = "Degree Of Over Irrigation"
    Degree_Of_Over_Irrigation.Unit = "-"
    
    del Degree_Of_Over_Irrigation_Data
    
    Degree_Of_Over_Irrigation.Save_As_Tiff(os.path.join(output_folder_L3, "Degree_Of_Over_Irrigation"))        
    
    ########################### Calculate Adequacy Degree Of Under Irrigation ##########################
    Degree_Of_Under_Irrigation_Data = Soil_Moisture.Data/Critical_Soil_Moisture.Data
 
    # Write in DataCube
    Degree_Of_Under_Irrigation = DataCube.Rasterdata_Empty()
    Degree_Of_Under_Irrigation.Data = Degree_Of_Under_Irrigation_Data * MASK
    Degree_Of_Under_Irrigation.Projection = ET.Projection
    Degree_Of_Under_Irrigation.GeoTransform = ET.GeoTransform
    Degree_Of_Under_Irrigation.Ordinal_time = ET.Ordinal_time
    Degree_Of_Under_Irrigation.Size = Degree_Of_Under_Irrigation_Data.shape
    Degree_Of_Under_Irrigation.Variable = "Adequacy Degree Of Under Irrigation"
    Degree_Of_Under_Irrigation.Unit = "-"
    
    del Degree_Of_Under_Irrigation_Data
    
    Degree_Of_Under_Irrigation.Save_As_Tiff(os.path.join(output_folder_L3, "Degree_Of_Under_Irrigation"))       
    
    ############################ Calculate Adequacy Crop Water Deficit ###########################
    Adequacy_Crop_Water_Deficit_Data = Crop_Water_Requirement.Data - ET.Data * Days_in_Dekads[:, None, None]
    
    # Write in DataCube
    Adequacy_Crop_Water_Deficit = DataCube.Rasterdata_Empty()
    Adequacy_Crop_Water_Deficit.Data = Adequacy_Crop_Water_Deficit_Data * MASK
    Adequacy_Crop_Water_Deficit.Projection = ET.Projection
    Adequacy_Crop_Water_Deficit.GeoTransform = ET.GeoTransform
    Adequacy_Crop_Water_Deficit.Ordinal_time = ET.Ordinal_time
    Adequacy_Crop_Water_Deficit.Size = Adequacy_Crop_Water_Deficit_Data.shape
    Adequacy_Crop_Water_Deficit.Variable = "Adequacy Crop Water Deficit"
    Adequacy_Crop_Water_Deficit.Unit = "mm-dekad-1"
    
    del Adequacy_Crop_Water_Deficit_Data
    
    Adequacy_Crop_Water_Deficit.Save_As_Tiff(os.path.join(output_folder_L3, "Adequacy_Crop_Water_Deficit"))          

    ################################# Calculate Spatial Target Evapotranspiration #################################
    L3_AEZ_ET = dict()
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        L3_AEZ_ET[int(AEZ_ID)] = np.nanpercentile(np.where(AEZ.Data == AEZ_ID, ET.Data, np.nan), 99, axis=(1,2))
    
    ################################# Create spatial target maps #################################
    ET_Target_Spatial_Data = np.ones(Adequacy_Crop_Water_Deficit.Size) * np.nan
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        ET_Target_Spatial_Data = np.where(AEZ.Data == AEZ_ID, L3_AEZ_ET[int(AEZ_ID)][:, None, None], ET_Target_Spatial_Data)
    
    ############################# Calculate Target Evapotranspiration ############################

    ET_Target_Spatial_Data = ET_Target_Spatial_Data
  
    # Write in DataCube
    ET_Target_Spatial = DataCube.Rasterdata_Empty()
    ET_Target_Spatial.Data = ET_Target_Spatial_Data * MASK
    ET_Target_Spatial.Projection = ET.Projection
    ET_Target_Spatial.GeoTransform = ET.GeoTransform
    ET_Target_Spatial.Ordinal_time = ET.Ordinal_time
    ET_Target_Spatial.Size = ET_Target_Spatial_Data.shape
    ET_Target_Spatial.Variable = "Target Evapotranspiration Spatial"
    ET_Target_Spatial.Unit = "mm-dekad-1"
    
    del ET_Target_Spatial_Data
    
    ET_Target_Spatial.Save_As_Tiff(os.path.join(output_folder_L3, "ET_Target_Spatial"))         
    
    ############################## Calculate Evapotranspiration Savings #############################
    ET_Savings_Spatial_Data = np.minimum(0, ET_Target_Spatial.Data - ET.Data * Days_in_Dekads[:, None, None])
 
    # Write in DataCube
    ET_Savings_Spatial = DataCube.Rasterdata_Empty()
    ET_Savings_Spatial.Data = ET_Savings_Spatial_Data * MASK
    ET_Savings_Spatial.Projection = ET.Projection
    ET_Savings_Spatial.GeoTransform = ET.GeoTransform
    ET_Savings_Spatial.Ordinal_time = ET.Ordinal_time
    ET_Savings_Spatial.Size = ET_Savings_Spatial_Data.shape
    ET_Savings_Spatial.Variable = "Evapotranspiration Savings Spatial"
    ET_Savings_Spatial.Unit = "mm-dekad-1"
    
    del ET_Savings_Spatial_Data
    
    ET_Savings_Spatial.Save_As_Tiff(os.path.join(output_folder_L3, "ET_Savings_Spatial"))          
    
    ################################# Calculate 10 year mean Evapotranspiration #################################
    
    Total_years = int(np.ceil(ET.Size[0]/36))
    Mean_Long_Term_ET_Data = np.ones([36, ET.Size[1], ET.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=ET.Size[0]]
        Mean_Long_Term_ET_Data[dekad, :, :] = np.nanmean(ET.Data[IDs_good,:,:] * Days_in_Dekads[IDs_good, None, None], axis = 0) 
 
    # Write in DataCube
    Mean_Long_Term_ET = DataCube.Rasterdata_Empty()
    Mean_Long_Term_ET.Data = Mean_Long_Term_ET_Data * MASK
    Mean_Long_Term_ET.Projection = ET.Projection
    Mean_Long_Term_ET.GeoTransform = ET.GeoTransform
    Mean_Long_Term_ET.Ordinal_time = "Long_Term_Decade"
    Mean_Long_Term_ET.Size = Mean_Long_Term_ET_Data.shape
    Mean_Long_Term_ET.Variable = "Mean Long Term Evapotranspiration"
    Mean_Long_Term_ET.Unit = "mm-dekad-1"       

    del Mean_Long_Term_ET_Data
    
    Mean_Long_Term_ET.Save_As_Tiff(os.path.join(output_folder_L3, "Mean_Long_Term_Evapotranspiration"))
    
    ################################## Calculate Gap in Evapotranspiration #################################
    ET_Gap_Temporal_Data = np.minimum(0, np.tile(Mean_Long_Term_ET.Data, (Total_years, 1, 1)) - ET.Data * Days_in_Dekads[:, None, None])

    # Write in DataCube    
    ET_Gap_Temporal = DataCube.Rasterdata_Empty()
    ET_Gap_Temporal.Data = ET_Gap_Temporal_Data * MASK
    ET_Gap_Temporal.Projection = ET.Projection
    ET_Gap_Temporal.GeoTransform = ET.GeoTransform
    ET_Gap_Temporal.Ordinal_time = ET.Ordinal_time
    ET_Gap_Temporal.Size = ET_Gap_Temporal_Data.shape
    ET_Gap_Temporal.Variable = "Evapotranspiration Gap Temporal"
    ET_Gap_Temporal.Unit = "mm-dekad-1"       

    del ET_Gap_Temporal_Data
    
    ET_Gap_Temporal.Save_As_Tiff(os.path.join(output_folder_L3, "ETgap"))

    ################################### Calculate Feasible Water Conservation ##################################
    Feasible_Water_Conservation_Data =(ET_Savings_Spatial.Data + ET_Gap_Temporal.Data)/2

    # Write in DataCube
    Feasible_Water_Conservation = DataCube.Rasterdata_Empty()
    Feasible_Water_Conservation.Data = Feasible_Water_Conservation_Data * MASK
    Feasible_Water_Conservation.Projection = ET.Projection
    Feasible_Water_Conservation.GeoTransform = ET.GeoTransform
    Feasible_Water_Conservation.Ordinal_time = ET.Ordinal_time
    Feasible_Water_Conservation.Size = Feasible_Water_Conservation_Data.shape
    Feasible_Water_Conservation.Variable = "Feasible Water Conservation"
    Feasible_Water_Conservation.Unit = "mm-dekad-1"       

    del Feasible_Water_Conservation_Data
    
    Feasible_Water_Conservation.Save_As_Tiff(os.path.join(output_folder_L3, "Feasible_Water_Conservation"))
    
    #################################### Calculate Non Beneficial Water Losses ###################################
    Non_Beneficial_Water_Losses_Data = (E.Data + I.Data) * Days_in_Dekads[:, None, None]

    # Write in DataCube 
    Non_Beneficial_Water_Losses = DataCube.Rasterdata_Empty()
    Non_Beneficial_Water_Losses.Data = Non_Beneficial_Water_Losses_Data * MASK
    Non_Beneficial_Water_Losses.Projection = ET.Projection
    Non_Beneficial_Water_Losses.GeoTransform = ET.GeoTransform
    Non_Beneficial_Water_Losses.Ordinal_time = ET.Ordinal_time
    Non_Beneficial_Water_Losses.Size = Non_Beneficial_Water_Losses_Data.shape
    Non_Beneficial_Water_Losses.Variable = "Non Beneficial Water Losses"
    Non_Beneficial_Water_Losses.Unit = "mm-dekad-1"       

    del Non_Beneficial_Water_Losses_Data
    
    Non_Beneficial_Water_Losses.Save_As_Tiff(os.path.join(output_folder_L3, "Non_Beneficial_Water_Losses"))    
    
    ##################################### Calculate Equity ####################################
    Soil_Moisture_Irrigated = Soil_Moisture.Data * Irrigation.Data
    Equity_Soil_Moisture_Data = np.nanstd(Soil_Moisture_Irrigated, axis = (1,2))/np.nanmean(Soil_Moisture_Irrigated, axis = (1,2))
    Equity_Soil_Moisture_Data_Map = np.where(Irrigation.Data == 1, Equity_Soil_Moisture_Data[:, None, None], np.nan)
 
    # Write in DataCube
    Equity_Soil_Moisture = DataCube.Rasterdata_Empty()
    Equity_Soil_Moisture.Data = Equity_Soil_Moisture_Data_Map * MASK
    Equity_Soil_Moisture.Projection = ET.Projection
    Equity_Soil_Moisture.GeoTransform = ET.GeoTransform
    Equity_Soil_Moisture.Ordinal_time = ET.Ordinal_time
    Equity_Soil_Moisture.Size = Equity_Soil_Moisture_Data_Map.shape
    Equity_Soil_Moisture.Variable = "Equity Soil Moisture"
    Equity_Soil_Moisture.Unit = "-"       

    del Equity_Soil_Moisture_Data_Map
    
    Equity_Soil_Moisture.Save_As_Tiff(os.path.join(output_folder_L3, "Equity_Soil_Moisture"))    
    
    ##################################### Calculate Reliability #####################################
    Soil_Moisture_Season = np.where(np.isnan(ETcum.Data), np.nan, Soil_Moisture.Data)
    Reliability_Soil_Moisture_Data = np.ones([Total_years, ET.Size[1], ET.Size[2]]) * np.nan
    for i in range(0, Total_years):
        Start = int(i * 36)
        End = int(Start + 36)
        Reliability_Soil_Moisture_Data[i, :, :] = np.nanstd(Soil_Moisture_Season[Start:End, : ,:], axis = 0)/np.nanmean(Soil_Moisture_Season[Start:End, : ,:], axis = 0) 

    # Write in DataCube    
    Reliability_Soil_Moisture = DataCube.Rasterdata_Empty()
    Reliability_Soil_Moisture.Data = Reliability_Soil_Moisture_Data * MASK
    Reliability_Soil_Moisture.Projection = ET.Projection
    Reliability_Soil_Moisture.GeoTransform = ET.GeoTransform
    Reliability_Soil_Moisture.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Reliability_Soil_Moisture.Size = Reliability_Soil_Moisture_Data.shape
    Reliability_Soil_Moisture.Variable = "Reliability Soil Moisture"
    Reliability_Soil_Moisture.Unit = "-"       

    del Reliability_Soil_Moisture_Data
    
    Reliability_Soil_Moisture.Save_As_Tiff(os.path.join(output_folder_L3, "Reliability_Soil_Moisture"))    
      
    return()