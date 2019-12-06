# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:24:32 2019

@author: timhe
"""
import sys
import json
import warnings

import WaporTranslator.LEVEL_3 as L3

def main(inputs):

    # Calculate Food Security Module
    L3.Food_Security.LEVEL_3_Calc_Food_Security.main(inputs)
    
    # Calculate Irrigation Management Module
    L3.Irrigation.LEVEL_3_Calc_Irrigation.main(inputs)
    
    # Calculate Water Productivity Module
    L3.Water_Productivity.LEVEL_3_Calc_Water_Productivity.main(inputs)
    
    # Calculate Drought Module
    L3.Drought.LEVEL_3_Calc_Drought.main(inputs)
    
    # Calculate Climate Smart Module
    L3.Climate_Smart.LEVEL_3_Calc_Climate_Smart.main(inputs)

if __name__== "__main__":
    
    # Do not show warnings
    warnings.filterwarnings('ignore')    
    
    # open json file
    with open(sys.argv[1]) as f:
        datastore = f.read()
    obj = json.loads(datastore)  
    inputs = obj["Inputs"][0]
    
    # run code
    main(inputs)
