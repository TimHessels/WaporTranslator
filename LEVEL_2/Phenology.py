# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Wed Sep 18 17:10:42 2019
"""

import os
import gdal
import datetime
import numpy as np
import pandas as pd
import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

input_folder = r"G:\Project_MetaMeta\Input_Data\L2_T_D"
input_format = "L2_T_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"

Output_Folder_L2 = r"G:\Project_MetaMeta\LEVEL_2"

Startdate = "2011-01-01"
Enddate = "2017-12-31"

Years = pd.date_range(Startdate, Enddate, freq = "AS")

# WAPOR LU format
input_file_LU_WAPOR = r"G:\Project_MetaMeta\Input_Data\L2_LCC_A\L2_LCC_A_WAPOR_YEAR_{yyyy}.01.01.tif"

# Open ESACCI
input_file_LU_ESACCI = r"G:\Project_MetaMeta\LU\product\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7.tif"

# Create output folder
if not os.path.exists(Output_Folder_L2):
    os.makedirs(Output_Folder_L2)

# open dictionary WAPOR
WAPOR_Conversions_dict = WAPOR_Conversions()
# open dictionary ESACCI
ESACCI_Conversions_dict = ESACCI_Conversions()

# Delete Array if it already exists
if "Array_T_Years" in locals():
    del Array_T_Years

for Year in Years:
    
    Year_nmbr = Year.year
    
    # Find dates dekades for one year
    Startdate_Year = "%d-01-01" %Year_nmbr
    Enddate_Year = "%d-12-31" %Year_nmbr

    # Define dates
    Dates = pd.date_range(Startdate_Year, Enddate_Year, freq = "MS")
    Dates_end = []
    
    # Define decade dates
    for Date in Dates:
        Dates_end.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 1)))
        Dates_end.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 11)))
        Dates_end.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 21)))
    
    # Delete Array if it already exists
    if "Array_T_Year" in locals():
        del Array_T_Year
      
    # Loop over dates    
    for Date in Dates_end:
        
        filename_T_in = os.path.join(input_folder, input_format.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
        
        if "Array_T_Year" not in locals():
            dest = gdal.Open(filename_T_in)
            filename_ex = filename_T_in
            Array_T_Year = dest.GetRasterBand(1).ReadAsArray()
            
        else:
            
            dest = gdal.Open(filename_T_in)
            Array_T = dest.GetRasterBand(1).ReadAsArray()    
            Array_T_Year = np.dstack((Array_T_Year, Array_T))
    
    # Open LU map
    dest_LU_WAPOR = RC.reproject_dataset_example(input_file_LU_WAPOR.format(yyyy = Year_nmbr), filename_T_in)
    LU_WAPOR = dest_LU_WAPOR.GetRasterBand(1).ReadAsArray()
    geo = dest_LU_WAPOR.GetGeoTransform()
    proj = dest_LU_WAPOR.GetProjection()    
     
    dest_LU_ESACCI = RC.reproject_dataset_example(input_file_LU_ESACCI, filename_T_in)
    LU_ESACCI = dest_LU_ESACCI.GetRasterBand(1).ReadAsArray()
       
    # Create LUmap
    LU_Map_WAPOR = np.ones(LU_WAPOR.shape) * np.nan
    LU_Map_ESACCI = np.ones(LU_WAPOR.shape) * np.nan
    
    for number in WAPOR_Conversions_dict.items():
    
        LU_Map_WAPOR = np.where(LU_WAPOR == number[0], number[1], LU_Map_WAPOR)
        
    for number in ESACCI_Conversions_dict.items():
    
        LU_Map_ESACCI = np.where(LU_ESACCI == number[0], number[1], LU_Map_ESACCI)      
    
    # Combine LU maps
    # 1 = rainfed, 2 = irrigated, 3 = Pasture
    LU_END = np.where(np.logical_and(LU_Map_WAPOR == 1, LU_Map_ESACCI == 1), 1, np.nan)    
    LU_END = np.where(LU_Map_WAPOR > 1, LU_Map_WAPOR, LU_END)
        
    Phenology_pixels_year = LU_END[np.logical_or(LU_END==1, LU_END==2)]    
    
    Array_T_Year = np.float_(Array_T_Year)
    Array_T_Year[Array_T_Year == 255] = np.nan
    Array_T_Year[np.logical_and(LU_END!=1, LU_END!=2), :] = np.nan
    
    if "Array_T_Years" not in locals():
        Array_T_Years = Array_T_Year
        
    else:
        Array_T_Years = np.dstack((Array_T_Years, Array_T_Year))

Seasons_dict_start = dict()
Seasons_dict_end = dict()
Seasons_dict_per_start = dict()
Seasons_dict_per_end = dict()

pixel = 0

for i in range(0, Array_T_Years.shape[0]):
    for j in range(0, Array_T_Years.shape[1]):    
      
      Ts = Array_T_Years[i, j, :]   
      if not np.isnan(np.nanmean(Ts)): 
       
          Start, End, Start_Per, End_Per = Calc_Season(Ts)

          Seasons_dict_start[pixel] = Start
          Seasons_dict_end[pixel] = End
          Seasons_dict_per_start[pixel] = Start_Per
          Seasons_dict_per_end[pixel] = End_Per
        
      print(pixel)


      pixel += 1

for Year in Years:
    
    year_nmbr = Year.year
    
    # Create empty output maps
    Start_Map_S1 = np.ones(LU_END.shape) * np.nan
    End_Map_S1 = np.ones(LU_END.shape) * np.nan
    Start_Map_S2 = np.ones(LU_END.shape) * np.nan
    End_Map_S2 = np.ones(LU_END.shape) * np.nan
    Per_Map_S2 = np.ones(LU_END.shape) * np.nan
    LU_Crop_Map = np.ones(LU_END.shape) * np.nan
    
    # create IDs for the Array to reconstruct the array from the dict later
    y,x = np.indices((LU_END.shape[0], LU_END.shape[1]))
    ID_Matrix = np.int32(np.ravel_multi_index(np.vstack((y.ravel(),x.ravel())),(LU_END.shape[0], LU_END.shape[1]),mode='clip').reshape(x.shape))
    
    # Select begin and end of the year for the array
    Year_DOY_Start = (year_nmbr - Years[0].year) * 36
    Year_DOY_End = Year_DOY_Start + 36
 
    # Create Perenial map
    for dict_in_per in Seasons_dict_per_start.items():        
      
        Starts_per = dict_in_per[1]
        Ends_per = Seasons_dict_per_end[dict_in_per[0]]
        
        for Start_per in Starts_per:
            
            End_per = Ends_per[np.argwhere(Start_per==Starts_per)][0][0]
            
            if np.logical_and(Start_per <= Year_DOY_End, End_per >= Year_DOY_Start):
                
                Per_Map_S2[dict_in_per[0]== ID_Matrix] = 1
                LU_Crop_Map[dict_in_per[0]== ID_Matrix] = 3

    # Create S1 and S2 maps
    for dict_in in Seasons_dict_start.items():   
        
        # Check if pixel is not perenial
        if Per_Map_S2[dict_in[0] == ID_Matrix] != 1:
         
            Starts = dict_in[1]
            
            if len(Starts)>0:
                Starts = Starts[np.logical_and(Starts<Year_DOY_End, Starts>=Year_DOY_Start)]
                
                # If it is a single season
                if len(Starts) > 0:
                   # Get the end value for this start period 
                   End = Seasons_dict_end[dict_in[0]][np.argwhere(Starts[0] == dict_in[1])][0][0]
                   
                   # Fill in array
                   Start_Map_S1[dict_in[0]== ID_Matrix] = Starts[0] - Year_DOY_Start
                   End_Map_S1[dict_in[0]== ID_Matrix] = End - Year_DOY_Start
                   LU_Crop_Map[dict_in[0]== ID_Matrix] = 1
                   
                # If it is a double season               
                if len(Starts) == 2:    
                   # Get the end value for this start period   
                   End = Seasons_dict_end[dict_in[0]][np.argwhere(Starts[1] == dict_in[1])][0][0]
                   
                   # Fill in array
                   Start_Map_S2[dict_in[0]== ID_Matrix] = Starts[1] - Year_DOY_Start      
                   End_Map_S2[dict_in[0]== ID_Matrix] = End - Year_DOY_Start
                   LU_Crop_Map[dict_in[0]== ID_Matrix] = 2
                   
    # Save files
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology_Start_S1_%s.tif" %year_nmbr), Start_Map_S1, geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology_Start_S2_%s.tif" %year_nmbr), Start_Map_S2, geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology_End_S1_%s.tif" %year_nmbr), End_Map_S1, geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology_End_S2_%s.tif" %year_nmbr), End_Map_S2, geo, proj)       
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology_Per_%s.tif" %year_nmbr), Per_Map_S2, geo, proj)  
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "LU_CropClass_%s.tif" %year_nmbr), LU_Crop_Map, geo, proj)      










def Calc_Season(Ts):
    
    Ts_MW = (Ts + np.append(Ts[1:], Ts[0]) + np.append(Ts[-1], Ts[:-1]) + np.append(Ts[-2:], Ts[:-2]) + np.append(Ts[2:], Ts[0:2]))/5
    
    Minimum_T = np.nanmin(Ts_MW)
    Maximum_T = np.nanmax(Ts_MW)
    
    Threshold_LVL = 0.4
    Threshold_LVL_min = 10
    
    if Maximum_T - Minimum_T > Threshold_LVL_min:
        Threshold_LVL_min = Maximum_T - Minimum_T
    
    Maximum_Threshold = np.minimum(Threshold_LVL * (Maximum_T + Minimum_T) / 2 + Minimum_T, Threshold_LVL_min)
    
    Start = []
    End = []
    
    Season_on = 0
    Values = np.where(np.isnan(Ts_MW), 0, 1)
    for i in range(0, len(Ts_MW)):
        
        if (Ts_MW[i]>Maximum_Threshold and Season_on == 0):
            #print("start ", i)
            Season_on = 1
            Start_Found = 0
            
            # Find start
            for j in np.flipud(range(0, i)):
            
                if (Ts_MW[j] < Ts_MW[j-1] and Start_Found == 0) or (np.isnan(Ts_MW[j-1]) and Start_Found == 0):
                    try:
                       Start = np.append(Start, np.maximum(j, End[-1]))
                    except:
                       Start = np.append(Start, j+1) 
                    Start_Found = 1
                else:
                    pass
        
                
        if (Ts_MW[i]<Maximum_Threshold and Season_on == 1):          
            #print("end ",i)
            Season_on = 0
            End_Found = 0
            
            # Find end    
            for k in range(i, len(Ts_MW)-1):
                
                if (Ts_MW[k+1] > Ts_MW[k] and End_Found == 0) or (np.isnan(Ts_MW[k+1]) and End_Found == 0):
                    End = np.append(End, k-1)
                    End_Found = 1
                else:
                    pass      
        
        if "Start_Found" not in locals():
            Start_Found = 1
            
        if (Start_Found == 0 and len(Start) == 0 and len(End) > 0):
            Start = np.append(np.argwhere(Values==1)[0], Start)
            
    
    try:    
        if np.max(Start)>np.max(End):
            End = np.append(End, np.argwhere(Values==1)[-1])
            
        if np.min(End)<np.min(Start):
            Start = np.append(np.argwhere(Values==1)[0], Start)
    except:
        pass
            
    if len(End)>len(Start):
        Start = np.append(np.argwhere(Values==1)[0], Start)
    
    if len(End)<len(Start):
        End = np.append(End, np.argwhere(Values==1)[-1])
        
    '''
    # Merge overlapping periods
    Boolean = End[:-1] - Start[1:] > 0
    End = np.append(np.where(Boolean,  np.nan, End[:-1]), End[-1])
    Start = np.append(Start[0], np.where(Boolean,  np.nan, Start[1:]))
    End = End[~np.isnan(End)]
    Start = Start[~np.isnan(Start)]   
    '''
    
    if len(Start) > 0:
       
        # If period is longer than 1 year it is a perennial crop
        Season_Amount_Decades = End - Start 
        
        # If two seasons in a row is lower than .... combine season
        Short_Season = np.where(Season_Amount_Decades<10, 1, 0)
        dist_right = Start - np.append(Start[1:], 0)
        dist_left = np.append(0, Start[:-1]) - Start  
        
        if np.nansum(Short_Season) > 0:
            Periods_to_Solve = np.argwhere(Short_Season==1) 
            
            for Period_to_Solve in Periods_to_Solve:
                
                if np.logical_and(Period_to_Solve>0, Period_to_Solve<len(Short_Season)-1):
                
                    if dist_left[Period_to_Solve] > np.maximum(dist_right[Period_to_Solve], -12):
                        
                        End[Period_to_Solve-1] = np.nan
                        Start[Period_to_Solve] = np.nan                
                        
                    elif dist_right[Period_to_Solve] >= np.maximum(dist_left[Period_to_Solve], -12):  
                        
                        End[Period_to_Solve] = np.nan
                        Start[Period_to_Solve+1] = np.nan
                        
                    else:
                    
                        End[Period_to_Solve] = np.nan
                        Start[Period_to_Solve] = np.nan            
                
                else:
        
                    End[Period_to_Solve] = np.nan
                    Start[Period_to_Solve] = np.nan                 
                    
         
        End = End[~np.isnan(End)]
        Start = Start[~np.isnan(Start)] 
         
        try:    
            if len(End) > len(Start):
                if np.nanmin(Start)>np.nanmin(End):
                    End[0] = np.nan
                else:
                    End[-1] = np.nan
            
            if len(Start) > len(End):
                if np.nanmax(Start)>np.nanmax(End):
                    Start[-1] = np.nan
                else:
                    Start[0] = np.nan           
        except:
            pass
        
        
        End = End[~np.isnan(End)]
        Start = Start[~np.isnan(Start)]   
           
        # Find perennial crops
        Season_Amount_Decades = End - Start 
        Long_Season = np.where(Season_Amount_Decades>60, 1, 0)
        Start_Per = Start[Long_Season == 1]
        End_Per = End[Long_Season == 1]
        End = End[Long_Season != 1]
        Start = Start[Long_Season != 1]  
    
    else:
        Start = [] 
        End = []
        Start_Per = []
        End_Per = []
        
    return(Start, End, Start_Per, End_Per)






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













import matplotlib as plt
plt.pyplot.plot(range(0, len(Ts)), Ts[:])
plt.pyplot.plot(range(0, len(Ts_MW)), Ts_MW[:])

for End_point in End:
    plt.pyplot.plot(End_point, Ts[int(End_point)], "r", marker='o', markersize=12)
for Start_point in Start:
    plt.pyplot.plot(Start_point, Ts[int(Start_point)], "g", marker='o', markersize=8)
for End_point in End_Per:
    plt.pyplot.plot(End_point, C[int(End_point)], "y", marker='o', markersize=15)
for Start_point in Start_Per:
    plt.pyplot.plot(Start_point, C[int(Start_point)], "y", marker='o', markersize=15)




 