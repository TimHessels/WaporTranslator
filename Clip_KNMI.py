# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 12:20:43 2020

@author: timhe
"""
Startdate = "2005-01-01"
Enddate = "2005-05-01"
freq = "D" # of MS for monthly
Example_file = r"D:/Project_MetaMeta/LEVEL_1/MSGCPP/SDS/daily/SDS_MSGCPP_W-m-2_daily_2018.01.21.tif"
input_format = r"F:\MSGCPP_Daily\{yyyy}\SDS_MSGCPP_W-m-2_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"
output_format = r"D:\Project_MetaMeta_test\LEVEL_1\MSGCPP\SDS\daily\SDS_MSGCPP_W-m-2_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"

import os
import osr
import gdal
import pandas as pd

def main(Startdate, Enddate, freq, Example_file, input_format, output_format):
    
    output_dir = os.path.dirname(output_format)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    Dates = pd.date_range(Startdate, Enddate, freq = freq)  
    
    for date in Dates:
        print("Process %s" %date)
        
        year = date.year
        month = date.month
        day = date.day
        
        input_file = input_format.format(yyyy=year, mm=month, dd=day)
        
        dest_end = reproject_dataset_example(input_file, Example_file, method = 2)
        Array_rep = dest_end.GetRasterBand(1).ReadAsArray()
        geo_rep = dest_end.GetGeoTransform()
    
        output_filename = output_format.format(yyyy=year, mm=month, dd=day)
    
        Save_as_tiff(output_filename, Array_rep, geo_rep, 4326)
    
    return()
       
def Save_as_tiff(name='', data='', geo='', projection=''):
    """
    This function save the array as a geotiff

    Keyword arguments:
    name -- string, directory name
    data -- [array], dataset of the geotiff
    geo -- [minimum lon, pixelsize, rotation, maximum lat, rotation,
            pixelsize], (geospatial dataset)
    projection -- integer, the EPSG code
    """
    
    dir_name = os.path.dirname(name)
    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
    # save as a geotiff
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(name, int(data.shape[1]), int(data.shape[0]), 1, gdal.GDT_Float32, ['COMPRESS=LZW'])
    srse = osr.SpatialReference()
    if projection == '':
        srse.SetWellKnownGeogCS("WGS84")

    else:
        try:
            if not srse.SetWellKnownGeogCS(projection) == 6:
                srse.SetWellKnownGeogCS(projection)
            else:
                try:
                    srse.ImportFromEPSG(int(projection))
                except:
                    srse.ImportFromWkt(projection)
        except:
            try:
                srse.ImportFromEPSG(int(projection))
            except:
                srse.ImportFromWkt(projection)

    dst_ds.SetProjection(srse.ExportToWkt())
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    dst_ds.SetGeoTransform(geo)
    dst_ds.GetRasterBand(1).WriteArray(data)
    dst_ds = None
    return()
    

def Get_epsg(g, extension = 'tiff'):
    """
    This function reads the projection of a GEOGCS file or tiff file

    Keyword arguments:
    g -- string
        Filename to the file that must be read
    extension -- tiff or GEOGCS
        Define the extension of the dataset (default is tiff)
    """
    try:
        if extension == 'tiff':
            # Get info of the dataset that is used for transforming
            try:
                dest = gdal.Open(g)
            except:
                dest = g
            g_proj = dest.GetProjection()
            Projection=g_proj.split('EPSG","')
            epsg_to=int((str(Projection[-1]).split(']')[0])[0:-1])
                
        if extension == 'GEOGCS':
            Projection = g
            epsg_to=int((str(Projection).split('"EPSG","')[-1].split('"')[0:-1])[0])

    except:
        epsg_to=4326
        #print 'Was not able to get the projection, so WGS84 is assumed'
        
    return(epsg_to)

def reproject_dataset_example(dataset, dataset_example, method=1):
    """
    A sample function to reproject and resample a GDAL dataset from within
    Python. The user can define the wanted projection and shape by defining an example dataset.

    Keywords arguments:
    dataset -- 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(filename))
        string that defines the input tiff file or gdal file
    dataset_example -- 'C:/file/to/path/file.tif' or a gdal file (gdal.Open(filename))
        string that defines the input tiff file or gdal file
    method -- 1,2,3,4 default = 1
        1 = Nearest Neighbour, 2 = Bilinear, 3 = lanzcos, 4 = average
    """
    # open dataset that must be transformed
    try:
        if (os.path.splitext(dataset)[-1] == '.tif' or os.path.splitext(dataset)[-1] == '.TIF'):
            g = gdal.Open(dataset)
        else:
            g = dataset
    except:
            g = dataset
    epsg_from = Get_epsg(g)

    #exceptions
    if epsg_from == 9001:
        epsg_from = 5070

    # open dataset that is used for transforming the dataset
    try:
        if (os.path.splitext(dataset_example)[-1] == '.tif' or os.path.splitext(dataset_example)[-1] == '.TIF'):
            gland = gdal.Open(dataset_example)
            epsg_to = Get_epsg(gland)
        else:
            gland = dataset_example
            epsg_to = Get_epsg(gland)
    except:
            gland = dataset_example
            epsg_to = Get_epsg(gland)

    # Set the EPSG codes
    osng = osr.SpatialReference()
    osng.ImportFromEPSG(epsg_to)
    wgs84 = osr.SpatialReference()
    wgs84.ImportFromEPSG(epsg_from)

    # Get shape and geo transform from example
    geo_land = gland.GetGeoTransform()
    col=gland.RasterXSize
    rows=gland.RasterYSize

    # Create new raster
    mem_drv = gdal.GetDriverByName('MEM')
    dest1 = mem_drv.Create('', col, rows, 1, gdal.GDT_Float32)
    dest1.SetGeoTransform(geo_land)
    dest1.SetProjection(osng.ExportToWkt())

    # Perform the projection/resampling
    if method == 1:
        gdal.ReprojectImage(g, dest1, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_NearestNeighbour)
    if method == 2:
        gdal.ReprojectImage(g, dest1, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Bilinear)
    if method == 3:
        gdal.ReprojectImage(g, dest1, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Lanczos)
    if method == 4:
        gdal.ReprojectImage(g, dest1, wgs84.ExportToWkt(), osng.ExportToWkt(), gdal.GRA_Average)
        
    return(dest1)
    
def Save_as_MEM(data='', geo='', projection=''):
    """
    This function save the array as a memory file

    Keyword arguments:
    data -- [array], dataset of the geotiff
    geo -- [minimum lon, pixelsize, rotation, maximum lat, rotation,
            pixelsize], (geospatial dataset)
    projection -- interger, the EPSG code
    """
    # save as a geotiff
    driver = gdal.GetDriverByName("MEM")
    dst_ds = driver.Create('', int(data.shape[1]), int(data.shape[0]), 1,
                           gdal.GDT_Float32)
    srse = osr.SpatialReference()
    if projection == '':
        srse.SetWellKnownGeogCS("WGS84")

    else:
        try:
            if not srse.SetWellKnownGeogCS(projection) == 6:
                srse.SetWellKnownGeogCS(projection)
            else:
                try:
                    srse.ImportFromEPSG(int(projection))
                except:
                    srse.ImportFromWkt(projection)
        except:
            try:
                srse.ImportFromEPSG(int(projection))
            except:
                srse.ImportFromWkt(projection)
    dst_ds.SetProjection(srse.ExportToWkt())
    dst_ds.GetRasterBand(1).SetNoDataValue(-9999)
    dst_ds.SetGeoTransform(geo)
    dst_ds.GetRasterBand(1).WriteArray(data)
    return(dst_ds)
    
main(Startdate, Enddate, freq, Example_file, input_format, output_format)