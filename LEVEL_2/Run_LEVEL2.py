# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 17:03:41 2019
"""
import os
import WaporTranslator.LEVEL_2 as L2

# inputs
Date = "2018-05-01"
output_folder = r"G:\Project_MetaMeta"

# Create output folder for LEVEL 2 data
output_folder_L2 = os.path.join(output_folder, "LEVEL_2")
if not os.path.exists(output_folder_L2):
    os.makedirs(output_folder_L2)

# Set example file
Year = Date.split("-")[0]    
example_file = os.path.join(output_folder, "LEVEL_1", "L2_LCC_A", "L2_LCC_A_WAPOR_YEAR_%s.01.01.tif" %Year)

# Calculate LAI
L2.LEVEL_2_Calc_Vegetation.Calc_LAI(output_folder_L2, Date, example_file)

# Calculate Root Depth
L2.LEVEL_2_Calc_Vegetation.Calc_Root_Depth(output_folder_L2, Date)

# Calculate Fractional Vegetation Cover
L2.LEVEL_2_Calc_Vegetation.Calc_Fractional_Vegt_Cover(output_folder_L2, Date)

# Calculate Crop coefficient of dry soil
L2.LEVEL_2_Calc_Vegetation.Calc_Crop_Coeff_Dry_Soil(output_folder_L2, Date)

# Calculate Land Surface Emissivity
L2.LEVEL_2_Calc_Radiation.Calc_Land_Surface_Emissivity(output_folder_L2, Date)

# Calculate Net Radiation
L2.LEVEL_2_Calc_Radiation.Calc_Net_Radiation(output_folder_L2, Date, example_file)

# Calculate Evaporative Fraction
L2.LEVEL_2_Calc_Radiation.Calc_Evaporative_Fraction(output_folder_L2, Date, example_file)

# Calculate Theta Saturated Subsoil
L2.LEVEL_2_Calc_Soil.Calc_Theta_Sat_Subsoil(output_folder_L2, example_file)

# Calculate Theta Field Capacity Subsoil
L2.LEVEL_2_Calc_Soil.Calc_Theta_FC_Subsoil(output_folder_L2)
        
# Calculate Theta Wilting Point Subsoil
L2.LEVEL_2_Calc_Soil.Calc_Theta_WP_Subsoil(output_folder_L2)
        
# Calculate Soil Water Holding Capacity
L2.LEVEL_2_Calc_Soil.Calc_Soil_Water_Holding_Capacity(output_folder_L2)
        
# Calculate Soil Moisture
L2.LEVEL_2_Calc_Soil.Calc_Soil_Moisture(output_folder_L2, Date) 

# Calculate Crop Water Requirements - ETpot
L2.LEVEL_2_Calc_Crop.Calc_Crop_Water_Requirement(output_folder_L2, Date, example_file) 
 
# Calculate Critical Soil Moisture
L2.LEVEL_2_Calc_Soil.Calc_Critical_Soil_Moisture(output_folder_L2, Date)
        
# Calculate Soil Moisture at start period
L2.LEVEL_2_Calc_Soil.Calc_Soil_Moisture_Start_End_Period(output_folder_L2, Date)
        
# Calculate soil water storage change        
L2.LEVEL_2_Calc_Soil.Calc_Soil_Water_Storage_Change(output_folder_L2, Date)
          
# Calculate net supply, net drainage
L2.LEVEL_2_Calc_Groundwater.Calc_Net_Supply_Drainage(output_folder_L2, Date, example_file)
       
# Calculate Deep Percolation
L2.LEVEL_2_Calc_Groundwater.Calc_Deep_Percolation(output_folder_L2, Date)

# Calculate Storage Coefficient for surface runoff S
L2.LEVEL_2_Calc_Groundwater.Calc_Storage_Coeff_Surface_Runoff(output_folder_L2, Date, example_file)

# Calculate Surface Runoff P
L2.LEVEL_2_Calc_Surfacewater.Calc_Surface_Runoff_P(output_folder_L2, Date, example_file)

# Calculate Surface Runoff Coefficient R/P
L2.LEVEL_2_Calc_Surfacewater.Calc_Surface_Runoff_Coefficient(output_folder_L2, Date, example_file)

# Calculate Crop Coefficient Updated
L2.LEVEL_2_Calc_Crop.Calc_Crop_Coef_Update(output_folder_L2, Date, example_file) 

# Calculate 10 year Mean Net Radiation, per Pixel

# Calculate 10 year mean evaporative fraction

# Calculate 10 yr mean soil moisture

# Calculate Phenelogy








