# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Mon Oct  7 12:45:54 2019
"""

class Input_Paths():
    
	# LEVEL 1
    ET = r"LEVEL_1\L%d_AETI_D" 
    E = r"LEVEL_1\L%d_E_D"
    T = r"LEVEL_1\L%d_T_D" 
    I = r"LEVEL_1\L%d_I_D" 
    P = r"LEVEL_1\L1_PCP_D" 
    ET0 = r"LEVEL_1\L1_RET_D"
    NPP = r"LEVEL_1\L%d_NPP_D" 
    LU = r"LEVEL_1\L%d_LCC_A" 
    
    LU_ESA = r"LEVEL_1\ESACCI\LU"
    
    DSLF = r"LEVEL_1\LANDSAF\DSLF"
    DSSF = r"LEVEL_1\LANDSAF\DSSF"
    KNMI = r"LEVEL_1\MSGCPP\SDS\daily"
    DSSF_GLDAS = r"LEVEL_1\Weather_Data\Model\GLDAS\daily\swdown_f_tavg\mean"  
    
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
    Temp_monthly = r"LEVEL_1\Weather_Data\Model\GLDAS\monthly\tair_f_inst"
    Wind_monthly = r"LEVEL_1\Weather_Data\Model\GLDAS\monthly\wind_f_inst"
    Hum_monthly = r"LEVEL_1\Weather_Data\Model\GLDAS\monthly\hum_f_inst\mean"
    DSSF_monthly = r"LEVEL_1\Weather_Data\Model\GLDAS\monthly\swdown_f_tavg"  
    
	# LEVEL 2
    Available_Before_Depletion = r"LEVEL_2\Available_Before_Depletion"
    Critical_Soil_Moisture = r"LEVEL_2\Critical_Soil_Moisture"
    Kc_MAX = r"LEVEL_2\Kc_MAX"
    Kc_MAX_Update = r"LEVEL_2\Kc_MAX_update"
    Crop_Water_Requirement = r"LEVEL_2\Crop_Water_Requirement"
    Cumulative_ET = r"LEVEL_2\Temp\Cumulative\Evapotranspiration"
    Cumulative_NPP = r"LEVEL_2\Temp\Cumulative\NPP"
    Cumulative_P = r"LEVEL_2\Temp\Cumulative\Precipitation"
    Cumulative_Temp = r"LEVEL_2\Temp\Cumulative\Temperature"
    Cumulative_T = r"LEVEL_2\Temp\Cumulative\Transpiration"
    Cumulative_ET0 = r"LEVEL_2\Temp\Cumulative\ET0"    
    Deep_Percolation = r"LEVEL_2\Deep_Percolation"
    EF = r"LEVEL_2\Evaporative_Fraction"
    EF_long_term = r"LEVEL_2\Evaporative_Fraction_Long_Term"
    Fractional_Vegetation_Cover = r"LEVEL_2\Fractional_Vegetation_Cover"
    LAI = r"LEVEL_2\LAI"
    Land_Surface_Emissivity = r"LEVEL_2\Land_Surface_Emissivity"
    LU_END = r"LEVEL_2\LU_END"
    Net_Radiation = r"LEVEL_2\Net_Radiation"
    Net_Radiation_Long_Term = r"LEVEL_2\Net_Radiation_Long_Term"
    Net_Supply_Drainage = r"LEVEL_2\Temp\Net_Supply_Drainage"
    CropSeason = r"LEVEL_2\Phenology\CropSeason"
    Season_Start_S1 = r"LEVEL_2\Phenology\Start\S1"
    Season_Start_S2 = r"LEVEL_2\Phenology\Start\S2"
    Season_Start_S3 = r"LEVEL_2\Phenology\Start\S3"    
    Season_End_S1 = r"LEVEL_2\Phenology\End\S1"
    Season_End_S2 = r"LEVEL_2\Phenology\End\S2"	
    Season_End_S3 = r"LEVEL_2\Phenology\End\S3"	
    Perennial_Start = r"LEVEL_2\Phenology\Perennial"
    Perennial_End = r"LEVEL_2\Phenology\Perennial"   
    Root_Depth = r"LEVEL_2\Root_Depth"
    Soil_Moisture = r"LEVEL_2\Soil_Moisture"
    Soil_Moisture_Change = r"LEVEL_2\Soil_Moisture_Change"
    Soil_Moisture_Start = r"LEVEL_2\Temp\Soil_Moisture_Start"
    Soil_Moisture_End = r"LEVEL_2\Temp\Soil_Moisture_End"
    Soil_Moisture_Long_Term = r"LEVEL_2\Soil_Moisture_Long_Term"
    Soil_Water_Holding_Capacity = r"LEVEL_2\Soil_Water_Holding_Capacity"
    Storage_Coefficient_Surface_Runoff = r"LEVEL_2\Storage_Coeff_Surface_Runoff"
    Surface_Runoff_Coefficient = r"LEVEL_2\Surface_Runoff_Coefficient"
    Surface_Runoff_P = r"LEVEL_2\Surface_Runoff_P"
    Theta_FC_Subsoil = r"LEVEL_2\Theta_FC_Subsoil"
    Theta_Sat_Subsoil = r"LEVEL_2\Theta_Sat_Subsoil"
    Theta_WP_Subsoil = r"LEVEL_2\Theta_WP_Subsoil"
	
	# LEVEL 3
    AEZ = r"LEVEL_3\Food_Security\AEZ"
    Irrigation = r"LEVEL_3\Food_Security\Irrigation_Maps_Yearly"
    Actual_Biomass_Production = r"LEVEL_3\Food_Security\Actual_Biomass_Production"
    Accumulated_Biomass_Production = r"LEVEL_3\Food_Security\Accumulated_Biomass_Production_Season\All"
    Accumulated_Biomass_Production_S1 = r"LEVEL_3\Food_Security\Accumulated_Biomass_Production_Season\S1"
    Accumulated_Biomass_Production_S2 = r"LEVEL_3\Food_Security\Accumulated_Biomass_Production_Season\S2"
    Accumulated_Biomass_Production_S3 = r"LEVEL_3\Food_Security\Accumulated_Biomass_Production_Season\S3"
    Accumulated_Biomass_Production_Per = r"LEVEL_3\Food_Security\Accumulated_Biomass_Production_Season\Perennial"    
    Target_Biomass_Production = r"LEVEL_3\Food_Security\Temp\Target_Biomass_Production"
    Yield = r"LEVEL_3\Food_Security\Yield\All"
    Yield_S1 = r"LEVEL_3\Food_Security\Yield\S1"
    Yield_S2 = r"LEVEL_3\Food_Security\Yield\S2"
    Yield_S3 = r"LEVEL_3\Food_Security\Yield\S3"
    Yield_Per = r"LEVEL_3\Food_Security\Yield\Perennial"
    
class Input_Formats:
  
	# LEVEL 1  
    ET = "L%d_AETI_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"    
    E = "L%d_E_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    T = "L%d_T_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    I = "L%d_I_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    P = "L1_PCP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"  
    ET0 = "L1_RET_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    NPP = "L%d_NPP_D_WAPOR_DEKAD_{yyyy}.{mm:02d}.{dd:02d}.tif"
    LU = "L%d_LCC_A_WAPOR_YEAR_{yyyy}.01.01.tif" 
  
    LU_ESA = r"LU_ESACCI.tif"
    
    DSLF = "DSLF_LSASAF_MSG_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    DSSF = "DSSF_LSASAF_MSG_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    KNMI = "SDS_MSGCPP_W-m-2_daily_{yyyy}.{mm:02d}.{dd:02d}.tif"
    DSSF_GLDAS = "SWdown_GLDAS-NOAH_W-m-2_daily_{yyyy}.{mm:02d}.{dd:02d}.tif" 
    
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
    Temp_monthly = "Tair_GLDAS-NOAH_C_monthly_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Wind_monthly = "W_GLDAS-NOAH_m-s-1_monthly_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Hum_monthly = "Hum_GLDAS-NOAH_percentage_monthly_{yyyy}.{mm:02d}.{dd:02d}.tif"
    DSSF_monthly = "SWdown_GLDAS-NOAH_W-m-2_monthly_{yyyy}.{mm:02d}.{dd:02d}.tif"
    
	# LEVEL 2
    Available_Before_Depletion = "Available_Before_Depletion_mm_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Critical_Soil_Moisture = "Critical_Soil_Moisture_cm3-cm-3_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Kc_MAX = "Kc_MAX_-_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Kc_MAX_Update = "Kc_MAX_update_-_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Crop_Water_Requirement = "Crop_Water_Requirement_mm-dekad-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Cumulative_ET = "ET_cum_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Cumulative_NPP = "NPP_cum_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Cumulative_P = "P_cum_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Cumulative_Temp = "Temp_cum_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Cumulative_T = "T_cum_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Cumulative_ET0 = "ET0_cum_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Deep_Percolation = "Deep_Percolation_mm-dekad-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    EF = "Evaporative_Fraction_-_{yyyy}.{mm:02d}.{dd:02d}.tif"
    EF_long_term = "Long_Term_Evaporative_Fraction_-_{mm:02d}.{dd:02d}.tif"
    Fractional_Vegetation_Cover = "Fractional_Vegetation_-_{yyyy}.{mm:02d}.{dd:02d}.tif"
    LAI = "Leaf_Area_Index_m2-m-2_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Land_Surface_Emissivity = "Land_Surface_Emissivity_-_{yyyy}.{mm:02d}.{dd:02d}.tif"
    LU_END = "LU_{yyyy}.tif"
    Net_Radiation = "Net_Radiation_W-m-2_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Net_Radiation_Long_Term = "Long_Term_Net_Radiation_W-m-2_{mm:02d}.{dd:02d}.tif"
    Net_Supply_Drainage = "Net_Supply_Drainage_mm-dekad-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    CropSeason = "LU_CropSeason_{yyyy}.tif"
    Season_Start_S1 = "S1_Start_{yyyy}.tif"
    Season_Start_S2 = "S2_Start_{yyyy}.tif"
    Season_Start_S3 = "S3_Start_{yyyy}.tif"    
    Season_End_S1 = "S1_End_{yyyy}.tif"
    Season_End_S2 = "S2_End_{yyyy}.tif"
    Season_End_S3 = "S3_End_{yyyy}.tif"    
    Perennial_Start = "Perennial_Start_{yyyy}.tif"
    Perennial_End = "Perennial_End_{yyyy}.tif"
    Root_Depth = "Root_Depth_cm_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Soil_Moisture = "Soil_Moisture_cm3-cm-3_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Soil_Moisture_Change = "Change_Soil_Moisture_mm-dekad-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Soil_Moisture_Start = "Soil_Moisture_Start_cm3-cm-3_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Soil_Moisture_End = "Soil_Moisture_End_cm3-cm-3_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Soil_Moisture_Long_Term = "Long_Term_Soil_Moisture_cm3-cm-3_{mm:02d}.{dd:02d}.tif"
    Soil_Water_Holding_Capacity = "Soil_Water_Holding_Capacity_mm-m-1.tif"
    Storage_Coefficient_Surface_Runoff = "Storage_Coefficient_Surface_Runoff_mm-dekad-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Surface_Runoff_Coefficient = "Surface_Runoff_Coefficient_-_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Surface_Runoff_P = "Surface_Runoff_Precipitation_mm-dekad-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Theta_FC_Subsoil = "Field_Capacity_Subsoil_cm3-cm-3.tif"
    Theta_Sat_Subsoil = "Saturated_Theta_Subsoil_cm3-cm-3.tif"
    Theta_WP_Subsoil =  "Wilting_Point_Subsoil_cm3-cm-3.tif"

	# LEVEL 3
    AEZ = "Agro_Ecological_Zonation_AEZ_{yyyy}.01.01.tif"
    Irrigation = "Irrigation_Yearly_-_{yyyy}.01.01.tif"
    Actual_Biomass_Production = "Actual_Biomass_Production_kg-ha-1-d-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Accumulated_Biomass_Production = "Accumulated_Biomass_Production_kg-ha-1-season-1_{yyyy}.01.01.tif" 
    Accumulated_Biomass_Production_S1 = "Accumulated_Biomass_Production_Season_1_kg-ha-1-season-1_{yyyy}.01.01.tif"
    Accumulated_Biomass_Production_S2 = "Accumulated_Biomass_Production_Season_2_kg-ha-1-season-1_{yyyy}.01.01.tif"
    Accumulated_Biomass_Production_S3 = "Accumulated_Biomass_Production_Season_3_kg-ha-1-season-1_{yyyy}.01.01.tif"
    Accumulated_Biomass_Production_Per = "Accumulated_Biomass_Production_Season_Perennial_kg-ha-1-season-1_{yyyy}.01.01.tif"  

    Target_Biomass_Production = "Target_Biomass_Production_kg-ha-1-d-1_{yyyy}.{mm:02d}.{dd:02d}.tif"
    Yield = "Yield_Season_kg-ha-1-season-1_{yyyy}.01.01.tif"
    Yield_S1 = "Yield_%s_Season_1_kg-ha-1-season-1_{yyyy}.01.01.tif"
    Yield_S2 = "Yield_%s_Season_2_kg-ha-1-season-1_{yyyy}.01.01.tif"
    Yield_S3 = "Yield_%s_Season_3_kg-ha-1-season-1_{yyyy}.01.01.tif"
    Yield_Per = "Yield_%s_Season_Per_kg-ha-1-season-1_{yyyy}.01.01.tif"
		
class Input_Conversions:    

	# LEVEL 1    
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
    KNMI = 1                        #w/m2
    DSSF_monthly = 1                #w/m2
    DSSF_GLDAS = 1                  #w/m2
    
    Albedo = 1                      # -
    
    DEM = 1                         #mm
        
    Bulk = 1                        #%
    Clay = 1                        #%
    Sand = 1                        #%
    Silt = 1                        #%
    PH10 = 0.1
    SOCC = 1                               
    SOCS = 1                           

    Temp = 1                        #C
    Wind = 1                        #m/s
    Hum = 1                         #%
    Temp_monthly = 1                        #C
    Wind_monthly = 1                        #m/s
    Hum_monthly = 1                         #%
        
 	# LEVEL 2
    Available_Before_Depletion = 1
    Critical_Soil_Moisture = 1
    Kc_MAX = 1
    Kc_MAX_Update = 1
    Crop_Water_Requirement = 1
    Cumulative_ET = 1
    Cumulative_NPP = 1
    Cumulative_P = 1
    Cumulative_Temp = 1
    Cumulative_T = 1
    Cumulative_ET0 = 1
    Deep_Percolation = 1
    EF = 1
    EF_long_term = 1
    Fractional_Vegetation_Cover = 1
    LAI = 1
    Land_Surface_Emissivity = 1
    LU_END = 1
    Net_Radiation = 1
    Net_Radiation_Long_Term = 1
    Net_Supply_Drainage = 1
    CropSeason = 1
    Season_Start_S1 = 1
    Season_Start_S2 = 1
    Season_Start_S3 = 1    
    Season_End_S1 = 1
    Season_End_S2 = 1
    Season_End_S3 = 1    
    Perennial_Start = 1
    Perennial_End = 1
    Root_Depth = 1
    Soil_Moisture = 1
    Soil_Moisture_Change = 1
    Soil_Moisture_Start = 1
    Soil_Moisture_End = 1
    Soil_Moisture_Long_Term = 1
    Soil_Water_Holding_Capacity = 1
    Storage_Coefficient_Surface_Runoff = 1
    Surface_Runoff_Coefficient = 1 
    Surface_Runoff_P = 1
    Theta_FC_Subsoil = 1
    Theta_Sat_Subsoil = 1
    Theta_WP_Subsoil = 1   
    
    # LEVEL 3
    AEZ = 1
    Irrigation = 1
    Actual_Biomass_Production = 1
    Accumulated_Biomass_Production = 1
    Accumulated_Biomass_Production_S1 = 1
    Accumulated_Biomass_Production_S2 = 1
    Accumulated_Biomass_Production_S3 = 1
    Accumulated_Biomass_Production_Per = 1
    Target_Biomass_Production = 1
    Yield = 1   
    Yield_S1 = 1  
    Yield_S2 = 1  
    Yield_S3 = 1  
    Yield_Per = 1      
    