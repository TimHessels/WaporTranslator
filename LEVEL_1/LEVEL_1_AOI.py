# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 08:55:41 2019

@author: timhe
"""
import shapefile
import numpy as np
import osr
from pyproj import Proj, transform

import watertools.General.raster_conversions as RC
import watertools.General.data_conversions as DC

def main(Input_shapefile, Threshold_Mask):
    
    # Create example dest
    Basin_shp = shapefile.Reader(Input_shapefile, Input_shapefile.replace(".shp", ".dbf"))
    Shapes = Basin_shp.shapes()
    nameID = Basin_shp.fields[-1][0]
    for shape in Shapes:
        bbox = shape.bbox
        if "Boundaries" not in locals():
            Boundaries = dict()
            Boundaries['Lonmin'] = bbox[0]
            Boundaries['Lonmax'] = bbox[2]
            Boundaries['Latmin'] = bbox[1]
            Boundaries['Latmax'] = bbox[3]
        else:
            Boundaries['Lonmin'] = np.minimum(bbox[0], Boundaries['Lonmin'])
            Boundaries['Lonmax'] = np.maximum(bbox[2], Boundaries['Lonmax'])
            Boundaries['Latmin'] = np.minimum(bbox[1], Boundaries['Latmin'])
            Boundaries['Latmax'] = np.maximum(bbox[3], Boundaries['Latmax'])	
            
    # Get the epsg code of the input shapefile
    proj_shp = RC.Get_epsg(Input_shapefile, extension = 'shp')

    if proj_shp != 4326:
    
        inProj = Proj(init='epsg:%d' %proj_shp)
        outProj = Proj(init='epsg:4326')
    
        Boundaries['Lonmin'], Boundaries['Latmax'] = transform(inProj, outProj, Boundaries['Lonmin'], Boundaries['Latmax'])
        Boundaries['Lonmax'], Boundaries['Latmin'] = transform(inProj, outProj, Boundaries['Lonmax'], Boundaries['Latmin'])    
        
    # make the final extend
    Boundaries['Lonmin'] = np.floor(Boundaries['Lonmin']*100)/100
    Boundaries['Lonmax'] = np.ceil(Boundaries['Lonmax']*100)/100
    Boundaries['Latmin'] = np.floor(Boundaries['Latmin']*100)/100
    Boundaries['Latmax'] = np.ceil(Boundaries['Latmax']*100)/100       
    
    if Threshold_Mask == "OFF":
        Resolution = 0.001       
    else:    
        Resolution = 0.0001

    size_x = int((Boundaries['Lonmax'] - Boundaries['Lonmin']) / Resolution)
    size_y = int((Boundaries['Latmax'] - Boundaries['Latmin']) / Resolution)
    Array_ex = np.zeros([size_y, size_x])
    geo_ex = tuple([Boundaries['Lonmin'], Resolution, 0,  Boundaries['Latmax'], 0, -Resolution])
    dest_ex = DC.Save_as_MEM(Array_ex, geo_ex, 4326)
    
    # Create AOI mask
    AOI_Array = Vector_to_Raster(Input_shapefile, dest_ex, nameID)
    AOI_MASK = np.where(AOI_Array<0, 0, 1)
    dest_AOI_MASK = DC.Save_as_MEM(AOI_MASK, geo_ex, 4326)

    # Create latlim, lonlim arrays
    latlim = [Boundaries['Latmin'], Boundaries['Latmax']]
    lonlim = [Boundaries['Lonmin'], Boundaries['Lonmax']]
    
    return(dest_AOI_MASK, latlim, lonlim)

def Vector_to_Raster(shapefile_name, dest_ex, Attribute_name):
    """
    This function creates a raster of a shp file

    Keyword arguments:
    shapefile_name -- 'C:/....../.shp'
        str: Path from the shape file
    reference_raster_data_name -- destination file as example file

    """
    from osgeo import gdal, ogr

    proj = RC.Get_epsg(dest_ex)
    geo = dest_ex.GetGeoTransform()
    size_X = dest_ex.RasterXSize
    size_Y = dest_ex.RasterYSize
    
    x_min = geo[0]
    x_max = geo[0] + size_X * geo[1]
    y_min = geo[3] + size_Y * geo[5]
    y_max = geo[3]
    pixel_size = geo[1]

    # Open the data source and read in the extent
    source_ds = ogr.Open(shapefile_name)
    source_layer = source_ds.GetLayer()

    # Create the destination data source
    x_res = int(round((x_max - x_min) / pixel_size))
    y_res = int(round((y_max - y_min) / pixel_size))

    # Create tiff file
    target_ds = gdal.GetDriverByName('MEM').Create('', x_res, y_res, 1, gdal.GDT_Float32)
    target_ds.SetGeoTransform(geo)
    srse = osr.SpatialReference()
    srse.ImportFromEPSG(int(proj))
    target_ds.SetProjection(srse.ExportToWkt())
    band = target_ds.GetRasterBand(1)
    target_ds.GetRasterBand(1).SetNoDataValue(-9999)
    band.Fill(-9999)

    # Rasterize the shape and save it as band in tiff file
    gdal.RasterizeLayer(target_ds, [1], source_layer, options=["ATTRIBUTE=%s" %Attribute_name])

    # Open array
    Raster_Basin = target_ds.GetRasterBand(1).ReadAsArray()
    target_ds = None
    
    return(Raster_Basin)