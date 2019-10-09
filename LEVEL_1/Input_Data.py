# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Mon Oct  7 12:45:54 2019
"""

class Input_Paths:
    
    ET = r"LEVEL_1\L2_AETI_D"
    E = r"LEVEL_1\L2_E_D"
    T = r"LEVEL_1\L2_T_D"
    I = r"LEVEL_1\L2_I_D"   
    P = r"LEVEL_1\L1_PCP_D" 
    ET0 = r"LEVEL_1\L1_RET_D"
    NPP = r"LEVEL_1\L2_NPP_D"
    LU = r"LEVEL_1\L2_LCC_A"
    
    LU_ESA = r"LEVEL_1\ESACCI\LU"
    
    DSLF = r"LEVEL_1\LANDSAF\DSLF"
    DSSF = r"LEVEL_1\LANDSAF\DSSF"
    
    Albedo = r"LEVEL_1\Albedo\MCD43"
    
    DEM = r"LEVEL_1\SRTM\DEM"
        
    Bulk = r"LEVEL_1\SoilGrids\Bulk_Density"
    Clay = r"LEVEL_1\SoilGrids\Clay_Content"
    Sand = r"LEVEL_1\SoilGrids\Sand_Content"
    Silt = r"LEVEL_1\SoilGrids\Silt_Content"
    PH10 = r"LEVEL_1\SoilGrids\PH10"
    SOCC = r"LEVEL_1\SoilGrids\Soil_Organic_Carbon_Content"                                 # Soil Organic Carbon Content
    SOCS = r"LEVEL_1\SoilGrids\Soil_Organic_Carbon_Stock"                                   # Soil Organic Carbon Stock

    Temp = r"LEVEL_1\Weather_Data\Model\GLDAS\daily\tair_f_inst\mean"
    Wind = r"LEVEL_1\Weather_Data\Model\GLDAS\daily\wind_f_inst\mean"
    Hum = r"LEVEL_1\Weather_Data\Model\GLDAS\daily\hum_f_inst\mean"
    
    
class Input_Formats:
    
    ET = "L2_AETI_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"    
    E = "L2_E_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    T = "L2_T_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    I = "L2_I_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    P = "L1_PCP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"  
    ET0 = "L1_RET_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    NPP = "L2_NPP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    LU = "L2_LCC_A_WAPOR_YEAR_{yyyy}.01.01.tif" 
  
    LU_ESA = r"LU_ESACCI.tif"
    
    DSLF = "DSLF_LSASAF_MSG_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    DSSF = "DSSF_LSASAF_MSG_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    
    Albedo = "Albedo_MCD43A3_-_daily_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    
    DEM = "DEM_SRTM_m_3s.tif"
    
    Bulk = "BulkDensity_sl{level}_SoilGrids_kg-m-3.tif" 
    Clay = "ClayContentMassFraction_sl{level}_SoilGrids_percentage.tif"
    Sand = "SandContentMassFraction_sl{level}_SoilGrids_percentage.tif"
    Silt = "SiltContentMassFraction_sl{level}_SoilGrids_percentage.tif"
    PH10 = "SoilPH_sl{level}_SoilGrids_KCi10.tif"
    SOCC = "SoilOrganicCarbonContent_sl{level}_SoilGrids_g_kg.tif"                                 # Soil Organic Carbon Content
    SOCS = "SoilOrganicCarbonStock_sd{level}_SoilGrids_tonnes-ha-1.tif"                                   # Soil Organic Carbon Stock    

    Temp = "Tair_GLDAS-NOAH_C_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Wind = "W_GLDAS-NOAH_m-s-1_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Hum = "Hum_GLDAS-NOAH_percentage_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"
    
class Input_Conversions:    
    
    ET = 0.1                        #mm/day
    E = 0.1                         #mm/day
    T = 0.1                         #mm/day
    I = 0.1                         #mm/day 
    P = 0.1                         #mm/day
    ET0 = 0.1                       #mm/day
    NPP = 10 * 0.001                # Scale factor is 0.001 and 10 to gofrom g/m2 to kg/ha
    LU = 1                           #-
    
    LU_ESA = 1
    
    DSLF = 0.000001                 #w/m2
    DSSF = 0.000001                 #w/m2
    
    Albedo = 1                      # -
    
    DEM = 1                         #mm
        
    Bulk = 1                        #%
    Clay = 1                        #%
    Sand = 1                        #%
    Silt = 1                        #%
    PH10 = 1
    SOCC = 1                               
    SOCS = 1                           

    Temp = 1                        #C
    Wind = 1                        #m/s
    Hum = 1                         #%
    
    