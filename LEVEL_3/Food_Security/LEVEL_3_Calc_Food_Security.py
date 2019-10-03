# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 13:25:22 2019
"""
import gdal
import os
import datetime
import numpy as np
import pandas as pd

import watertools.General.data_conversions as DC
import watertools.General.raster_conversions as RC

# Date
Startdate = "2011-01-01"
Enddate = "2018-05-01"

# Static maps
LU_LU_filename = r"G:\Project_MetaMeta\LEVEL_2\Phenelogy\CropClass\LU_CropType_2018.tif" # irrigated non irrigated and pasture
LU_Crop_Type_filename = r"G:\Project_MetaMeta\LEVEL_2\Phenelogy\CropClass\LU_CropSeason_2018.tif" # Single Double Perenial
Clay_filename = r"G:\Project_MetaMeta\LEVEL_1\SoilGrids\Clay_Content\ClayContentMassFraction_sl6_SoilGrids_percentage.tif"
Silt_filename = r"G:\Project_MetaMeta\LEVEL_1\SoilGrids\Silt_Content\SiltContentMassFraction_sl6_SoilGrids_percentage.tif"
Sand_filename = r"G:\Project_MetaMeta\LEVEL_1\SoilGrids\Sand_Content\SandContentMassFraction_sl6_SoilGrids_percentage.tif"
DEM_filename = r"G:\Project_MetaMeta\LEVEL_1\SRTM\DEM\DEM_SRTM_m_3s.tif"

# Dynamic map
ET0_folder = r"G:\Project_MetaMeta\LEVEL_1\L1_RET_D"
P_folder = r"G:\Project_MetaMeta\LEVEL_1\L1_PCP_D"

# formats
ET0_format = "L1_RET_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
P_format = "L1_PCP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"

# Set date range for dekads
Dates_dek = Calc_Dekads_range(Startdate, Enddate)

# Calculate Aridity Array
Aridity = Calc_Aridity(Dates_dek, ET0_folder, ET0_format, P_folder, P_format, LU_LU_filename)

# Calculate Slope Array
Slope, DEM = Calc_Slope(DEM_filename, LU_LU_filename)

# Calculate Soil Layers Array
Clay, Silt, Sand = Calc_Soil(Clay_filename, Silt_filename, Sand_filename, LU_LU_filename)

# Calculate Crop Season and LU
Season, LU = Calc_Crops(LU_Crop_Type_filename, LU_LU_filename)

# Created AEZ numbers
AEZ = Calc_AEZ(Aridity, Slope, DEM, Clay, Silt, Sand, Season, LU)



















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

def Calc_Aridity(Dates_dek, ET0_folder, ET0_format, P_folder, P_format, example_file):

    # Calculate Aridity long term
    for Date in Dates_dek:
        
        input_file_ET0 = os.path.join(ET0_folder, ET0_format.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
        input_file_P = os.path.join(P_folder, P_format.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
    
        # Open Files
        destet0 = gdal.Open(input_file_ET0)
        destp = gdal.Open(input_file_P)
        
        if Date == Dates_dek[0]:
            
            # Get geo ET0
            geo_ET0 = destet0.GetGeoTransform()
            proj_ET0 = destet0.GetProjection()
            ET0_one = destet0.GetRasterBand(1).ReadAsArray()
            ET0_one = np.float_(ET0_one)
            ET0_one[ET0_one<0] = np.nan
            ET0_one[ET0_one == 255.] = np.nan
            ET0 = RC.gap_filling(ET0_one, np.nan)
            
            # Get geo P
            geo_P = destp.GetGeoTransform()
            proj_P = destp.GetProjection()
            P_one = destp.GetRasterBand(1).ReadAsArray()
            P_one = np.float_(P_one)
            P_one[P_one<0] = np.nan
            P_one[P_one == 255.] = np.nan
            P = RC.gap_filling(P_one, np.nan)
    
        else:
            ET0_one = destet0.GetRasterBand(1).ReadAsArray()
            ET0_one = np.float_(ET0_one)
            ET0_one[ET0_one<0] = np.nan
            ET0_one[ET0_one == 255.] = np.nan
            ET0_one = RC.gap_filling(ET0_one, np.nan)
            ET0 += ET0_one
            
            P_one = destp.GetRasterBand(1).ReadAsArray()
            P_one = np.float_(P_one)
            P_one[P_one<0] = np.nan
            P_one[P_one == 255.] = np.nan
            P_one = RC.gap_filling(P_one, np.nan)
            P += P_one
    
    # Calculate aridity and reproject to LU map
    destsumet0 = DC.Save_as_MEM(ET0, geo_ET0, proj_ET0)  
    destsump = DC.Save_as_MEM(P, geo_P, proj_P)     
    
    destsumet0_rep = RC.reproject_dataset_example(destsumet0, example_file, 2)   
    destsumep_rep = RC.reproject_dataset_example(destsump, example_file, 2)   
    
    # Open Arrays
    ET0_rep = destsumet0_rep.GetRasterBand(1).ReadAsArray()
    P_rep = destsumep_rep.GetRasterBand(1).ReadAsArray()        
    Aridity_index = ET0_rep / P_rep
    
    return(Aridity_index)

def Calc_Slope(DEM_filename, LU_LU_filename):
    
    rad2deg = 180.0 / np.pi  # Factor to transform from rad to degree
    pixel_spacing = 100     # LVL 2 of WAPOR is 100m resolution
    
    dest = RC.reproject_dataset_example(DEM_filename, LU_LU_filename, 2)
    DEM = dest.GetRasterBand(1).ReadAsArray()
    
    # Calculate slope
    x, y = np.gradient(DEM, pixel_spacing, pixel_spacing)
    hypotenuse_array = np.hypot(x,y)
    Slope = np.arctan(hypotenuse_array) * rad2deg

    return(Slope, DEM)

def Calc_Soil(Clay_filename, Silt_filename, Sand_filename, example_file):
    
    destclay = RC.reproject_dataset_example(Clay_filename, example_file, 2)
    destsilt = RC.reproject_dataset_example(Silt_filename, example_file, 2)
    destsand = RC.reproject_dataset_example(Sand_filename, example_file, 2)
    
    Clay = destclay.GetRasterBand(1).ReadAsArray()
    Silt = destsilt.GetRasterBand(1).ReadAsArray()    
    Sand = destsand.GetRasterBand(1).ReadAsArray()    
    return(Clay, Silt, Sand)
 
def Calc_Crops(LU_Crop_Type_filename, LU_LU_filename):

    destseason = RC.reproject_dataset_example(LU_Crop_Type_filename, LU_LU_filename, 2)
    destlu = gdal.Open(LU_LU_filename)

    Season = destseason.GetRasterBand(1).ReadAsArray()
    LU = destlu.GetRasterBand(1).ReadAsArray() 
    
    Season_Type = np.ones(Season.shape) * np.nan
    
    # Set irrigation mask
    Irrigation = np.where(LU == 42, 2, 1)

    # Create Season Type map
    Season_Type = np.where()

    return(Season_Type, Irrigation)

def Calc_AEZ(Aridity, Slope, DEM, Clay, Silt, Sand, Season, LU):
    
    # Create Aridity AEZ
    dict_ipi = Performances()
    
     for Ind in list_Ind:
                csv_score = np.nan
                    
                for keys in dict_ipi[Ind].keys():
                    
                    if len(str(Ind)) == 2:
                        ind_nmr = int(str(Ind)[1:]) + 10    
                    else:
                        ind_nmr = int(str(Ind)[2:])
                    if len(Array_csv.shape)>1:
                        csv_values = Array_csv[:, ind_nmr]
                    else:
                        csv_values = Array_csv[ind_nmr]
                    
           
    
    
    return(AEZ)


    
def AEZ_Conversions(version = '1.0'):
    
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
                
    'Irrigated':    {1: 1,
                    2: 2},         
                            
    'Crop':    {1: 1,
               2: 2,
               3: 3,
               4: 4},    
                     
                     
                     
    AEZ_Conversions =dict()
    AEZ_Conversions['1.0'] = AEZ_V1

    return AEZ_Conversions[version]
    
    
    
    
Number = tiggesc


