# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 13:48:19 2019
"""

import os
import gdal
import pandas as pd
import numpy as np
from joblib import Parallel, delayed

import watertools
import watertools.General.data_conversions as DC

def main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim, cores, Radiation_Data, method = "Daily"):

    # Get Date range
    Startdate = "%s-01-01" %Start_year_analyses
    Enddate = "%s-12-31" %End_year_analyses
    if method == "Daily":
        Dates = pd.date_range(Startdate, Enddate, freq = "D")
        if Radiation_Data == "GLDAS":
             Vars = ['tair_f_inst', 'wind_f_inst', 'qair_f_inst', 'psurf_f_inst', 'swdown_f_tavg']   
        else:
             Vars = ['tair_f_inst', 'wind_f_inst', 'qair_f_inst', 'psurf_f_inst']   
            
            
    if method == "Monthly": 
        Dates = pd.date_range(Startdate, Enddate, freq = "MS")
        Vars = ['tair_f_inst', 'wind_f_inst', 'qair_f_inst', 'psurf_f_inst', 'swdown_f_tavg']           
 
    print("Downloading METEO data from GLDAS")

    # Download required GLDAS data    
    Parallel(n_jobs=cores)(delayed(Download_GLDAS_Parallel)(Var, output_folder_L1, Startdate, Enddate, latlim, lonlim, method)
                                             for Var in Vars)
           
    # Create folder for relative humidity
    output_dir = os.path.join(output_folder_L1, "Weather_Data", "Model", "GLDAS", method.lower(), "hum_f_inst", "mean")
        
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Calculate Humidity
    for Date_one in Dates:
        output_filename = os.path.join(output_dir, "Hum_GLDAS-NOAH_percentage_%s_%d.%02d.%02d.tif" %(method.lower(), Date_one.year, Date_one.month, Date_one.day))
        if not os.path.exists(output_filename):
            Calc_Humidity(output_folder_L1, output_filename, method)
        
    return()
    
def Download_GLDAS_Parallel(Var, output_folder_L1, Startdate, Enddate, latlim, lonlim, method):
    
    Var_array = ["%s" %Var]
    if method == "Daily":
        watertools.Collect.GLDAS.daily(output_folder_L1, Var_array, Startdate, Enddate, latlim, lonlim, Waitbar = 0)
    if method == "Monthly":
        watertools.Collect.GLDAS.monthly(output_folder_L1, Var_array, Startdate, Enddate, latlim, lonlim, Waitbar = 0)    

def Calc_Humidity(output_folder_L1, output_filename, method):
    
    # find date
    year = int((output_filename.split("_")[-1]).split(".")[0])
    month = int((output_filename.split("_")[-1]).split(".")[1])
    day = int((output_filename.split("_")[-1]).split(".")[2])
    
    if method == "Daily":
    
        # find paths
        file_t = os.path.join(output_folder_L1, "Weather_Data", "Model", "GLDAS", method.lower(), "tair_f_inst", "mean", "Tair_GLDAS-NOAH_C_%s_%d.%02d.%02d.tif" %(method.lower(), year, month, day))
        file_h = os.path.join(output_folder_L1, "Weather_Data", "Model", "GLDAS", method.lower(), "qair_f_inst", "mean", "Hum_GLDAS-NOAH_kg-kg_%s_%d.%02d.%02d.tif" %(method.lower(), year, month, day))
        file_p = os.path.join(output_folder_L1, "Weather_Data", "Model", "GLDAS", method.lower(), "psurf_f_inst", "mean", "P_GLDAS-NOAH_kpa_%s_%d.%02d.%02d.tif" %(method.lower(), year, month, day))
    
    if method == "Monthly":
    
        # find paths
        file_t = os.path.join(output_folder_L1, "Weather_Data", "Model", "GLDAS", method.lower(), "tair_f_inst", "Tair_GLDAS-NOAH_C_%s_%d.%02d.%02d.tif" %(method.lower(), year, month, day))
        file_h = os.path.join(output_folder_L1, "Weather_Data", "Model", "GLDAS", method.lower(), "qair_f_inst", "Hum_GLDAS-NOAH_kg-kg_%s_%d.%02d.%02d.tif" %(method.lower(), year, month, day))
        file_p = os.path.join(output_folder_L1, "Weather_Data", "Model", "GLDAS", method.lower(), "psurf_f_inst", "P_GLDAS-NOAH_kpa_%s_%d.%02d.%02d.tif" %(method.lower(), year, month, day))

    # Open paths
    destt = gdal.Open(file_t)
    desth = gdal.Open(file_h)  
    destp = gdal.Open(file_p)  
   
    # Get Geo information
    geo = destt.GetGeoTransform()
    proj = destt.GetProjection()
    
    # Open Arrays
    Array_T = destt.GetRasterBand(1).ReadAsArray()
    Array_H = desth.GetRasterBand(1).ReadAsArray()    
    Array_P = destp.GetRasterBand(1).ReadAsArray()    
    Array_T[Array_T==-9999] = np.nan
    Array_H[Array_H==-9999] = np.nan    
    Array_P[Array_P==-9999] = np.nan       
    
    # Calculate relative humidity
    ESArray = 0.6108 * np.exp((17.27*Array_T)/(Array_T+237.3))
    RHarray = np.minimum((1.6077717*Array_H * Array_P/ESArray),1)*100
    
    # Save array
    DC.Save_as_tiff(output_filename, RHarray, geo, proj)

    return()

        