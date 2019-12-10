# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 17:40:22 2019

@author: timhe
"""
import os
import gdal
import warnings
import datetime
import numpy as np
import pandas as pd

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

def main(inputs):

    # Set Variables
    Start_year_analyses = inputs["Start_year"]
    End_year_analyses = inputs["End_year"]
    output_folder = inputs["Output_folder"]  
    WAPOR_LVL = inputs["WAPOR_LEVEL"]  
    Phenology_Threshold = inputs["Phenology_Threshold"]    
    try:
        Radiation_Data = inputs["Radiation_Source"]   
    except:
        Radiation_Data = "KNMI"   
    try:
        Albedo_Data = inputs["Albedo_Source"]   
    except:
        Albedo_Data = "MODIS"    
        
    import WaporTranslator.LEVEL_1.Input_Data as Inputs
    import WaporTranslator.LEVEL_1.DataCube as DataCube
    import WaporTranslator.LEVEL_2 as L2
    import WaporTranslator.LEVEL_2.Functions as Functions
    
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
    Dates_yearly = list(pd.date_range("%s-01-01" %str(Start_year_analyses), "%s-12-31" %End_year_analyses, freq = "AS")) 
    Dates_Daily = list(pd.date_range("%s-01-01" %str(Start_year_analyses), "%s-12-31" %End_year_analyses))
    if Radiation_Data == "LANDSAF":
        Start_Rad = 2016
    if Radiation_Data == "KNMI":    
        Start_Rad = 2017
        
    Dates_Net_Radiation_Daily = list(pd.date_range("%s-01-01" %str(np.maximum(int(Start_year_analyses), Start_Rad)), "%s-12-31" %End_year_analyses))
    Dates_Net_Radiation = Functions.Get_Dekads(str(np.maximum(int(Start_year_analyses), Start_Rad)), End_year_analyses)    

    # Get path and formats
    Paths = Inputs.Input_Paths()
    Formats = Inputs.Input_Formats()
    Conversions = Inputs.Input_Conversions()
    
    # Set example file
    example_file = os.path.join(output_folder, "LEVEL_1", "MASK", "MASK.tif")
    
    # Open Mask
    dest_mask = gdal.Open(example_file)
    MASK = dest_mask.GetRasterBand(1).ReadAsArray()
    
    # Load inputs for LEVEL 2
    T = DataCube.Rasterdata_tiffs(os.path.join(output_folder, str(Paths.T) %WAPOR_LVL), str(Formats.T) %WAPOR_LVL, Dates, Conversion = Conversions.T, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'T', Product = 'WAPOR', Unit = 'mm/day')
    ET0 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET0), Formats.ET0, Dates, Conversion = Conversions.ET0, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET0', Product = 'WAPOR', Unit = 'mm/day')
    LU = DataCube.Rasterdata_tiffs(os.path.join(output_folder, str(Paths.LU) %WAPOR_LVL), str(Formats.LU) %WAPOR_LVL, Dates_yearly, Conversion = Conversions.LU, Example_Data = example_file, Mask_Data = example_file, Variable = 'LU', Product = 'WAPOR', Unit = 'LU')
    LUdek = DataCube.Rasterdata_tiffs(os.path.join(output_folder,str(Paths.LU) %WAPOR_LVL), str(Formats.LU) %WAPOR_LVL, Dates, Conversion = Conversions.LU, Example_Data = example_file, Mask_Data = example_file, Variable = 'LU', Product = 'WAPOR', Unit = 'LU')

    ################################## Calculate LU map ##########################################
    
    Phenology_pixels_year, Grassland_pixels_year = Create_LU_MAP(output_folder, Dates_yearly, LU, LUdek, Paths.LU_ESA, Formats.LU_ESA, example_file)
    LU_END = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.LU_END), Formats.LU_END, list(Dates_yearly), Conversion = Conversions.LU_END, Variable = 'LU_END', Product = '', Unit = '-')

    del LU
    
    ################################## Get ALBEDO data ############################################

    if Albedo_Data == "MODIS":
        Albedo = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Albedo), Formats.Albedo, Dates_Net_Radiation, Conversion = Conversions.Albedo, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Albedo', Product = 'MODIS', Unit = '-')
    else:
        Albedo_Array = np.ones([len(Dates_Net_Radiation), T.Size[1], T.Size[2]])* 0.17
        
        for Dates_albedo in Dates_Net_Radiation:
            Year_now = Dates_albedo.year
            LU_Now = LU_END.Data[Year_now-Start_year_analyses,:,:]
            Albedo_Array_now = np.ones([T.Size[1], T.Size[2]])* 0.17
            Albedo_Array_now = np.where(LU_Now==1, 0.20, Albedo_Array_now)
            Albedo_Array_now= np.where(LU_Now==3, 0.23, Albedo_Array_now)             
            Albedo_Array[Year_now-Start_year_analyses,:,:] = Albedo_Array_now
  
        Albedo = DataCube.Rasterdata_Empty()
        Albedo.Data = Albedo_Array * MASK
        Albedo.Projection = T.Projection
        Albedo.GeoTransform = T.GeoTransform
        Albedo.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Net_Radiation)))
        Albedo.Size = Albedo_Array.shape
        Albedo.Variable = "Albedo"
        Albedo.Unit = "-"
    
    # Open daily
    if Radiation_Data == "LANDSAF":
        DSLF_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.DSLF), Formats.DSLF, Dates_Net_Radiation_Daily, Conversion = Conversions.DSLF, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'DSLF', Product = 'LANDSAF', Unit = 'W/m2')
        DSSF_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.DSSF), Formats.DSSF, Dates_Net_Radiation_Daily, Conversion = Conversions.DSLF, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'DSSF', Product = 'LANDSAF', Unit = 'W/m2')
    if Radiation_Data == "KNMI":
        KNMI_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.KNMI), Formats.KNMI, Dates_Net_Radiation_Daily, Conversion = Conversions.KNMI, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'SDS', Product = 'KNMI', Unit = 'W/m2')
        
    Temp_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Temp), Formats.Temp, Dates_Daily, Conversion = Conversions.Temp, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Temperature', Product = 'GLDAS', Unit = 'Celcius')
    Hum_daily = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Hum), Formats.Hum, Dates_Daily, Conversion = Conversions.Hum, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Humidity', Product = 'GLDAS', Unit = 'Percentage')
 
    #################### Convert into daily datasets ############################################
    Albedo_Daily = Functions.Calc_Daily_from_Dekads(Albedo)

    ################################### Calculate LAI ############################################
    LAI_Data = np.log((1-np.minimum(T.Data/ET0.Data, 0.99)))/(-0.55)
    LAI_Data[LUdek.Data==80] = 0.0
    LAI_Data = LAI_Data.clip(0.0, 7.0)
    
    # Write in DataCube
    LAI = DataCube.Rasterdata_Empty()
    LAI.Data = LAI_Data * MASK
    LAI.Projection = T.Projection
    LAI.GeoTransform = T.GeoTransform
    LAI.Ordinal_time = T.Ordinal_time
    LAI.Size = LAI_Data.shape
    LAI.Variable = "Leaf Area Index"
    LAI.Unit = "m2-m-2"
    
    del LAI_Data, LUdek
    
    LAI.Save_As_Tiff(os.path.join(output_folder_L2, "LAI"))

    #################### Calculate Net Radiation LANDSAF method ###################################    
    if Radiation_Data == "LANDSAF":
        
        ################# Calculate Land Surface Emissivity ###########################################
        Land_Surface_Emissivity_Data = np.minimum(1, 0.9 + 0.017 * LAI.Data[np.isin(LAI.Ordinal_time, Albedo.Ordinal_time), :, :])
        Land_Surface_Emissivity_Data = Land_Surface_Emissivity_Data.clip(0, 1.0)
        
        # Write in DataCube
        Land_Surface_Emissivity = DataCube.Rasterdata_Empty()
        Land_Surface_Emissivity.Data = Land_Surface_Emissivity_Data * MASK
        Land_Surface_Emissivity.Projection = Albedo.Projection
        Land_Surface_Emissivity.GeoTransform = Albedo.GeoTransform
        Land_Surface_Emissivity.Ordinal_time = Albedo.Ordinal_time
        Land_Surface_Emissivity.Size = Land_Surface_Emissivity_Data.shape
        Land_Surface_Emissivity.Variable = "Land Surface Emissivity"
        Land_Surface_Emissivity.Unit = "-"
        
        del Land_Surface_Emissivity_Data
        
        Land_Surface_Emissivity.Save_As_Tiff(os.path.join(output_folder_L2, "Land_Surface_Emissivity"))
        
        #################### Convert into daily datasets ############################################
        Land_Surface_Emissivity_Daily = Functions.Calc_Daily_from_Dekads(Land_Surface_Emissivity)   

        ###################### Calculate Net Radiation (daily) #####################################
        Net_Radiation_Data_Daily = (1 - Albedo_Daily.Data) * DSSF_daily.Data + DSLF_daily.Data * 1.15 - Land_Surface_Emissivity_Daily.Data * 0.0000000567 * (273.15 + Temp_daily.Data[np.isin(Temp_daily.Ordinal_time, DSLF_daily.Ordinal_time)] - 4)**4
        Net_Radiation_Data_Daily  = Net_Radiation_Data_Daily.clip(0, 500)
        Net_Radiation_Data_Daily[Net_Radiation_Data_Daily == 0] = np.nan
        
        del Land_Surface_Emissivity_Daily, DSSF_daily, DSLF_daily
        
    #################### Calculate Net Radiation KNMI method ###################################  
    if Radiation_Data == "KNMI":
        
        DEM =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.DEM), Formats.DEM, Dates = None, Conversion = Conversions.DEM, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'DEM', Product = 'SRTM', Unit = 'm')

        ###################### Calculate Net Radiation (daily) #####################################
        DOY = np.array(list(map(lambda i : int(datetime.datetime.fromordinal(i).strftime('%j')), Albedo_Daily.Ordinal_time[np.isin(Albedo_Daily.Ordinal_time, KNMI_daily.Ordinal_time)])))
        Latitude = Albedo.GeoTransform[3] + Albedo.GeoTransform[5] * np.float_(list(range(0,Albedo.Size[1]))) - 0.5 * Albedo.GeoTransform[5]
        Inverse_Relative_Distance_Earth_Sun = 1 + 0.033* np.cos(2 * np.pi * DOY/365)
        Solar_Declanation = 0.409 * np.sin(2 * np.pi * DOY/365 - 1.39) 
        Sunset_Hour_Angle = np.squeeze(np.arccos(-np.tan(Latitude[None, :, None]/180 * np.pi)*np.tan(Solar_Declanation[:, None, None])))
        Extra_Terrestrial_Radiation = np.squeeze(435.2 * Inverse_Relative_Distance_Earth_Sun[:, None, None] * (Sunset_Hour_Angle[:, :, None] * np.sin((Latitude[None, :, None]/180) * np.pi) * np.sin(Solar_Declanation[:, None, None]) + np.cos((Latitude[None, :, None]/180) * np.pi) * np.cos(Solar_Declanation[:, None, None]) * np.sin(Sunset_Hour_Angle[:, :, None])))
        Saturated_Vapor_Pressure = 0.611 * np.exp((17.27 * Temp_daily.Data)/(237.3 + Temp_daily.Data))
        Actual_Vapor_Pressure = Hum_daily.Data * 0.01 * Saturated_Vapor_Pressure     
        Slope_Saturated_Vapor_Pressure = 4098 * Saturated_Vapor_Pressure/(Temp_daily.Data+237.3)**2
        Psy_Constant = 0.665 * 0.001 * 101.3 * ((293 - 0.0065 * DEM.Data)/293)**(5.26)
        Net_Longwave_FAO = (0.34 - 0.14 * (Actual_Vapor_Pressure[np.isin(Temp_daily.Ordinal_time, KNMI_daily.Ordinal_time), :, :])**(0.5)) * (1.35 * KNMI_daily.Data/(0.8 * Extra_Terrestrial_Radiation[:, :, None]) - 0.35) * 0.0000000567 * (273.15+Temp_daily.Data[np.isin(Temp_daily.Ordinal_time, KNMI_daily.Ordinal_time), :, :])**4
        Net_Longwave_Slob = 110 * (KNMI_daily.Data/Extra_Terrestrial_Radiation[:, :, None])
        Net_Longwave = np.where(Net_Longwave_FAO>Net_Longwave_Slob, Net_Longwave_FAO, Net_Longwave_Slob) 
        Net_Radiation_Data_Daily =(1 - Albedo_Daily.Data[np.isin(Albedo_Daily.Ordinal_time, KNMI_daily.Ordinal_time), :, :])*KNMI_daily.Data - Net_Longwave

        del Hum_daily, Latitude, Inverse_Relative_Distance_Earth_Sun, Solar_Declanation, Sunset_Hour_Angle, Saturated_Vapor_Pressure, Actual_Vapor_Pressure, Net_Longwave_FAO, Net_Longwave

        ###################### Calculate ET0 de Bruin Daily #####################################
        ET0_deBruin_Daily_Data = ((Slope_Saturated_Vapor_Pressure[np.isin(Temp_daily.Ordinal_time, KNMI_daily.Ordinal_time), :, :]/(Slope_Saturated_Vapor_Pressure[np.isin(Temp_daily.Ordinal_time, KNMI_daily.Ordinal_time), :, :] + Psy_Constant[None, :, :])) * ((1 - 0.23) * KNMI_daily.Data - Net_Longwave_Slob) + 20)/28.4

        # Write in DataCube
        ET0_deBruin_Daily = DataCube.Rasterdata_Empty()
        ET0_deBruin_Daily.Data = ET0_deBruin_Daily_Data * MASK
        ET0_deBruin_Daily.Projection = Albedo.Projection
        ET0_deBruin_Daily.GeoTransform = Albedo.GeoTransform
        ET0_deBruin_Daily.Ordinal_time = Albedo_Daily.Ordinal_time
        ET0_deBruin_Daily.Size = ET0_deBruin_Daily_Data.shape
        ET0_deBruin_Daily.Variable = "ET0 de Bruin"
        ET0_deBruin_Daily.Unit = "mm-d-1"
        
        # change from daily to decads
        ET0_deBruin = Functions.Calc_Dekads_from_Daily(ET0_deBruin_Daily, flux_state = "flux")
        ET0_deBruin.Unit = "mm-dekad-1"
        
        del ET0_deBruin_Daily_Data, Net_Longwave_Slob, KNMI_daily, Psy_Constant
        
        ET0_deBruin.Save_As_Tiff(os.path.join(output_folder_L2, "ET0_deBruin"))

    # Write in DataCube
    Net_Radiation_Daily = DataCube.Rasterdata_Empty()
    Net_Radiation_Daily.Data = Net_Radiation_Data_Daily * MASK
    Net_Radiation_Daily.Projection = Albedo.Projection
    Net_Radiation_Daily.GeoTransform = Albedo.GeoTransform
    Net_Radiation_Daily.Ordinal_time = Albedo_Daily.Ordinal_time
    Net_Radiation_Daily.Size = Net_Radiation_Data_Daily.shape
    Net_Radiation_Daily.Variable = "Net Radiation"
    Net_Radiation_Daily.Unit = "W-m-2"
    
    del Net_Radiation_Data_Daily, Albedo_Daily, ET0_deBruin_Daily, Albedo
    
    ############### convert Net Radiation to dekadal ############################################
    Net_Radiation = Functions.Calc_Dekads_from_Daily(Net_Radiation_Daily, flux_state = "state")
    Temp = Functions.Calc_Dekads_from_Daily(Temp_daily, flux_state = "state")
    
    del Net_Radiation_Daily, Temp_daily

    # Calc net Radiation of before 2016 if required
    if int(Start_year_analyses) < Start_Rad:
        
        Total_years = int(np.ceil(Net_Radiation.Size[0]/36))
        Net_Radiation_Per_Dekad = np.ones([36, Net_Radiation.Size[1], Net_Radiation.Size[2]]) * np.nan
        ET0_Per_Dekad = np.ones([36, Net_Radiation.Size[1], Net_Radiation.Size[2]]) * np.nan
        
        IDs_diff = ET0.Size[0] - Net_Radiation.Size[0]
        for dekad in range(0,36):
            IDs_rad = np.array(range(0, Total_years)) * 36 + dekad  
            IDs_rad_good = IDs_rad[IDs_rad<=Net_Radiation.Size[0]]
            IDs_et0 = np.array(range(0, Total_years)) * 36 + dekad + IDs_diff 
            IDs_et0_good = IDs_et0[IDs_et0<=ET0.Size[0]]
            Net_Radiation_Per_Dekad[dekad, :, :] = np.nanmean(Net_Radiation.Data[IDs_rad_good,:,:], axis = 0)
            ET0_Per_Dekad[dekad, :, :] = np.nanmean(ET0.Data[IDs_et0_good,:,:], axis = 0)

        Ratio_per_dekad = Net_Radiation_Per_Dekad/ET0_Per_Dekad
        
        Ratios = Ratio_per_dekad 
        for i in range(0, Start_Rad - int(Start_year_analyses)-1):
            Ratios = np.vstack([Ratios, Ratio_per_dekad])
        
        Net_Radiation_Before_Start_Rad = Ratios * ET0.Data[0:Ratios.shape[0],:,:]
        Net_Radiation_Data = np.vstack([Net_Radiation_Before_Start_Rad, Net_Radiation.Data])
        
        Net_Radiation.Data = Net_Radiation_Data
        Net_Radiation.Size = Net_Radiation_Data.shape
        Net_Radiation.Ordinal_time = T.Ordinal_time    

        del Net_Radiation_Data
        
    Net_Radiation.Unit = "W-m-2"     
    Net_Radiation.Save_As_Tiff(os.path.join(output_folder_L2, "Net_Radiation"))

    ############################ Calculate Root Depth ##########################################    

    # Load inputs for LEVEL 2    
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, str(Paths.ET) %WAPOR_LVL), str(Formats.ET) %WAPOR_LVL, Dates, Conversion = Conversions.ET, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = 'mm/day')
    P = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.P), Formats.P, Dates, Conversion = Conversions.P, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'P', Product = 'WAPOR', Unit = 'mm/day')
    NPP = DataCube.Rasterdata_tiffs(os.path.join(output_folder, str(Paths.NPP) %WAPOR_LVL), str(Formats.NPP) %WAPOR_LVL, Dates, Conversion = Conversions.NPP, Example_Data = example_file, Mask_Data = example_file, Variable = 'NPP', Product = 'WAPOR', Unit = 'kg/ha/day')
 
    ############################ Calculate Root Depth ##########################################
    Root_Depth_Data = 0.85 * 100 * np.maximum(0, -0.0326 * LAI.Data**2 + 0.4755 * LAI.Data - 0.0411)
    Root_Depth_Data = Root_Depth_Data.clip(0, 500)
    
    # Write in DataCube
    Root_Depth = DataCube.Rasterdata_Empty()
    Root_Depth.Data = Root_Depth_Data * MASK
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
    Fract_vegt.Data = Fract_vegt_Data * MASK
    Fract_vegt.Projection = ET.Projection
    Fract_vegt.GeoTransform = ET.GeoTransform
    Fract_vegt.Ordinal_time = ET.Ordinal_time
    Fract_vegt.Size = Fract_vegt_Data.shape
    Fract_vegt.Variable = "Fractional Vegetation"
    Fract_vegt.Unit = "-"
    
    del Fract_vegt_Data
    
    Fract_vegt.Save_As_Tiff(os.path.join(output_folder_L2, "Fractional_Vegetation_Cover"))
    
    ########################## Calculate maximum Kc ####################################
    Kc_MAX_Data = np.minimum(1.4 ,0.95 * Fract_vegt.Data + 0.2)
    Kc_MAX_Data = Kc_MAX_Data.clip(0, 500)
    
    # Write in DataCube
    Kc_MAX = DataCube.Rasterdata_Empty()
    Kc_MAX.Data = Kc_MAX_Data * MASK
    Kc_MAX.Projection = ET.Projection
    Kc_MAX.GeoTransform = ET.GeoTransform
    Kc_MAX.Ordinal_time = ET.Ordinal_time
    Kc_MAX.Size = Kc_MAX_Data.shape
    Kc_MAX.Variable = "Kc MAX"
    Kc_MAX.Unit = "-"
    
    del Kc_MAX_Data, Fract_vegt
    
    Kc_MAX.Save_As_Tiff(os.path.join(output_folder_L2, "Kc_MAX"))
 
    ################# Calculate Evaporative Fraction ############################################
    Evaporative_Fraction_Data = ET.Data *28.4/Net_Radiation.Data
    Evaporative_Fraction_Data = Evaporative_Fraction_Data.clip(0, 1.5)
    
    # Write in DataCube
    Evaporative_Fraction = DataCube.Rasterdata_Empty()
    Evaporative_Fraction.Data = Evaporative_Fraction_Data * MASK
    Evaporative_Fraction.Projection = ET.Projection
    Evaporative_Fraction.GeoTransform = ET.GeoTransform
    Evaporative_Fraction.Ordinal_time = ET.Ordinal_time
    Evaporative_Fraction.Size = Evaporative_Fraction_Data.shape
    Evaporative_Fraction.Variable = "Evaporative Fraction"
    Evaporative_Fraction.Unit = "-"
    
    del Evaporative_Fraction_Data
    
    Evaporative_Fraction.Save_As_Tiff(os.path.join(output_folder_L2, "Evaporative_Fraction"))

    ############## Calculate Land Theta Saturated Subsoil ##################################
    
    # Open Constant
    Bulk =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Bulk), Formats.Bulk.format(level=6), Dates = None, Conversion = Conversions.Bulk, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Bulk', Product = 'SoilGrids', Unit = 'kg/m3')
    Sand =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Sand), Formats.Sand.format(level=6), Dates = None, Conversion = Conversions.Sand, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Sand', Product = 'SoilGrids', Unit = 'Percentage')
    Clay =  DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Clay), Formats.Clay.format(level=6), Dates = None, Conversion = Conversions.Clay, Example_Data = example_file, Mask_Data = example_file, reprojection_type = 2, Variable = 'Clay', Product = 'SoilGrids', Unit = 'Percentage')

    Theta_Sat_Subsoil_Data = 0.85 * (1 - Bulk.Data/2650) + 0.13 * Clay.Data * 0.01
    
    # Write in DataCube
    Theta_Sat_Subsoil = DataCube.Rasterdata_Empty()
    Theta_Sat_Subsoil.Data = Theta_Sat_Subsoil_Data * MASK
    Theta_Sat_Subsoil.Projection = ET.Projection
    Theta_Sat_Subsoil.GeoTransform = ET.GeoTransform
    Theta_Sat_Subsoil.Ordinal_time = None
    Theta_Sat_Subsoil.Size = Theta_Sat_Subsoil_Data.shape
    Theta_Sat_Subsoil.Variable = "Saturated Theta Subsoil"
    Theta_Sat_Subsoil.Unit = "cm3-cm-3"
    
    del Theta_Sat_Subsoil_Data
    
    Theta_Sat_Subsoil.Save_As_Tiff(os.path.join(output_folder_L2, "Theta_Sat_Subsoil"))
    
    ################### Calculate Theta Field Capacity Subsoil #############################
    Theta_FC_Subsoil_Data = -2.2 * Theta_Sat_Subsoil.Data**2 + 2.92 * Theta_Sat_Subsoil.Data - 0.59
    
    # Write in DataCube
    Theta_FC_Subsoil = DataCube.Rasterdata_Empty()
    Theta_FC_Subsoil.Data = Theta_FC_Subsoil_Data * MASK
    Theta_FC_Subsoil.Projection = ET.Projection
    Theta_FC_Subsoil.GeoTransform = ET.GeoTransform
    Theta_FC_Subsoil.Ordinal_time = None
    Theta_FC_Subsoil.Size = Theta_FC_Subsoil_Data.shape
    Theta_FC_Subsoil.Variable = "Field Capacity Subsoil"
    Theta_FC_Subsoil.Unit = "cm3-cm-3"
    
    del Theta_FC_Subsoil_Data
    
    Theta_FC_Subsoil.Save_As_Tiff(os.path.join(output_folder_L2, "Theta_FC_Subsoil"))
    
    ################### Calculate Theta Wilting Point Subsoil ##############################
    Theta_WP_Subsoil_Data = 3.0575 * Theta_FC_Subsoil.Data**4.5227
    
    # Write in DataCube
    Theta_WP_Subsoil = DataCube.Rasterdata_Empty()
    Theta_WP_Subsoil.Data = Theta_WP_Subsoil_Data * MASK
    Theta_WP_Subsoil.Projection = ET.Projection
    Theta_WP_Subsoil.GeoTransform = ET.GeoTransform
    Theta_WP_Subsoil.Ordinal_time = None
    Theta_WP_Subsoil.Size = Theta_WP_Subsoil_Data.shape
    Theta_WP_Subsoil.Variable = "Wilting Point Subsoil"
    Theta_WP_Subsoil.Unit = "cm3-cm-3"
    
    del Theta_WP_Subsoil_Data
    
    Theta_WP_Subsoil.Save_As_Tiff(os.path.join(output_folder_L2, "Theta_WP_Subsoil"))
    
    ################### Calculate Theta Wilting Point Subsoil ##############################
    Soil_Water_Holding_Capacity_Data = (Theta_FC_Subsoil.Data - Theta_WP_Subsoil.Data ) * 1000
    
    # Write in DataCube
    Soil_Water_Holding_Capacity = DataCube.Rasterdata_Empty()
    Soil_Water_Holding_Capacity.Data = Soil_Water_Holding_Capacity_Data * MASK
    Soil_Water_Holding_Capacity.Projection = ET.Projection
    Soil_Water_Holding_Capacity.GeoTransform = ET.GeoTransform
    Soil_Water_Holding_Capacity.Ordinal_time = None
    Soil_Water_Holding_Capacity.Size = Soil_Water_Holding_Capacity_Data.shape
    Soil_Water_Holding_Capacity.Variable = "Soil Water Holding Capacity"
    Soil_Water_Holding_Capacity.Unit = "mm-m-1"
    
    del Soil_Water_Holding_Capacity_Data
    
    Soil_Water_Holding_Capacity.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Water_Holding_Capacity"))
    
    ################### Calculate Soil Moisture ############################################
    Soil_Moisture_Data = Theta_Sat_Subsoil.Data * np.exp((np.minimum(Evaporative_Fraction.Data, 0.9) - 1)/0.421)
    
    # Write in DataCube
    Soil_Moisture = DataCube.Rasterdata_Empty()
    Soil_Moisture.Data = Soil_Moisture_Data * MASK
    Soil_Moisture.Projection = ET.Projection
    Soil_Moisture.GeoTransform = ET.GeoTransform
    Soil_Moisture.Ordinal_time = ET.Ordinal_time
    Soil_Moisture.Size = Soil_Moisture_Data.shape
    Soil_Moisture.Variable = "Soil Moisture"
    Soil_Moisture.Unit = "cm3-cm-3"
    
    del Soil_Moisture_Data
    
    Soil_Moisture.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture"))
    
    ######################## Calculate days in each dekads #################################
    
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)
    
    ######################## Calculate Crop Water Requirement ########################
    
    Crop_Water_Requirement_Data = np.squeeze(np.maximum(Days_in_Dekads[:, None, None] * ET.Data, Kc_MAX.Data[None, :, :] * ET0.Data * Days_in_Dekads[:, None, None]), axis = 0)
    
    # Write in DataCube
    Crop_Water_Requirement = DataCube.Rasterdata_Empty()
    Crop_Water_Requirement.Data = Crop_Water_Requirement_Data * MASK
    Crop_Water_Requirement.Projection = ET.Projection
    Crop_Water_Requirement.GeoTransform = ET.GeoTransform
    Crop_Water_Requirement.Ordinal_time = ET.Ordinal_time
    Crop_Water_Requirement.Size = Crop_Water_Requirement_Data.shape
    Crop_Water_Requirement.Variable = "Crop Water Requirement"
    Crop_Water_Requirement.Unit = "mm-dekad-1"
    
    del Crop_Water_Requirement_Data, Kc_MAX
    
    Crop_Water_Requirement.Save_As_Tiff(os.path.join(output_folder_L2, "Crop_Water_Requirement"))
    
    ######################## Calculate Critical Soil Moisture ########################
    
    # Calculate Critical Soil Moisture
    Critical_Soil_Moisture_Data = Theta_WP_Subsoil.Data[None,:,:] + (Theta_FC_Subsoil.Data[None,:,:] - Theta_WP_Subsoil.Data[None,:,:]) * (0.47+0.04*(5 - Crop_Water_Requirement.Data/Days_in_Dekads[:, None, None]))
    
    # Write in DataCube
    Critical_Soil_Moisture = DataCube.Rasterdata_Empty()
    Critical_Soil_Moisture.Data = Critical_Soil_Moisture_Data * MASK
    Critical_Soil_Moisture.Projection = ET.Projection
    Critical_Soil_Moisture.GeoTransform = ET.GeoTransform
    Critical_Soil_Moisture.Ordinal_time = ET.Ordinal_time
    Critical_Soil_Moisture.Size = Critical_Soil_Moisture_Data.shape
    Critical_Soil_Moisture.Variable = "Critical Soil Moisture"
    Critical_Soil_Moisture.Unit = "cm3-cm-3"
    
    del Critical_Soil_Moisture_Data
    
    Critical_Soil_Moisture.Save_As_Tiff(os.path.join(output_folder_L2, "Critical_Soil_Moisture"))
    
    del Critical_Soil_Moisture
    
    ################## Calculate Soil Moisture Start and End ########################
    
    Soil_Moisture_Start_Data = np.concatenate((Soil_Moisture.Data[0,:,:][None, :, :],(Soil_Moisture.Data[:-1,:,:]+Soil_Moisture.Data[1:,:,:])/2), axis=0)
    Soil_Moisture_End_Data = np.concatenate(((Soil_Moisture.Data[1:,:,:]+Soil_Moisture.Data[:-1,:,:])/2, Soil_Moisture.Data[-1,:,:][None, :, :]), axis=0)  
    
    # Write in DataCube
    Soil_Moisture_Start = DataCube.Rasterdata_Empty()
    Soil_Moisture_Start.Data = Soil_Moisture_Start_Data * MASK
    Soil_Moisture_Start.Projection = Soil_Moisture.Projection
    Soil_Moisture_Start.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_Start.Ordinal_time = Soil_Moisture.Ordinal_time
    Soil_Moisture_Start.Size = Soil_Moisture_Start_Data.shape
    Soil_Moisture_Start.Variable = "Soil Moisture Start"
    Soil_Moisture_Start.Unit = "cm3-cm-3"
    
    # Write in DataCube
    Soil_Moisture_End = DataCube.Rasterdata_Empty()
    Soil_Moisture_End.Data = Soil_Moisture_End_Data * MASK
    Soil_Moisture_End.Projection = Soil_Moisture.Projection
    Soil_Moisture_End.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_End.Ordinal_time = Soil_Moisture.Ordinal_time
    Soil_Moisture_End.Size = Soil_Moisture_End_Data.shape
    Soil_Moisture_End.Variable = "Soil Moisture End"
    Soil_Moisture_End.Unit = "cm3-cm-3"
    
    del Soil_Moisture_End_Data, Soil_Moisture_Start_Data
    
    Soil_Moisture_Start.Save_As_Tiff(os.path.join(output_folder_L2, "Temp", "Soil_Moisture_Start"))
    Soil_Moisture_End.Save_As_Tiff(os.path.join(output_folder_L2, "Temp", "Soil_Moisture_End"))
    
    ################## Calculate Soil Moisture Change ##################################  
    
    Soil_Moisture_Change_Data = 10 * Root_Depth.Data * Days_in_Dekads[:, None, None] * (Soil_Moisture_End.Data - Soil_Moisture_Start.Data)
    
    # Write in DataCube
    Soil_Moisture_Change = DataCube.Rasterdata_Empty()
    Soil_Moisture_Change.Data = Soil_Moisture_Change_Data * MASK
    Soil_Moisture_Change.Projection = Soil_Moisture.Projection
    Soil_Moisture_Change.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_Change.Ordinal_time = Soil_Moisture.Ordinal_time
    Soil_Moisture_Change.Size = Soil_Moisture_Change_Data.shape
    Soil_Moisture_Change.Variable = "Change Soil Moisture"
    Soil_Moisture_Change.Unit = "mm-dekad-1"
    
    del Soil_Moisture_Change_Data, Soil_Moisture_Start, Soil_Moisture_End
    
    Soil_Moisture_Change.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture_Change"))
    
    ################## Calculate Net Supply / Net Drainage ##############################
    
    Net_Supply_Drainage_Data = (ET.Data - P.Data) * Days_in_Dekads[:, None, None] + Soil_Moisture_Change.Data
    
    # Write in DataCube
    Net_Supply_Drainage = DataCube.Rasterdata_Empty()
    Net_Supply_Drainage.Data = Net_Supply_Drainage_Data * MASK
    Net_Supply_Drainage.Projection = Soil_Moisture.Projection
    Net_Supply_Drainage.GeoTransform = Soil_Moisture.GeoTransform
    Net_Supply_Drainage.Ordinal_time = Soil_Moisture.Ordinal_time
    Net_Supply_Drainage.Size = Net_Supply_Drainage_Data.shape
    Net_Supply_Drainage.Variable = "Net Supply Drainage"
    Net_Supply_Drainage.Unit = "mm-dekad-1"
    
    del Net_Supply_Drainage_Data, Soil_Moisture_Change
    
    Net_Supply_Drainage.Save_As_Tiff(os.path.join(output_folder_L2, "Temp", "Net_Supply_Drainage"))
    
    del Net_Supply_Drainage
    
    #################### Calculate Deep Percolation ###################################    
    
    Deep_Percolation_Data = np.maximum(0, (Soil_Moisture.Data - Theta_FC_Subsoil.Data[None, :, :]) * Root_Depth.Data * Days_in_Dekads[:, None, None])
    
    # Write in DataCube
    Deep_Percolation = DataCube.Rasterdata_Empty()
    Deep_Percolation.Data = Deep_Percolation_Data * MASK
    Deep_Percolation.Projection = Soil_Moisture.Projection
    Deep_Percolation.GeoTransform = Soil_Moisture.GeoTransform
    Deep_Percolation.Ordinal_time = Soil_Moisture.Ordinal_time
    Deep_Percolation.Size = Deep_Percolation_Data.shape
    Deep_Percolation.Variable = "Deep Percolation"
    Deep_Percolation.Unit = "mm-dekad-1"
    
    del Deep_Percolation_Data
    
    Deep_Percolation.Save_As_Tiff(os.path.join(output_folder_L2, "Deep_Percolation"))
    
    del Deep_Percolation
    
    ############### Calculate Storage coefficient for surface runoff #################   
    
    Storage_Coeff_Surface_Runoff_Data = 4 * (Sand.Data[None, :, :] * LAI.Data) * (Theta_Sat_Subsoil.Data[None, :, :] - Soil_Moisture.Data)
    
    # Write in DataCube
    Storage_Coeff_Surface_Runoff = DataCube.Rasterdata_Empty()
    Storage_Coeff_Surface_Runoff.Data = Storage_Coeff_Surface_Runoff_Data * MASK
    Storage_Coeff_Surface_Runoff.Projection = Soil_Moisture.Projection
    Storage_Coeff_Surface_Runoff.GeoTransform = Soil_Moisture.GeoTransform
    Storage_Coeff_Surface_Runoff.Ordinal_time = Soil_Moisture.Ordinal_time
    Storage_Coeff_Surface_Runoff.Size = Storage_Coeff_Surface_Runoff_Data.shape
    Storage_Coeff_Surface_Runoff.Variable = "Storage Coefficient Surface Runoff"
    Storage_Coeff_Surface_Runoff.Unit = "mm-dekad-1"
    
    del Storage_Coeff_Surface_Runoff_Data
    
    Storage_Coeff_Surface_Runoff.Save_As_Tiff(os.path.join(output_folder_L2, "Storage_Coeff_Surface_Runoff"))
    
    ######################## Calculate Surface Runoff P  #############################
    I = DataCube.Rasterdata_tiffs(os.path.join(output_folder, str(Paths.I) %WAPOR_LVL), str(Formats.I) %WAPOR_LVL, Dates, Conversion = Conversions.I, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'I', Product = 'WAPOR', Unit = 'mm/day')
    
    Surface_Runoff_P_Data = (Days_in_Dekads[:, None, None] * (P.Data - I.Data))**2/(Days_in_Dekads[:, None, None] * (P.Data- I.Data) + Storage_Coeff_Surface_Runoff.Data)
    Surface_Runoff_P_Data[np.isnan(Surface_Runoff_P_Data)] = 0.0
    
    # Write in DataCube
    Surface_Runoff_P = DataCube.Rasterdata_Empty()
    Surface_Runoff_P.Data = Surface_Runoff_P_Data * MASK
    Surface_Runoff_P.Projection = Soil_Moisture.Projection
    Surface_Runoff_P.GeoTransform = Soil_Moisture.GeoTransform
    Surface_Runoff_P.Ordinal_time = Soil_Moisture.Ordinal_time
    Surface_Runoff_P.Size = Surface_Runoff_P_Data.shape
    Surface_Runoff_P.Variable = "Surface Runoff Precipitation"
    Surface_Runoff_P.Unit = "mm-dekad-1"
    
    del Surface_Runoff_P_Data, I, Storage_Coeff_Surface_Runoff
    
    Surface_Runoff_P.Save_As_Tiff(os.path.join(output_folder_L2, "Surface_Runoff_P"))
    
    ######################## Calculate Surface Runoff P ##############################  
    
    Surface_Runoff_Coefficient_Data = np.maximum(0.1, Surface_Runoff_P.Data/(P.Data * Days_in_Dekads[:, None, None]))
    Surface_Runoff_Coefficient_Data[np.isnan(Surface_Runoff_Coefficient_Data)] = 0.1
     
    # Write in DataCube
    Surface_Runoff_Coefficient = DataCube.Rasterdata_Empty()
    Surface_Runoff_Coefficient.Data = Surface_Runoff_Coefficient_Data * MASK
    Surface_Runoff_Coefficient.Projection = Soil_Moisture.Projection
    Surface_Runoff_Coefficient.GeoTransform = Soil_Moisture.GeoTransform
    Surface_Runoff_Coefficient.Ordinal_time = Soil_Moisture.Ordinal_time
    Surface_Runoff_Coefficient.Size = Surface_Runoff_Coefficient_Data.shape
    Surface_Runoff_Coefficient.Variable = "Surface Runoff Coefficient"
    Surface_Runoff_Coefficient.Unit = "-"
    
    del Surface_Runoff_Coefficient_Data
    
    Surface_Runoff_Coefficient.Save_As_Tiff(os.path.join(output_folder_L2, "Surface_Runoff_Coefficient"))
    
    del Surface_Runoff_P, Surface_Runoff_Coefficient
    
    ######################## Calculate updated maximum kc ######################
    
    Kc_MAX_update_Data = Crop_Water_Requirement.Data/(Days_in_Dekads[:, None, None] * ET0.Data)
    
    # Write in DataCube
    Kc_MAX_update = DataCube.Rasterdata_Empty()
    Kc_MAX_update.Data = Kc_MAX_update_Data * MASK
    Kc_MAX_update.Projection = LAI.Projection
    Kc_MAX_update.GeoTransform = LAI.GeoTransform
    Kc_MAX_update.Ordinal_time = LAI.Ordinal_time
    Kc_MAX_update.Size = Kc_MAX_update_Data.shape
    Kc_MAX_update.Variable = "Kc MAX update"
    Kc_MAX_update.Unit = "-"
    
    del Kc_MAX_update_Data
    
    Kc_MAX_update.Save_As_Tiff(os.path.join(output_folder_L2, "Kc_MAX_update"))
    
    del Kc_MAX_update
    
    ################# Calculate 10 year Mean Net Radiation, per Pixel ########################
    
    Total_years = int(np.ceil(Net_Radiation.Size[0]/36))
    Net_Radiation_Long_Term_Data = np.ones([36, Net_Radiation.Size[1], Net_Radiation.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=Net_Radiation.Size[0]]
        Net_Radiation_Long_Term_Data[dekad, :, :] = np.nanmean(Net_Radiation.Data[IDs_good,:,:], axis = 0)
    
    # Write in DataCube
    Net_Radiation_Long_Term = DataCube.Rasterdata_Empty()
    Net_Radiation_Long_Term.Data = Net_Radiation_Long_Term_Data * MASK
    Net_Radiation_Long_Term.Projection = Soil_Moisture.Projection
    Net_Radiation_Long_Term.GeoTransform = Soil_Moisture.GeoTransform
    Net_Radiation_Long_Term.Ordinal_time = "Long_Term_Decade"
    Net_Radiation_Long_Term.Size = Net_Radiation_Long_Term_Data.shape
    Net_Radiation_Long_Term.Variable = "Long Term Net Radiation"
    Net_Radiation_Long_Term.Unit = "W-m-2"
    
    del Net_Radiation_Long_Term_Data
    
    Net_Radiation_Long_Term.Save_As_Tiff(os.path.join(output_folder_L2, "Net_Radiation_Long_Term"))
    
    del Net_Radiation_Long_Term
    
    ##################### Calculate 10 year mean evaporative fraction ###########################
    
    Total_years = int(np.ceil(Evaporative_Fraction.Size[0]/36))
    Evaporative_Fraction_Long_Term_Data = np.ones([36, Evaporative_Fraction.Size[1], Evaporative_Fraction.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=Evaporative_Fraction.Size[0]]
        Evaporative_Fraction_Long_Term_Data[dekad, :, :] = np.nanmean(Evaporative_Fraction.Data[IDs_good,:,:], axis = 0)
    
    # Write in DataCube
    Evaporative_Fraction_Long_Term = DataCube.Rasterdata_Empty()
    Evaporative_Fraction_Long_Term.Data = Evaporative_Fraction_Long_Term_Data * MASK
    Evaporative_Fraction_Long_Term.Projection = Soil_Moisture.Projection
    Evaporative_Fraction_Long_Term.GeoTransform = Soil_Moisture.GeoTransform
    Evaporative_Fraction_Long_Term.Ordinal_time = "Long_Term_Decade"
    Evaporative_Fraction_Long_Term.Size = Evaporative_Fraction_Long_Term_Data.shape
    Evaporative_Fraction_Long_Term.Variable = "Long Term Evaporative Fraction"
    Evaporative_Fraction_Long_Term.Unit = "-"
    
    del Evaporative_Fraction_Long_Term_Data
    
    Evaporative_Fraction_Long_Term.Save_As_Tiff(os.path.join(output_folder_L2, "Evaporative_Fraction_Long_Term"))
    
    del Evaporative_Fraction_Long_Term
    
    ######################### Calculate 10 yr mean soil moisture ###########################
    
    Total_years = int(np.ceil(Evaporative_Fraction.Size[0]/36))
    Soil_Moisture_Long_Term_Data = np.ones([36, Soil_Moisture.Size[1], Soil_Moisture.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=Soil_Moisture.Size[0]]
        Soil_Moisture_Long_Term_Data[dekad, :, :] = np.nanmean(Soil_Moisture.Data[IDs_good,:,:], axis = 0)
    
    # Write in DataCube
    Soil_Moisture_Long_Term = DataCube.Rasterdata_Empty()
    Soil_Moisture_Long_Term.Data = Soil_Moisture_Long_Term_Data * MASK
    Soil_Moisture_Long_Term.Projection = Soil_Moisture.Projection
    Soil_Moisture_Long_Term.GeoTransform = Soil_Moisture.GeoTransform
    Soil_Moisture_Long_Term.Ordinal_time = "Long_Term_Decade"
    Soil_Moisture_Long_Term.Size = Soil_Moisture_Long_Term_Data.shape
    Soil_Moisture_Long_Term.Variable = "Long Term Soil Moisture"
    Soil_Moisture_Long_Term.Unit = "cm3-cm-3"
    
    del Soil_Moisture_Long_Term_Data
    
    Soil_Moisture_Long_Term.Save_As_Tiff(os.path.join(output_folder_L2, "Soil_Moisture_Long_Term"))
    
    del Soil_Moisture_Long_Term
    
    ################## Calculate Available Water Before Depletion ##########################
    
    Available_Before_Depletion_Data = 0.8 * (Theta_FC_Subsoil.Data[None, :, :] - 0.12) * 10 * Root_Depth.Data
    
    # Write in DataCube
    Available_Before_Depletion = DataCube.Rasterdata_Empty()
    Available_Before_Depletion.Data = Available_Before_Depletion_Data * MASK
    Available_Before_Depletion.Projection = Root_Depth.Projection
    Available_Before_Depletion.GeoTransform = Root_Depth.GeoTransform
    Available_Before_Depletion.Ordinal_time = Root_Depth.Ordinal_time
    Available_Before_Depletion.Size = Available_Before_Depletion_Data.shape
    Available_Before_Depletion.Variable = "Available Before Depletion"
    Available_Before_Depletion.Unit = "mm"
    
    del Theta_WP_Subsoil, Root_Depth
    
    Available_Before_Depletion.Save_As_Tiff(os.path.join(output_folder_L2, "Available_Before_Depletion"))
    
    del Available_Before_Depletion
    
    ############################### Calculate Phenelogy ####################################
    
    L2.Phenology.Calc_Phenology(output_folder, Start_year_analyses, End_year_analyses, T, ET, NPP, P, Temp, ET0, LU_END, Phenology_pixels_year, Grassland_pixels_year, example_file, Days_in_Dekads, Phenology_Threshold)

    return()    
    
def Create_LU_MAP(output_folder, Dates_yearly, LU, LUdek, Paths_LU_ESA, Formats_LU_ESA, example_file):
    
    # Create output folder LVL2
    output_folder_L2 = os.path.join(output_folder, "LEVEL_2")
    
    # Open ESACCI
    input_file_LU_ESACCI = os.path.join(output_folder, Paths_LU_ESA, Formats_LU_ESA)
    
    # Converting LU maps into one LU map
    # open dictionary WAPOR 
    WAPOR_Conversions_dict = WAPOR_Conversions()
    # open dictionary ESACCI
    ESACCI_Conversions_dict = ESACCI_Conversions()
    
    Phenology_pixels_year = np.ones(LUdek.Size) * np.nan
    Grassland_pixels_year = np.ones(LUdek.Size) * np.nan
    
    # Loop over the years
    for Year in Dates_yearly:
        
        Year_start = int(Dates_yearly[0].year)
        Year_int = int(Year.year)
        
        geo = LU.GeoTransform
        proj = LU.Projection   
         
        destLUESACCI = RC.reproject_dataset_example(input_file_LU_ESACCI, example_file)
        LU_ESACCI = destLUESACCI.GetRasterBand(1).ReadAsArray()
        
        # Create LUmap
        LU_Map_WAPOR = np.ones([LU.Size[1], LU.Size[2]]) * np.nan
        LU_Map_ESACCI = np.ones([LU.Size[1], LU.Size[2]]) * np.nan
        
        for number in WAPOR_Conversions_dict.items():
        
            LU_Map_WAPOR = np.where(LU.Data[int((Year_int - Year_start)),: ,:] == number[0], number[1], LU_Map_WAPOR)
            
        for number in ESACCI_Conversions_dict.items():
        
            LU_Map_ESACCI = np.where(LU_ESACCI == number[0], number[1], LU_Map_ESACCI)      
        
        # Combine LU maps
        # 1 = rainfed, 2 = irrigated, 3 = Pasture
        LU_END = np.where(np.logical_and(LU_Map_WAPOR == 1, LU_Map_ESACCI == 1), 1, np.nan)    
        LU_END = np.where(LU_Map_WAPOR > 1, LU_Map_WAPOR, LU_END)
          
        # Save LU map
        DC.Save_as_tiff(os.path.join(output_folder_L2, "LU_END", "LU_%s.tif" %Year_int), LU_END, geo, proj)  
        
        # find posible Perennial pixels
        Phenology_pixels_year[int((Year_int - Year_start) * 36):int((Year_int - Year_start) * 36)+36,: ,:] = np.where(np.logical_or(LU_END==1, LU_END==2), 1, np.nan)[None, :, :]  
        Grassland_pixels_year[int((Year_int - Year_start) * 36):int((Year_int - Year_start) * 36)+36,: ,:] = np.where(LU_END==3, 1, np.nan)[None, :, :]  
    
    return(Phenology_pixels_year, Grassland_pixels_year)
        
def WAPOR_Conversions(version = '1.0'):
    
    converter = {
         41: 1,
         43: 1,
         42: 2,
         30: 3}

    WAPOR_Conversions =dict()
    WAPOR_Conversions['1.0'] = converter

    return WAPOR_Conversions[version]

def ESACCI_Conversions(version = '1.0'):
    
    converter = {
         10: 1,
         #30: 1,
         20: 2,
         130: 3}

    ESACCI_Conversions =dict()
    ESACCI_Conversions['1.0'] = converter

    return ESACCI_Conversions[version]

