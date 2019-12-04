# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Sun Sep 29 17:03:41 2019
"""

import WaporTranslator.LEVEL_2 as L2

# User inputs
Start_year_analyses = "2009"
End_year_analyses = "2018"
output_folder = r"G:\Project_MetaMeta"

def main(Start_year_analyses, End_year_analyses, output_folder):

    # run WaporTranslator intermediate parameters (all of LEVEL2)
    L2.Run_Intermediate_Parameters.main(Start_year_analyses, End_year_analyses, output_folder)
   
    return()

main(Start_year_analyses, End_year_analyses, output_folder)





