# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 16:38:09 2019
"""
import sys
import numpy as np
import watertools
import WaporTranslator.LEVEL_2.Functions as Functions

def main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim):

    Start_year_analyses = np.maximum(Start_year_analyses, 2016)
    
    # Find dates
    dates_dek = Functions.Get_Dekads(Start_year_analyses, End_year_analyses)

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
    
