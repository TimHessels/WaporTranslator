# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:47:00 2019

@author: timhe
"""
import os
import glob
import gdal
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

import watertools
import watertools.General.data_conversions as DC

def main(output_folder_L1, End_year_analyses, latlim, lonlim, cores):

    # Get Date range
    Startdate = "%s-01-01" %End_year_analyses
    Enddate = "%s-12-31" %End_year_analyses
    Dates = pd.date_range(Startdate, Enddate, freq = "D")
    
    print("Downloading MSGCPP data from KNMI")
    
    output_folder_knmi = os.path.join(output_folder_L1, "MSGCPP", "SDS", "15min")
    if not os.path.exists(output_folder_knmi):
        os.makedirs(output_folder_knmi)
        
    output_folder_knmi_daily = os.path.join(output_folder_L1, "MSGCPP", "SDS", "daily")
    if not os.path.exists(output_folder_knmi_daily):
        os.makedirs(output_folder_knmi_daily)   

    # Download required GLDAS data    
    Parallel(n_jobs=cores)(delayed(Download_MSGCPP_Parallel)(Date, output_folder_L1, latlim, lonlim)
                                             for Date in Dates)
    
    for Date in Dates:
        Calc_daily_radiation(output_folder_knmi, output_folder_knmi_daily, Date)
    
    return()
    
def Download_MSGCPP_Parallel(Date, output_folder_L1, latlim, lonlim):
    
    Startdate = Date
    Enddate = Date
    watertools.Collect.MSGCPP.SDS(output_folder_L1, Startdate, Enddate, latlim, lonlim, Waitbar = 0)

def Calc_daily_radiation(folder_in, folder_out, Date):

    filename_trans = "SDS_MSGCPP_W-m-2_15min_%d.%02d.%02d_H{hour}.M{minutes}.tif"  %(Date.year, Date.month, Date.day)
    filename_trans_out = "SDS_MSGCPP_W-m-2_daily_%d.%02d.%02d.tif" %(Date.year, Date.month, Date.day)           
    
    os.chdir(folder_in)
    files = glob.glob(filename_trans.format(hour = "*", minutes = "*"))
    i = 0
    
    # Open all the 15 minutes files
    for file in files:
        file_in = os.path.join(folder_in, file)
        destswgone = gdal.Open(file_in)
        try:
            swgnet_one = destswgone.GetRasterBand(1).ReadAsArray()
            swgnet_one[swgnet_one<0] = 0                 
            if not "geo_trans" in locals():
                swgnet = np.ones([destswgone.RasterYSize, destswgone.RasterXSize, len(files)]) * np.nan
                geo_trans = destswgone.GetGeoTransform()
                proj_trans = destswgone.GetProjection()
            swgnet[:,:,i] = swgnet_one
        except:
            pass
        i+=1 
        
    # Calculate the daily mean     
    swgnet_mean = np.nansum(swgnet, 2)/(24*4)
    
    Dir_trans_out = os.path.join(folder_out, filename_trans_out)
    
    DC.Save_as_tiff(Dir_trans_out, swgnet_mean, geo_trans, proj_trans)
    
    return()   
