# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sat Sep 28 11:51:01 2019
"""

import WaporAPI

def main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim, API_WAPOR_KEY):
    
    Startdate = "%s-01-01" %Start_year_analyses
    Enddate = "%s-12-31" %End_year_analyses
    
    # Download 10 year data
    Parameters_10Y = ["L2_NPP_D", "L2_T_D", "L2_AETI_D", "L1_RET_D", "L2_LCC_A", "L1_PCP_D", "L2_I_D", "L2_E_D"]
    
    for Parameter_10Y in Parameters_10Y:

        WaporAPI.Collect.WAPOR(output_folder_L1, Startdate, Enddate, latlim, lonlim, API_WAPOR_KEY, Parameter_10Y)

        
    return()