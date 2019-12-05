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

def Calc_Phenology(output_folder, Start_year_analyses, End_year_analyses, T, ET, NPP, P, Temp, ET0, LU, example_file, Days_in_Dekads):

    import WaporTranslator.LEVEL_1.Input_Data as Inputs
    
    # Define start and enddate
    Startdate = "%s-01-01" %Start_year_analyses
    Enddate = "%s-12-31" %End_year_analyses
    
    # Create datetime from start and enddate
    Startdate_monitor = datetime.datetime.strptime(Startdate, "%Y-%m-%d")
    Enddate_monitor = datetime.datetime.strptime(Enddate, "%Y-%m-%d")
    
    # Get the years 
    Years = pd.date_range(Startdate, Enddate, freq = "AS")

    # Get path and formats
    Paths = Inputs.Input_Paths()
    Formats = Inputs.Input_Formats()
        
    # Open ESACCI
    input_file_LU_ESACCI = os.path.join(output_folder, Paths.LU_ESA, Formats.LU_ESA)
    
    # Create the output folder for the tiff files
    Output_Folder_L2 = os.path.join(output_folder, "LEVEL_2")
    
    # Create output folder
    if not os.path.exists(Output_Folder_L2):
        os.makedirs(Output_Folder_L2)
    
    # Converting LU maps into one LU map
    # open dictionary WAPOR 
    WAPOR_Conversions_dict = WAPOR_Conversions()
    # open dictionary ESACCI
    ESACCI_Conversions_dict = ESACCI_Conversions()
    
    Phenology_pixels_year = np.ones(T.Size) * np.nan
    Grassland_pixels_year = np.ones(T.Size) * np.nan
    
    # Loop over the years
    for Year in Years:
        
        Year_start = int(Years[0].year)
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
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "LU_END", "LU_%s.tif" %Year_int), LU_END, geo, proj)  
        
        # find posible Perennial pixels
        Phenology_pixels_year[int((Year_int - Year_start) * 36):int((Year_int - Year_start) * 36)+36,: ,:] = np.where(np.logical_or(LU_END==1, LU_END==2), 1, np.nan)[None, :, :]  
        Grassland_pixels_year[int((Year_int - Year_start) * 36):int((Year_int - Year_start) * 36)+36,: ,:] = np.where(LU_END==3, 1, np.nan)[None, :, :]  

    # calculate cumulative  
    T_cum = np.where(np.isnan(T.Data), 0, T.Data * Days_in_Dekads[:, None, None])
    T_cum = T_cum.cumsum(axis = 0)
    ET_cum = np.where(np.isnan(ET.Data), 0, ET.Data * Days_in_Dekads[:, None, None])
    ET_cum = ET_cum.cumsum(axis = 0)
    P_cum = np.where(np.isnan(P.Data), 0, P.Data * Days_in_Dekads[:, None, None])
    P_cum = P_cum.cumsum(axis = 0)
    NPP_cum = np.where(np.isnan(NPP.Data), 0, NPP.Data * Days_in_Dekads[:, None, None])
    NPP_cum = NPP_cum.cumsum(axis = 0)
    Temp_cum = np.where(np.isnan(Temp.Data), 0, Temp.Data * Days_in_Dekads[:, None, None])
    Temp_cum = Temp_cum.cumsum(axis = 0)
    ET0_cum = np.where(np.isnan(ET0.Data), 0, ET0.Data * Days_in_Dekads[:, None, None])
    ET0_cum = ET0_cum.cumsum(axis = 0)
    
    Seasons_dict_start = dict()
    Seasons_dict_end = dict()
    Seasons_dict_per_start = dict()
    Seasons_dict_per_end = dict()
    
    pixel = 1
    
    T_selected = T.Data * Phenology_pixels_year
    
    for i in range(0, T.Size[1]):
        for j in range(0, T.Size[2]):    
          
          Ts = T_selected[:, i, j]
          if not np.isnan(np.nanmean(Ts)): 
           
              Start, End, Start_Per, End_Per = Calc_Season(Ts)
    
              Seasons_dict_start[pixel] = Start
              Seasons_dict_end[pixel] = End
              Seasons_dict_per_start[pixel] = Start_Per
              Seasons_dict_per_end[pixel] = End_Per
            
          sys.stdout.write("\rCalculate Phenology %i/%i (%f %%)" %(pixel, T.Size[1] * T.Size[2], pixel/(T.Size[1] * T.Size[2]) * 100))
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
    ET0_end_sum = np.ones(P_cum.shape) * np.nan
     
    # create IDs for the Array to reconstruct the array from the dict later
    y,x = np.indices((LU_END.shape[0], LU_END.shape[1]))
    ID_Matrix = np.int32(np.ravel_multi_index(np.vstack((y.ravel(),x.ravel())),(LU_END.shape[0], LU_END.shape[1]),mode='clip').reshape(x.shape)) + 1
    
    for Year in Years:
        
        year_nmbr = Year.year  
        
        # Create empty output maps
        Start_Map_S1 = np.ones(LU_END.shape) * np.nan
        End_Map_S1 = np.ones(LU_END.shape) * np.nan
        Start_Map_S2 = np.ones(LU_END.shape) * np.nan
        End_Map_S2 = np.ones(LU_END.shape) * np.nan
        Start_Map_S3 = np.ones(LU_END.shape) * np.nan
        End_Map_S3 = np.ones(LU_END.shape) * np.nan
        Per_Map_Start = np.ones(LU_END.shape) * np.nan
        Per_Map_End = np.ones(LU_END.shape) * np.nan        
        LU_Crop_Map = np.ones(LU_END.shape) * np.nan
    
        # Select begin and end of the year for the array
        Year_DOY_Start = (year_nmbr - Years[0].year) * 36
        Year_DOY_End = Year_DOY_Start + 36
        count = 1
        
        # Create Perennial map
        for dict_in_per in Seasons_dict_per_start.items():        
 
            sys.stdout.write("\rCreate Maps Perennial of year %s %i/%i (%f %%)" %(year_nmbr, count, len(Seasons_dict_per_start.items()), count/len(Seasons_dict_per_start.items())*100))
            sys.stdout.flush()
        
            Starts_per = dict_in_per[1]
            Ends_per = Seasons_dict_per_end[dict_in_per[0]]
            
            for Start_per in Starts_per:
                
                Start_per = int(Start_per)
                End_per = int(Ends_per[np.argwhere(Start_per == Starts_per)][0][0])
                
                if np.logical_and(Start_per < Year_DOY_End, End_per > Year_DOY_Start):
                                   
                    T_end_sum[Start_per:End_per, dict_in_per[0]== ID_Matrix] = T_cum[Start_per:End_per, dict_in_per[0]== ID_Matrix] - T_cum[int(np.maximum(Start_per-1, 0)), dict_in_per[0] == ID_Matrix]
                    ET_end_sum[Start_per:End_per, dict_in_per[0]== ID_Matrix] = ET_cum[Start_per:End_per, dict_in_per[0]== ID_Matrix] - ET_cum[int(np.maximum(Start_per-1, 0)), dict_in_per[0] == ID_Matrix]
                    P_end_sum[Start_per:End_per, dict_in_per[0]== ID_Matrix] = P_cum[Start_per:End_per, dict_in_per[0]== ID_Matrix] - P_cum[int(np.maximum(Start_per-1, 0)), dict_in_per[0] == ID_Matrix]
                    NPP_end_sum[Start_per:End_per, dict_in_per[0]== ID_Matrix] = NPP_cum[Start_per:End_per, dict_in_per[0]== ID_Matrix] - NPP_cum[int(np.maximum(Start_per-1, 0)), dict_in_per[0] == ID_Matrix]
                    Temp_end_sum[Start_per:End_per, dict_in_per[0]== ID_Matrix] = Temp_cum[Start_per:End_per, dict_in_per[0]== ID_Matrix] - Temp_cum[int(np.maximum(Start_per-1, 0)), dict_in_per[0] == ID_Matrix]
                    ET0_end_sum[Start_per:End_per, dict_in_per[0]== ID_Matrix] = ET0_cum[Start_per:End_per, dict_in_per[0]== ID_Matrix] - ET0_cum[int(np.maximum(Start_per-1, 0)), dict_in_per[0] == ID_Matrix]
                  
                    if np.logical_and(Start_per < Year_DOY_End, End_per > Year_DOY_Start):
                        
                        Per_Map_Start[dict_in_per[0]== ID_Matrix] = Start_per - Year_DOY_Start
                        Per_Map_End[dict_in_per[0]== ID_Matrix] = End_per - Year_DOY_Start                        
                        LU_Crop_Map[dict_in_per[0]== ID_Matrix] = 4    
            count += 1

        count = 1
        
        print("                                                                                          ")
        # Create S1 and S2 maps
        for dict_in in Seasons_dict_start.items():   

            sys.stdout.write("\rCreate Maps Other Crops of year %s %i/%i (%f %%)" %(year_nmbr, count, len(Seasons_dict_start.items()), count/len(Seasons_dict_start.items())*100))
            sys.stdout.flush()
            
            # Check if pixel is not Perennial
            if np.isnan(Per_Map_Start[dict_in[0] == ID_Matrix]):
             
                Starts = dict_in[1]
                
                if len(Starts)>0:
                    Starts = Starts[np.logical_and(Starts<Year_DOY_End, Starts>=Year_DOY_Start)]
                    
                    # If it is a single season
                    if len(Starts) > 0:
                        
                       # Get the end value for this start period 
                       End = int(Seasons_dict_end[dict_in[0]][np.argwhere(Starts[0] == dict_in[1])][0][0])
    
                       # Set cumulative
                       T_end_sum[int(Starts[0]):End, dict_in[0]== ID_Matrix] = T_cum[int(Starts[0]):End, dict_in[0]== ID_Matrix] - T_cum[int(np.maximum(int(Starts[0])-1, 0)), dict_in[0] == ID_Matrix]
                       ET_end_sum[int(Starts[0]):End, dict_in[0]== ID_Matrix] = ET_cum[int(Starts[0]):End, dict_in[0]== ID_Matrix] - ET_cum[int(np.maximum(int(Starts[0])-1, 0)), dict_in[0] == ID_Matrix]
                       P_end_sum[int(Starts[0]):End, dict_in[0]== ID_Matrix] = P_cum[int(Starts[0]):End, dict_in[0]== ID_Matrix] - P_cum[int(np.maximum(int(Starts[0])-1, 0)), dict_in[0] == ID_Matrix]
                       NPP_end_sum[int(Starts[0]):End, dict_in[0]== ID_Matrix] = NPP_cum[int(Starts[0]):End, dict_in[0]== ID_Matrix] - NPP_cum[int(np.maximum(int(Starts[0])-1, 0)), dict_in[0] == ID_Matrix]
                       Temp_end_sum[int(Starts[0]):End, dict_in[0]== ID_Matrix] = Temp_cum[int(Starts[0]):End, dict_in[0]== ID_Matrix] - Temp_cum[int(np.maximum(int(Starts[0])-1, 0)), dict_in[0] == ID_Matrix]
                       ET0_end_sum[int(Starts[0]):End, dict_in[0]== ID_Matrix] = ET0_cum[int(Starts[0]):End, dict_in[0]== ID_Matrix] - ET0_cum[int(np.maximum(int(Starts[0])-1, 0)), dict_in[0] == ID_Matrix]
    
                       # Fill in array
                       Start_Map_S1[dict_in[0]== ID_Matrix] = Starts[0] - Year_DOY_Start
                       End_Map_S1[dict_in[0]== ID_Matrix] = End - Year_DOY_Start
                       LU_Crop_Map[dict_in[0]== ID_Matrix] = 1
                       
                    # If it is a double season               
                    if len(Starts) > 1:    
                        
                       # Get the end value for this start period   
                       End = int(Seasons_dict_end[dict_in[0]][np.argwhere(Starts[1] == dict_in[1])][0][0])
             
                       # Set cumulative
                       T_end_sum[int(Starts[1]):End, dict_in[0]== ID_Matrix] = T_cum[int(Starts[1]):End, dict_in[0]== ID_Matrix] - T_cum[int(np.maximum(int(Starts[1])-1, 0)), dict_in[0] == ID_Matrix]
                       ET_end_sum[int(Starts[1]):End, dict_in[0]== ID_Matrix] = ET_cum[int(Starts[1]):End, dict_in[0]== ID_Matrix] - ET_cum[int(np.maximum(int(Starts[1])-1, 0)), dict_in[0] == ID_Matrix]
                       P_end_sum[int(Starts[1]):End, dict_in[0]== ID_Matrix] = P_cum[int(Starts[1]):End, dict_in[0]== ID_Matrix] - P_cum[int(np.maximum(int(Starts[1])-1, 0)), dict_in[0] == ID_Matrix]
                       NPP_end_sum[int(Starts[1]):End, dict_in[0]== ID_Matrix] = NPP_cum[int(Starts[1]):End, dict_in[0]== ID_Matrix] - NPP_cum[int(np.maximum(int(Starts[1])-1, 0)), dict_in[0] == ID_Matrix]
                       Temp_end_sum[int(Starts[1]):End, dict_in[0]== ID_Matrix] = Temp_cum[int(Starts[1]):End, dict_in[0]== ID_Matrix] - Temp_cum[int(np.maximum(int(Starts[1])-1, 0)), dict_in[0] == ID_Matrix]
                       ET0_end_sum[int(Starts[1]):End, dict_in[0]== ID_Matrix] = ET0_cum[int(Starts[1]):End, dict_in[0]== ID_Matrix] - ET0_cum[int(np.maximum(int(Starts[1])-1, 0)), dict_in[0] == ID_Matrix]
      
                       # Fill in array
                       Start_Map_S2[dict_in[0]== ID_Matrix] = Starts[1] - Year_DOY_Start      
                       End_Map_S2[dict_in[0]== ID_Matrix] = End - Year_DOY_Start
                       LU_Crop_Map[dict_in[0] == ID_Matrix] = 2

                    # If it is a triple season               
                    if len(Starts) > 2:    
                        
                       # Get the end value for this start period   
                       End = int(Seasons_dict_end[dict_in[0]][np.argwhere(Starts[2] == dict_in[1])][0][0])
             
                       # Set cumulative
                       T_end_sum[int(Starts[2]):End, dict_in[0]== ID_Matrix] = T_cum[int(Starts[2]):End, dict_in[0]== ID_Matrix] - T_cum[int(np.maximum(int(Starts[2])-1, 0)), dict_in[0] == ID_Matrix]
                       ET_end_sum[int(Starts[2]):End, dict_in[0]== ID_Matrix] = ET_cum[int(Starts[2]):End, dict_in[0]== ID_Matrix] - ET_cum[int(np.maximum(int(Starts[2])-1, 0)), dict_in[0] == ID_Matrix]
                       P_end_sum[int(Starts[2]):End, dict_in[0]== ID_Matrix] = P_cum[int(Starts[2]):End, dict_in[0]== ID_Matrix] - P_cum[int(np.maximum(int(Starts[2])-1, 0)), dict_in[0] == ID_Matrix]
                       NPP_end_sum[int(Starts[2]):End, dict_in[0]== ID_Matrix] = NPP_cum[int(Starts[2]):End, dict_in[0]== ID_Matrix] - NPP_cum[int(np.maximum(int(Starts[2])-1, 0)), dict_in[0] == ID_Matrix]
                       Temp_end_sum[int(Starts[2]):End, dict_in[0]== ID_Matrix] = Temp_cum[int(Starts[2]):End, dict_in[0]== ID_Matrix] - Temp_cum[int(np.maximum(int(Starts[2])-1, 0)), dict_in[0] == ID_Matrix]
                       ET0_end_sum[int(Starts[2]):End, dict_in[0]== ID_Matrix] = ET0_cum[int(Starts[2]):End, dict_in[0]== ID_Matrix] - ET0_cum[int(np.maximum(int(Starts[2])-1, 0)), dict_in[0] == ID_Matrix]
      
                       # Fill in array
                       Start_Map_S3[dict_in[0]== ID_Matrix] = Starts[2] - Year_DOY_Start      
                       End_Map_S3[dict_in[0]== ID_Matrix] = End - Year_DOY_Start
                       LU_Crop_Map[dict_in[0] == ID_Matrix] = 3
                       
            count += 1        
        print("                                                                                         ")      


        # Do a Growing Degrees Days check
        GDD_CHECK = np.nanmax(Temp_end_sum, axis = 0)
        
        # Make Perennial crop from single crop
        Per_Map_Start = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==1), Start_Map_S1, Per_Map_Start)
        Per_Map_End = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==1), End_Map_S1, Per_Map_End)       
        Start_Map_S1 = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==1), np.nan, Start_Map_S1)
        End_Map_S1 = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==1), np.nan, End_Map_S1)
        Start_Map_S2 = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==2), np.nan, Start_Map_S2)
        End_Map_S2 = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==2), np.nan, End_Map_S2)
        Start_Map_S3 = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==3), np.nan, Start_Map_S3)
        End_Map_S3 = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==3), np.nan, End_Map_S3)
        
        # Make Single crop from Perennial crop       
        Start_Map_S1 = np.where(np.logical_and(GDD_CHECK<7000,LU_Crop_Map==4), Per_Map_Start, Start_Map_S1)        
        End_Map_S1 = np.where(np.logical_and(GDD_CHECK<7000,LU_Crop_Map==4), Per_Map_End, End_Map_S1)        
        Per_Map_Start = np.where(np.logical_and(GDD_CHECK<7000,LU_Crop_Map==4), np.nan, Per_Map_Start)  
        Per_Map_End = np.where(np.logical_and(GDD_CHECK<7000,LU_Crop_Map==4), np.nan, Per_Map_End)          

        LU_Crop_Map = np.where(np.logical_and(GDD_CHECK>7000,LU_Crop_Map==1), 4, LU_Crop_Map)
        LU_Crop_Map = np.where(np.logical_and(GDD_CHECK<7000,LU_Crop_Map==4), 1, LU_Crop_Map)

        # Save files
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "Start", "S1", "S1_Start_%s.tif" %year_nmbr), Start_Map_S1, geo, proj)    
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "Start", "S2", "S2_Start_%s.tif" %year_nmbr), Start_Map_S2, geo, proj)    
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "Start", "S3", "S3_Start_%s.tif" %year_nmbr), Start_Map_S3, geo, proj)    

        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "End", "S1", "S1_End_%s.tif" %year_nmbr), End_Map_S1, geo, proj)    
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "End", "S2", "S2_End_%s.tif" %year_nmbr), End_Map_S2, geo, proj)       
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "End", "S3", "S3_End_%s.tif" %year_nmbr), End_Map_S3, geo, proj)       

        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "Perennial", "Perennial_Start_%s.tif" %year_nmbr), Per_Map_Start, geo, proj)  
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "Perennial", "Perennial_End_%s.tif" %year_nmbr), Per_Map_End, geo, proj)          
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Phenology", "CropSeason","LU_CropSeason_%s.tif" %year_nmbr), LU_Crop_Map, geo, proj)      

    for Year in Years:
        
        year_ID = int(Year.year - Years[0].year)
        Start = int(year_ID * 36)
        End = int(Start + 36)
       
        T_end_sum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] = T_cum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] - T_cum[int(np.maximum(Start-1, 0)), Grassland_pixels_year[year_ID,:,:]==1]
        ET_end_sum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] = ET_cum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] - ET_cum[int(np.maximum(Start-1, 0)), Grassland_pixels_year[year_ID,:,:]==1]
        P_end_sum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] = P_cum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] - P_cum[int(np.maximum(Start-1, 0)), Grassland_pixels_year[year_ID,:,:]==1]
        NPP_end_sum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] = NPP_cum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] - NPP_cum[int(np.maximum(Start-1, 0)), Grassland_pixels_year[year_ID,:,:]==1]
        Temp_end_sum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] = Temp_cum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] - Temp_cum[int(np.maximum(Start-1, 0)), Grassland_pixels_year[year_ID,:,:]==1]
        ET0_end_sum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] = ET0_cum[Start:End, Grassland_pixels_year[year_ID,:,:]==1] - ET0_cum[int(np.maximum(Start-1, 0)), Grassland_pixels_year[year_ID,:,:]==1]

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
    for i in range(0, T_cum.shape[0]):
        
        Date_cum = Dates_end2[int(i)]
        
        # Save files
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Temp", "Cumulative", "Transpiration", "T_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), T_end_sum[i,:,:], geo, proj)    
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Temp", "Cumulative", "Evapotranspiration", "ET_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), ET_end_sum[i,:,:], geo, proj)    
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Temp", "Cumulative", "Precipitation", "P_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), P_end_sum[i,:,:], geo, proj)    
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Temp", "Cumulative", "NPP", "NPP_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), NPP_end_sum[i,:,:], geo, proj)       
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Temp", "Cumulative", "Temperature", "Temp_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), Temp_end_sum[i,:,:], geo, proj)  
        DC.Save_as_tiff(os.path.join(Output_Folder_L2, "Temp", "Cumulative", "ET0", "ET0_cum_%d.%02d.%02d.tif" %(Date_cum.year, Date_cum.month, Date_cum.day)), ET0_end_sum[i,:,:], geo, proj)  
       
    return()
    
