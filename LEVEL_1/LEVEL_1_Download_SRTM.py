# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 13:42:27 2019
"""

import watertools

def main(output_folder_L1, latlim, lonlim):
    
    # Download DEM from SRTM
    watertools.Collect.DEM.SRTM(output_folder_L1, latlim, lonlim)
    
    return()