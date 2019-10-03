# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 18:08:02 2019
"""

import os
import gdal
import calendar
import datetime
import numpy as np
import pandas as pd

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC


def Calc_Land_Surface_Emissivity(output_folder_L2, Date):
    
    # Get dates
    Dates_dek = Get_Dekads(Date)
    
    # Create output folder for Land_Surface_Emissivity
    output_folder_Land_Surface_Emissivity = os.path.join(output_folder_L2, "Land_Surface_Emissivity")
    if not os.path.exists(output_folder_Land_Surface_Emissivity):
        os.makedirs(output_folder_Land_Surface_Emissivity)

    for Date_one in Dates_dek:
            
        # Define output file
        filename_out = os.path.join(output_folder_Land_Surface_Emissivity, "Land_Surface_Emissivity_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames
            filelai = os.path.join(output_folder_L2, "LAI", "LAI_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))
            
            # Open required files
            destlai = gdal.Open(filelai)
     
            # Get georeference
            geo = destlai.GetGeoTransform()
            proj = destlai.GetProjection()
               
            # Open Arrays
            LAI = destlai.GetRasterBand(1).ReadAsArray()      
            
            # Calculate Land Surface Emissivity
            Land_Surface_Emissivity = np.minimum(1, 0.92 + 0.016 * LAI)
            Land_Surface_Emissivity = Land_Surface_Emissivity.clip(0, 1.0)
            
            # Save result
            DC.Save_as_tiff(filename_out, Land_Surface_Emissivity, geo, proj)
        
    return()
    
def Calc_Net_Radiation(output_folder_L2, Date, example_file):
    
    # Get dates
    Dates_dek = Get_Dekads(Date)
    
    # Create output folder for Net_Radiation
    output_folder_Net_Radiation = os.path.join(output_folder_L2, "Net_Radiation")
    if not os.path.exists(output_folder_Net_Radiation):
        os.makedirs(output_folder_Net_Radiation)

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
        
    for Date_one in Dates_dek:
                    
        # Define output file
        filename_out = os.path.join(output_folder_Net_Radiation, "Net_Radiation_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames that are already dekades
            filet = os.path.join(input_folder_L1, "Weather_Data", "Model", "GLDAS", "daily", "tair_f_inst", "mean", "Tair_GLDAS-NOAH_C_daily_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))
            filelse = os.path.join(output_folder_L2, "Land_Surface_Emissivity", "Land_Surface_Emissivity_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))

            # define format of daily required datasets
            input_folder_alb = os.path.join(input_folder_L1, "Albedo", "MCD43")
            input_folder_dslf = os.path.join(input_folder_L1, "LANDSAF", "DSLF")            
            input_folder_dssf = os.path.join(input_folder_L1, "LANDSAF", "DSSF")           
            filealb_format = "Albedo_MCD43A3_-_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"
            filedslf_format = "DSLF_LSASAF_MSG_{yyyy}.{mm:02d}.{dd:02d}.tif"
            filedssf_format = "DSSF_LSASAF_MSG_{yyyy}.{mm:02d}.{dd:02d}.tif"
            
            # Get dekad dataset
            filealb = Calc_Dekad_Raster_from_Daily(input_folder_alb, filealb_format, Date_one, flux_state = "state")
            filedslf = Calc_Dekad_Raster_from_Daily(input_folder_dslf, filedslf_format, Date_one, flux_state = "state")
            filedssf = Calc_Dekad_Raster_from_Daily(input_folder_dssf, filedssf_format, Date_one, flux_state = "state")
            
            # Open required files
            destt = RC.reproject_dataset_example(filet, example_file, 2)
            destalb = RC.reproject_dataset_example(filealb, example_file, 2)
            destdslf = RC.reproject_dataset_example(filedslf, example_file, 2)
            destdssf = RC.reproject_dataset_example(filedssf, example_file, 2)
            destlse = gdal.Open(filelse)
            
            # Get georeference
            geo = destt.GetGeoTransform()
            proj = destt.GetProjection()
               
            # Open Arrays
            T = destt.GetRasterBand(1).ReadAsArray()  
            Albedo = destalb.GetRasterBand(1).ReadAsArray()  
            DSLF = destdslf.GetRasterBand(1).ReadAsArray() 
            DSSF = destdssf.GetRasterBand(1).ReadAsArray() 
            Land_Surface_Emissivity = destlse.GetRasterBand(1).ReadAsArray()  
            
            # Convert to W/m2
            DSLF = DSLF/1e6
            DSSF = DSSF/1e6     
            
            # Fill in Albedo
            Albedo = RC.gap_filling(Albedo, 0)
            
            # Calculate Net Radiation
            Net_Radiation = (1-Albedo)*DSSF+DSLF-Land_Surface_Emissivity*0.0000000567*(273.15 + T)**4
            Net_Radiation = Net_Radiation.clip(0, 500)
            
            # Save result
            DC.Save_as_tiff(filename_out, Net_Radiation, geo, proj)
        
    return()     
    
    
def Calc_Evaporative_Fraction(output_folder_L2, Date, example_file):
    
    # Get dates
    Dates_dek = Get_Dekads(Date)
    
    # Create output folder for Evaporative_Fraction
    output_folder_Evaporative_Fraction = os.path.join(output_folder_L2, "Evaporative_Fraction")
    if not os.path.exists(output_folder_Evaporative_Fraction):
        os.makedirs(output_folder_Evaporative_Fraction)

    # Get folder L1
    input_folder_L1 = output_folder_L2.replace("LEVEL_2", "LEVEL_1")
        
    for Date_one in Dates_dek:
                   
        # Define output file
        filename_out = os.path.join(output_folder_Evaporative_Fraction, "Evaporative_Fraction_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))    
        
        if not os.path.exists(filename_out):
    
            # define required filenames
            fileet = os.path.join(input_folder_L1, "L2_AETI_D", "L2_AETI_D_WAPOR_DEKAD_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))
            filern = os.path.join(output_folder_L2, "Net_Radiation", "Net_Radiation_%d.%02d.%02d.tif" %(Date_one.year, Date_one.month, Date_one.day))

            # Open required files
            destet = RC.reproject_dataset_example(fileet, example_file, 2)
            destrn = RC.reproject_dataset_example(filern, example_file, 2)
            
            # Get georeference
            geo = destet.GetGeoTransform()
            proj = destet.GetProjection()
               
            # Open Arrays
            ET = destet.GetRasterBand(1).ReadAsArray()  
            Net_Radiation = destrn.GetRasterBand(1).ReadAsArray()  
            
            # Convert from WAPOR units to mm/day
            ET = ET/10
            
            # Calculate Evaporative Fraction
            Evaporative_Fraction = ET*28.4/Net_Radiation
            Evaporative_Fraction = Evaporative_Fraction.clip(0, 1.1)
            
            # Save result
            DC.Save_as_tiff(filename_out, Evaporative_Fraction, geo, proj)
        
    return()   

def Calc_Dekad_Raster_from_Daily(input_folder, input_format, Date, flux_state = "flux", example_file = None):    
    
    # Calculate the start and enddate of the decade
    Startdate = Date
    
    # date in dekad
    day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Startdate.day)))[0]), 2)))

    # Get end date day of dekad
    if day_dekad == 2:
        year = Startdate.year
        month = Startdate.month
        End_day_dekad= calendar.monthrange(year, month)[1]
    else:
        End_day_dekad = int(str(int(day_dekad)) + "1")  + 9

    # Set Dates
    Enddate = datetime.datetime(Startdate.year, Startdate.month, End_day_dekad)
    Dates = pd.date_range(Startdate, Enddate, freq = "D")
    i = 0
    
    for Date_one in Dates:
        
        if example_file == None:
            dest = gdal.Open(os.path.join(input_folder, input_format.format(yyyy=Date_one.year, mm = Date_one.month, dd = Date_one.day)))
        else:
            dest = RC.reproject_dataset_example(os.path.join(input_folder, input_format.format(yyyy=Date_one.year, mm = Date_one.month, dd = Date_one.day)), example_file, 2)
        
        if Date_one == Dates[0]:
            size_y = dest.RasterYSize
            size_x = dest.RasterXSize      
            geo = dest.GetGeoTransform()
            proj = dest.GetProjection()
            data = np.ones([len(Dates), size_y, size_x])
    
        array = dest.GetRasterBand(1).ReadAsArray()
        array = np.float_(array)
        array[array==-9999] = np.nan
        data[i, :, :] = array
        i += 1
       
    if flux_state == "flux":
        data = np.nansum(data, axis = 0)
    if flux_state == "state":  
        data = np.nanmean(data, axis = 0)        
 
    dest = DC.Save_as_MEM(data, geo, proj)
    
    return(dest)

def Get_Dekads(date):
    
    # Get Date
    Date_datetime = datetime.datetime.strptime(date, "%Y-%m-%d")
    
    # date in dekad
    day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date_datetime.day)))[0]), 2)))

    # date minus 1 and date plus 1 dekad
    offset_month_p1 = 0
    offset_month_m1 = 0
    day_dekad_m1 = day_dekad - 1   
    if day_dekad_m1<0:
        day_dekad_m1 = 2
        offset_month_m1 = 1    
    day_dekad_p1 = day_dekad + 1
    if day_dekad_p1>2:
        day_dekad_p1 = 0
        offset_month_p1 = 1
    
    # set dates dekads before and after after dekads    
    Date_datetime_m1 = datetime.datetime(Date_datetime.year, Date_datetime.month, int(str(str(day_dekad_m1)[0] + "1"))) - pd.DateOffset(months = offset_month_m1)
    Date_datetime_p1 = datetime.datetime(Date_datetime.year, Date_datetime.month, int(str(str(day_dekad_p1)[0] + "1"))) + pd.DateOffset(months = offset_month_p1)
    
    # Set start and enddate
    Dates = [Date_datetime_m1, pd.Timestamp(Date_datetime), Date_datetime_p1]

    return(Dates)