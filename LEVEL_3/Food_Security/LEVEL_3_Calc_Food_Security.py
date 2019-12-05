# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 13:25:22 2019
"""
import os
import gdal
import numpy as np
import pandas as pd
import warnings
import datetime

import WaporTranslator.LEVEL_1.Input_Data as Inputs
import WaporTranslator.LEVEL_1.DataCube as DataCube
import WaporTranslator.LEVEL_2.Functions as Functions

import watertools.General.raster_conversions as RC

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
    output_folder_L3 = os.path.join(output_folder, "LEVEL_3", "Food_Security")
    if not os.path.exists(output_folder_L3):
        os.makedirs(output_folder_L3)
    
    ################################# Dynamic maps #################################
    CropType = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.LU_END), Formats.LU_END, list(Dates_Years), Conversion = Conversions.LU_END, Variable = 'LU_END', Product = '', Unit = '-')
    CropSeason = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.CropSeason), Formats.CropSeason, list(Dates_Years), Conversion = Conversions.CropSeason, Variable = 'CropSeason', Product = '', Unit = '-')
    ET0 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET0), Formats.ET0, Dates, Conversion = Conversions.ET0, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET0', Product = 'WAPOR', Unit = 'mm/day')
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET), Formats.ET, Dates, Conversion = Conversions.ET, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = 'mm/day')
    P = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.P), Formats.P, Dates, Conversion = Conversions.P, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'P', Product = 'WAPOR', Unit = 'mm/day')
    NPP = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.NPP), Formats.NPP, Dates, Conversion = Conversions.NPP, Example_Data = example_file, Mask_Data = example_file, Variable = 'NPP', Product = 'WAPOR', Unit = 'kg/ha/day')
    Pcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_P), Formats.Cumulative_P, Dates, Conversion = Conversions.Cumulative_P, Variable = 'Pcum', Product = '', Unit = 'mm')
    ETcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_ET), Formats.Cumulative_ET, Dates, Conversion = Conversions.Cumulative_ET, Variable = 'ETcum', Product = '', Unit = 'mm')
    NPPcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_NPP), Formats.Cumulative_NPP, Dates, Conversion = Conversions.Cumulative_NPP, Variable = 'NPPcum', Product = '', Unit = 'kg/ha')
    Avail_Water_Depl = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Available_Before_Depletion), Formats.Available_Before_Depletion, Dates, Conversion = Conversions.Available_Before_Depletion, Variable = 'Available Water Depletion', Product = '', Unit = 'mm')
    Critical_Soil_Moisture = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Critical_Soil_Moisture), Formats.Critical_Soil_Moisture, Dates, Conversion = Conversions.Critical_Soil_Moisture, Variable = 'Critical Soil Moisture', Product = 'SoilGrids', Unit = 'cm3/cm3')
    Soil_Moisture = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Soil_Moisture), Formats.Soil_Moisture, Dates, Conversion = Conversions.Soil_Moisture, Variable = 'Soil Moisture', Product = '', Unit = 'cm3/cm3')
    Crop_S1_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S1), Formats.Season_End_S1, list(Dates_Years), Conversion = Conversions.Season_End_S1, Variable = 'Season 1 End', Product = '', Unit = 'DOY')
    Crop_S2_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S2), Formats.Season_End_S2, list(Dates_Years), Conversion = Conversions.Season_End_S2, Variable = 'Season 2 End', Product = '', Unit = 'DOY')
    Crop_S3_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S3), Formats.Season_End_S3, list(Dates_Years), Conversion = Conversions.Season_End_S3, Variable = 'Season 3 End', Product = '', Unit = 'DOY')
    Per_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Perennial_Start), Formats.Perennial_Start, list(Dates_Years), Conversion = Conversions.Perennial_Start, Variable = 'Perennial Start', Product = '', Unit = 'DOY')
    Per_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Perennial_End), Formats.Perennial_End, list(Dates_Years), Conversion = Conversions.Perennial_End, Variable = 'Perennial End', Product = '', Unit = 'DOY')
    
    ################################# Static maps #################################
    Clay =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Clay), Formats.Clay.format(level=6), Dates = None, Conversion = Conversions.Clay, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Clay', Product = 'SoilGrids', Unit = 'Percentage')
    Silt =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Silt), Formats.Silt.format(level=6), Dates = None, Conversion = Conversions.Silt, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Silt', Product = 'SoilGrids', Unit = 'Percentage')
    Sand =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Sand), Formats.Sand.format(level=6), Dates = None, Conversion = Conversions.Sand, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Sand', Product = 'SoilGrids', Unit = 'Percentage')
    DEM =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.DEM), Formats.DEM, Dates = None, Conversion = Conversions.DEM, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'DEM', Product = 'SRTM', Unit = 'm')
    Theta_WP_Subsoil = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Theta_WP_Subsoil), Formats.Theta_WP_Subsoil, Dates = None, Conversion = Conversions.Theta_WP_Subsoil, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Theta Wilting Point Subsoil', Product = 'SoilGrids', Unit = 'cm3/cm3')
    
    ################################# Calculate Irrigation yes/no #################################
    Irrigation = Calc_Irrigation(Pcum, ETcum, Avail_Water_Depl, MASK)
    Irrigation.Save_As_Tiff(os.path.join(output_folder_L3, "Irrigation"))

    ################################# Calculate Irrigation yes/no #################################
    Grassland_Data = np.where(CropType.Data==3, 1, np.nan)
    Grassland = DataCube.Rasterdata_Empty()
    Grassland.Data = Grassland_Data * MASK
    Grassland.Projection = Irrigation.Projection
    Grassland.GeoTransform = Irrigation.GeoTransform
    Grassland.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Grassland.Size = Grassland_Data.shape
    Grassland.Variable = "Grassland Yearly"
    Grassland.Unit = "-"       
    
    Grassland.Save_As_Tiff(os.path.join(output_folder_L3, "Grassland"))
    
    ######################## Calculate days in each dekads #################################
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)
    
    ################################# Calculate yearly irrigation maps #################################
    
    Irrigation_year_Data = np.ones([len(Dates_Years), Irrigation.Size[1], Irrigation.Size[2]]) * np.nan
    
    for Date_Year in Dates_Years:
        Start = (Date_Year.year - Dates_Years[0].year) * 36
        End = Start + 36
        Irrigation_year_Data[Dates_Years == Date_Year, :, :] = np.nansum(Irrigation.Data[Start:End, :, :], axis = 0)
    
    Irrigation_Yearly = DataCube.Rasterdata_Empty()
    Irrigation_Yearly.Data = Irrigation_year_Data * MASK
    Irrigation_Yearly.Projection = Irrigation.Projection
    Irrigation_Yearly.GeoTransform = Irrigation.GeoTransform
    Irrigation_Yearly.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Irrigation_Yearly.Size = Irrigation_year_Data.shape
    Irrigation_Yearly.Variable = "Irrigation Yearly"
    Irrigation_Yearly.Unit = "-"   
    
    Irrigation_Yearly.Save_As_Tiff(os.path.join(output_folder_L3, "Irrigation_Maps_Yearly"))
    
    ################################# Calculate Aridity Array #################################
    Aridity = Calc_Aridity(ET0, P, MASK)
    
    ################################# Calculate Slope Array #################################
    Slope = Calc_Slope(DEM, MASK)
    
    ################################# Calculate Crop Season and LU #################################
    Season_Type = Calc_Crops(CropType, CropSeason, MASK)
    
    ################################# Created AEZ numbers #################################
    AEZ = Calc_AEZ(Irrigation_Yearly, Aridity, Slope, DEM, Clay, Silt, Sand, Season_Type, MASK)
    AEZ.Save_As_Tiff(os.path.join(output_folder_L3, "AEZ"))
    
    ################################# Create dictionary for all AEZ #################################
    L3_AEZ_AREA = dict()
    L3_AEZ_Yield = dict()
    ################################# Calculate Areas every AEZ per year #################################
    AREA_M2 = Degrees_to_m2(example_file)
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        L3_AEZ_AREA[int(AEZ_ID)] = np.nansum(np.where(AEZ.Data == AEZ_ID, AREA_M2[None, :, :], np.nan), axis = (1,2))/1e4  # in hectare
    
    ################################# Calculate actual biomass production #################################
    C3_C4 = 0.45
    Actual_Biomass_Production_Data = NPP.Data/C3_C4
    
    Actual_Biomass_Production = DataCube.Rasterdata_Empty()
    Actual_Biomass_Production.Data = Actual_Biomass_Production_Data * MASK
    Actual_Biomass_Production.Projection = NPP.Projection
    Actual_Biomass_Production.GeoTransform = NPP.GeoTransform
    Actual_Biomass_Production.Ordinal_time = NPP.Ordinal_time
    Actual_Biomass_Production.Size = Actual_Biomass_Production_Data.shape
    Actual_Biomass_Production.Variable = "Actual Biomass Production"
    Actual_Biomass_Production.Unit = "kg-ha-1-d-1"       
    Actual_Biomass_Production.Save_As_Tiff(os.path.join(output_folder_L3, "Actual_Biomass_Production"))
    
    del Actual_Biomass_Production_Data
    
    ################################# Calculate Spatial Target Actual Biomass Production #################################
    AEZ_decads = np.repeat(AEZ.Data, 36, 0).reshape([36 * AEZ.Size[0], AEZ.Size[1], AEZ.Size[2]])
    L3_AEZ_NPP = dict()
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        L3_AEZ_NPP[int(AEZ_ID)] = np.nanpercentile(np.where(AEZ_decads == AEZ_ID, Actual_Biomass_Production.Data, np.nan), 99, axis=(1,2))
    
    ################################# Create spatial target maps #################################
    NPP_target_Data = np.ones(Actual_Biomass_Production.Size) * np.nan
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        NPP_target_Data = np.where(AEZ_decads == AEZ_ID, L3_AEZ_NPP[int(AEZ_ID)][:, None, None], NPP_target_Data)
    
    Target_Biomass_Production = DataCube.Rasterdata_Empty()
    Target_Biomass_Production.Data = NPP_target_Data * MASK
    Target_Biomass_Production.Projection = NPP.Projection
    Target_Biomass_Production.GeoTransform = NPP.GeoTransform
    Target_Biomass_Production.Ordinal_time = NPP.Ordinal_time
    Target_Biomass_Production.Size = NPP_target_Data.shape
    Target_Biomass_Production.Variable = "Target Biomass Production"
    Target_Biomass_Production.Unit = "kg-ha-1-d-1"      
    Target_Biomass_Production.Save_As_Tiff(os.path.join(output_folder_L3, "Temp", "Target_Biomass_Production"))
    
    del NPP_target_Data
    
    ################################# Dekadal production gap Spatial #################################
    
    Production_Gap_Spatial_Data = np.minimum(Actual_Biomass_Production.Data - Target_Biomass_Production.Data, 0)
    
    Production_Gap_Spatial = DataCube.Rasterdata_Empty()
    Production_Gap_Spatial.Data = Production_Gap_Spatial_Data * MASK
    Production_Gap_Spatial.Projection = NPP.Projection
    Production_Gap_Spatial.GeoTransform = NPP.GeoTransform
    Production_Gap_Spatial.Ordinal_time = NPP.Ordinal_time
    Production_Gap_Spatial.Size = Production_Gap_Spatial_Data.shape
    Production_Gap_Spatial.Variable = "Production Gap Spatial"
    Production_Gap_Spatial.Unit = "kg-ha-1-d-1"      
    Production_Gap_Spatial.Save_As_Tiff(os.path.join(output_folder_L3, "Production_Gap_Spatial"))
    
    del Production_Gap_Spatial_Data
    
    ################################# Calculate 10 year mean biomass production #################################
    
    Total_years = int(np.ceil(Actual_Biomass_Production.Size[0]/36))
    Mean_Biomass_Production_Data = np.ones([36, Actual_Biomass_Production.Size[1], Actual_Biomass_Production.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=Actual_Biomass_Production.Size[0]]
        Mean_Biomass_Production_Data[dekad, :, :] = np.nanmean(Actual_Biomass_Production.Data[IDs_good,:,:], axis = 0)
    
    Mean_Biomass_Production = DataCube.Rasterdata_Empty()
    Mean_Biomass_Production.Data = Mean_Biomass_Production_Data * MASK
    Mean_Biomass_Production.Projection = Actual_Biomass_Production.Projection
    Mean_Biomass_Production.GeoTransform = Actual_Biomass_Production.GeoTransform
    Mean_Biomass_Production.Ordinal_time = "Long_Term_Decade"
    Mean_Biomass_Production.Size = Mean_Biomass_Production_Data.shape
    Mean_Biomass_Production.Variable = "10Y Mean Biomass Production"
    Mean_Biomass_Production.Unit = "kg-ha-1-d-1"       
    Mean_Biomass_Production.Save_As_Tiff(os.path.join(output_folder_L3, "Mean_Biomass_Production"))
    
    del Mean_Biomass_Production_Data
    
    ################################# production gap Temporal #################################
        
    Production_Gap_Temporal_Data = np.minimum((Actual_Biomass_Production.Data - np.tile(Mean_Biomass_Production.Data, (Total_years, 1, 1))), 0)
    
    Production_Gap_Temporal = DataCube.Rasterdata_Empty()
    Production_Gap_Temporal.Data = Production_Gap_Temporal_Data * MASK
    Production_Gap_Temporal.Projection = NPP.Projection
    Production_Gap_Temporal.GeoTransform = NPP.GeoTransform
    Production_Gap_Temporal.Ordinal_time = NPP.Ordinal_time
    Production_Gap_Temporal.Size = Production_Gap_Temporal_Data.shape
    Production_Gap_Temporal.Variable = "Production Gap Temporal"
    Production_Gap_Temporal.Unit = "kg-ha-1-d-1"      
    Production_Gap_Temporal.Save_As_Tiff(os.path.join(output_folder_L3, "Production_Gap_Temporal"))
    
    del Production_Gap_Temporal_Data
    
    ##################################### Biomass anomalies ###################################
        
    Biomass_Anomalies_Data = Actual_Biomass_Production.Data - np.tile(Mean_Biomass_Production.Data, (Total_years, 1, 1))
    
    Biomass_Anomalies = DataCube.Rasterdata_Empty()
    Biomass_Anomalies.Data = Biomass_Anomalies_Data * MASK
    Biomass_Anomalies.Projection = NPP.Projection
    Biomass_Anomalies.GeoTransform = NPP.GeoTransform
    Biomass_Anomalies.Ordinal_time = NPP.Ordinal_time
    Biomass_Anomalies.Size = Biomass_Anomalies_Data.shape
    Biomass_Anomalies.Variable = "Biomass Anomalies"
    Biomass_Anomalies.Unit = "kg-ha-1-d-1"      
    Biomass_Anomalies.Save_As_Tiff(os.path.join(output_folder_L3, "Biomass_Anomalies"))
    
    del Biomass_Anomalies_Data
    
   ################################# Soil Moisture stress #################################
    Soil_Moisture_Stress_Data = np.maximum(0.0,(Critical_Soil_Moisture.Data-Soil_Moisture.Data)/(Critical_Soil_Moisture.Data-Theta_WP_Subsoil.Data[None, :, :]))

    Soil_Moisture_Stress = DataCube.Rasterdata_Empty()
    Soil_Moisture_Stress.Data = Soil_Moisture_Stress_Data * MASK
    Soil_Moisture_Stress.Projection = NPP.Projection
    Soil_Moisture_Stress.GeoTransform = NPP.GeoTransform
    Soil_Moisture_Stress.Ordinal_time = NPP.Ordinal_time
    Soil_Moisture_Stress.Size = Soil_Moisture_Stress_Data.shape
    Soil_Moisture_Stress.Variable = "Soil Moisture Stress"
    Soil_Moisture_Stress.Unit = "-"    
    
    del  Soil_Moisture_Stress_Data
    
    Soil_Moisture_Stress.Save_As_Tiff(os.path.join(output_folder_L3, "Soil_Moisture_Stress"))
    
    ################################# Production gap due to soil moisture #################################
    
    Production_Gap_Soil_Moisture_Data = np.where(Soil_Moisture_Stress.Data<=0., 0., -Actual_Biomass_Production.Data * Soil_Moisture_Stress.Data) # !!! heb hier keer van gemaakt
    Production_Gap_Soil_Moisture_Data = Production_Gap_Soil_Moisture_Data.clip(-10000, 0)
    
    Production_Gap_Soil_Moisture = DataCube.Rasterdata_Empty()
    Production_Gap_Soil_Moisture.Data = Production_Gap_Soil_Moisture_Data * MASK
    Production_Gap_Soil_Moisture.Projection = NPP.Projection
    Production_Gap_Soil_Moisture.GeoTransform = NPP.GeoTransform
    Production_Gap_Soil_Moisture.Ordinal_time = NPP.Ordinal_time
    Production_Gap_Soil_Moisture.Size = Production_Gap_Soil_Moisture_Data.shape
    Production_Gap_Soil_Moisture.Variable = "Production Gap Due to Soil Moisture"
    Production_Gap_Soil_Moisture.Unit = "kg-ha-1-d-1"      
    Production_Gap_Soil_Moisture.Save_As_Tiff(os.path.join(output_folder_L3, "Production_Gap_Soil_Moisture"))
    
    del Production_Gap_Soil_Moisture_Data
    
    ################################# Water Unlimited Biomass Production #################################
    
    Water_Unlimited_Biomass_Production_Data = (Actual_Biomass_Production.Data - Production_Gap_Soil_Moisture.Data)
    
    Water_Unlimited_Biomass_Production = DataCube.Rasterdata_Empty()
    Water_Unlimited_Biomass_Production.Data = Water_Unlimited_Biomass_Production_Data * MASK
    Water_Unlimited_Biomass_Production.Projection = NPP.Projection
    Water_Unlimited_Biomass_Production.GeoTransform = NPP.GeoTransform
    Water_Unlimited_Biomass_Production.Ordinal_time = NPP.Ordinal_time
    Water_Unlimited_Biomass_Production.Size = Water_Unlimited_Biomass_Production_Data.shape
    Water_Unlimited_Biomass_Production.Variable = "Water Unlimited Biomass Production"
    Water_Unlimited_Biomass_Production.Unit = "kg-ha-1-d-1"      
    Water_Unlimited_Biomass_Production.Save_As_Tiff(os.path.join(output_folder_L3, "Temp", "Water_Unlimited_Biomass_Production"))
    
    del Water_Unlimited_Biomass_Production_Data
    
    ################################# Accumulated NPP season #################################
    
    # For perennial crop clip the season at start and end year
    Accumulated_NPP_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_NPP_Data_End = np.ones(Per_Start.Size) * np.nan
    '''
    Start_Array = np.maximum(0, Per_Start.Data)
    End_Array = np.minimum(35, Per_End.Data)  

    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)
        for dekad in range(0,36):
            Accumulated_NPP_Data_Start[year_diff, Start_Array[year_diff, :, :] == dekad] = NPPcum.Data[int(year_diff * 36 + dekad), Start_Array[year_diff, :, :] == dekad] 
            Accumulated_NPP_Data_End[year_diff, End_Array[year_diff, :, :] == dekad] = NPPcum.Data[int(year_diff * 36 + dekad-1), End_Array[year_diff, :, :] == dekad] 
    '''
    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)
        Harvest = np.where(Per_End.Data[year_diff, :, :]<37, 1, 0)
        for dekad in range(int(np.nanmin(Per_Start.Data[year_diff, :, :])), 36):
            Accumulated_NPP_Data_Start[year_diff, np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] = NPPcum.Data[int(year_diff * 36 + dekad), np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] 
        for dekad in range(0,37):
            Accumulated_NPP_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = NPPcum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
    
    Accumulated_NPP_Data_Per = Accumulated_NPP_Data_End - Accumulated_NPP_Data_Start

    # For other crops (double and single) take the start and end of the seasons
    Accumulated_NPP_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_NPP_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_NPP_Data_Start_S3 = np.ones(Per_Start.Size) * np.nan
    
    if not np.isnan(np.nanmean(Crop_S1_End.Data)):
        for Date_Year in Dates_Years:
            year_diff = int(Date_Year.year - Dates_Years[0].year)
            for dekad in range(0,int(np.nanmax(Crop_S3_End.Data))):
                Accumulated_NPP_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = NPPcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_NPP_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = NPPcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_NPP_Data_Start_S3[year_diff, Crop_S3_End.Data[year_diff, :, :] == dekad] = NPPcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S3_End.Data[year_diff, :, :] == dekad] 
   
    Accumulated_NPP_Data_Start_S1[np.isnan(Accumulated_NPP_Data_Start_S1)] = 0
    Accumulated_NPP_Data_Start_S2[np.isnan(Accumulated_NPP_Data_Start_S2)] = 0 
    Accumulated_NPP_Data_Start_S3[np.isnan(Accumulated_NPP_Data_Start_S3)] = 0 
     
    # Calculate pasture
    Accumulated_NPP_Data_Past = np.ones(Per_Start.Size) * np.nan
    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)
        dekad = 35 # Always take end in pasture
        Accumulated_NPP_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 5] = NPPcum.Data[int(year_diff * 36 + dekad - 1), Season_Type.Data[year_diff, :, :] == 5] 
    
    Accumulated_NPP_Data_Past[np.isnan(Accumulated_NPP_Data_Past)] = 0
    Accumulated_NPP_Data_Per[np.isnan(Accumulated_NPP_Data_Per)] = 0
    
    # Add all seasons 
    Accumulated_NPP_Data = Accumulated_NPP_Data_Start_S1 + Accumulated_NPP_Data_Start_S2 + Accumulated_NPP_Data_Start_S3 + Accumulated_NPP_Data_Per + Accumulated_NPP_Data_Past
    Accumulated_NPP_Data[Accumulated_NPP_Data==0] = np.nan
        
    Accumulated_NPP = DataCube.Rasterdata_Empty()
    Accumulated_NPP.Data = Accumulated_NPP_Data * MASK
    Accumulated_NPP.Projection = Per_Start.Projection
    Accumulated_NPP.GeoTransform = Per_Start.GeoTransform
    Accumulated_NPP.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_NPP.Size = Accumulated_NPP_Data.shape
    Accumulated_NPP.Variable = "Accumulated NPP Season"
    Accumulated_NPP.Unit = "kg-ha-1-season-1"      
    Accumulated_NPP.Save_As_Tiff(os.path.join(output_folder_L3, "Temp", "Accumulated_NPP_Season", "All"))

    # Add Season 1
    Accumulated_NPP_Data_Start_S1[Accumulated_NPP_Data_Start_S1==0] = np.nan
        
    Accumulated_NPP_S1 = DataCube.Rasterdata_Empty()
    Accumulated_NPP_S1.Data = Accumulated_NPP_Data_Start_S1 * MASK
    Accumulated_NPP_S1.Projection = Per_Start.Projection
    Accumulated_NPP_S1.GeoTransform = Per_Start.GeoTransform
    Accumulated_NPP_S1.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_NPP_S1.Size = Accumulated_NPP_Data_Start_S1.shape
    Accumulated_NPP_S1.Variable = "Accumulated NPP Season 1"
    Accumulated_NPP_S1.Unit = "kg-ha-1-season-1"      
    Accumulated_NPP_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Temp", "Accumulated_NPP_Season", "S1"))

    # Add Season 2
    Accumulated_NPP_Data_Start_S2[Accumulated_NPP_Data_Start_S2==0] = np.nan
        
    Accumulated_NPP_S2 = DataCube.Rasterdata_Empty()
    Accumulated_NPP_S2.Data = Accumulated_NPP_Data_Start_S2 * MASK
    Accumulated_NPP_S2.Projection = Per_Start.Projection
    Accumulated_NPP_S2.GeoTransform = Per_Start.GeoTransform
    Accumulated_NPP_S2.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_NPP_S2.Size = Accumulated_NPP_Data_Start_S2.shape
    Accumulated_NPP_S2.Variable = "Accumulated NPP Season 2"
    Accumulated_NPP_S2.Unit = "kg-ha-1-season-1"      
    Accumulated_NPP_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Temp", "Accumulated_NPP_Season", "S2"))

    # Add Season 3
    Accumulated_NPP_Data_Start_S3[Accumulated_NPP_Data_Start_S3==0] = np.nan
        
    Accumulated_NPP_S3 = DataCube.Rasterdata_Empty()
    Accumulated_NPP_S3.Data = Accumulated_NPP_Data_Start_S3 * MASK
    Accumulated_NPP_S3.Projection = Per_Start.Projection
    Accumulated_NPP_S3.GeoTransform = Per_Start.GeoTransform
    Accumulated_NPP_S3.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_NPP_S3.Size = Accumulated_NPP_Data_Start_S3.shape
    Accumulated_NPP_S3.Variable = "Accumulated NPP Season 3"
    Accumulated_NPP_S3.Unit = "kg-ha-1-season-1"      
    Accumulated_NPP_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Temp", "Accumulated_NPP_Season", "S3"))

    # Add Per
    Accumulated_NPP_Data_Per[Accumulated_NPP_Data_Per==0] = np.nan
        
    Accumulated_NPP_Per = DataCube.Rasterdata_Empty()
    Accumulated_NPP_Per.Data = Accumulated_NPP_Data_Per * MASK
    Accumulated_NPP_Per.Projection = Per_Start.Projection
    Accumulated_NPP_Per.GeoTransform = Per_Start.GeoTransform
    Accumulated_NPP_Per.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_NPP_Per.Size = Accumulated_NPP_Data_Per.shape
    Accumulated_NPP_Per.Variable = "Accumulated NPP Season Perennial"
    Accumulated_NPP_Per.Unit = "kg-ha-1-season-1"      
    Accumulated_NPP_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Temp", "Accumulated_NPP_Season", "Perennial"))
    
    ################################# Accumulated Biomass Production season #################################
    
    Accumulated_Biomass_Production_Data = Accumulated_NPP.Data/C3_C4
    
    Accumulated_Biomass_Production = DataCube.Rasterdata_Empty()
    Accumulated_Biomass_Production.Data = Accumulated_Biomass_Production_Data * MASK
    Accumulated_Biomass_Production.Projection = Per_Start.Projection
    Accumulated_Biomass_Production.GeoTransform = Per_Start.GeoTransform
    Accumulated_Biomass_Production.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_Biomass_Production.Size = Accumulated_Biomass_Production_Data.shape
    Accumulated_Biomass_Production.Variable = "Accumulated Biomass Production"
    Accumulated_Biomass_Production.Unit = "kg-ha-1-season-1"      
    Accumulated_Biomass_Production.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_Biomass_Production_Season", "All"))

    # Season 1
    Accumulated_Biomass_Production_Data_S1 = Accumulated_NPP_S1.Data/C3_C4
    
    Accumulated_Biomass_Production_S1 = DataCube.Rasterdata_Empty()
    Accumulated_Biomass_Production_S1.Data = Accumulated_Biomass_Production_Data_S1 * MASK
    Accumulated_Biomass_Production_S1.Projection = Per_Start.Projection
    Accumulated_Biomass_Production_S1.GeoTransform = Per_Start.GeoTransform
    Accumulated_Biomass_Production_S1.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_Biomass_Production_S1.Size = Accumulated_Biomass_Production_Data_S1.shape
    Accumulated_Biomass_Production_S1.Variable = "Accumulated Biomass Production Season 1"
    Accumulated_Biomass_Production_S1.Unit = "kg-ha-1-season-1"      
    Accumulated_Biomass_Production_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_Biomass_Production_Season", "S1"))

    # Season 2
    Accumulated_Biomass_Production_Data_S2 = Accumulated_NPP_S2.Data/C3_C4
    
    Accumulated_Biomass_Production_S2 = DataCube.Rasterdata_Empty()
    Accumulated_Biomass_Production_S2.Data = Accumulated_Biomass_Production_Data_S2 * MASK
    Accumulated_Biomass_Production_S2.Projection = Per_Start.Projection
    Accumulated_Biomass_Production_S2.GeoTransform = Per_Start.GeoTransform
    Accumulated_Biomass_Production_S2.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_Biomass_Production_S2.Size = Accumulated_Biomass_Production_Data_S2.shape
    Accumulated_Biomass_Production_S2.Variable = "Accumulated Biomass Production Season 2"
    Accumulated_Biomass_Production_S2.Unit = "kg-ha-1-season-1"      
    Accumulated_Biomass_Production_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_Biomass_Production_Season", "S2"))

     # Season 3
    Accumulated_Biomass_Production_Data_S3 = Accumulated_NPP_S3.Data/C3_C4
    
    Accumulated_Biomass_Production_S3 = DataCube.Rasterdata_Empty()
    Accumulated_Biomass_Production_S3.Data = Accumulated_Biomass_Production_Data_S3 * MASK
    Accumulated_Biomass_Production_S3.Projection = Per_Start.Projection
    Accumulated_Biomass_Production_S3.GeoTransform = Per_Start.GeoTransform
    Accumulated_Biomass_Production_S3.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_Biomass_Production_S3.Size = Accumulated_Biomass_Production_Data_S3.shape
    Accumulated_Biomass_Production_S3.Variable = "Accumulated Biomass Production Season 3"
    Accumulated_Biomass_Production_S3.Unit = "kg-ha-1-season-1"      
    Accumulated_Biomass_Production_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_Biomass_Production_Season", "S3"))   

     # Season Perennial
    Accumulated_Biomass_Production_Data_Per = Accumulated_NPP_Per.Data/C3_C4
    
    Accumulated_Biomass_Production_Per = DataCube.Rasterdata_Empty()
    Accumulated_Biomass_Production_Per.Data = Accumulated_Biomass_Production_Data_Per * MASK
    Accumulated_Biomass_Production_Per.Projection = Per_Start.Projection
    Accumulated_Biomass_Production_Per.GeoTransform = Per_Start.GeoTransform
    Accumulated_Biomass_Production_Per.Ordinal_time = Per_Start.Ordinal_time
    Accumulated_Biomass_Production_Per.Size = Accumulated_Biomass_Production_Data_Per.shape
    Accumulated_Biomass_Production_Per.Variable = "Accumulated Biomass Production Season Perennial"
    Accumulated_Biomass_Production_Per.Unit = "kg-ha-1-season-1"      
    Accumulated_Biomass_Production_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_Biomass_Production_Season", "Perennial"))   
    
    ################################# Calculate Yield season #################################
    Harvest_Index = 0.35
    Moisture_Index = 0.15
        
    Yield_Data = Harvest_Index * ((Accumulated_NPP.Data)/C3_C4)/(1 - Moisture_Index)
    
    Yield = DataCube.Rasterdata_Empty()
    Yield.Data = Yield_Data * MASK
    Yield.Projection = Per_Start.Projection
    Yield.GeoTransform = Per_Start.GeoTransform
    Yield.Ordinal_time = Per_Start.Ordinal_time
    Yield.Size = Yield_Data.shape
    Yield.Variable = "Yield Season"
    Yield.Unit = "kg-ha-1-season-1"      
    Yield.Save_As_Tiff(os.path.join(output_folder_L3, "Yield", "All"))

    # Season 1
    Yield_Data_S1 = Harvest_Index * ((Accumulated_NPP_S1.Data)/C3_C4)/(1 - Moisture_Index)
    
    Yield_S1 = DataCube.Rasterdata_Empty()
    Yield_S1.Data = Yield_Data_S1 * MASK
    Yield_S1.Projection = Per_Start.Projection
    Yield_S1.GeoTransform = Per_Start.GeoTransform
    Yield_S1.Ordinal_time = Per_Start.Ordinal_time
    Yield_S1.Size = Yield_Data_S1.shape
    Yield_S1.Variable = "Yield Season 1"
    Yield_S1.Unit = "kg-ha-1-season-1"      
    Yield_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Yield", "S1"))

    # Season 2
    Yield_Data_S2 = Harvest_Index * ((Accumulated_NPP_S2.Data)/C3_C4)/(1 - Moisture_Index)
    
    Yield_S2 = DataCube.Rasterdata_Empty()
    Yield_S2.Data = Yield_Data_S2 * MASK
    Yield_S2.Projection = Per_Start.Projection
    Yield_S2.GeoTransform = Per_Start.GeoTransform
    Yield_S2.Ordinal_time = Per_Start.Ordinal_time
    Yield_S2.Size = Yield_Data_S2.shape
    Yield_S2.Variable = "Yield Season 2"
    Yield_S2.Unit = "kg-ha-1-season-1"      
    Yield_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Yield", "S2"))

    # Season 3
    Yield_Data_S3 = Harvest_Index * ((Accumulated_NPP_S3.Data)/C3_C4)/(1 - Moisture_Index)
    
    Yield_S3 = DataCube.Rasterdata_Empty()
    Yield_S3.Data = Yield_Data_S3 * MASK
    Yield_S3.Projection = Per_Start.Projection
    Yield_S3.GeoTransform = Per_Start.GeoTransform
    Yield_S3.Ordinal_time = Per_Start.Ordinal_time
    Yield_S3.Size = Yield_Data_S3.shape
    Yield_S3.Variable = "Yield Season 3"
    Yield_S3.Unit = "kg-ha-1-season-1"      
    Yield_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Yield", "S3"))

    # Season Perennial
    Yield_Data_Per = Harvest_Index * ((Accumulated_NPP_Per.Data)/C3_C4)/(1 - Moisture_Index)
    
    Yield_Per = DataCube.Rasterdata_Empty()
    Yield_Per.Data = Yield_Data_Per * MASK
    Yield_Per.Projection = Per_Start.Projection
    Yield_Per.GeoTransform = Per_Start.GeoTransform
    Yield_Per.Ordinal_time = Per_Start.Ordinal_time
    Yield_Per.Size = Yield_Data_Per.shape
    Yield_Per.Variable = "Yield Season Perennial"
    Yield_Per.Unit = "kg-ha-1-season-1"      
    Yield_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Yield", "Perennial"))
    
    ################################# Calculate Fresh Grass Yield season #################################
    
    Yield_Fresh_Grass_Data = 0.45 * ((Accumulated_NPP.Data)/C3_C4)/(1 - 0.6) * Grassland.Data
    
    Yield_Fresh_Grass = DataCube.Rasterdata_Empty()
    Yield_Fresh_Grass.Data = Yield_Fresh_Grass_Data * MASK
    Yield_Fresh_Grass.Projection = Per_Start.Projection
    Yield_Fresh_Grass.GeoTransform = Per_Start.GeoTransform
    Yield_Fresh_Grass.Ordinal_time = Per_Start.Ordinal_time
    Yield_Fresh_Grass.Size = Yield_Fresh_Grass_Data.shape
    Yield_Fresh_Grass.Variable = "Accumulated Yield Season"
    Yield_Fresh_Grass.Unit = "kg-ha-1-season-1"      
    Yield_Fresh_Grass.Save_As_Tiff(os.path.join(output_folder_L3, "Yield_Fresh_Grass"))
    
    ################################# Calculate Mean Biomass Production over every AEZ per year #################################
    
    L3_AEZ_Bio = dict()
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        L3_AEZ_Bio[int(AEZ_ID)] = np.nanmean(np.where(AEZ.Data == AEZ_ID, Accumulated_Biomass_Production.Data, np.nan), axis = (1,2))
        
    ################################# Calculate Mean Yield over every AEZ per year #################################
    L3_AEZ_Yield = dict()
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        L3_AEZ_Yield[int(AEZ_ID)] = np.nanmean(np.where(AEZ.Data == AEZ_ID, Yield.Data, np.nan), axis = (1,2))
    
    ################################# Calculate Mean Yield Fresh Grass over every AEZ per year #################################
    L3_AEZ_Yield_Fresh_Grass = dict()
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        L3_AEZ_Yield_Fresh_Grass[int(AEZ_ID)] = np.nanmean(np.where(AEZ.Data == AEZ_ID, Yield_Fresh_Grass.Data, np.nan), axis = (1,2))
    
    ################################# Create CSVs #################################
        
    # Create Aridity AEZ
    dict_names = AEZ_Names()  
    
    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)   
        year = Date_Year.year
        
        filename_logfile =os.path.join(output_folder_L3, "CSV_%s.csv" %year)
        
        textfile = open(filename_logfile,'w')  
        text_first_line = "AEZ, Croptype, Rainfed/Irrigated, Soiltype, Elevation, Slope, Climate, Area (ha), Biomass Production (kg/ha/Season), Yield (ton/ha), Food Production (tonnes)\n"
        textfile.write(text_first_line)
    
            
        for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
            
            AEZ_str = str(int(AEZ_ID))
            CROPTYPE = dict_names["Crop"][int(AEZ_str[0:1])]
            RAINIRRI = dict_names["Irrigated"][int(AEZ_str[1:2])]
            SOILTYPE = dict_names["Soil"][int(AEZ_str[2:4])]
            ELEVATION = dict_names["Elevation"][int(AEZ_str[4:5])]
            SLOPE = dict_names["Slope"][int(AEZ_str[5:6])]
            CLIMATE = dict_names["Aridity"][int(AEZ_str[6:7])]
            AREA = L3_AEZ_AREA[AEZ_ID][year_diff]
            BIO = L3_AEZ_Bio[AEZ_ID][year_diff]
            if int(AEZ_str[0:1]) < 4:
                YIELD = L3_AEZ_Yield[AEZ_ID][year_diff]
            else:
                YIELD = L3_AEZ_Yield_Fresh_Grass[AEZ_ID][year_diff]    
                
            FOOD = YIELD * AREA
                
            text_one_line = "%s, %s, %s, %s, %s, %s, %s, %.2f, %.2f, %.2f, %.2f\n" %(int(AEZ_ID), CROPTYPE, RAINIRRI, SOILTYPE, ELEVATION, SLOPE, CLIMATE, AREA, BIO, YIELD, FOOD)
            textfile.write(text_one_line)
    
    textfile.close() 

    return()


def Calc_Irrigation(Pcum, ETcum, Avail_Water_Depl, MASK):

    Irrigation_Data = np.where(np.abs(Pcum.Data - ETcum.Data) > Avail_Water_Depl.Data, 1, 0)
    
    Irrigation = DataCube.Rasterdata_Empty()
    Irrigation.Data = Irrigation_Data * MASK
    Irrigation.Projection = Pcum.Projection
    Irrigation.GeoTransform = Pcum.GeoTransform
    Irrigation.Ordinal_time = Pcum.Ordinal_time
    Irrigation.Size = Irrigation_Data.shape
    Irrigation.Variable = "Irrigation"
    Irrigation.Unit = "-"
    
    return(Irrigation)
    
def Calc_Dekads_range(Startdate, Enddate):

    # Get dekads time steps
    Enddate_datetime = datetime.datetime.strptime(Enddate, "%Y-%m-%d")
    Years = pd.date_range(Startdate, Enddate, freq = "AS")
    
    Dates_dek = []
    for Year in Years:
        
        Year_nmbr = Year.year
        
        # Find dates dekades for one year
        Startdate_Year = "%d-01-01" %Year_nmbr
        Enddate_Year = "%d-12-31" %Year_nmbr
        day_dekad_end = 2
        
        if Year == Years[-1]:
            Enddate_Year = Enddate_datetime
            day_dekad_end = int("%d" %int(np.minimum(int(("%02d" %int(str(Enddate_datetime.day)))[0]), 2)))
    
        # Define dates
        Dates = pd.date_range(Startdate_Year, Enddate_Year, freq = "MS")
    
        # Define decade dates
        for Date in Dates:
            if Date != Dates[-1]:
                Dates_dek.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 1)))
                Dates_dek.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 11)))
                Dates_dek.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 21)))
            else:
                Dates_dek.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 1)))
                if day_dekad_end > 0:
                    Dates_dek.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 11)))
                if day_dekad_end > 1:
                    Dates_dek.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 21)))   
                    
    return(Dates_dek)                    

def Calc_Aridity(ET0, P, MASK):

    # Calculate Aridity long term
    ET0_long_term = np.nansum(ET0.Data, axis = 0)
    P_long_term = np.nansum(P.Data, axis = 0)
     
    # Calculate aridity and reproject to LU map
    Aridity_index_data = ET0_long_term / P_long_term
 
    Aridity_index = DataCube.Rasterdata_Empty()
    Aridity_index.Data = Aridity_index_data * MASK
    Aridity_index.Projection = ET0.Projection
    Aridity_index.GeoTransform = ET0.GeoTransform
    Aridity_index.Ordinal_time = ''
    Aridity_index.Size = Aridity_index_data.shape
    Aridity_index.Variable = "Aridity Index"
    Aridity_index.Unit = "-"    
    
    return(Aridity_index)

def Calc_Slope(DEM, MASK):
    
    rad2deg = 180.0 / np.pi  # Factor to transform from rad to degree
    pixel_spacing = 100     # LVL 2 of WAPOR is 100m resolution
    
    DEM_data = DEM.Data
    
    # Calculate slope
    x, y = np.gradient(DEM_data, pixel_spacing, pixel_spacing)
    hypotenuse_array = np.hypot(x,y)
    Slope_data = np.arctan(hypotenuse_array) * rad2deg

    Slope = DataCube.Rasterdata_Empty()
    Slope.Data = Slope_data * MASK
    Slope.Projection = DEM.Projection
    Slope.GeoTransform = DEM.GeoTransform
    Slope.Ordinal_time = ''
    Slope.Size = Slope_data.shape
    Slope.Variable = "Slope"
    Slope.Unit = "Degrees"   

    return(Slope)
 
def Calc_Crops(CropType, CropClass, MASK):

    Type_Data = CropType.Data
    Class_Data = CropClass.Data
    
    # Create Season Type map
    Season_Type_Data = np.where(Type_Data == 3, 5, Class_Data)

    Season_Type = DataCube.Rasterdata_Empty()
    Season_Type.Data = Season_Type_Data * MASK
    Season_Type.Projection = CropType.Projection
    Season_Type.GeoTransform = CropType.GeoTransform
    Season_Type.Ordinal_time = CropType.Ordinal_time
    Season_Type.Size = Season_Type_Data.shape
    Season_Type.Variable = "Season_Type"
    Season_Type.Unit = "-"

    return(Season_Type)
    
def Calc_AEZ(Irrigation_Yearly, Aridity, Slope, DEM, Clay, Silt, Sand, Season_Type, MASK):
    
    # Create Aridity AEZ
    dict_ipi = AEZ_Conversions()
    
    AEZ1 = np.ones(Season_Type.Size) * np.nan
    AEZ2 = np.ones(Irrigation_Yearly.Size) * np.nan 
    AEZ3 = np.ones(Clay.Size) * np.nan    
    AEZ4 = np.ones(DEM.Size) * np.nan        
    AEZ5 = np.ones(Slope.Size) * np.nan
    AEZ6 = np.ones(Aridity.Size) * np.nan
    
    for ID, value in dict_ipi['Crop'].items():
        AEZ1[Season_Type.Data==ID] = value      
        
    for ID, value in dict_ipi['Irrigated'].items():
        AEZ2[Irrigation_Yearly.Data==ID] = value
          
    for ID, value in dict_ipi['Soil'].items():
        AEZ3[np.logical_and.reduce((Clay.Data > value[0][0], Clay.Data <= value[0][1],Silt.Data > value[1][0], Silt.Data <= value[1][1], Sand.Data > value[2][0], Sand.Data <= value[2][1]))] = ID       
    
    for ID, value in dict_ipi['Elevation'].items():
        AEZ4[np.logical_and(DEM.Data > value[0], DEM.Data <= value[1])] = ID       
    
    for ID, value in dict_ipi['Slope'].items():
        AEZ5[np.logical_and(Slope.Data > value[0], Slope.Data <= value[1])] = ID       
    
    for ID, value in dict_ipi['Aridity'].items():
        AEZ6[np.logical_and(Aridity.Data > value[0], Aridity.Data <= value[1])] = ID           
    
    AEZ_Data = AEZ1 * 1000000 + AEZ2 * 100000 + AEZ3[None, :, :] * 1000 + AEZ4[None, :, :] * 100 + AEZ5[None, :, :] * 10 + AEZ6

    AEZ = DataCube.Rasterdata_Empty()
    AEZ.Data = AEZ_Data * MASK
    AEZ.Projection = Irrigation_Yearly.Projection
    AEZ.GeoTransform = Irrigation_Yearly.GeoTransform
    AEZ.Ordinal_time = Irrigation_Yearly.Ordinal_time
    AEZ.Size = AEZ_Data.shape
    AEZ.Variable = "Agro_Ecological_Zonation"
    AEZ.Unit = "AEZ"  
    
    return(AEZ)
    
def Degrees_to_m2(Reference_data):
    """
    This functions calculated the area of each pixel in squared meter.

    Parameters
    ----------
    Reference_data: str
        Path to a tiff file or nc file or memory file of which the pixel area must be defined

    Returns
    -------
    area_in_m2: array
        Array containing the area of each pixel in squared meters

    """
    try:
        # Get the extension of the example data
        filename, file_extension = os.path.splitext(Reference_data)

        # Get raster information
        if str(file_extension) == '.tif':
            geo_out, proj, size_X, size_Y = RC.Open_array_info(Reference_data)
        elif str(file_extension) == '.nc':
            geo_out, epsg, size_X, size_Y, size_Z, Time = RC.Open_nc_info(Reference_data)

    except:
        geo_out = Reference_data.GetGeoTransform()
        size_X = Reference_data.RasterXSize()
        size_Y = Reference_data.RasterYSize()

    # Calculate the difference in latitude and longitude in meters
    dlat, dlon = Calc_dlat_dlon(geo_out, size_X, size_Y)

    # Calculate the area in squared meters
    area_in_m2 =  dlat * dlon

    return(area_in_m2)

def Calc_dlat_dlon(geo_out, size_X, size_Y):
    """
    This functions calculated the distance between each pixel in meter.

    Parameters
    ----------
    geo_out: array
        geo transform function of the array
    size_X: int
        size of the X axis
    size_Y: int
        size of the Y axis

    Returns
    -------
    dlat: array
        Array containing the vertical distance between each pixel in meters
    dlon: array
        Array containing the horizontal distance between each pixel in meters
    """

    # Create the lat/lon rasters
    lon = np.arange(size_X + 1)*geo_out[1]+geo_out[0] - 0.5 * geo_out[1]
    lat = np.arange(size_Y + 1)*geo_out[5]+geo_out[3] - 0.5 * geo_out[5]

    dlat_2d = np.array([lat,]*int(np.size(lon,0))).transpose()
    dlon_2d =  np.array([lon,]*int(np.size(lat,0)))

    # Radius of the earth in meters
    R_earth = 6371000

    # Calculate the lat and lon in radians
    lonRad = dlon_2d * np.pi/180
    latRad = dlat_2d * np.pi/180

    # Calculate the difference in lat and lon
    lonRad_dif = abs(lonRad[:,1:] - lonRad[:,:-1])
    latRad_dif = abs(latRad[:-1] - latRad[1:])

    # Calculate the distance between the upper and lower pixel edge
    a = np.sin(latRad_dif[:,:-1]/2) * np.sin(latRad_dif[:,:-1]/2)
    clat = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a));
    dlat = R_earth * clat

    # Calculate the distance between the eastern and western pixel edge
    b = np.cos(latRad[1:,:-1]) * np.cos(latRad[:-1,:-1]) * np.sin(lonRad_dif[:-1,:]/2) * np.sin(lonRad_dif[:-1,:]/2)
    clon = 2 * np.arctan2(np.sqrt(b), np.sqrt(1-b));
    dlon = R_earth * clon

    return(dlat, dlon)

    
def AEZ_Conversions(version = '2.0'):
    
    AEZ_V1 = {
    'Aridity':    {1: [3, 9999],
               2: [2, 3],
               3: [1.5, 2],
               4: [1, 1.5],
               5: [0.7, 1],
               6: [0.35, 0.7],
               7: [-9999, 0.35]},
    
    'Slope':    {1: [8, 9999],
               2: [4, 8],
               3: [1, 4],
               4: [-9999, 1]},
               
    'Elevation':    {1: [2000, 9999],
               2: [1000, 2000],
               3: [500, 1000],
               4: [100, 500],
               5: [-9999, 100]},
                     
    'Soil':    {1: [[40, 9999],[-9999, 40],[-9999, 45]],
               2: [[25, 40],[20, 9999],[20, 9999]],
               3: [[25, 40],[40, 9999],[-9999, 20]],
               4: [[40, 9999],[40, 9999],[-9999, 20]],
               5: [[35, 9999],[-9999, 20],[45, 9999]],
               6: [[25, 35],[-9999, 30],[45, 9999]],
               7: [[-9999, 20],[-9999, 20],[50, 9999]],
               8: [[10, 25],[-9999, 50],[-9999, 50]],
               9: [[-9999, 30],[50, 80],[-9999, 50]],
               10: [[-9999, 15],[80, 9999],[-9999, 20]],
               11: [[-9999, 20],[-9999, 20],[70, 9999]],
               12: [[-9999, 10],[-9999, 10],[90, 9999]]},

    'Irrigated':    {0: 1,
                    1: 2},         
                            
    'Crop':    {1: 1,
               2: 2,
               3: 3,
               4: 4}
    }    
    
    AEZ_V2 = {
    'Aridity':    {1: [2, 9999],
                   2: [0.5, 2],
                   3: [-9999, 0.5]},
    
    'Slope':    {1: [2, 9999],
                 2: [-9999, 2]},
               
    'Elevation':    {1: [1000, 9999],
                     2: [500, 1000],
                     3: [-9999, 500]},
                     
    'Soil':    {1: [[35, 9999],[-9999, 9999],[-9999, 9999]],
                2: [[-9999, 35],[-9999, 9999],[-9999, 55]],
                3: [[-9999, 35],[-9999, 9999],[55, 9999]]},

    'Irrigated':    {0: 1,
                    1: 2},         
                            
    'Crop':    {1: 1,
               2: 2,
               3: 3,
               4: 4}
    }                         
                     
                     
    AEZ_Conversions = dict()
    AEZ_Conversions['1.0'] = AEZ_V1
    AEZ_Conversions['2.0'] = AEZ_V2
    
    return AEZ_Conversions[version]
    
    
def AEZ_Names(version = '2.0'):
    
    AEZ_V1 = {
    'Aridity':    {1: "Hyper-Arid",
               2: "Arid",
               3: "Semi-Arid",
               4: "Dry Sub-Humid",
               5: "Dry Sub-Humid",
               6: "Humid",
               7: "Hyper-Humid"},
    
    'Slope':    {1: "Flat",
               2: "Intermediate",
               3: "Steep",
               4: "Very Steep"},
               
    'Elevation':    {1: "Sea Level",
               2: "Lowland",
               3: "Intermediate",
               4: "Highland",
               5: "Alpine"},
                     
    'Soil':    {1: "Clay",
               2: "Clay Loam",
               3: "Silty Clay Loam",
               4: "Silty Clay",
               5: "Sandy Clay",
               6: "Sandy Clay Loam",
               7: "Sandy Loam",
               8: "Medium Loam",
               9: "Silty Loam",
               10: "Silt",
               11: "Loamy Sand",
               12: "Sand"},

    'Irrigated':    {1: "Irrigated",
                    2: "Rainfed"},          
                            
    'Crop':    {1: "Single",
               2: "Double",
               3: "Perennial",
               4: "Pasture"}
    }    
    
    AEZ_V2 = {
    'Aridity':    {1: "Arid",
                   2: "Average",
                   3: "Humid"},
    
    'Slope':    {1: "Flat",
                 2: "Steep"},
               
    'Elevation':    {1: "Lowland",
                     2: "Intermediate",
                     3: "Highland"},
                     
    'Soil':          {1: "Clay",
                     2: "Loam",
                     3: "Sand"},

    'Irrigated':    {1: "Irrigated",
                    2: "Rainfed"},         
                            
    'Crop':    {1: "Single",
               2: "Double",
               3: "Perennial",
               4: "Pasture"}
    }                         
                     
                     
    AEZ_Names = dict()
    AEZ_Names['1.0'] = AEZ_V1
    AEZ_Names['2.0'] = AEZ_V2
    
    return AEZ_Names[version]
        
    



