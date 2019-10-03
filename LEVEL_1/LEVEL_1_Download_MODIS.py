# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 16:38:09 2019
"""

import watertools

def main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim):

    # Get Date range
    Startdate = "%s-01-01" %Start_year_analyses
    Enddate = "%s-01-01" %End_year_analyses

    # Download albedo data
    watertools.Collect.MCD43.Albedo_daily(output_folder_L1, Startdate, Enddate, latlim, lonlim)
    
    return()
    
