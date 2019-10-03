# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:06:20 2019
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


def Calc_Irrigation(output_folder_L2, Date, example_file):

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

    # Create output folder for Irrigation
    output_folder_Irrigation = os.path.join(output_folder_L3, "Irrigation")
    if not os.path.exists(output_folder_Irrigation):
        os.makedirs(output_folder_Irrigation)
        
    # Define output files
    filename_out_irrigation_water_requirement = os.path.join(output_folder_Irrigation, "Irrigation_Water_Requirement", "Irrigation_Water_Requirement_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_gross_irrigation_water_supply = os.path.join(output_folder_Irrigation, "Gross_Irrigation_Water_Supply", "Gross_Irrigation_Water_Supply_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_adequacy_relative_water_supply = os.path.join(output_folder_Irrigation, "Adequacy_Relative_Water_Supply", "Adequacy_Relative_Water_Supply_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_adequacy_relative_irrigation_water_supply = os.path.join(output_folder_Irrigation, "Adequacy_Relative_Irrigation_Water_Supply", "Adequacy_Relative_Irrigation_Water_Supply_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_etblue = os.path.join(output_folder_Irrigation, "ETblue", "ETblue_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_non_consumptive_use_due_to_irrigation = os.path.join(output_folder_Irrigation, "Non_Consumptive_Use_Due_To_Irrigation", "Non_Consumptive_Use_Due_To_Irrigation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_onfarm_irrigation_efficiency = os.path.join(output_folder_Irrigation, "Onfarm_Irrigation_Efficiency", "Onfarm_Irrigation_Efficiency_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_degree_of_over_irrigation = os.path.join(output_folder_Irrigation, "Degree_Of_Over_Irrigation", "Degree_Of_Over_Irrigation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_adequacy_degree_of_under_irrigation = os.path.join(output_folder_Irrigation, "Adequacy_Degree_Of_Under_Irrigation", "Adequacy_Degree_Of_Under_Irrigation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_adequacy_crop_water_deficit = os.path.join(output_folder_Irrigation, "Adequacy_Crop_Water_Deficit", "Adequacy_Crop_Water_Deficit_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_target_et = os.path.join(output_folder_Irrigation, "Target_ET", "Target_ET_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_et_savings = os.path.join(output_folder_Irrigation, "ET_Savings", "ET_Savings_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_long_term_etmean = os.path.join(output_folder_Irrigation, "Long_Term_ETmean", "Long_Term_ETmean_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_etgap = os.path.join(output_folder_Irrigation, "ETgap", "ETgap_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_feasible_water_conservation = os.path.join(output_folder_Irrigation, "Feasible_Water_Conservation", "Feasible_Water_Conservation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_non_beneficial_water_losses = os.path.join(output_folder_Irrigation, "Non_Beneficial_Water_Losses", "Non_Beneficial_Water_Losses_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_equity = os.path.join(output_folder_Irrigation, "Equity", "Equity_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    
    filename_out_reliability = os.path.join(output_folder_Irrigation, "Reliability", "Reliability_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))    


    if not os.path.exists(filename_out_reliability):
   
        # Get georeference
        dest_ex = gdal.Open(example_file)
        geo = dest_ex.GetGeoTransform()
        proj = dest_ex.GetProjection()
        
        # define required filenames
        filep = os.path.join(input_folder_L1, "L1_PCP_D", "L1_PCP_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filee = os.path.join(input_folder_L1, "L2_E_D", "L2_E_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filecwr = os.path.join(output_folder_L2, "Crop_Water_Requirement", "Crop_Water_Requirement_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filensd = os.path.join(output_folder_L2, "Net_Supply_Drainage", "Net_Supply_Drainage_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filedp = os.path.join(output_folder_L2, "Deep_Percolation", "Deep_Percolation_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filesrp = os.path.join(output_folder_L2, "Surface_Runoff_P", "Surface_Runoff_P_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filesrc = os.path.join(output_folder_L2, "Surface_Runoff_Coefficient", "Surface_Runoff_Coefficient_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filesm = os.path.join(output_folder_L2, "Soil_Moisture", "Soil_Moisture_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filecsm = os.path.join(output_folder_L2, "Critical_Soil_Moisture", "Critical_Soil_Moisture_%d.%02d.%02d.tif" %(Date_datetime.year, Date_datetime.month, Date_datetime.day))
        filetfc = os.path.join(output_folder_L2, "Theta_FC_Subsoil", "Theta_FC_Subsoil.tif")

        # Open required files
        destp = RC.reproject_dataset_example(filep, example_file, 2)
        destet = RC.reproject_dataset_example(fileet, example_file, 2)
        deste = RC.reproject_dataset_example(filee, example_file, 2)
        destcwr = gdal.Open(filecwr)
        destnsd = gdal.Open(filensd)
        destdp = gdal.Open(filedp)
        destsrp = gdal.Open(filesrp)
        destsrc = gdal.Open(filesrc)
        destsm = gdal.Open(filesm)
        destcsm = gdal.Open(filecsm)
        desttfc = gdal.Open(filetfc)
         
        # Open Arrays
        P = destp.GetRasterBand(1).ReadAsArray()
        ET = destet.GetRasterBand(1).ReadAsArray()        
        E = deste.GetRasterBand(1).ReadAsArray() 
        Crop_Water_Requirement = destcwr.GetRasterBand(1).ReadAsArray()
        Net_Supply_Drainage = destnsd.GetRasterBand(1).ReadAsArray()        
        Deep_Percolation = destdp.GetRasterBand(1).ReadAsArray()         
        Surface_Runoff_P = destsrp.GetRasterBand(1).ReadAsArray()
        Surface_Runoff_Coefficient = destsrc.GetRasterBand(1).ReadAsArray()        
        Soil_Moisture = destsm.GetRasterBand(1).ReadAsArray()         
        Critical_Soil_Moisture = destcsm.GetRasterBand(1).ReadAsArray()
        Theta_FC_Subsoil = desttfc.GetRasterBand(1).ReadAsArray()        

        # Calculate Irrigation Water Requirement
        Irrigation_Water_Requirement = (Crop_Water_Requirement - 0.7 * P * NOD)/(0.65)
        
        # Calculate Gross Irrigation Water Supply
        Gross_Irrigation_Water_Supply = np.maximum(0, (Net_Supply_Drainage + Deep_Percolation + Surface_Runoff_P) * (1 + Surface_Runoff_Coefficient))
        
        # Calculate Adequacy Relative Water Supply
        Adequacy_Relative_Water_Supply = (Gross_Irrigation_Water_Supply + P * NOD)/Crop_Water_Requirement
        
        # Calculate Adequacy Relative Irrigation Water Suppy
        Adequacy_Relative_Irrigation_Water_Supply = Gross_Irrigation_Water_Supply/Irrigation_Water_Requirement
        
        # Calculate ETblue
        ETblue = np.where(ET > 0.7 * P, NOD * (ET - 0.7 * P), 0)
        
        # Calculate Non Consumptive Use Due To Irrigation
        Non_Consumptive_Use_Due_To_Irrigation = np.maximum(0, Gross_Irrigation_Water_Supply - ETblue)
        
        # Calculate Onfarm Irrigation Efficiency
        Onfarm_Irrigation_Efficiency = ETblue/Gross_Irrigation_Water_Supply * 100
        
        # Calculate Degree Of Over Irrigation
        Degree_Of_Over_Irrigation = Soil_Moisture/Theta_FC_Subsoil
        
        # Calculate Adequacy Degree Of Under Irrigation
        Adequacy_Degree_Of_Under_Irrigation = Soil_Moisture/Critical_Soil_Moisture
        
        # Calculate Adequacy Crop Water Deficit
        Adequacy_Crop_Water_Deficit = Crop_Water_Requirement - ET * NOD
        
        # Calculate Target Evapotranspiration
        Target_ET = I8 * NOD #!!!
        
        # Calculate Evapotranspiration Savings
        ET_Savings = np.minimum(0, Target_ET - ET * NOD)
        
        # Calculate Long Term Average Evapotranspiration
        Long_Term_ETmean = H8 * NOD #!!!
        
        # Calculate Gap in Evapotranspiration
        ETgap = np.minimum(0, Long_Term_ETmean - ET * NOD)
        
        # Calculate Feasible Water Conservation
        Feasible_Water_Conservation =(ET_Savings + ETgap)/2
        
        # Calculate Non Beneficial Water Losses
        Non_Beneficial_Water_Losses = E * NOD
        
        # Calculate Equity
        Equity = 2#!!!
        
        # Calculate Reliability
        Reliability = 2#!!!  
            
        # Save result
        DC.Save_as_tiff(filename_out_irrigation_water_requirement, Irrigation_Water_Requirement, geo, proj)
        DC.Save_as_tiff(filename_out_gross_irrigation_water_supply, Gross_Irrigation_Water_Supply, geo, proj)
        DC.Save_as_tiff(filename_out_adequacy_relative_water_supply, Adequacy_Relative_Water_Supply, geo, proj)
        DC.Save_as_tiff(filename_out_adequacy_relative_irrigation_water_supply, Adequacy_Relative_Irrigation_Water_Supply, geo, proj)
        DC.Save_as_tiff(filename_out_etblue, ETblue, geo, proj)
        DC.Save_as_tiff(filename_out_non_consumptive_use_due_to_irrigation, Non_Consumptive_Use_Due_To_Irrigation, geo, proj)
        DC.Save_as_tiff(filename_out_onfarm_irrigation_efficiency, Onfarm_Irrigation_Efficiency, geo, proj)
        DC.Save_as_tiff(filename_out_degree_of_over_irrigation, Degree_Of_Over_Irrigation, geo, proj)
        DC.Save_as_tiff(filename_out_adequacy_degree_of_under_irrigation, Adequacy_Degree_Of_Under_Irrigation, geo, proj)
        DC.Save_as_tiff(filename_out_adequacy_crop_water_deficit, Adequacy_Crop_Water_Deficit, geo, proj)
        DC.Save_as_tiff(filename_out_target_et, Target_ET, geo, proj)
        DC.Save_as_tiff(filename_out_et_savings, ET_Savings, geo, proj)
        DC.Save_as_tiff(filename_out_long_term_etmean, Long_Term_ETmean, geo, proj)
        DC.Save_as_tiff(filename_out_etgap, ETgap, geo, proj)
        DC.Save_as_tiff(filename_out_feasible_water_conservation, Feasible_Water_Conservation, geo, proj)
        DC.Save_as_tiff(filename_out_non_beneficial_water_losses, Non_Beneficial_Water_Losses, geo, proj)
        DC.Save_as_tiff(filename_out_equity, Equity, geo, proj)
        DC.Save_as_tiff(filename_out_reliability, Reliability, geo, proj)

        

        
    return()