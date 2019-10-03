# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 22 17:15:51 2019
"""

output_folder = r"G:\Project_MetaMeta\Input_Data"
Startdate = "2017-06-01"
Enddate = "2017-12-31"
latlim = [8.2, 8.7]
lonlim = [39, 39.5]
auth_token='1d8d1a64c4742e71e223595a37bb4f600d51e426db97586e681157ee7000f0dfbe12866f79b887fd'
Parameter = "L2_T_D"
Version = "2"

import WaporAPI
WaporAPI.Collect.WAPOR(output_folder, Startdate, Enddate, latlim, lonlim, auth_token, Parameter, Version)