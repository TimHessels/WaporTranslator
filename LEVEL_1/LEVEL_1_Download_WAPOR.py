# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sat Sep 28 11:51:01 2019
"""

import WaporAPI

def main(output_folder_L1, Start_year_analyses, End_year_analyses, latlim, lonlim, WAPOR_LVL, API_WAPOR_KEY):
    
    Startdate = "%s-01-01" %Start_year_analyses
    Enddate = "%s-12-31" %End_year_analyses
    
    # Download 10 year data
    Parameters_10Y = ["L%d_NPP_D"%WAPOR_LVL, "L%d_T_D"%WAPOR_LVL, "L%d_AETI_D"%WAPOR_LVL, "L1_RET_D", "L%d_LCC_A"%WAPOR_LVL, "L1_PCP_D", "L%d_I_D"%WAPOR_LVL, "L%d_E_D"%WAPOR_LVL]
    
    for Parameter_10Y in Parameters_10Y:

        WaporAPI.Collect.WAPOR(output_folder_L1, Startdate, Enddate, latlim, lonlim, API_WAPOR_KEY, Parameter_10Y)

    return()