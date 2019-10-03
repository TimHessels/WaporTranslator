# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sat Sep 28 13:16:31 2019
"""
import watertools

def main(output_folder_L1, latlim, lonlim):
    
    # Download sand content from SoilGrids
    watertools.Collect.SoilGrids.Sand_Content(output_folder_L1, latlim, lonlim, level = 'sl6')

    # Download silt content from SoilGrids
    watertools.Collect.SoilGrids.Silt_Content(output_folder_L1, latlim, lonlim, level = 'sl6')

    # Download clay content from SoilGrids
    watertools.Collect.SoilGrids.Clay_Content(output_folder_L1, latlim, lonlim, level = 'sl6')

    # Download bulk density from SoilGrids    
    watertools.Collect.SoilGrids.Bulk_Density(output_folder_L1, latlim, lonlim, level = 'sl6')    

    # Download organic carbon content from SoilGrids        
    watertools.Collect.SoilGrids.Organic_Carbon_Content(output_folder_L1, latlim, lonlim, level = 'sl1')     

    # Download organic carbon stock from SoilGrid for 6 different layers 
    watertools.Collect.SoilGrids.Organic_Carbon_Stock(output_folder_L1, latlim, lonlim, level = 'sd1')  
    watertools.Collect.SoilGrids.Organic_Carbon_Stock(output_folder_L1, latlim, lonlim, level = 'sd2')  
    watertools.Collect.SoilGrids.Organic_Carbon_Stock(output_folder_L1, latlim, lonlim, level = 'sd3')  
    watertools.Collect.SoilGrids.Organic_Carbon_Stock(output_folder_L1, latlim, lonlim, level = 'sd4')  
    watertools.Collect.SoilGrids.Organic_Carbon_Stock(output_folder_L1, latlim, lonlim, level = 'sd5')       
    watertools.Collect.SoilGrids.Organic_Carbon_Stock(output_folder_L1, latlim, lonlim, level = 'sd6')     
     
    # Download pH from SoilGrids for the top layer
    watertools.Collect.SoilGrids.Soil_pH(output_folder_L1, latlim, lonlim, level = 'sl1')
        
    return()