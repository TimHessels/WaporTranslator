# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sat Sep 28 11:51:01 2019
"""
import watertools

def main(output_folder_L1, latlim, lonlim):
    
    watertools.Collect.ESACCI.LU(output_folder_L1, latlim, lonlim)
        
    return()
