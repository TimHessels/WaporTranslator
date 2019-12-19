# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Thu Oct  3 18:43:59 2019
"""

import os
import sys
import gdal
import datetime
import numpy as np

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

class Rasterdata_tiffs:
    
    # Basic Raster Data
    Projection = []
    Size = []
    GeoTransform = []
    Data = []
    ScaleFactor = []
    NoData = []
    Ordinal_time = []

    # Origin Of Data
    Directory = ''
    Format = ''

    # Describtion of dataset
    Variable = ''
    Product = ''
    Description = ''
    Unit = ''
    Dimension_description = ''
    Conversion_rate = ''
    
    # Time Series
    Startdate = ''
    Enddate = ''    
    Timestep = ''
    
    def __init__(self, input_folder, input_format, Dates = None, Conversion = 1, Example_Data = None, Mask_Data = None, gap_filling = None, reprojection_type = 2, Variable = '', Product = '', Description = '', Unit = '', Dimension_description = ''):

        if Mask_Data != None:
            dest_MASK = RC.reproject_dataset_example(Mask_Data, Example_Data, 1)
            MASK = dest_MASK.GetRasterBand(1).ReadAsArray()
            MASK = np.where(MASK==1, 1, np.nan)
        else:
            MASK = 1
        
        if Dates != None: 
            
            # Get Ordinal time
            time_or = np.array(list(map(lambda i : i.toordinal(), Dates)))
            i = 1
            
            # Define start and enddate string
            Startdate_str = '%d-%02d-%02d' %(Dates[0].year, Dates[0].month, Dates[0].day)
            Enddate_str = '%d-%02d-%02d' %(Dates[-1].year, Dates[-1].month, Dates[-1].day) 
            
            # Define dimensions
            size_z = len(Dates)

            for Date in Dates:
                try:
                    sys.stdout.write("\rLoading Data %s %i/%i (%f %%)" %(Variable, i, len(Dates), i/(len(Dates)) * 100))
                    sys.stdout.flush()
        
                    # Create input filename
                    filename_in = os.path.join(input_folder, input_format.format(yyyy = Date.year, mm = Date.month, dd = Date.day))
                    
                    dest, Array, proj, geo = Get_Data(filename_in, Example_Data, reprojection_type)
                    
                    if Date == Dates[0]:
                        size_x = dest.RasterXSize
                        size_y = dest.RasterYSize
                        proj = dest.GetProjection()
                        geo = dest.GetGeoTransform()            
                        Array_end = np.ones([len(Dates), size_y, size_x]) * np.nan
                        
                    if gap_filling != None and ~np.isnan(np.nanmean(Array)):   
                        Array[np.isnan(Array)] = -9999
                        Array = RC.gap_filling(Array, -9999, gap_filling)
                        
                    Array_end[time_or==Date.toordinal(), :, : ] = Array * Conversion * MASK    
                    i += 1
                except:
                    print("Was not able to collect %s %s" %(Variable, Date))
                
            shape = [size_z, size_y, size_x]
                        
                
        else:
            
            sys.stdout.write("\rLoading Constant Data %s" %(Variable))
            sys.stdout.flush()
            
            # Define start and enddate string
            Startdate_str = ''
            Enddate_str = ''
            
            # Get constant data
            filename_in = os.path.join(input_folder, input_format)
            dest, Array_end, proj, geo = Get_Data(filename_in, Example_Data, reprojection_type)   
            
            # Get dimension
            size_x = dest.RasterXSize
            size_y = dest.RasterYSize
            shape = [size_y, size_x]
            time_or = ''
            
            # Apply gapfilling if needed
            if gap_filling != None and ~np.isnan(np.nanmean(Array_end)):     
                Array_end[np.isnan(Array_end)] = -9999
                Array_end = RC.gap_filling(Array_end, -9999, gap_filling)
            Array_end = Array_end * MASK
            
        self.Projection = proj
        self.Size = shape
        self.GeoTransform = geo
        self.Data = Array_end.astype(np.float64)
        self.NoData = np.nan
        self.Ordinal_time = time_or
    
        # Origin Of Data
        self.Directory = input_folder
        self.Format = input_format
    
        # Describtion of dataset
        self.Variable = Variable
        self.Product = Product
        self.Description = Description
        self.Unit = Unit
        self.Dimension_description = Dimension_description
        
        # Time Series
        self.Startdate = Startdate_str
        self.Enddate = Enddate_str  
        self.Timestep = ''            
        print("                                                                                                                      ")
           
    def Save_As_Tiff(self, output_folder):
                
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        Dates = self.Ordinal_time
        geo = self.GeoTransform
        proj = self.Projection
        Data = self.Data
        Variable = self.Variable
        Unit = self.Unit
        
        print("Save %s as tiff file in %s" %(Variable, output_folder))
        
        if Dates == "Long_Term_Decade":
            
            import WaporTranslator.LEVEL_2.Functions as Functions
            
            Dates_dek = Functions.Get_Dekads(2009, 2009)
            
            i = 0
            for Date in Dates_dek:
                
                try:
                    output_filename = os.path.join(output_folder, "%s_%s_%02d.%02d.tif" %(Variable.replace(" ", "_"), Unit, Date.month, Date.day))
                    Data_one = Data[i, :, :]  
                    DC.Save_as_tiff(output_filename, Data_one, geo, proj)  
                    i += 1
                    
                except:
                    print("Was not able to collect %s %s" %(Variable, Date))
                        
        elif np.any(Dates != None):
            for Date in Dates:
                
                Date_datetime = datetime.datetime.fromordinal(Date)
                output_filename = os.path.join(output_folder, "%s_%s_%d.%02d.%02d.tif" %(Variable.replace(" ", "_"), Unit, Date_datetime.year, Date_datetime.month, Date_datetime.day))
                Data_one = np.squeeze(Data[Dates==Date, :, :],0)
                DC.Save_as_tiff(output_filename, Data_one, geo, proj)
         
        else:
            output_filename = os.path.join(output_folder, "%s_%s.tif" %(Variable.replace(" ", "_"), Unit))
            DC.Save_as_tiff(output_filename, Data, geo, proj)  
            
class Rasterdata_Empty:
    
    # Basic Raster Data
    Projection = []
    Size = []
    GeoTransform = []
    Data = []
    ScaleFactor = []
    NoData = []
    Ordinal_time = []

    # Origin Of Data
    Directory = ''
    Format = ''

    # Describtion of dataset
    Variable = ''
    Product = ''
    Description = ''
    Unit = ''
    Dimension_description = ''
    Conversion_rate = ''
    
    # Time Series
    Startdate = ''
    Enddate = ''    
    Timestep = ''     
           
    def Save_As_Tiff(self, output_folder):
                
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        Dates = self.Ordinal_time
        geo = self.GeoTransform
        proj = self.Projection
        Data = self.Data.astype(np.float64)
        Variable = self.Variable
        Unit = self.Unit
        
        print("Save %s as tiff file in %s" %(Variable, output_folder))
        
        if Dates == "Long_Term_Decade":
            
            import WaporTranslator.LEVEL_2.Functions as Functions
            
            Dates_dek = Functions.Get_Dekads(2009, 2009)
            
            i = 0
            for Date in Dates_dek:
                
                output_filename = os.path.join(output_folder, "%s_%s_%02d.%02d.tif" %(Variable.replace(" ", "_"), Unit, Date.month, Date.day))
                Data_one = Data[i, :, :]  
                DC.Save_as_tiff(output_filename, Data_one, geo, proj)  
                i += 1
                        
        elif np.any(Dates != None):
            for Date in Dates:
                
                Date_datetime = datetime.datetime.fromordinal(Date)
                output_filename = os.path.join(output_folder, "%s_%s_%d.%02d.%02d.tif" %(Variable.replace(" ", "_"), Unit, Date_datetime.year, Date_datetime.month, Date_datetime.day))
                Data_one = np.squeeze(Data[Dates==Date, :, :],0)
                DC.Save_as_tiff(output_filename, Data_one, geo, proj)
         
        else:
            output_filename = os.path.join(output_folder, "%s_%s.tif" %(Variable.replace(" ", "_"), Unit))
            DC.Save_as_tiff(output_filename, Data, geo, proj)  
                
    
def Get_Data(filename_in, Example_Data, reprojection_type):
    
    if Example_Data == None:
        dest = gdal.Open(filename_in)
        proj = dest.GetProjection()
        geo = dest.GetGeoTransform()
        band = dest.GetRasterBand(1)
        NDV = band.GetNoDataValue()
        Array = dest.GetRasterBand(1).ReadAsArray()
        Array = np.float_(Array)
        Array[Array == NDV] = np.nan
                   
    else:
        dest_br = gdal.Open(filename_in)
        band = dest_br.GetRasterBand(1)
        NDV = band.GetNoDataValue()
        Array = band.ReadAsArray()
        Array = np.float_(Array)
        Array[Array == NDV] = np.nan
        Array_NDV = np.where(Array == NDV, 0, 1)
        proj_br = dest_br.GetProjection()
        geo_br = dest_br.GetGeoTransform()
        destNDV = DC.Save_as_MEM(Array_NDV, geo_br, proj_br)
        destArray = DC.Save_as_MEM(Array, geo_br, proj_br)         
        dest_NDV_rep = RC.reproject_dataset_example(destNDV, Example_Data, 1)
        dest = RC.reproject_dataset_example(destArray, Example_Data, reprojection_type)   
        proj = dest.GetProjection()
        geo = dest.GetGeoTransform()           
        Array = dest.GetRasterBand(1).ReadAsArray()          
        ArrayNDV = dest_NDV_rep.GetRasterBand(1).ReadAsArray()            
        Array = np.float_(Array)
        Array[ArrayNDV == 0] = np.nan                
                
    return(dest, Array, proj, geo)
            
            
             
            
    
    