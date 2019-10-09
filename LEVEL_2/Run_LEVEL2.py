# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 17:03:41 2019
"""
import os
import numpy as np
import pandas as pd
import warnings

import WaporTranslator.LEVEL_1.Input_Data as Inputs
import WaporTranslator.LEVEL_2 as L2
import WaporTranslator.LEVEL_2.DataCube as DataCube
import WaporTranslator.LEVEL_2.Functions as Functions

# User inputs
Start_year_analyses = "2009"
End_year_analyses = "2018"
output_folder = r"G:\Project_MetaMeta"


def main(Start_year_analyses, End_year_analyses, output_folder):

    # Do not show non relevant warnings
    warnings.filterwarnings("ignore")
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    # Create output folder for LEVEL 2 data
    output_folder_L2 = os.path.join(output_folder, "LEVEL_2")
    if not os.path.exists(output_folder_L2):
        os.makedirs(output_folder_L2)
    
    # Define dates
    Dates = Functions.Get_Dekads(Start_year_analyses, End_year_analyses)
    Dates_Net_Radiation = Functions.Get_Dekads(str(np.maximum(int(Start_year_analyses), 2016)), End_year_analyses)
    Dates_Daily = list(pd.date_range("%s-01-01" %str(Start_year_analyses), "%s-12-31" %End_year_analyses))
    Dates_Net_Radiation_Daily = list(pd.date_range("%s-01-01" %str(np.maximum(int(Start_year_analyses), 2016)), "%s-12-31" %End_year_analyses))
    
    # Get path and formats
    Paths = Inputs.Input_Paths()
    Formats = Inputs.Input_Formats()
    Conversions = Inputs.Input_Conversions()
    
    # Set example file
    example_file = os.path.join(os.path.join(output_folder, Paths.LU), Formats.LU.format(yyyy = Dates[0].year))
    
    # Load inputs for LEVEL 2
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET), Formats.ET, Dates, Conversion = Conversions.ET, Example_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = '10 x mm/day')
    T = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.T), Formats.T, Dates, Conversion = Conversions.T, Example_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'T', Product = 'WAPOR', Unit = '10 x mm/day')
    I = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.I), Formats.I, Dates, Conversion = Conversions.I, Example_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'I', Product = 'WAPOR', Unit = '10 x mm/day')
    P = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.P), Formats.P, Dates, Conversion = Conversions.P, Example_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'P', Product = 'WAPOR', Unit = '10 x mm/day')
    ET0 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET0), Formats.ET0, Dates, Conversion = Conversions.ET0, Example_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET0', Product = 'WAPOR', Unit = '10 x mm/day')
    LU = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.LU), Formats.LU, Dates, Conversion = Conversions.LU, Variable = 'LU', Product = 'WAPOR', Unit = 'LU')
    NPP = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.NPP), Formats.NPP, Dates, Conversion = Conversions.NPP, Variable = 'NPP', Product = 'WAPOR', Unit = 'kg/ha/day')
    Albedo = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Albedo), Formats.Albedo, Dates_Net_Radiation, Conversion = Conversions.Albedo, Example_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Albedo', Product = 'MODIS', Unit = '-')
    
    # Open daily
    DSLF_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.DSLF), Formats.DSLF, Dates_Net_Radiation_Daily, Conversion = Conversions.DSLF, Example_Data = example_file, reprojection_type = 2, Variable = 'DSLF', Product = 'LANDSAF', Unit = '1e6 x W/m2')
    DSSF_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.DSSF), Formats.DSSF, Dates_Net_Radiation_Daily, Conversion = Conversions.DSLF, Example_Data = example_file, reprojection_type = 2, Variable = 'DSSF', Product = 'LANDSAF', Unit = '1e6 x W/m2')
    Temp_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Temp), Formats.Temp, Dates_Daily, Conversion = Conversions.Temp, Example_Data = example_file, reprojection_type = 2, Variable = 'Temperature', Product = 'GLDAS', Unit = 'Celcius')
    
    # Open Constant
    Bulk =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Bulk), Formats.Bulk.format(level=6), Dates = None, Conversion = Conversions.Bulk, Example_Data = example_file, reprojection_type = 2, Variable = 'Bulk', Product = 'SoilGrids', Unit = 'kg/m3')
    Sand =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Sand), Formats.Sand.format(level=6), Dates = None, Conversion = Conversions.Sand, Example_Data = example_file, reprojection_type = 2, Variable = 'Sand', Product = 'SoilGrids', Unit = 'Percentage')
    Silt =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Silt), Formats.Silt.format(level=6), Dates = None, Conversion = Conversions.Silt, Example_Data = example_file, reprojection_type = 2, Variable = 'Silt', Product = 'SoilGrids', Unit = 'Percentage')
    Clay =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Clay), Formats.Clay.format(level=6), Dates = None, Conversion = Conversions.Silt, Example_Data = example_file, reprojection_type = 2, Variable = 'Clay', Product = 'SoilGrids', Unit = 'Percentage')
    
    ################################### Calculate LAI ############################################
    LAI_Data = np.log((1-np.minimum(T.Data/ET0.Data, 0.99)))/(-0.69)
    LAI_Data[LU.Data==80] = 0.0
    LAI_Data = LAI_Data.clip(0.0, 7.0)
    
    # Write in DataCube
    LAI = DataCube.Rasterdata_Empty()
    LAI.Data = LAI_Data
    LAI.Projection = ET.Projection
    LAI.GeoTransform = ET.GeoTransform
    LAI.Ordinal_time = ET.Ordinal_time
    LAI.Size = LAI_Data.shape
    LAI.Variable = "Leaf Area Index"
    LAI.Unit = "m2/m2"
    
    del LAI_Data
    
    LAI.Save_As_Tiff(os.path.join(output_folder_L2, "LAI"))
    
    ############################ Calculate Root Depth ##########################################
    Root_Depth_Data = 0.7 * 100 * np.maximum(0, -0.0326 * LAI.Data**2 + 0.4755 * LAI.Data - 0.0411)
    Root_Depth_Data = Root_Depth_Data.clip(0, 500)
    
    # Write in DataCube
    Root_Depth = DataCube.Rasterdata_Empty()
    Root_Depth.Data = Root_Depth_Data
    Root_Depth.Projection = ET.Projection
    Root_Depth.GeoTransform = ET.GeoTransform
    Root_Depth.Ordinal_time = ET.Ordinal_time
    Root_Depth.Size = Root_Depth_Data.shape
    Root_Depth.Variable = "Root Depth"
    Root_Depth.Unit = "cm"
    
    del Root_Depth_Data
    
    Root_Depth.Save_As_Tiff(os.path.join(output_folder_L2, "Root_Depth"))
    
    ################# Calculate Fractional Vegetation Cover #######################################
    Fract_vegt_Data = 1-np.exp(-0.65 * LAI.Data)
    Fract_vegt_Data = Fract_vegt_Data.clip(0, 1.0)
    
    # Write in DataCube
    Fract_vegt = DataCube.Rasterdata_Empty()
    Fract_vegt.Data = Fract_vegt_Data
    Fract_vegt.Projection = ET.Projection
    Fract_vegt.GeoTransform = ET.GeoTransform
    Fract_vegt.Ordinal_time = ET.Ordinal_time
    Fract_vegt.Size = Fract_vegt_Data.shape
    Fract_vegt.Variable = "Fractional Vegetation"
    Fract_vegt.Unit = "-"
    
    del Fract_vegt_Data
    
    Fract_vegt.Save_As_Tiff(os.path.join(output_folder_L2, "Fractional_Vegetation_Cover"))
    
    ##################### Calculate Dry Soil Crop Coefficient ####################################
    Crop_Coef_Dry_Soil_Data = np.minimum(1.4 ,0.95 * Fract_vegt.Data + 0.2)
    Crop_Coef_Dry_Soil_Data = Crop_Coef_Dry_Soil_Data.clip(0, 500)
    
    # Write in DataCube
    Crop_Coef_Dry_Soil = DataCube.Rasterdata_Empty()
    Crop_Coef_Dry_Soil.Data = Crop_Coef_Dry_Soil_Data
    Crop_Coef_Dry_Soil.Projection = ET.Projection
    Crop_Coef_Dry_Soil.GeoTransform = ET.GeoTransform
    Crop_Coef_Dry_Soil.Ordinal_time = ET.Ordinal_time
    Crop_Coef_Dry_Soil.Size = Crop_Coef_Dry_Soil_Data.shape
    Crop_Coef_Dry_Soil.Variable = "Crop Coefficient Dry Soil"
    Crop_Coef_Dry_Soil.Unit = "-"
    
    del Crop_Coef_Dry_Soil_Data
    
    Crop_Coef_Dry_Soil.Save_As_Tiff(os.path.join(output_folder_L2, "Crop_Coef_Dry_Soil"))
    
    ################# Calculate Land Surface Emissivity ###########################################
    Land_Surface_Emissivity_Data = np.minimum(1, 0.9 + 0.017 * LAI.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :])
    Land_Surface_Emissivity_Data = Land_Surface_Emissivity_Data.clip(0, 1.0)
    
    # Write in DataCube
    Land_Surface_Emissivity = DataCube.Rasterdata_Empty()
    Land_Surface_Emissivity.Data = Land_Surface_Emissivity_Data
    Land_Surface_Emissivity.Projection = Albedo.Projection
    Land_Surface_Emissivity.GeoTransform = Albedo.GeoTransform
    Land_Surface_Emissivity.Ordinal_time = Albedo.Ordinal_time
    Land_Surface_Emissivity.Size = Land_Surface_Emissivity_Data.shape
    Land_Surface_Emissivity.Variable = "Land Surface Emissivity"
    Land_Surface_Emissivity.Unit = "-"
    
    del Land_Surface_Emissivity_Data
    
    Land_Surface_Emissivity.Save_As_Tiff(os.path.join(output_folder_L2, "Land_Surface_Emissivity"))
    
    #################### Convert into daily datasets ############################################
    Albedo_Daily = Functions.Calc_Daily_from_Dekads(Albedo)
    Land_Surface_Emissivity_Daily = Functions.Calc_Daily_from_Dekads(Land_Surface_Emissivity)
    
    ###################### Calculate Net Radiation (daily) #####################################
    Net_Radiation_Data_Daily = (1 - Albedo_Daily.Data) * DSSF_daily.Data + DSLF_daily.Data - Land_Surface_Emissivity_Daily.Data * 0.0000000567 * (273.15 + Temp_daily.Data[np.isin(Temp_daily.Ordinal_time, DSLF_daily.Ordinal_time)] - 4)**4
    Net_Radiation_Data_Daily  = Net_Radiation_Data_Daily.clip(0, 500)
    Net_Radiation_Data_Daily[Net_Radiation_Data_Daily == 0] = np.nan
    
    # Write in DataCube
    Net_Radiation_Daily = DataCube.Rasterdata_Empty()
    Net_Radiation_Daily.Data = Net_Radiation_Data_Daily
    Net_Radiation_Daily.Projection = Albedo.Projection
    Net_Radiation_Daily.GeoTransform = Albedo.GeoTransform
    Net_Radiation_Daily.Ordinal_time = Albedo_Daily.Ordinal_time
    Net_Radiation_Daily.Size = Net_Radiation_Data_Daily.shape
    Net_Radiation_Daily.Variable = "Net Radiation"
    Net_Radiation_Daily.Unit = "W/m2"
    
    del Net_Radiation_Data_Daily
    
    ############### convert Net Radiation to dekadal ############################################
    Net_Radiation = Functions.Calc_Dekads_from_Daily(Net_Radiation_Daily, flux_state = "state")
    Temp = Functions.Calc_Dekads_from_Daily(Temp_daily, flux_state = "state")
    
    del Net_Radiation_Daily, Albedo_Daily, Land_Surface_Emissivity_Daily, DSSF_daily, DSLF_daily, Temp_daily
    
    Net_Radiation.Save_As_Tiff(os.path.join(output_folder_L2, "Net_Radiation"))
    
    ################# Calculate Evaporative Fraction ############################################
    Evaporative_Fraction_Data = ET.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :]*28.4/Net_Radiation.Data
    Evaporative_Fraction_Data = Evaporative_Fraction_Data.clip(0, 1.5)
    
    # Write in DataCube
    Evaporative_Fraction = DataCube.Rasterdata_Empty()
    Evaporative_Fraction.Data = Evaporative_Fraction_Data
    Evaporative_Fraction.Projection = Albedo.Projection
    Evaporative_Fraction.GeoTransform = Albedo.GeoTransform
    Evaporative_Fraction.Ordinal_time = Albedo.Ordinal_time
    Evaporative_Fraction.Size = Evaporative_Fraction_Data.shape
    Evaporative_Fraction.Variable = "Evaporative Fraction"
    Evaporative_Fraction.Unit = "-"
    
    del Evaporative_Fraction_Data
    
    Evaporative_Fraction.Save_As_Tiff(os.path.join(output_folder_L2, "Evaporative_Fraction"))
    
    ############## Calculate Land Theta Saturated Subsoil ##################################
    Theta_Sat_Subsoil_Data = 0.85 * (1 - Bulk.Data/2650) + 0.13 * Clay.Data * 0.01
    
    # Write in DataCube
    Theta_Sat_Subsoil = DataCube.Rasterdata_Empty()
    Theta_Sat_Subsoil.Data = Theta_Sat_Subsoil_Data
    Theta_Sat_Subsoil.Projection = Albedo.Projection
    Theta_Sat_Subsoil.GeoTransform = Albedo.GeoTransform
    Theta_Sat_Subsoil.Ordinal_time = None
    Theta_Sat_Subsoil.Size = Theta_Sat_Subsoil_Data.shape
    Theta_Sat_Subsoil.Variable = "Saturated Theta Subsoil"
    Theta_Sat_Subsoil.Unit = "cm3/cm3"
    
    del Theta_Sat_Subsoil_Data
    
    Theta_Sat_Subsoil.Save_As_Tiff(os.path.join(output_folder_L2, "Theta_Sat_Subsoil"))
    
    ################### Calculate Theta Field Capacity Subsoil #############################
    Theta_FC_Subsoil_Data = -2.2 * Theta_Sat_Subsoil.Data**2 + 2.92 * Theta_Sat_Subsoil.Data - 0.59
    
    # Write in DataCube
    Theta_FC_Subsoil = DataCube.Rasterdata_Empty()
    Theta_FC_Subsoil.Data = Theta_FC_Subsoil_Data
    Theta_FC_Subsoil.Projection = Albedo.Projection
    Theta_FC_Subsoil.GeoTransform = Albedo.GeoTransform
    Theta_FC_Subsoil.Ordinal_time = None
    Theta_FC_Subsoil.Size = Theta_FC_Subsoil_Data.shape
    Theta_FC_Subsoil.Variable = "Field Capacity Subsoil"
    Theta_FC_Subsoil.Unit = "cm3/cm3"
    
    del Theta_FC_Subsoil_Data
    
    Theta_FC_Subsoil.Save_As_Tiff(os.path.join(output_folder_L2, "Theta_FC_Subsoil"))
    
    ################### Calculate Theta Wilting Point Subsoil ##############################
    Theta_WP_Subsoil_Data = 1.7 * Theta_FC_Subsoil.Data**4
    
    # Write in DataCube
    Theta_WP_Subsoil = DataCube.Rasterdata_Empty()
    Theta_WP_Subsoil.Data = Theta_WP_Subsoil_Data
    Theta_WP_Subsoil.Projection = Albedo.Projection
    Theta_WP_Subsoil.GeoTransform = Albedo.GeoTransform
    Theta_WP_Subsoil.Ordinal_time = None
    Theta_WP_Subsoil.Size = Theta_WP_Subsoil_Data.shape
    Theta_WP_Subsoil.Variable = "Wilting Point Subsoil"
    Theta_WP_Subsoil.Unit = "cm3/cm3"
    
    del Theta_WP_Subsoil_Data
    
    Theta_WP_Subsoil.Save_As_Tiff(os.path.join(output_folder_L2, "Theta_WP_Subsoil"))
    
    ################### Calculate Theta Wilting Point Subsoil ##############################
    Soil_Water_Holding_Capacity_Data = (Theta_FC_Subsoil.Data - Theta_WP_Subsoil.Data ) * 1000
    
    # Write in DataCube
    Soil_Water_Holding_Capacity = DataCube.Rasterdata_Empty()
    Soil_Water_Holding_Capacity.Data = Soil_Water_Holding_Capacity_Data
    Soil_Water_Holding_Capacity.Projection = Albedo.Projection
    Soil_Water_Holding_Capacity.GeoTransform = Albedo.GeoTransform
    Soil_Water_Holding_Capacity.Ordinal_time = None
    Soil_Water_Holding_Capacity.Size = Soil_Water_Holding_Capacity_Data.shape
    Soil_Water_Holding_Capacity.Variable = "Soil Water Holding Capacity"
    Soil_Water_Holding_Capacity.Unit = "mm/m"
    
    del Soil_Water_Holding_Capacity_Data
    
    Soil_Water_Holding_Capacity.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Water_Holding_Capacity"))
    
    ################### Calculate Soil Moisture ############################################
    Soil_Moisture_Data = Theta_Sat_Subsoil.Data * np.exp((np.minimum(Evaporative_Fraction.Data, 1.0) - 1)/0.421)
    
    # Write in DataCube
    Soil_Moisture = DataCube.Rasterdata_Empty()
    Soil_Moisture.Data = Soil_Moisture_Data
    Soil_Moisture.Projection = Albedo.Projection
    Soil_Moisture.GeoTransform = Albedo.GeoTransform
    Soil_Moisture.Ordinal_time = Evaporative_Fraction.Ordinal_time
    Soil_Moisture.Size = Soil_Moisture_Data.shape
    Soil_Moisture.Variable = "Soil Moisture"
    Soil_Moisture.Unit = "cm3/cm3"
    
    del Soil_Moisture_Data
    
    Soil_Moisture.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture"))
    
    ######################## Calculate days in each dekads #################################
    
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)
    
    ######################## Calculate Crop Water Requirement ########################
    
    Crop_Water_Requirement_Data = np.squeeze(np.maximum(Days_in_Dekads[:, None, None] * ET.Data, Crop_Coef_Dry_Soil.Data[None, :, :] * ET0.Data * Days_in_Dekads[:, None, None]), axis = 0)
    
    # Write in DataCube
    Crop_Water_Requirement = DataCube.Rasterdata_Empty()
    Crop_Water_Requirement.Data = Crop_Water_Requirement_Data
    Crop_Water_Requirement.Projection = ET.Projection
    Crop_Water_Requirement.GeoTransform = ET.GeoTransform
    Crop_Water_Requirement.Ordinal_time = ET.Ordinal_time
    Crop_Water_Requirement.Size = Crop_Water_Requirement_Data.shape
    Crop_Water_Requirement.Variable = "Crop Water Requirement"
    Crop_Water_Requirement.Unit = "mm/decade"
    
    del Crop_Water_Requirement_Data
    
    Crop_Water_Requirement.Save_As_Tiff(os.path.join(output_folder_L2, "Crop_Water_Requirement"))
    
    ######################## Calculate Critical Soil Moisture ########################
    
    # Calculate Critical Soil Moisture
    Critical_Soil_Moisture_Data = Theta_WP_Subsoil.Data[None,:,:] + (Theta_FC_Subsoil.Data[None,:,:] - Theta_WP_Subsoil.Data[None,:,:]) * (0.65+0.04*(5 - Crop_Water_Requirement.Data/Days_in_Dekads[:, None, None]))
    
    # Write in DataCube
    Critical_Soil_Moisture = DataCube.Rasterdata_Empty()
    Critical_Soil_Moisture.Data = Critical_Soil_Moisture_Data
    Critical_Soil_Moisture.Projection = ET.Projection
    Critical_Soil_Moisture.GeoTransform = ET.GeoTransform
    Critical_Soil_Moisture.Ordinal_time = ET.Ordinal_time
    Critical_Soil_Moisture.Size = Critical_Soil_Moisture_Data.shape
    Critical_Soil_Moisture.Variable = "Critical Soil Moisture"
    Critical_Soil_Moisture.Unit = "cm3/cm3"
    
    del Critical_Soil_Moisture_Data
    
    Critical_Soil_Moisture.Save_As_Tiff(os.path.join(output_folder_L2, "Critical_Soil_Moisture"))
    
    ################## Calculate Soil Moisture Start and End ########################
    
    Soil_Moisture_Start_Data = np.concatenate((Soil_Moisture.Data[0,:,:][None, :, :],(Soil_Moisture.Data[:-1,:,:]+Soil_Moisture.Data[1:,:,:])/2), axis=0)
    Soil_Moisture_End_Data = np.concatenate(((Soil_Moisture.Data[1:,:,:]+Soil_Moisture.Data[:-1,:,:])/2, Soil_Moisture.Data[-1,:,:][None, :, :]), axis=0)  
    
    # Write in DataCube
    Soil_Moisture_Start = DataCube.Rasterdata_Empty()
    Soil_Moisture_Start.Data = Soil_Moisture_Start_Data
    Soil_Moisture_Start.Projection = Soil_Moisture.Projection
    Soil_Moisture_Start.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_Start.Ordinal_time = Soil_Moisture.Ordinal_time
    Soil_Moisture_Start.Size = Soil_Moisture_Start_Data.shape
    Soil_Moisture_Start.Variable = "Soil Moisture Start"
    Soil_Moisture_Start.Unit = "cm3/cm3"
    
    # Write in DataCube
    Soil_Moisture_End = DataCube.Rasterdata_Empty()
    Soil_Moisture_End.Data = Soil_Moisture_End_Data
    Soil_Moisture_End.Projection = Soil_Moisture.Projection
    Soil_Moisture_End.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_End.Ordinal_time = Soil_Moisture.Ordinal_time
    Soil_Moisture_End.Size = Soil_Moisture_End_Data.shape
    Soil_Moisture_End.Variable = "Soil Moisture End"
    Soil_Moisture_End.Unit = "cm3/cm3"
    
    del Soil_Moisture_End_Data, Soil_Moisture_Start_Data
    
    Soil_Moisture_Start.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture_Start"))
    Soil_Moisture_End.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture_End"))
    
    ################## Calculate Soil Moisture Change ##################################  
    
    Soil_Moisture_Change_Data = Root_Depth.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :] * Days_in_Dekads[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), None, None] * (Soil_Moisture_End.Data - Soil_Moisture_Start.Data)
    
    # Write in DataCube
    Soil_Moisture_Change = DataCube.Rasterdata_Empty()
    Soil_Moisture_Change.Data = Soil_Moisture_Change_Data
    Soil_Moisture_Change.Projection = Soil_Moisture.Projection
    Soil_Moisture_Change.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_Change.Ordinal_time = Soil_Moisture.Ordinal_time
    Soil_Moisture_Change.Size = Soil_Moisture_Change_Data.shape
    Soil_Moisture_Change.Variable = "Change Soil Moisture"
    Soil_Moisture_Change.Unit = "mm/decade"
    
    del Soil_Moisture_Change_Data
    
    Soil_Moisture_Change.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture_Change"))
    
    ################## Calculate Net Supply / Net Drainage ##############################
    
    Net_Supply_Drainage_Data = (ET.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :] - P.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :]) * Days_in_Dekads[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), None, None] + Soil_Moisture_Change.Data
    
    # Write in DataCube
    Net_Supply_Drainage = DataCube.Rasterdata_Empty()
    Net_Supply_Drainage.Data = Net_Supply_Drainage_Data
    Net_Supply_Drainage.Projection = Soil_Moisture.Projection
    Net_Supply_Drainage.GeoTransform = Soil_Moisture.GeoTransform
    Net_Supply_Drainage.Ordinal_time = Soil_Moisture.Ordinal_time
    Net_Supply_Drainage.Size = Net_Supply_Drainage_Data.shape
    Net_Supply_Drainage.Variable = "Net Supply Drainage"
    Net_Supply_Drainage.Unit = "mm/decade"
    
    del Net_Supply_Drainage_Data
    
    Net_Supply_Drainage.Save_As_Tiff(os.path.join(output_folder_L2, "Net_Supply_Drainage"))
    
    #################### Calculate Deep Percolation ###################################    
    
    Deep_Percolation_Data = np.maximum(0, (Soil_Moisture.Data - Theta_FC_Subsoil.Data[None, :, :]) * Root_Depth.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :] * Days_in_Dekads[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), None, None])
    
    # Write in DataCube
    Deep_Percolation = DataCube.Rasterdata_Empty()
    Deep_Percolation.Data = Deep_Percolation_Data
    Deep_Percolation.Projection = Soil_Moisture.Projection
    Deep_Percolation.GeoTransform = Soil_Moisture.GeoTransform
    Deep_Percolation.Ordinal_time = Soil_Moisture.Ordinal_time
    Deep_Percolation.Size = Deep_Percolation_Data.shape
    Deep_Percolation.Variable = "Deep Percolation"
    Deep_Percolation.Unit = "mm/decade"
    
    del Deep_Percolation_Data
    
    Deep_Percolation.Save_As_Tiff(os.path.join(output_folder_L2, "Deep_Percolation"))
    
    ############### Calculate Storage coefficient for surface runoff #################   
    
    Storage_Coeff_Surface_Runoff_Data = 8 * (Sand.Data[None, :, :] * LAI.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :]) * (Theta_Sat_Subsoil.Data[None, :, :] - Soil_Moisture.Data)
    
    # Write in DataCube
    Storage_Coeff_Surface_Runoff = DataCube.Rasterdata_Empty()
    Storage_Coeff_Surface_Runoff.Data = Storage_Coeff_Surface_Runoff_Data
    Storage_Coeff_Surface_Runoff.Projection = Soil_Moisture.Projection
    Storage_Coeff_Surface_Runoff.GeoTransform = Soil_Moisture.GeoTransform
    Storage_Coeff_Surface_Runoff.Ordinal_time = Soil_Moisture.Ordinal_time
    Storage_Coeff_Surface_Runoff.Size = Storage_Coeff_Surface_Runoff_Data.shape
    Storage_Coeff_Surface_Runoff.Variable = "Storage Coefficient Surface Runoff"
    Storage_Coeff_Surface_Runoff.Unit = "mm/decade"
    
    del Storage_Coeff_Surface_Runoff_Data
    
    Storage_Coeff_Surface_Runoff.Save_As_Tiff(os.path.join(output_folder_L2, "Storage_Coeff_Surface_Runoff"))
    
    ######################## Calculate Surface Runoff P  #############################
    
    Surface_Runoff_P_Data = (Days_in_Dekads[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), None, None] * (P.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :] - I.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :]))**2/(Days_in_Dekads[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), None, None] * (P.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :] - I.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :] ) + Storage_Coeff_Surface_Runoff.Data)
     
    # Write in DataCube
    Surface_Runoff_P = DataCube.Rasterdata_Empty()
    Surface_Runoff_P.Data = Surface_Runoff_P_Data
    Surface_Runoff_P.Projection = Soil_Moisture.Projection
    Surface_Runoff_P.GeoTransform = Soil_Moisture.GeoTransform
    Surface_Runoff_P.Ordinal_time = Soil_Moisture.Ordinal_time
    Surface_Runoff_P.Size = Surface_Runoff_P_Data.shape
    Surface_Runoff_P.Variable = "Surface Runoff Precipitation"
    Surface_Runoff_P.Unit = "mm/decade"
    
    del Surface_Runoff_P_Data
    
    Surface_Runoff_P.Save_As_Tiff(os.path.join(output_folder_L2, "Surface_Runoff_P"))
    
    ######################## Calculate Surface Runoff P ##############################  
    
    Surface_Runoff_Coefficient_Data = np.maximum(0.1, Surface_Runoff_P.Data/(P.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :] * Days_in_Dekads[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), None, None]))
     
    # Write in DataCube
    Surface_Runoff_Coefficient = DataCube.Rasterdata_Empty()
    Surface_Runoff_Coefficient.Data = Surface_Runoff_Coefficient_Data
    Surface_Runoff_Coefficient.Projection = Soil_Moisture.Projection
    Surface_Runoff_Coefficient.GeoTransform = Soil_Moisture.GeoTransform
    Surface_Runoff_Coefficient.Ordinal_time = Soil_Moisture.Ordinal_time
    Surface_Runoff_Coefficient.Size = Surface_Runoff_Coefficient_Data.shape
    Surface_Runoff_Coefficient.Variable = "Surface Runoff Coefficient"
    Surface_Runoff_Coefficient.Unit = "-"
    
    del Surface_Runoff_Coefficient_Data
    
    Surface_Runoff_Coefficient.Save_As_Tiff(os.path.join(output_folder_L2, "Surface_Runoff_Coefficient"))
    
    ######################## Calculate updated crop coefficient ######################
    
    Crop_Coef_Update_Data = Crop_Water_Requirement.Data/(Days_in_Dekads[:, None, None] * ET0.Data)
    
    # Write in DataCube
    Crop_Coef_Update = DataCube.Rasterdata_Empty()
    Crop_Coef_Update.Data = Crop_Coef_Update_Data
    Crop_Coef_Update.Projection = LAI.Projection
    Crop_Coef_Update.GeoTransform = LAI.GeoTransform
    Crop_Coef_Update.Ordinal_time = LAI.Ordinal_time
    Crop_Coef_Update.Size = Crop_Coef_Update_Data.shape
    Crop_Coef_Update.Variable = "Crop Coefficient Update"
    Crop_Coef_Update.Unit = "-"
    
    del Crop_Coef_Update_Data
    
    Crop_Coef_Update.Save_As_Tiff(os.path.join(output_folder_L2, "Crop_Coef_Update"))
    
    ################# Calculate 10 year Mean Net Radiation, per Pixel ########################
    
    Total_years = int(np.ceil(Net_Radiation.Size[0]/36))
    Net_Radiation_Long_Term_Data = np.ones([36, Net_Radiation.Size[1], Net_Radiation.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=Net_Radiation.Size[0]]
        Net_Radiation_Long_Term_Data[dekad, :, :] = np.nanmean(Net_Radiation.Data[IDs_good,:,:], axis = 0)
    
    # Write in DataCube
    Net_Radiation_Long_Term = DataCube.Rasterdata_Empty()
    Net_Radiation_Long_Term.Data = Net_Radiation_Long_Term_Data
    Net_Radiation_Long_Term.Projection = Soil_Moisture.Projection
    Net_Radiation_Long_Term.GeoTransform = Soil_Moisture.GeoTransform
    Net_Radiation_Long_Term.Ordinal_time = "Long_Term_Decade"
    Net_Radiation_Long_Term.Size = Net_Radiation_Long_Term_Data.shape
    Net_Radiation_Long_Term.Variable = "Long Term Net Radiation"
    Net_Radiation_Long_Term.Unit = "W/m2"
    
    del Net_Radiation_Long_Term_Data
    
    Net_Radiation_Long_Term.Save_As_Tiff(os.path.join(output_folder_L2, "Net_Radiation_Long_Term"))
    
    ##################### Calculate 10 year mean evaporative fraction ###########################
    
    Total_years = int(np.ceil(Evaporative_Fraction.Size[0]/36))
    Evaporative_Fraction_Long_Term_Data = np.ones([36, Evaporative_Fraction.Size[1], Evaporative_Fraction.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=Evaporative_Fraction.Size[0]]
        Evaporative_Fraction_Long_Term_Data[dekad, :, :] = np.nanmean(Evaporative_Fraction.Data[IDs_good,:,:], axis = 0)
    
    # Write in DataCube
    Evaporative_Fraction_Long_Term = DataCube.Rasterdata_Empty()
    Evaporative_Fraction_Long_Term.Data = Evaporative_Fraction_Long_Term_Data
    Evaporative_Fraction_Long_Term.Projection = Soil_Moisture.Projection
    Evaporative_Fraction_Long_Term.GeoTransform = Soil_Moisture.GeoTransform
    Evaporative_Fraction_Long_Term.Ordinal_time = "Long_Term_Decade"
    Evaporative_Fraction_Long_Term.Size = Evaporative_Fraction_Long_Term_Data.shape
    Evaporative_Fraction_Long_Term.Variable = "Long Term Evaporative Fraction"
    Evaporative_Fraction_Long_Term.Unit = "W/m2"
    
    del Evaporative_Fraction_Long_Term_Data
    
    Evaporative_Fraction_Long_Term.Save_As_Tiff(os.path.join(output_folder_L2, "Evaporative_Fraction_Long_Term"))
    
    ######################### Calculate 10 yr mean soil moisture ###########################
    
    Total_years = int(np.ceil(Evaporative_Fraction.Size[0]/36))
    Soil_Moisture_Long_Term_Data = np.ones([36, Soil_Moisture.Size[1], Soil_Moisture.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=Soil_Moisture.Size[0]]
        Soil_Moisture_Long_Term_Data[dekad, :, :] = np.nanmean(Soil_Moisture.Data[IDs_good,:,:], axis = 0)
    
    # Write in DataCube
    Soil_Moisture_Long_Term = DataCube.Rasterdata_Empty()
    Soil_Moisture_Long_Term.Data = Soil_Moisture_Long_Term_Data
    Soil_Moisture_Long_Term.Projection = Soil_Moisture.Projection
    Soil_Moisture_Long_Term.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_Long_Term.Ordinal_time = "Long_Term_Decade"
    Soil_Moisture_Long_Term.Size = Soil_Moisture_Long_Term_Data.shape
    Soil_Moisture_Long_Term.Variable = "Long Term Soil Moisture"
    Soil_Moisture_Long_Term.Unit = "cm3/cm3"
    
    del Soil_Moisture_Long_Term_Data
    
    Soil_Moisture_Long_Term.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture_Long_Term"))
    
    ################## Calculate Available Water Before Depletion ##########################
    
    Available_Before_Depletion_Data = 0.8 * (0.125 - Theta_WP_Subsoil.Data[None, :, :]) * 10 * Root_Depth.Data
    
    # Write in DataCube
    Available_Before_Depletion = DataCube.Rasterdata_Empty()
    Available_Before_Depletion.Data = Available_Before_Depletion_Data
    Available_Before_Depletion.Projection = Root_Depth.Projection
    Available_Before_Depletion.GeoTransform = Root_Depth.GeoTransform
    Available_Before_Depletion.Ordinal_time = Root_Depth.Ordinal_time
    Available_Before_Depletion.Size = Available_Before_Depletion_Data.shape
    Available_Before_Depletion.Variable = "Available Before Depletion"
    Available_Before_Depletion.Unit = "mm"
    
    del Theta_WP_Subsoil, Root_Depth
    
    Available_Before_Depletion.Save_As_Tiff(os.path.join(output_folder_L2, "Available_Before_Depletion"))
    
    ############################### Calculate Phenelogy ####################################
    
    L2.Phenology.Calc_Phenology(output_folder, Start_year_analyses, End_year_analyses, T, ET, NPP, P, Temp, LU, example_file, Days_in_Dekads)
    
    return()

main(Start_year_analyses, End_year_analyses, output_folder)