def Calc_Season(Ts):
    
    # Create a moving window of the Transpiration
    Ts_MW = (Ts + np.append(Ts[1:], Ts[0]) + np.append(Ts[-1], Ts[:-1]) + np.append(Ts[-2:], Ts[:-2]) + np.append(Ts[2:], Ts[0:2]))/5
    
    # Get the minimum and maximum Transpiration over the period
    Minimum_T = np.nanpercentile(Ts_MW,5)
    Maximum_T = np.nanpercentile(Ts_MW, 95)
    
    # Find the threshold values
    Threshold_LVL = 0.7
    Threshold_LVL_min = 1.5
    
    if Maximum_T - Minimum_T > Threshold_LVL_min:
        Threshold_LVL_min = (Maximum_T - Minimum_T) * 0.2 + Minimum_T
    
    # In the end I have set the threshold values on 1.5 and 1.0
    #Maximum_Threshold = np.minimum(Threshold_LVL * (Maximum_T + Minimum_T) / 2 + Minimum_T, Threshold_LVL_min)
    Maximum_Threshold = 2.8
    #Threshold_stop = np.maximum(0.2 * Maximum_Threshold + Minimum_T, 0.3 * Maximum_Threshold)
    Threshold_stop = 2.8
    
    # Set the start point
    Start = []
    End = []
    Endmax = 0
    Season_on = 0
    
    # Find the non nan values
    Values = np.where(np.isnan(Ts_MW), 0, 1)
    
    # Check over the days
    if (Maximum_Threshold > 1.2 and Maximum_T > Maximum_Threshold):
        for i in range(0, len(Ts_MW)):
            
            # Find start of a period
            if (Ts_MW[i]>Maximum_Threshold and Season_on == 0) and (np.nanmax(Endmax) < i):
                #print("start ", i)
                
                # Set start of period paramters
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
                    
            # Find end of a period (only when a start is detected)    
            if (Ts_MW[i]<Maximum_Threshold and Season_on == 1):          
          
                # Set end of period parameters
                Season_on = 0
                End_Found = 0
                
                # Find end    
                for k in range(i, len(Ts_MW)-1):
                    if (Ts_MW[k+1] > Ts_MW[k] and End_Found == 0) or (Ts_MW[k] < Threshold_stop and End_Found == 0):
                        if np.nanmax(Endmax) <= k:
                            End = np.append(End, k-1)
                            
                        End_Found = 1
                        Endmax = k-1
                    else:
                        pass      
                
                if len(range(i, len(Ts_MW)-1)) == 0:
                    k = int(len(Ts_MW)-1)
                
                # If no end is found set the end as end point
                if End_Found == 0:
                    End = np.append(End, k)
                    Endmax = k
            
            # If there was no Start found, set begin as starting point
            if "Start_Found" not in locals():
                Start_Found = 1
     
            # If a start was not found but there is a end, set start to begin           
            if (Start_Found == 0 and len(Start) == 0 and len(End) > 0):
                Start = np.append(np.argwhere(Values==1)[0], Start)
 
        # if T values are high but no start point or end point is found. Set start and end over the whole period       
        if np.nanmin(Ts_MW) >= Maximum_Threshold:
            Start = np.array(np.argwhere(Values==1)[0])
            End = np.array([9999])
        
        try:    
            if np.max(Start)>np.max(End):
                if np.min(Values[int(np.max(Start)):])==0:
                    End = np.append(End, np.argwhere(Values==1)[-1])
                else:
                    End = np.append(End, 9999)
                     
            if np.min(End)<np.min(Start):
                Start = np.append(np.argwhere(Values==1)[0], Start)
        except:
            pass
                
        if len(End)>len(Start):
            Start = np.append(np.argwhere(Values==1)[0], Start)
        
        if len(End)<len(Start):
            if np.min(Values[int(np.max(Start)):])==0:
                End = np.append(End, np.argwhere(Values==1)[-1])
            else:
                End = np.append(End, 9999)
            
        
        if len(Start) > 0:
           
            # If period is longer than 1 year it is a perennial crop
            End_4_Perennial = np.where(End==9999, np.argwhere(Values==1)[-1], End)
            Season_Amount_Decades = End_4_Perennial - Start 
            
            # If two seasons in a row is lower than .... combine season
            Short_Season = np.where(Season_Amount_Decades<7, 1, 0)
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
                Short_Season = np.where(Season_Amount_Decades<7, 1, 0)
                dist_right = Start - np.append(Start[1:], 0)
                dist_left = np.append(0, Start[:-1]) - Start  
                
            # If periods are small merge datasets that are close together
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
            Long_Season = np.where(Season_Amount_Decades>36, 1, 0)
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









"""

import matplotlib as plt
plt.pyplot.plot(range(0, len(Ts)), Ts[:])
plt.pyplot.plot(range(0, len(Ts_MW)), Ts_MW[:])

for End_point in End:
    plt.pyplot.plot(End_point, Ts[int(End_point)], "r", marker='o', markersize=12)
for Start_point in Start:
    plt.pyplot.plot(Start_point, Ts[int(Start_point)], "g", marker='o', markersize=8)
for End_point in End_Per:
    plt.pyplot.plot(End_point, Ts[int(End_point)], "y", marker='o', markersize=15)
for Start_point in Start_Per:
    plt.pyplot.plot(Start_point, Ts[int(Start_point)], "c", marker='o', markersize=15)

"""


 