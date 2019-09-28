# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sat Sep 28 11:51:01 2019
"""
import datetime
import pandas as pd
import WaporAPI

def main(output_folder_L1, Date, latlim, lonlim, API_WAPOR_KEY):
    
    Startdate_10Y = "%d-01-01" %(int(Date.split("-")[0]) - 9)
    Enddate_10Y = datetime.datetime.strptime(Date, "%Y-%m-%d") + pd.DateOffset(days = 11)
    
    # Download 10 year data
    Parameters_10Y = ["L2_NPP_D", "L2_T_D", "L2_AETI_D", "L1_RET_D", "L2_LCC_A"]
    
    for Parameter_10Y in Parameters_10Y:

        WaporAPI.Collect.WAPOR(output_folder_L1, Startdate_10Y, Enddate_10Y, latlim, lonlim, API_WAPOR_KEY, Parameter_10Y)
    
    # Download 1 dekades    
    Parameters_D = ["L2_T_D", "L2_I_D", "L2_E_D", "L1_PCP_D"]
    
    Startdate_D = Date
    Enddate_D = Date
    
    for Parameter_D in Parameters_D:

        WaporAPI.Collect.WAPOR(output_folder_L1, Startdate_D, Enddate_D, latlim, lonlim, API_WAPOR_KEY, Parameter_D)
        
    return()