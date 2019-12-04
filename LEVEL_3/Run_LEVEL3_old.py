# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:24:32 2019

@author: timhe
"""

import WaporTranslator.LEVEL_3 as L3

# User inputs
Start_year_analyses = "2009"
End_year_analyses = "2018"
output_folder = r"G:\Project_MetaMeta"

# Calculate Food Security Module
L3.Food_Security.LEVEL_3_Calc_Food_Security.main(Start_year_analyses, End_year_analyses, output_folder)

# Calculate Irrigation Management Module
L3.Irrigation.LEVEL_3_Calc_Irrigation.main(Start_year_analyses, End_year_analyses, output_folder)

# Calculate Water Productivity Module
L3.Water_Productivity.LEVEL_3_Calc_Water_Productivity.main(Start_year_analyses, End_year_analyses, output_folder)

# Calculate Drought Module
L3.Drought.LEVEL_3_Calc_Drought.main(Start_year_analyses, End_year_analyses, output_folder)

# Calculate Climate Smart Module
L3.Climate_Smart.LEVEL_3_Calc_Climate_Smart.main(Start_year_analyses, End_year_analyses, output_folder)