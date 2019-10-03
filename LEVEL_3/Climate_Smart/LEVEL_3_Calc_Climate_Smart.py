# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:05:39 2019
"""

import os
import gdal
import datetime
import pandas as pd
import calendar
import numpy as np

import WaporTranslator.LEVEL_3.LEVEL_3_Calc_Food_Security as L3_Food_Security

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC


def Calc_Climate_Smart(output_folder_L2, Date, example_file):

    # Get Date
    Date_datetime = datetime.datetime.strptime(Date, "%Y-%m-%d")
    Startdate = Date_datetime - pd.DateOffset(years = 9)
    
    # Set date range for dekads
    Dates_dek = L3_Food_Security.Calc_Dekads_range(datetime.datetime.strftime(Startdate,"%Y-%m-%d"), datetime.datetime.strftime(Date_datetime,"%Y-%m-%d"))

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

    # Create output folder for Climate_Smart
    output_folder_Climate_Smart = os.path.join(output_folder_L3, "Climate_Smart")
    if not os.path.exists(output_folder_Climate_Smart):
        os.makedirs(output_folder_Climate_Smart)
        
    # Define output files
    filename_out_carbon_rz_crop = os.path.join(output_folder_Climate_Smart, "Carbon_Root_Zone_Cropland", "Carbon_Root_Zone_Cropland_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_carbon_rz_pasture = os.path.join(output_folder_Climate_Smart, "Carbon_Root_Zone_Pasture", "Carbon_Root_Zone_Pasture_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_carbon_seq_crop = os.path.join(output_folder_Climate_Smart, "Carbon_Sequestration_Cropland", "Carbon_Sequestration_Cropland_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_carbon_seq_pasture = os.path.join(output_folder_Climate_Smart, "Carbon_Sequestration_Pasture", "Carbon_Sequestration_Pasture_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_climatic_cooling = os.path.join(output_folder_Climate_Smart, "Climatic_Cooling", "Climatic_Cooling_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_water_generation = os.path.join(output_folder_Climate_Smart, "Water_Generation", "Water_Generation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_soil_erodibility = os.path.join(output_folder_Climate_Smart, "Soil_Erodibility", "Soil_Erodibility_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_combating_soil_erosion = os.path.join(output_folder_Climate_Smart, "Combating_Soil_Erosion", "Combating_Soil_Erosion_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_sustaining_rainfall = os.path.join(output_folder_Climate_Smart, "Sustaining_Rainfall", "Sustaining_Rainfall_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_npp_change = os.path.join(output_folder_Climate_Smart, "NPP_Change_In_Time", "NPP_Change_In_Time_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    


    if not os.path.exists(filename_out_npp_change):
   
        # Get georeference
        dest_ex = gdal.Open(example_file)
        geo = dest_ex.GetGeoTransform()
        proj = dest_ex.GetProjection()
        
        # npp filenames
        npp_folder = os.path.join(input_folder_L1, "L2_NPP_D")
        npp_format = "L2_NPP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
        
        # define required filenames
        filesocssd2 = os.path.join(input_folder_L1, "SoilGrids", "Soil_Organic_Carbon_Stock", "SoilOrganicCarbonStock_sd2_SoilGrids_tonnes-ha-1.tif")
        filesocssd3 = os.path.join(input_folder_L1, "SoilGrids", "Soil_Organic_Carbon_Stock", "SoilOrganicCarbonStock_sd3_SoilGrids_tonnes-ha-1.tif")
        filesocssd4 = os.path.join(input_folder_L1, "SoilGrids", "Soil_Organic_Carbon_Stock", "SoilOrganicCarbonStock_sd4_SoilGrids_tonnes-ha-1.tif")
        fileph10sl1 = os.path.join(input_folder_L1, "SoilGrids", "PH10", "SoilPH_sl1_SoilGrids_KCi10.tif")
        filesoccsl1 = os.path.join(input_folder_L1, "SoilGrids", "Soil_Organic_Carbon_Content", "SoilOrganicCarbonContent_sl1_SoilGrids_g_kg.tif")
        filesf = os.path.join(input_folder_L1, "SoilGrids", "Sand_Content", "SandContentMassFraction_sl6_SoilGrids_percentage.tif")
        filecf = os.path.join(input_folder_L1, "SoilGrids", "Clay_Content", "ClayContentMassFraction_sl6_SoilGrids_percentage.tif")
        filesif = os.path.join(input_folder_L1, "SoilGrids", "Silt_Content", "SiltContentMassFraction_sl6_SoilGrids_percentage.tif")
        filedem = os.path.join(input_folder_L1, "SRTM", "DEM", "DEM_SRTM_m_3s.tif")
        fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filenpp = os.path.join(input_folder_L1, "L2_NPP_D", "L2_NPP_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filew = os.path.join(input_folder_L1, "Weather_Data", "Model", "GLDAS", "daily", "wind_f_inst", "mean", "W_GLDAS-NOAH_m-s-1_daily_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filenr = os.path.join(output_folder_L2, "Net_Radiation", "Net_Radiation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        fileef = os.path.join(output_folder_L2, "Evaporative_Fraction", "Evaporative_Fraction_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filedp = os.path.join(output_folder_L2, "Deep_Percolation", "Deep_Percolation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filesrp = os.path.join(output_folder_L2, "Surface_Runoff_P", "Surface_Runoff_P_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filefvc = os.path.join(output_folder_L2, "Fractional_Vegetation_Cover", "Fractional_Vegetation_Cover_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))

        # Open required files
        destsocssd2 = RC.reproject_dataset_example(filesocssd2, example_file, 2)
        destsocssd3 = RC.reproject_dataset_example(filesocssd3, example_file, 2)
        destsocssd4 = RC.reproject_dataset_example(filesocssd4, example_file, 2)
        destph10sl1 = RC.reproject_dataset_example(fileph10sl1, example_file, 2)
        destsoccsl1 = RC.reproject_dataset_example(filesoccsl1, example_file, 2)
        destsf = RC.reproject_dataset_example(filesf, example_file, 2)
        destcf = RC.reproject_dataset_example(filecf, example_file, 2)
        destsif = RC.reproject_dataset_example(filesif, example_file, 2)
        destdem = RC.reproject_dataset_example(filedem, example_file, 2)        
        destet = RC.reproject_dataset_example(fileet, example_file, 2)
        destnpp = RC.reproject_dataset_example(filenpp, example_file, 2)
        destw = RC.reproject_dataset_example(filew, example_file, 2)
        destnr = gdal.Open(filenr)
        destef = gdal.Open(fileef)
        destdp = gdal.Open(filedp)
        destsrp = gdal.Open(filesrp)
        destfvc = gdal.Open(filefvc)
         
        # Open Arrays
        Soil_Organic_Carbon_Stock2 = destsocssd2.GetRasterBand(1).ReadAsArray()
        Soil_Organic_Carbon_Stock3 = destsocssd3.GetRasterBand(1).ReadAsArray()        
        Soil_Organic_Carbon_Stock4 = destsocssd4.GetRasterBand(1).ReadAsArray() 
        PH10 = destph10sl1.GetRasterBand(1).ReadAsArray()
        Soil_Organic_Carbon_Content1 = destsoccsl1.GetRasterBand(1).ReadAsArray()        
        Sand_Content = destsf.GetRasterBand(1).ReadAsArray()         
        Clay_Content = destcf.GetRasterBand(1).ReadAsArray()
        Silt_Content = destsif.GetRasterBand(1).ReadAsArray()        
        DEM = destdem.GetRasterBand(1).ReadAsArray()         
        ET = destet.GetRasterBand(1).ReadAsArray()
        NPP = destnpp.GetRasterBand(1).ReadAsArray()        
        Wind = destw.GetRasterBand(1).ReadAsArray()         
        Net_Radiation = destnr.GetRasterBand(1).ReadAsArray()
        Evaporative_Fraction = destef.GetRasterBand(1).ReadAsArray()        
        Deep_Percolation = destdp.GetRasterBand(1).ReadAsArray()         
        Surface_Runoff_P = destsrp.GetRasterBand(1).ReadAsArray()        
        Fractional_Vegetation_Cover = destfvc.GetRasterBand(1).ReadAsArray()         
        
        # Calculate Carbon Root Zone Cropland
        Carbon_Root_Zone_Cropland = (Soil_Organic_Carbon_Stock2 + Soil_Organic_Carbon_Stock3 + Soil_Organic_Carbon_Stock4) * 1000
        
        # Calculate Carbon Root Zone Pasture
        Carbon_Root_Zone_Pasture =(Soil_Organic_Carbon_Stock2 + Soil_Organic_Carbon_Stock3) * 1000
        
        # Calculate Carbon Sequestration Cropland
        Carbon_Sequestration_Cropland =10 * NPP * (1 - 4/(4 + 1)) * NOD * 0.3
        
        # Calculate Sequestration Pasture
        Carbon_Sequestration_Pasture =10 * NPP * (1 - 1.5/(1.5 + 1)) * NOD * 0.7
        
        # Calculate Climatic Cooling
        Climatic_Cooling =((0.7 * Net_Radiation - (1 - Evaporative_Fraction) * Net_Radiation) * (208/Wind))/(1.15 * 1004)
        
        # Calculate Water Generation
        Water_Generation =(Surface_Runoff_P + Deep_Percolation) * 10
        
        # Calculate Soil Erodibility
        Soil_Erodibility =(0.043 * PH10 + 0.062/(Soil_Organic_Carbon_Content1 * 10) + 0.0082 * Sand_Content - 0.0062 * Clay_Content) * Silt_Content/10
        
        # Calculate Combating Soil Erosion
        Combating_Soil_Erosion =50 * Water_Generation * Soil_Erodibility * 1 * DEM * Fractional_Vegetation_Cover * 0.5
        
        # Calculate Sustaining Rainfall
        Sustaining_Rainfall = 0.2 * ET * NOD
        
        # Calculate NPP Change In Time
        i = 0
        for Date in Dates_dek:
            input_file_npp = os.path.join(npp_folder, npp_format.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
      
            # Open Files
            destnpp = RC.reproject_dataset_example(input_file_npp, example_file, 2)       
            NPP_ONE = destnpp.GetRasterBand(1).ReadAsArray()
            if Date == Dates_dek[0]:
                NPP_ALL = np.ones([len(Dates_dek), NPP_ONE.shape[0], NPP_ONE.shape[1]])
            NPP_ALL[i,:,:] = NPP_ONE
            i += 1
        
        # Set time
        T = np.arange(i) 
        
        # Calculate trend
        trend_dekad = ((np.sum(np.where(np.isnan(NPP_ALL),0,1),axis = 0) * np.nansum(NPP_ALL * T[:,None,None], axis = 0)) - (np.nansum(NPP_ALL, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(NPP_ALL),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
        trend_year = trend_dekad * 36 
        NPP_Change_In_Time = trend_year / np.nanmean(NPP_ALL, axis = 0) * 100
            
        # Save result
        DC.Save_as_tiff(filename_out_carbon_rz_crop, Carbon_Root_Zone_Cropland, geo, proj)
        DC.Save_as_tiff(filename_out_carbon_rz_pasture, Carbon_Root_Zone_Pasture, geo, proj)
        DC.Save_as_tiff(filename_out_carbon_seq_crop, Carbon_Sequestration_Cropland, geo, proj)
        DC.Save_as_tiff(filename_out_carbon_seq_pasture, Carbon_Sequestration_Pasture, geo, proj)
        DC.Save_as_tiff(filename_out_climatic_cooling, Climatic_Cooling, geo, proj)
        DC.Save_as_tiff(filename_out_water_generation, Water_Generation, geo, proj)
        DC.Save_as_tiff(filename_out_soil_erodibility, Soil_Erodibility, geo, proj)
        DC.Save_as_tiff(filename_out_combating_soil_erosion, Combating_Soil_Erosion, geo, proj)
        DC.Save_as_tiff(filename_out_sustaining_rainfall, Sustaining_Rainfall, geo, proj)
        DC.Save_as_tiff(filename_out_npp_change, NPP_Change_In_Time, geo, proj)
        
    return()