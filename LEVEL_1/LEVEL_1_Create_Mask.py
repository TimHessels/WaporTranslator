# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:56:57 2019

@author: timhe
"""

import os
import glob
import numpy as np

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

def main(output_folder_L1, dest_AOI_MASK, Threshold_Mask):
    
    # select input folder
    input_folder_LCC = os.path.join(output_folder_L1, "L2_LCC_A")
    
    # Set input folder as working directory
    os.chdir(input_folder_LCC)
    
    # Find file for extend
    re = glob.glob("L2_LCC_A_*.tif")[0]
    
    # Open file
    Filename_Example = os.path.join(input_folder_LCC, re)
    
    # Open info array
    dest_shp = RC.reproject_dataset_example(dest_AOI_MASK, Filename_Example, 4)
    geo = dest_shp.GetGeoTransform()
    proj = dest_shp.GetProjection()
    
    # Array mask
    Mask_with_Edge = dest_shp.GetRasterBand(1).ReadAsArray()
    
    if Threshold_Mask == "OFF":
        Threshold_Mask = 20
    
    # Create End Mask
    Mask = np.where(Mask_with_Edge<Threshold_Mask/100., np.nan, 1)
    
    # output file
    output_file = os.path.join(output_folder_L1, "MASK", "MASK.tif")
    DC.Save_as_tiff(output_file, Mask, geo, proj)
    
    return()