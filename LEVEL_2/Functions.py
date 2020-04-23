# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Thu Oct  3 18:40:38 2019
"""

import os
import sys
import gdal
import calendar
import datetime
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

def Calc_Dekads_from_Daily(DataCube_in, flux_state = "flux"):
    
    import WaporTranslator.LEVEL_1.DataCube as DataCube
    
    # Get the timesteps of the dekads and the daily
    Time = DataCube_in.Ordinal_time
    
    # Open data
    Data_array = DataCube_in.Data
    
    # Find dekades dates
    Dates_dek = Get_Dekads(str(datetime.datetime.fromordinal(Time[0]).year), str(datetime.datetime.fromordinal(Time[-1]).year))
    
    # Define the output array
    Data_out = np.ones([len(Dates_dek), DataCube_in.Size[1], DataCube_in.Size[2]]) * np.nan
    
    Counter = 1
    for Date_dek in Dates_dek:

        sys.stdout.write("\rCreate Daily %s %i/%i (%f %%)" %(DataCube_in.Variable, Counter, len(Dates_dek), Counter/(len(Dates_dek)) * 100))
        sys.stdout.flush()

        # date in dekad
        day_dekad = int("%d" %int(np.minimum(int(("%02d" %int(str(Date_dek.day)))[0]), 2)))
        year = Date_dek.year
        month = Date_dek.month    
        
        # Get end date day of dekad
        if day_dekad == 2:
            End_day_dekad= calendar.monthrange(year, month)[1]
        else:
            End_day_dekad = int(str(int(day_dekad)) + "1")  + 9
            
        Startdate_or = Date_dek.toordinal()
        Enddate_or = datetime.datetime(year, month, End_day_dekad).toordinal()
        
        Time_good = np.where(np.logical_and(Time >= Startdate_or, Time <= Enddate_or), True, False)
        
        Array_dek = Data_array[Time_good, :, :]
        
        if flux_state == "flux":
            Data_out[int(Counter - 1), :, :] = np.nansum(Array_dek, axis = 0)
        if flux_state == "state":  
            Data_out[int(Counter - 1), :, :] = np.nanmean(Array_dek, axis = 0)  
            
        Counter += 1    
        
    DataCube_out = DataCube.Rasterdata_Empty()
    DataCube_out.Data = Data_out
    DataCube_out.GeoTransform = DataCube_in.GeoTransform
    DataCube_out.Projection = DataCube_in.Projection
    DataCube_out.Size = [len(Dates_dek), DataCube_in.Size[1], DataCube_in.Size[2]]
    DataCube_out.GeoTransform = DataCube_in.GeoTransform
    DataCube_out.NoData = np.nan
    DataCube_out.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_dek)))     
    DataCube_out.Variable = DataCube_in.Variable
    
    print("                                                                                                                      ")
        
    return(DataCube_out)         

def Calc_Dekads_from_Monthly(DataCube_in):
    
    import WaporTranslator.LEVEL_1.DataCube as DataCube
    
    # Get the timesteps of the dekads and the monthly
    Time_monthly = DataCube_in.Ordinal_time
    Time = Get_Dekads(datetime.datetime.fromordinal(Time_monthly[0]).year, datetime.datetime.fromordinal(Time_monthly[-1]).year)
    Time = np.array(list(map(lambda i : i.toordinal(), Time)))
    
    # Create empty array
    Data_out = np.ones([len(Time_monthly) * 3, DataCube_in.Size[1], DataCube_in.Size[2]]) * np.nan
    
    Counter = 1
    
    for i in range(0, DataCube_in.Size[1]):
        for j in range(0, DataCube_in.Size[2]):
            
            sys.stdout.write("\rCreate Dekads %s %i/%i (%f %%)" %(DataCube_in.Variable, Counter, (DataCube_in.Size[1] * DataCube_in.Size[2]), Counter/(DataCube_in.Size[1] * DataCube_in.Size[2]) * 100))
            sys.stdout.flush()

            x = np.append(Time_monthly, Time[-1])
            y = np.append(DataCube_in.Data[:,i,j], DataCube_in.Data[-1,i,j])
            try:
                f2 = interp1d(x, y, kind='linear')
                inter = f2(Time)
            except:
                inter = np.ones(len(Time)) * np.nan
                
            Data_out[:,i,j] = inter
            Counter += 1
    
    DataCube_out = DataCube.Rasterdata_Empty()
    DataCube_out.Data = Data_out
    DataCube_out.Projection = DataCube_in.Projection
    DataCube_out.Size = [len(Time), DataCube_in.Size[1], DataCube_in.Size[2]]
    DataCube_out.GeoTransform = DataCube_in.GeoTransform
    DataCube_out.NoData = np.nan
    DataCube_out.Ordinal_time = Time

    # Origin Of Data
    DataCube_out.Directory = ''
    DataCube_out.Format = ''

    # Describtion of dataset
    DataCube_out.Variable = DataCube_in.Variable
    DataCube_out.Product = DataCube_in.Product
    DataCube_out.Description = DataCube_in.Description
    DataCube_out.Unit = DataCube_in.Unit
    DataCube_out.Dimension_description = DataCube_in.Dimension_description
    
    # Time Series
    DataCube_out.Startdate = '%d-%02d-%02d' %(datetime.datetime.fromordinal(Time[0]).year, datetime.datetime.fromordinal(Time[0]).month, datetime.datetime.fromordinal(Time[0]).day)
    DataCube_out.Enddate = '%d-%02d-%02d' %(datetime.datetime.fromordinal(Time[-1]).year, datetime.datetime.fromordinal(Time[-1]).month, datetime.datetime.fromordinal(Time[-1]).day)   
    DataCube_out.Timestep = ''    

    print("                                                                                                                      ")
            
    return(DataCube_out)            


def Calc_Daily_from_Dekads(DataCube_in):
    
    import WaporTranslator.LEVEL_1.DataCube as DataCube
    
    # Get the timesteps of the dekads and the daily
    Time = DataCube_in.Ordinal_time
    Time_day = np.array(list(range(Time[0], Time[-1] + 11)))
    
    # Create empty array
    Data_out = np.ones([len(Time_day), DataCube_in.Size[1], DataCube_in.Size[2]]) * np.nan
    
    Counter = 1
    
    for i in range(0, DataCube_in.Size[1]):
        for j in range(0, DataCube_in.Size[2]):
            
            sys.stdout.write("\rCreate Daily %s %i/%i (%f %%)" %(DataCube_in.Variable, Counter, (DataCube_in.Size[1] * DataCube_in.Size[2]), Counter/(DataCube_in.Size[1] * DataCube_in.Size[2]) * 100))
            sys.stdout.flush()

            x = np.append(Time, Time_day[-1])
            y = np.append(DataCube_in.Data[:,i,j], DataCube_in.Data[-1,i,j])
            try:
                f2 = interp1d(x, y, kind='linear')
                inter = f2(Time_day)
            except:
                inter = np.ones(len(Time_day)) * np.nan
                
            Data_out[:,i,j] = inter
            Counter += 1
    
    DataCube_out = DataCube.Rasterdata_Empty()
    DataCube_out.Data = Data_out
    DataCube_out.Projection = DataCube_in.Projection
    DataCube_out.Size = [len(Time_day), DataCube_in.Size[1], DataCube_in.Size[2]]
    DataCube_out.GeoTransform = DataCube_in.GeoTransform
    DataCube_out.NoData = np.nan
    DataCube_out.Ordinal_time = Time_day

    # Origin Of Data
    DataCube_out.Directory = ''
    DataCube_out.Format = ''

    # Describtion of dataset
    DataCube_out.Variable = DataCube_in.Variable
    DataCube_out.Product = DataCube_in.Product
    DataCube_out.Description = DataCube_in.Description
    DataCube_out.Unit = DataCube_in.Unit
    DataCube_out.Dimension_description = DataCube_in.Dimension_description
    
    # Time Series
    DataCube_out.Startdate = '%d-%02d-%02d' %(datetime.datetime.fromordinal(Time_day[0]).year, datetime.datetime.fromordinal(Time_day[0]).month, datetime.datetime.fromordinal(Time_day[0]).day)
    DataCube_out.Enddate = '%d-%02d-%02d' %(datetime.datetime.fromordinal(Time_day[-1]).year, datetime.datetime.fromordinal(Time_day[-1]).month, datetime.datetime.fromordinal(Time_day[-1]).day)   
    DataCube_out.Timestep = ''    

    print("                                                                                                                      ")
            
    return(DataCube_out)            
                    
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

                   
def Convert_Dekads_to_Monthly(input_folder, input_format, output_folder, output_format, Startdate, Enddate, flux_state = "flux"):    
    
    # Define dates
    Dates = pd.date_range(Startdate, Enddate, freq = "MS")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for date in Dates:
        
        year = date.year
        month = date.month
        day = date.day
        
        Dates_dek = []
        Dates_dek.append(datetime.datetime(date.year, date.month, 1))
        Dates_dek.append(datetime.datetime(date.year, date.month, 11))
        Dates_dek.append(datetime.datetime(date.year, date.month, 21))
        
        output_filename = os.path.join(output_folder, output_format.format(yyyy=year, mm=month, dd=day))
        
        if "Array_End" in locals():
            del Array_End
            
        i = 0
        
        for date_dek in Dates_dek:
                
            year_dek = date_dek.year
            month_dek = date_dek.month
            day_dek = date_dek.day    
            
            dest = gdal.Open(os.path.join(input_folder, input_format.format(yyyy=year_dek, mm=month_dek, dd=day_dek)))
            Array_one = dest.GetRasterBand(1).ReadAsArray()
            
            if day_dek == 1:
                
                Array_End = np.ones([3, Array_one.shape[0], Array_one.shape[1]]) * np.nan
                geo = dest.GetGeoTransform()
                proj = dest.GetProjection()
                
            Array_End[i, :, :] = Array_one
            i+=1
            
        if flux_state == "state":
            Array_month = np.nanmean(Array_End, axis = 0)
        
        if flux_state == "flux":
            Array_month = np.nansum(Array_End, axis = 0)    
             
        DC.Save_as_tiff(output_filename, Array_month, geo, proj)
    
    return()



def Get_Dekads(Start_year_analyses, End_year_analyses):
    
    # Get dekads time steps
    Startdate_Year = "%s-01-01" %Start_year_analyses
    Enddate_Year = "%s-12-31" %End_year_analyses
    
    # Define dates
    Dates = pd.date_range(Startdate_Year, Enddate_Year, freq = "MS")

    Dates_dek = []
    # Define decade dates
    for Date in Dates:
        Dates_dek.append(datetime.datetime(Date.year, Date.month, 1))
        Dates_dek.append(datetime.datetime(Date.year, Date.month, 11))
        Dates_dek.append(datetime.datetime(Date.year, Date.month, 21))

    return(Dates_dek)