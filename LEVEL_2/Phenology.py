# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Wed Sep 18 17:10:42 2019
"""

import os
import sys
import gdal
import datetime
import numpy as np
import pandas as pd
import calendar
import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

import WaporTranslator.LEVEL_2.LEVEL_2_Calc_Radiation as L2_Rad


Output_Folder_L2 = r"G:\Project_MetaMeta\LEVEL_2"

Startdate = "2011-01-01"
Enddate = "2018-12-31"

Date_monitor = "2018-05-01"
Enddate_monitor = datetime.datetime.strptime(Date_monitor, "%Y-%m-%d")
Startdate_monitor = datetime.datetime.strptime(Enddate, "%Y-%m-%d") - pd.DateOffset(years = 2)

Years = pd.date_range(Startdate, Enddate, freq = "AS")

# input_folders
folder_T_WAPOR = r"G:\Project_MetaMeta\LEVEL_1\L2_T_D"
folder_ET_WAPOR = r"G:\Project_MetaMeta\LEVEL_1\L2_AETI_D"
folder_NPP_WAPOR = r"G:\Project_MetaMeta\LEVEL_1\L2_NPP_D"
folder_P_WAPOR = r"G:\Project_MetaMeta\LEVEL_1\L1_PCP_D"
folder_Temp_GLDAS = r"G:\Project_MetaMeta\LEVEL_1\Weather_Data\Model\GLDAS\daily\tair_f_inst\mean"
folder_LU_Wapor = r"G:\Project_MetaMeta\LEVEL_1\L2_LCC_A"

# input formats
format_T_WAPOR = "L2_T_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
format_ET_WAPOR = "L2_AETI_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
format_NPP_WAPOR = "L2_NPP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
format_P_WAPOR = "L1_PCP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
format_Temp_GLDAS = "Tair_GLDAS-NOAH_C_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"
format_LU_WAPOR = "L2_LCC_A_WAPOR_YEAR_{yyyy}.01.01.tif"

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
if "Array_ET_Years" in locals():
    del Array_ET_Years
if "Array_P_Years" in locals():
    del Array_P_Years
if "Array_NPP_Years" in locals():
    del Array_NPP_Years    
if "Array_Temp_Years" in locals():
    del Array_Temp_Years

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
    if "Array_ET_Year" in locals():
        del Array_ET_Year
    if "Array_P_Year" in locals():
        del Array_P_Year
    if "Array_NPP_Year" in locals():
        del Array_NPP_Year           
    if "Array_Temp_Year" in locals():
        del Array_Temp_Year        
        
    # Loop over dates    
    for Date in Dates_end:
        
        print(Date)
        # date in dekad
        day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date.day)))[0]), 2)))
            
        # Conversion WAPOR unit to mm/Dekade
        if day_dekad == 2:
            year = Date.year
            month = Date.month
            NOD = calendar.monthrange(year, month)[1]
            conversion_rate = (NOD - 20)/10
        else:
            NOD = 10
            conversion_rate = 1

        filename_T_in = os.path.join(folder_T_WAPOR, format_T_WAPOR.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
        filename_ET_in = os.path.join(folder_ET_WAPOR, format_ET_WAPOR.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
        filename_NPP_in = os.path.join(folder_NPP_WAPOR, format_NPP_WAPOR.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
        filename_P_in = os.path.join(folder_P_WAPOR, format_P_WAPOR.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
        
        if "Array_T_Year" not in locals():
            dest = gdal.Open(filename_T_in)
            filename_ex = filename_T_in
            Array_T_Year = dest.GetRasterBand(1).ReadAsArray()
            Array_T_Year = np.float_(Array_T_Year) * conversion_rate
            
        else:
            dest = gdal.Open(filename_T_in)
            Array_T = dest.GetRasterBand(1).ReadAsArray()    
            Array_T_Year = np.dstack((Array_T_Year, np.float_(Array_T) * conversion_rate))

        if (Date > Startdate_monitor and Date <= Enddate_monitor):

            if "Array_ET_Year" not in locals():     
                
                destet = gdal.Open(filename_ET_in)
                Array_ET_Year = destet.GetRasterBand(1).ReadAsArray()  
                Array_ET_Year = np.float_(Array_ET_Year) * conversion_rate
    
                destnpp = gdal.Open(filename_NPP_in)
                Array_NPP_Year = destnpp.GetRasterBand(1).ReadAsArray()  
                Array_NPP_Year = np.float_(Array_NPP_Year) * NOD  * 0.001
                
                destp = RC.reproject_dataset_example(filename_P_in, filename_ex, 2)
                Array_P_Year = destp.GetRasterBand(1).ReadAsArray()    
                Array_P_Year = np.float_(Array_P_Year) * conversion_rate
                
                desttemp = L2_Rad.Calc_Dekad_Raster_from_Daily(folder_Temp_GLDAS, format_Temp_GLDAS, Date, flux_state = "flux", example_file = filename_ex)
                Array_Temp_Year = desttemp.GetRasterBand(1).ReadAsArray() 
                
            else:
                destet = gdal.Open(filename_ET_in)
                Array_ET = destet.GetRasterBand(1).ReadAsArray()    
                Array_ET_Year = np.dstack((Array_ET_Year, np.float_(Array_ET) * conversion_rate))
     
                destnpp = gdal.Open(filename_NPP_in)
                Array_NPP = destnpp.GetRasterBand(1).ReadAsArray()    
                Array_NPP_Year = np.dstack((Array_NPP_Year, np.float_(Array_NPP) * NOD * 0.001))
               
                destp = RC.reproject_dataset_example(filename_P_in, filename_ex, 2)
                Array_P = destp.GetRasterBand(1).ReadAsArray()    
                Array_P_Year = np.dstack((Array_P_Year, np.float_(Array_P) * conversion_rate))
                
                desttemp = L2_Rad.Calc_Dekad_Raster_from_Daily(folder_Temp_GLDAS, format_Temp_GLDAS, Date, flux_state = "flux", example_file = filename_ex)
                Array_Temp = desttemp.GetRasterBand(1).ReadAsArray() 
                Array_Temp_Year = np.dstack((Array_Temp_Year, Array_Temp))

    # Open LU map
    dest_LU_WAPOR = RC.reproject_dataset_example(os.path.join(folder_LU_Wapor, format_LU_WAPOR.format(yyyy = Year_nmbr)), filename_T_in)
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
      
    # Save LU map
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "LU", "LU_%s.tif" %Year_nmbr), LU_END, geo, proj)  
    
    # find posible perenial pixels
    Phenology_pixels_year = LU_END[np.logical_or(LU_END==1, LU_END==2)]    
    
    Array_T_Year[Array_T_Year >= 255] = np.nan
    Array_T_Year[np.isnan(LU_END), :] = np.nan    
    
    if "Array_T_Years" not in locals():
        Array_T_Years = Array_T_Year
        
    else:
        Array_T_Years = np.dstack((Array_T_Years, Array_T_Year))    
    
    
    if Date > Startdate_monitor:
        
        Array_ET_Year[Array_ET_Year >= 255] = np.nan
        Array_NPP_Year[Array_P_Year < 0] = np.nan 
        Array_P_Year[Array_P_Year >= 255] = np.nan
        #Array_T_Year[np.logical_and(LU_END!=1, LU_END!=2,), :] = np.nan
    
        Array_ET_Year[np.isnan(LU_END), :] = np.nan
        Array_P_Year[np.isnan(LU_END), :] = np.nan
        Array_NPP_Year[np.isnan(LU_END), :] = np.nan       
        Array_Temp_Year[np.isnan(LU_END), :] = np.nan             
        
        if "Array_ET_Years" not in locals():
            Array_ET_Years = Array_ET_Year
            
        else:
            Array_ET_Years = np.dstack((Array_ET_Years, Array_ET_Year))
    
        if "Array_NPP_Years" not in locals():
            Array_NPP_Years = Array_NPP_Year
            
        else:
            Array_NPP_Years = np.dstack((Array_NPP_Years, Array_NPP_Year))
    
        if "Array_P_Years" not in locals():
            Array_P_Years = Array_P_Year
            
        else:
            Array_P_Years = np.dstack((Array_P_Years, Array_P_Year))
    
        if "Array_Temp_Years" not in locals():
            Array_Temp_Years = Array_Temp_Year
            
        else:
            Array_Temp_Years = np.dstack((Array_Temp_Years, Array_Temp_Year))        


# calculate cumulative  
T_cum = np.where(np.isnan(Array_T_Years[:,:,-72:-(72-Array_ET_Years.shape[2])]), 0, Array_T_Years[:,:,-72:-(72-Array_ET_Years.shape[2])])
T_cum = T_cum.cumsum(axis = 2)
ET_cum = np.where(np.isnan(Array_ET_Years), 0, Array_ET_Years)
ET_cum = ET_cum.cumsum(axis = 2)
P_cum = np.where(np.isnan(Array_P_Years), 0, Array_P_Years)
P_cum = P_cum.cumsum(axis = 2)
NPP_cum = np.where(np.isnan(Array_NPP_Years), 0, Array_NPP_Years)
NPP_cum = NPP_cum.cumsum(axis = 2)
Temp_cum = np.where(np.isnan(Array_Temp_Years), 0, Array_Temp_Years)
Temp_cum = Temp_cum.cumsum(axis = 2)

Seasons_dict_start = dict()
Seasons_dict_end = dict()
Seasons_dict_per_start = dict()
Seasons_dict_per_end = dict()

pixel = 1

for i in range(0, Array_T_Years.shape[0]):
    for j in range(0, Array_T_Years.shape[1]):    
      
      Ts = Array_T_Years[i, j, :]   
      if not np.isnan(np.nanmean(Ts)): 
       
          Start, End, Start_Per, End_Per = Calc_Season(Ts)

          Seasons_dict_start[pixel] = Start
          Seasons_dict_end[pixel] = End
          Seasons_dict_per_start[pixel] = Start_Per
          Seasons_dict_per_end[pixel] = End_Per
        
      sys.stdout.write("\rCalculate Phenology %i/%i (%f %%)" %(pixel, Array_T_Years.shape[0]*Array_T_Years.shape[1], pixel/(Array_T_Years.shape[0]*Array_T_Years.shape[1]) * 100))
      sys.stdout.flush()


      pixel += 1

Seasons_dict_per_start = dict( [(k,v) for k,v in Seasons_dict_per_start.items() if len(v)>0])
Seasons_dict_per_end = dict( [(k,v) for k,v in Seasons_dict_per_end.items() if len(v)>0])
Seasons_dict_start = dict( [(k,v) for k,v in Seasons_dict_start.items() if len(v)>0])
Seasons_dict_end = dict( [(k,v) for k,v in Seasons_dict_end.items() if len(v)>0])

# End cumulative Arrays
T_end_sum = np.ones(P_cum.shape) * np.nan
ET_end_sum = np.ones(P_cum.shape) * np.nan
NPP_end_sum = np.ones(P_cum.shape) * np.nan
P_end_sum = np.ones(P_cum.shape) * np.nan
Temp_end_sum = np.ones(P_cum.shape) * np.nan
 
# create IDs for the Array to reconstruct the array from the dict later
y,x = np.indices((LU_END.shape[0], LU_END.shape[1]))
ID_Matrix = np.int32(np.ravel_multi_index(np.vstack((y.ravel(),x.ravel())),(LU_END.shape[0], LU_END.shape[1]),mode='clip').reshape(x.shape))

for Year in Years[-2:]:
    
    year_nmbr = Year.year  
    
    # Create empty output maps
    Start_Map_S1 = np.ones(LU_END.shape) * np.nan
    End_Map_S1 = np.ones(LU_END.shape) * np.nan
    Start_Map_S2 = np.ones(LU_END.shape) * np.nan
    End_Map_S2 = np.ones(LU_END.shape) * np.nan
    Per_Map_S2 = np.ones(LU_END.shape) * np.nan
    LU_Crop_Map = np.ones(LU_END.shape) * np.nan

    # Select begin and end of the year for the array
    Year_DOY_Start = (year_nmbr - Years[0].year) * 36
    Year_DOY_End = Year_DOY_Start + 36
    
    Total_length_period = Array_T_Years.shape[2]
    ID_start_last_year = np.argwhere(Enddate_monitor == pd.to_datetime(Dates_end))
    Start_Cum = Total_length_period - 72
    
    count = 1
    # Create Perenial map
    for dict_in_per in Seasons_dict_per_start.items():        
    
        sys.stdout.write("\rCreate Maps Perenial of year %s %i/%i (%f %%)" %(year_nmbr, count, len(Seasons_dict_per_start.items()), count/len(Seasons_dict_per_start.items())*100))
        sys.stdout.flush()
    
        Starts_per = dict_in_per[1]
        Ends_per = Seasons_dict_per_end[dict_in_per[0]]
        
        for Start_per in Starts_per:
            
            End_per = Ends_per[np.argwhere(Start_per==Starts_per)][0][0]
            
            if np.logical_and(Start_per<Year_DOY_End, End_per > Year_DOY_Start):
            
                if Year > Years[-3]:
                    
                    Tstart = int(np.maximum(0, Start_per - Start_Cum))
                    Tend = int(np.minimum(T_cum.shape[2], End_per - Start_Cum))
                    
                    if (Tstart < T_cum.shape[2] + 1 and Tend > -1):
                    
                        T_end_sum[dict_in_per[0]== ID_Matrix, Tstart:Tend] = T_cum[dict_in_per[0]== ID_Matrix,  Tstart:Tend] - T_cum[dict_in_per[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                        ET_end_sum[dict_in_per[0]== ID_Matrix, Tstart:Tend] = ET_cum[dict_in_per[0]== ID_Matrix, Tstart:Tend] - ET_cum[dict_in_per[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                        P_end_sum[dict_in_per[0]== ID_Matrix, Tstart:Tend] = P_cum[dict_in_per[0]== ID_Matrix, Tstart:Tend] - P_cum[dict_in_per[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                        NPP_end_sum[dict_in_per[0]== ID_Matrix, Tstart:Tend] = NPP_cum[dict_in_per[0]== ID_Matrix, Tstart:Tend] - NPP_cum[dict_in_per[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                        Temp_end_sum[dict_in_per[0]== ID_Matrix, Tstart:Tend] = Temp_cum[dict_in_per[0]== ID_Matrix,Tstart:Tend] - Temp_cum[dict_in_per[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                       
                if np.logical_and(Start_per <= Year_DOY_End, End_per >= Year_DOY_Start):
                    
                    Per_Map_S2[dict_in_per[0]== ID_Matrix] = 1
                    LU_Crop_Map[dict_in_per[0]== ID_Matrix] = 3
                    
        count += 1
    
    count = 1
    
    print("                                                                                          ")
    # Create S1 and S2 maps
    for dict_in in Seasons_dict_start.items():   
     
        sys.stdout.write("\rCreate Maps Other Crops of year %s %i/%i (%f %%)" %(year_nmbr, count, len(Seasons_dict_start.items()), count/len(Seasons_dict_start.items())*100))
        sys.stdout.flush()
        
        # Check if pixel is not perenial
        if Per_Map_S2[dict_in[0] == ID_Matrix] != 1:
         
            Starts = dict_in[1]
            
            if len(Starts)>0:
                Starts = Starts[np.logical_and(Starts<Year_DOY_End, Starts>=Year_DOY_Start)]
                
                # If it is a single season
                if len(Starts) > 0:
                    
                   # Get the end value for this start period 
                   End = Seasons_dict_end[dict_in[0]][np.argwhere(Starts[0] == dict_in[1])][0][0]
    
                   if Year > Years[-3]:
     
                       Tstart = int(np.maximum(0, Starts[0] - Start_Cum))
                       Tend = int(np.minimum(T_cum.shape[2], End - Start_Cum))
                       
                       if (Tstart < T_cum.shape[2] +1  and Tend > -1):
                 
                           # Set cumulative
                           T_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = T_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - T_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           ET_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = ET_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - ET_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           P_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = P_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - P_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           NPP_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = NPP_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - NPP_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           Temp_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = Temp_cum[dict_in[0]== ID_Matrix,Tstart:Tend] - Temp_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
    
                   # Fill in array
                   Start_Map_S1[dict_in[0]== ID_Matrix] = Starts[0] - Year_DOY_Start
                   End_Map_S1[dict_in[0]== ID_Matrix] = End - Year_DOY_Start
                   LU_Crop_Map[dict_in[0]== ID_Matrix] = 1
                   
                # If it is a double season               
                if len(Starts) >= 2:    
                   # Get the end value for this start period   
                   End = Seasons_dict_end[dict_in[0]][np.argwhere(Starts[1] == dict_in[1])][0][0]
    
                   if Year > Years[-3]:
                       
                       Tstart = int(np.maximum(0, Starts[1] - Start_Cum))
                       Tend = int(np.minimum(T_cum.shape[2], End - Start_Cum))
                       
                       if (Tstart < T_cum.shape[2] +1 and Tend > -1):
                 
                           # Set cumulative
                           T_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = T_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - T_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           ET_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = ET_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - ET_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           P_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = P_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - P_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           NPP_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = NPP_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - NPP_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
                           Temp_end_sum[dict_in[0]== ID_Matrix, Tstart:Tend] = Temp_cum[dict_in[0]== ID_Matrix, Tstart:Tend] - Temp_cum[dict_in[0] == ID_Matrix, int(np.maximum(Tstart-1, 0))]
    
                   # Fill in array
                   Start_Map_S2[dict_in[0]== ID_Matrix] = Starts[1] - Year_DOY_Start      
                   End_Map_S2[dict_in[0]== ID_Matrix] = End - Year_DOY_Start
                   LU_Crop_Map[dict_in[0]== ID_Matrix] = 2
                   
        count += 1        
    print("                                                                                         ")      
        
    # Save files
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenelogy", "Start", "S1", "Phenology_Start_S1_%s.tif" %year_nmbr), Start_Map_S1, geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenelogy", "Start", "S2", "Phenology_Start_S2_%s.tif" %year_nmbr), Start_Map_S2, geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenelogy", "End", "S1", "Phenology_End_S1_%s.tif" %year_nmbr), End_Map_S1, geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenelogy", "End", "S2", "Phenology_End_S2_%s.tif" %year_nmbr), End_Map_S2, geo, proj)       
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenelogy", "Perenial", "Phenology_Per_%s.tif" %year_nmbr), Per_Map_S2, geo, proj)  
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenelogy", "CropClass","LU_CropSeason_%s.tif" %year_nmbr), LU_Crop_Map, geo, proj)      
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenelogy", "CropClass","LU_CropType_%s.tif" %year_nmbr), LU_END, geo, proj)
    
# Get dekads time steps
Dates_end2 = []
for Year in Years:
    
    Year_nmbr = Year.year
    
    # Find dates dekades for one year
    Startdate_Year = "%d-01-01" %Year_nmbr
    Enddate_Year = "%d-12-31" %Year_nmbr
    day_dekad_end = 2
    
    if Year == Years[-1]:
        Enddate_Year = Enddate_monitor
        day_dekad_end = int("%d" %int(np.minimum(int(("%02d" %int(str(Enddate_monitor.day)))[0]), 2)))

    # Define dates
    Dates = pd.date_range(Startdate_Year, Enddate_Year, freq = "MS")

    # Define decade dates
    for Date in Dates:
        if Date != Dates[-1]:
            Dates_end2.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 1)))
            Dates_end2.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 11)))
            Dates_end2.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 21)))
        else:
            Dates_end2.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 1)))
            if day_dekad_end > 0:
                Dates_end2.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 11)))
            if day_dekad_end > 1:
                Dates_end2.append(pd.Timestamp(datetime.datetime(Date.year, Date.month, 21)))   

# Save the cumulative paramters
for i in range(0,T_cum.shape[2]):
    
    Date_cum = Dates_end2[int(Start_Cum+i)]
    
    # Save files
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Cumulative", "Transpiration", "T_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), T_end_sum[:,:,i], geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Cumulative", "Evapotranspiration", "ET_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), ET_end_sum[:,:,i], geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Cumulative", "Precipitation", "P_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), P_end_sum[:,:,i], geo, proj)    
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Cumulative", "NPP", "NPP_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), NPP_end_sum[:,:,i], geo, proj)       
    DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Cumulative", "Temperature", "Temp_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), Temp_end_sum[:,:,i], geo, proj)  
    







def Calc_Season(Ts):
    
    Ts_MW = (Ts + np.append(Ts[1:], Ts[0]) + np.append(Ts[-1], Ts[:-1]) + np.append(Ts[-2:], Ts[:-2]) + np.append(Ts[2:], Ts[0:2]))/5
    
    Minimum_T = np.nanmin(Ts_MW)
    Maximum_T = np.nanmax(Ts_MW)
    
    Threshold_LVL = 0.7
    Threshold_LVL_min = 15
    
    if Maximum_T - Minimum_T > Threshold_LVL_min:
        Threshold_LVL_min = Maximum_T - Minimum_T
    
    Maximum_Threshold = np.minimum(Threshold_LVL * (Maximum_T + Minimum_T) / 2 + Minimum_T, Threshold_LVL_min)
    
    Threshold_stop = 0.3 * Maximum_Threshold
    
    Start = []
    End = []
    
    Season_on = 0
    Values = np.where(np.isnan(Ts_MW), 0, 1)
    
    if Maximum_Threshold > 10:
        for i in range(0, len(Ts_MW)):
            
            if (Ts_MW[i]>Maximum_Threshold and Season_on == 0):
                #print("start ", i)
                Season_on = 1
                Start_Found = 0
                
                # Find start
                for j in np.flipud(range(0, i)):
                
                    if (Ts_MW[j] < Ts_MW[j-1] and Start_Found == 0) or (np.isnan(Ts_MW[j-1]) and Start_Found == 0) or (Ts_MW[j] < Threshold_stop and Start_Found == 0):
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
                    
                    if (Ts_MW[k+1] > Ts_MW[k] and End_Found == 0) or (np.isnan(Ts_MW[k+1]) and End_Found == 0) or (Ts_MW[k] < Threshold_stop and End_Found == 0):
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
            
            Short_Season_Que = Short_Season[1:-1] + Short_Season[2:]+ Short_Season[:-2]
            
            if len(np.argwhere(Short_Season_Que == 3))>0:
                
                IDs = np.argwhere(Short_Season_Que == 3)
                
                for ID in IDs:
                    IDnow = ID + 1
                    Start[IDnow] = np.nan
                    End[IDnow] = np.nan    
                     
                End = End[~np.isnan(End)]
                Start = Start[~np.isnan(Start)] 
                    
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
                    
                        if dist_left[Period_to_Solve] >= np.maximum(dist_right[Period_to_Solve], -12):
                            
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




 