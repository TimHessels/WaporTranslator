# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 16:38:09 2019
"""
import os
import sys
import glob
import numpy as np
import watertools
import WaporTranslator.LEVEL_2.Functions as Functions

def main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim, Radiation_Data, METEO_timestep):

    if METEO_timestep == "Monthly":    
        Start_year_analyses_adj = int(Start_year_analyses)
    
    if METEO_timestep == "Daily":       
        if Radiation_Data == "LANDSAF":
            Start_year_analyses_adj = np.maximum(int(Start_year_analyses), 2016)
        elif Radiation_Data == "KNMI":
            Start_year_analyses_adj = np.maximum(int(Start_year_analyses), 2017)   
            input_folder_KNMI = os.path.join(output_folder_L1, "MSGCPP", "SDS", "daily")
            os.chdir(input_folder_KNMI)
            files_KNMI = glob.glob("SDS_MSGCPP_W-m-2_daily_%s.01.01.tif" %Start_year_analyses)
            if len(files_KNMI) > 0:
                Start_year_analyses_adj = int(Start_year_analyses)
          
        else:
            print("Choose for Radiation input LANDSAF or KNMI")

    # Find dates
    dates_dek = Functions.Get_Dekads(Start_year_analyses_adj, End_year_analyses)

    i = 1
    for Date in dates_dek:

        sys.stdout.write("\rDownload MODIS ALBEDO %i/%i (%f %%)" %(i,len(dates_dek), i/(len(dates_dek)) * 100))
        sys.stdout.flush()

        # Get Date range
        Startdate = "%d-%02d-%02d" %(Date.year, Date.month, Date.day)
        Enddate = "%d-%02d-%02d" %(Date.year, Date.month, Date.day)
        
        # Download albedo data
        watertools.Collect.MCD43.Albedo_daily(output_folder_L1, Startdate, Enddate, latlim, lonlim, Waitbar = 0)
        i += 1
    
    return()
    
