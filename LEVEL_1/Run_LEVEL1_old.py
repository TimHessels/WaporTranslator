# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sat Sep 28 10:35:31 2019
"""
import os
import WaporTranslator.LEVEL_1 as L1

# inputs
Start_year_analyses = ""
End_year_analyses = ""
Input_shapefile = r""
Threshold_Mask = 20
output_folder = r""
API_WAPOR_KEY = ''


# Create output folder for LEVEL 1 data
output_folder_L1 = os.path.join(output_folder, "LEVEL_1")
if not os.path.exists(output_folder_L1):
    os.makedirs(output_folder_L1)

# Get latlim and lonlim and create a mask of the shapefile
dest_AOI_MASK, latlim, lonlim = L1.LEVEL_1_AOI.main(Input_shapefile)

# Download WAPOR data
L1.LEVEL_1_Download_WAPOR.main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim, API_WAPOR_KEY)

# Download ESACCI data
L1.LEVEL_1_Download_ESACCI.main(output_folder_L1, latlim, lonlim)

# Download SoilGrids data
L1.LEVEL_1_Download_SoilGrids.main(output_folder_L1, latlim, lonlim)

# Download SRTM data
L1.LEVEL_1_Download_SRTM.main(output_folder_L1, latlim, lonlim)

# Download GLDAS data
L1.LEVEL_1_Download_GLDAS.main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim)

# Download MODIS data
L1.LEVEL_1_Download_MODIS.main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim)

# Process MSGCCP data
L1.LEVEL_1_Process_MSGCCP.main(output_folder_L1, End_year_analyses, latlim, lonlim)

# Create Mask
L1.LEVEL_1_Create_Mask.main(output_folder_L1, dest_AOI_MASK, Threshold_Mask)

