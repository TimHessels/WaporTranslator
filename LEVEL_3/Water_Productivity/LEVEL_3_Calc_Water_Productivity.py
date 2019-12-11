# -*- coding: utf-8 -*-
"""
WaterSat
author: Tim Martijn Hessels
Created on Tue Oct  1 19:06:37 2019
"""
import os
import gdal
import warnings
import pandas as pd
import numpy as np

def main(inputs):  

    # Set Variables
    Start_year_analyses = inputs["Start_year"]
    End_year_analyses = inputs["End_year"]
    output_folder = inputs["Output_folder"]  
    WAPOR_LVL = inputs["WAPOR_LEVEL"]   
    Yield_info_S1 = inputs["Yield_info_S1"]       
    Yield_info_S2 = inputs["Yield_info_S2"]       
    Yield_info_S3 = inputs["Yield_info_S3"]       
    Yield_info_Per = inputs["Yield_info_Per"]   
    
    import WaporTranslator.LEVEL_1.Input_Data as Inputs
    import WaporTranslator.LEVEL_1.DataCube as DataCube
    import WaporTranslator.LEVEL_2.Functions as Functions
    import WaporTranslator.LEVEL_3.Food_Security.LEVEL_3_Calc_Food_Security as L3_Food

    # Do not show non relevant warnings
    warnings.filterwarnings("ignore")
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    
    Startdate = "%s-01-01" %Start_year_analyses
    Enddate = "%s-12-31" %End_year_analyses
    
    # Define dates
    Dates = Functions.Get_Dekads(Start_year_analyses, End_year_analyses)
    Dates_Years = pd.date_range(Startdate, Enddate, freq = "AS")
    
    # Get path and formats
    Paths = Inputs.Input_Paths()
    Formats = Inputs.Input_Formats()
    Conversions = Inputs.Input_Conversions()
    
    # Set example file
    example_file = os.path.join(output_folder, "LEVEL_1", "MASK", "MASK.tif")
    
    # Open Mask
    dest_mask = gdal.Open(example_file)
    MASK = dest_mask.GetRasterBand(1).ReadAsArray()
    
    # Define output folder LEVEL 3
    output_folder_L3 = os.path.join(output_folder, "LEVEL_3", "Water_Productivity")
    if not os.path.exists(output_folder_L3):
        os.makedirs(output_folder_L3)
 
    ################################# Dynamic maps #################################
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, str(Paths.ET) %WAPOR_LVL), str(Formats.ET) %WAPOR_LVL, Dates, Conversion = Conversions.ET, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = 'mm/day')
    T = DataCube.Rasterdata_tiffs(os.path.join(output_folder, str(Paths.T) %WAPOR_LVL), str(Formats.T) %WAPOR_LVL, Dates, Conversion = Conversions.T, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'T', Product = 'WAPOR', Unit = 'mm/day')
    ET0 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET0), Formats.ET0, Dates, Conversion = Conversions.ET0, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET0', Product = 'WAPOR', Unit = 'mm/day')
    Actual_Biomass_Production = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Actual_Biomass_Production), Formats.Actual_Biomass_Production, Dates, Conversion = Conversions.Actual_Biomass_Production, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Actual Biomass Production', Product = '', Unit = 'kg/ha/d')
    NPPcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_NPP), Formats.Cumulative_NPP, Dates, Conversion = Conversions.Cumulative_NPP, Variable = 'Cumulated NPP', Product = '', Unit = 'mm/decade')      
    Crop_S1_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_Start_S1), Formats.Season_Start_S1, list(Dates_Years), Conversion = Conversions.Season_Start_S1, Variable = 'Season 1 Start', Product = '', Unit = 'DOY')
    Crop_S2_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_Start_S2), Formats.Season_Start_S2, list(Dates_Years), Conversion = Conversions.Season_Start_S2, Variable = 'Season 2 Start', Product = '', Unit = 'DOY')
    Crop_S3_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_Start_S3), Formats.Season_Start_S3, list(Dates_Years), Conversion = Conversions.Season_Start_S3, Variable = 'Season 3 Start', Product = '', Unit = 'DOY')
    Crop_S1_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S1), Formats.Season_End_S1, list(Dates_Years), Conversion = Conversions.Season_End_S1, Variable = 'Season 1 End', Product = '', Unit = 'DOY')
    Crop_S2_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S2), Formats.Season_End_S2, list(Dates_Years), Conversion = Conversions.Season_End_S2, Variable = 'Season 2 End', Product = '', Unit = 'DOY')
    Crop_S3_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S3), Formats.Season_End_S3, list(Dates_Years), Conversion = Conversions.Season_End_S3, Variable = 'Season 3 End', Product = '', Unit = 'DOY')
    Per_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Perennial_Start), Formats.Perennial_Start, list(Dates_Years), Conversion = Conversions.Perennial_Start, Variable = 'Perennial Start', Product = '', Unit = 'DOY')
    Per_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Perennial_End), Formats.Perennial_End, list(Dates_Years), Conversion = Conversions.Perennial_End, Variable = 'Perennial End', Product = '', Unit = 'DOY')
    Pcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_P), Formats.Cumulative_P, Dates, Conversion = Conversions.Cumulative_P, Variable = 'Cumulated P', Product = '', Unit = 'mm/decade')  
    ET0cum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_ET0), Formats.Cumulative_ET0, Dates, Conversion = Conversions.Cumulative_ET0, Variable = 'Cumulated ET0', Product = '', Unit = 'mm/decade')      
    ETcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_ET), Formats.Cumulative_ET, Dates, Conversion = Conversions.Cumulative_ET, Variable = 'Cumulated ET', Product = '', Unit = 'mm/decade')      
    Tcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_T), Formats.Cumulative_T, Dates, Conversion = Conversions.Cumulative_T, Variable = 'Cumulated T', Product = '', Unit = 'mm/decade')      
    AEZ = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.AEZ), Formats.AEZ, Dates, Conversion = Conversions.AEZ, Variable = 'Surface Runoff Coefficient', Product = '', Unit = '-')  
    CropType = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.LU_END), Formats.LU_END, list(Dates_Years), Conversion = Conversions.LU_END, Variable = 'LU_END', Product = '', Unit = '-')
    CropSeason = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.CropSeason), Formats.CropSeason, list(Dates_Years), Conversion = Conversions.CropSeason, Variable = 'CropSeason', Product = '', Unit = '-')
    Accumulated_Biomass_Production = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Accumulated_Biomass_Production), Formats.Accumulated_Biomass_Production, list(Dates_Years), Conversion = Conversions.Accumulated_Biomass_Production, Variable = 'Accumulated Biomass Production', Product = '', Unit = 'ton/ha/season')
    Accumulated_Biomass_Production_S1 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Accumulated_Biomass_Production_S1), Formats.Accumulated_Biomass_Production_S1, list(Dates_Years), Conversion = Conversions.Accumulated_Biomass_Production_S1, Variable = 'Accumulated Biomass Production Season 1', Product = '', Unit = 'ton/ha/season')
    Accumulated_Biomass_Production_S2 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Accumulated_Biomass_Production_S2), Formats.Accumulated_Biomass_Production_S2, list(Dates_Years), Conversion = Conversions.Accumulated_Biomass_Production_S2, Variable = 'Accumulated Biomass Production Season 2', Product = '', Unit = 'ton/ha/season')
    Accumulated_Biomass_Production_S3 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Accumulated_Biomass_Production_S3), Formats.Accumulated_Biomass_Production_S3, list(Dates_Years), Conversion = Conversions.Accumulated_Biomass_Production_S3, Variable = 'Accumulated Biomass Production Season 3', Product = '', Unit = 'ton/ha/season')
    Accumulated_Biomass_Production_Per = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Accumulated_Biomass_Production_Per), Formats.Accumulated_Biomass_Production_Per, list(Dates_Years), Conversion = Conversions.Accumulated_Biomass_Production_Per, Variable = 'Accumulated Biomass Production Season Perennial', Product = '', Unit = 'ton/ha/season')
    Target_Biomass_Production = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Target_Biomass_Production), Formats.Target_Biomass_Production, Dates, Conversion = Conversions.Target_Biomass_Production, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Target Biomass Production', Product = '', Unit = 'kg/ha/d')
    Yield = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Yield), Formats.Yield, list(Dates_Years), Conversion = Conversions.Yield, Variable = 'Yield', Product = '', Unit = 'ton/ha')
    Yield_S1 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Yield_S1), str(Formats.Yield_S1) %Yield_info_S1["Croptype"], list(Dates_Years), Conversion = Conversions.Yield_S1, Variable = 'Yield Season 1', Product = '', Unit = 'ton/ha')
    Yield_S2 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Yield_S2), str(Formats.Yield_S2) %Yield_info_S2["Croptype"], list(Dates_Years), Conversion = Conversions.Yield_S2, Variable = 'Yield Season 2', Product = '', Unit = 'ton/ha')
    Yield_S3 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Yield_S3), str(Formats.Yield_S3) %Yield_info_S3["Croptype"], list(Dates_Years), Conversion = Conversions.Yield_S3, Variable = 'Yield Season 3', Product = '', Unit = 'ton/ha')
    Yield_Per = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Yield_Per), str(Formats.Yield_Per) %Yield_info_Per["Croptype"], list(Dates_Years), Conversion = Conversions.Yield_Per, Variable = 'Yield Season Perennial', Product = '', Unit = 'ton/ha')

    ######################## Calculate days in each dekads #################################
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)

    ################################# Calculate Crop Season and LU #################################
    Season_Type = L3_Food.Calc_Crops(CropType, CropSeason, MASK)

    ######################## Calculate Transpiration Efficiency ########################
    T_Efficiency_Data = Actual_Biomass_Production.Data/(T.Data * 10)

    # Write in DataCube
    T_Efficiency = DataCube.Rasterdata_Empty()
    T_Efficiency.Data = T_Efficiency_Data * MASK
    T_Efficiency.Projection = ET.Projection
    T_Efficiency.GeoTransform = ET.GeoTransform
    T_Efficiency.Ordinal_time = ET.Ordinal_time
    T_Efficiency.Size = T_Efficiency_Data.shape
    T_Efficiency.Variable = "Transpiration Efficiency"
    T_Efficiency.Unit = "mm-dekad-1"
    
    del T_Efficiency_Data
    
    T_Efficiency.Save_As_Tiff(os.path.join(output_folder_L3, "T_Efficiency"))         

    ######################### Calculate accumulated parameters #######################

    # Calculate cummulative ET and ET0 over the seasons
    DOYcum = np.ones(Tcum.Size) * Days_in_Dekads[:, None, None]
    DOYcum = DOYcum.cumsum(axis = 0)    
    
    # For Perennial crop clip the season at start and end year
    Accumulated_T_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_T_Data_End = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_End = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_End = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_End = np.ones(Per_Start.Size) * np.nan
    Accumulated_P_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_P_Data_End = np.ones(Per_Start.Size) * np.nan    
    '''
    Start_Array = np.maximum(0, Per_Start.Data)
    End_Array = np.minimum(35, Per_End.Data)  
    
    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)
        for dekad in range(0,36):
            Accumulated_T_Data_Start[year_diff, Start_Array[year_diff, :, :] == dekad] = Tcum.Data[int(year_diff * 36 + dekad), Start_Array[year_diff, :, :] == dekad] 
            Accumulated_T_Data_End[year_diff, End_Array[year_diff, :, :] == dekad] = Tcum.Data[int(year_diff * 36 + dekad-1), End_Array[year_diff, :, :] == dekad] 
            Accumulated_ET0_Data_Start[year_diff, Start_Array[year_diff, :, :] == dekad] = ET0cum.Data[int(year_diff * 36 + dekad), Start_Array[year_diff, :, :] == dekad] 
            Accumulated_ET0_Data_End[year_diff, End_Array[year_diff, :, :] == dekad] = ET0cum.Data[int(year_diff * 36 + dekad-1), End_Array[year_diff, :, :] == dekad] 
            Accumulated_DOY_Data_Start[year_diff, Start_Array[year_diff, :, :] == dekad] = DOYcum[int(year_diff * 36 + dekad), Start_Array[year_diff, :, :] == dekad] 
            Accumulated_DOY_Data_End[year_diff, End_Array[year_diff, :, :] == dekad] = DOYcum[int(year_diff * 36 + dekad-1), End_Array[year_diff, :, :] == dekad] 
            Accumulated_ET_Data_Start[year_diff, Start_Array[year_diff, :, :] == dekad] = ETcum.Data[int(year_diff * 36 + dekad), Start_Array[year_diff, :, :] == dekad] 
            Accumulated_ET_Data_End[year_diff, End_Array[year_diff, :, :] == dekad] = ETcum.Data[int(year_diff * 36 + dekad-1), End_Array[year_diff, :, :] == dekad] 
    '''
    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)
        Harvest = np.where(Per_End.Data[year_diff, :, :]<37, 1, 0)
        for dekad in range(int(np.nanmin(Per_Start.Data[year_diff, :, :])), 36):
            Accumulated_T_Data_Start[year_diff, np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] = NPPcum.Data[int(year_diff * 36 + dekad), np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] 
            Accumulated_ET0_Data_Start[year_diff, np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] = ET0cum.Data[int(year_diff * 36 + dekad), np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] 
            Accumulated_DOY_Data_Start[year_diff, np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] = DOYcum[int(year_diff * 36 + dekad), np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] 
            Accumulated_ET_Data_Start[year_diff, np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] = ETcum.Data[int(year_diff * 36 + dekad), np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] 
            Accumulated_P_Data_Start[year_diff, np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] = Pcum.Data[int(year_diff * 36 + dekad), np.logical_and(Per_Start.Data[year_diff, :, :] == dekad, Harvest==1)] 
 
        for dekad in range(0,37):
            Accumulated_T_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = NPPcum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
            Accumulated_ET0_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad]= ET0cum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
            Accumulated_DOY_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = DOYcum[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
            Accumulated_ET_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = ETcum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
            Accumulated_P_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = Pcum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
    
    Accumulated_T_Data_Per =  Accumulated_T_Data_End - Accumulated_T_Data_Start
    Accumulated_ET0_Data_Per =  Accumulated_ET0_Data_End - Accumulated_ET0_Data_Start
    Accumulated_DOY_Data_Per =  Accumulated_DOY_Data_End - Accumulated_DOY_Data_Start
    Accumulated_ET_Data_Per =  Accumulated_ET_Data_End - Accumulated_ET_Data_Start
    Accumulated_P_Data_Per =  Accumulated_P_Data_End - Accumulated_P_Data_Start
    
    # For other crops (triple, double and single) take the start and end of the seasons
    Accumulated_T_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_T_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_T_Data_Start_S3 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Start_S3 = np.ones(Per_Start.Size) * np.nan    
    Accumulated_DOY_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_Start_S3 = np.ones(Per_Start.Size) * np.nan    
    Accumulated_DOY_Data_End_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_End_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_End_S3 = np.ones(Per_Start.Size) * np.nan    
    Accumulated_ET_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_Start_S3 = np.ones(Per_Start.Size) * np.nan
    Accumulated_P_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_P_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_P_Data_Start_S3 = np.ones(Per_Start.Size) * np.nan
    
    if not np.isnan(np.nanmean(Crop_S1_End.Data)):
        for Date_Year in Dates_Years:
            year_diff = int(Date_Year.year - Dates_Years[0].year)
            for dekad in range(0,int(np.nanmax(Crop_S3_End.Data))):
                Accumulated_T_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = Tcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_T_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = Tcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_T_Data_Start_S3[year_diff, Crop_S3_End.Data[year_diff, :, :] == dekad] = Tcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S3_End.Data[year_diff, :, :] == dekad] 

                Accumulated_ET0_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = ET0cum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_ET0_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = ET0cum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_ET0_Data_Start_S3[year_diff, Crop_S3_End.Data[year_diff, :, :] == dekad] = ET0cum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S3_End.Data[year_diff, :, :] == dekad] 
 
                Accumulated_DOY_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_Start_S3[year_diff, Crop_S3_End.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S3_End.Data[year_diff, :, :] == dekad] 

                Accumulated_DOY_Data_End_S1[year_diff, Crop_S1_Start.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S1_Start.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_End_S2[year_diff, Crop_S2_Start.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_Start.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_End_S3[year_diff, Crop_S3_Start.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S3_Start.Data[year_diff, :, :] == dekad] 

                Accumulated_ET_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = ETcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_ET_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = ETcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_ET_Data_Start_S3[year_diff, Crop_S3_End.Data[year_diff, :, :] == dekad] = ETcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S3_End.Data[year_diff, :, :] == dekad] 

                Accumulated_P_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = Pcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_P_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = Pcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_P_Data_Start_S3[year_diff, Crop_S3_End.Data[year_diff, :, :] == dekad] = Pcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S3_End.Data[year_diff, :, :] == dekad] 

    
    Accumulated_T_Data_Start_S1[np.isnan(Accumulated_T_Data_Start_S1)] = 0
    Accumulated_T_Data_Start_S2[np.isnan(Accumulated_T_Data_Start_S2)] = 0 
    Accumulated_T_Data_Start_S3[np.isnan(Accumulated_T_Data_Start_S3)] = 0 
    Accumulated_ET0_Data_Start_S1[np.isnan(Accumulated_ET0_Data_Start_S1)] = 0
    Accumulated_ET0_Data_Start_S2[np.isnan(Accumulated_ET0_Data_Start_S2)] = 0 
    Accumulated_ET0_Data_Start_S3[np.isnan(Accumulated_ET0_Data_Start_S3)] = 0 
    Accumulated_DOY_Data_Start_S1[np.isnan(Accumulated_DOY_Data_Start_S1)] = 0
    Accumulated_DOY_Data_Start_S2[np.isnan(Accumulated_DOY_Data_Start_S2)] = 0 
    Accumulated_DOY_Data_Start_S3[np.isnan(Accumulated_DOY_Data_Start_S3)] = 0 
    Accumulated_DOY_Data_End_S1[np.isnan(Accumulated_DOY_Data_End_S1)] = 0
    Accumulated_DOY_Data_End_S2[np.isnan(Accumulated_DOY_Data_End_S2)] = 0 
    Accumulated_DOY_Data_End_S3[np.isnan(Accumulated_DOY_Data_End_S3)] = 0 
    Accumulated_ET_Data_Start_S1[np.isnan(Accumulated_ET_Data_Start_S1)] = 0
    Accumulated_ET_Data_Start_S2[np.isnan(Accumulated_ET_Data_Start_S2)] = 0 
    Accumulated_ET_Data_Start_S3[np.isnan(Accumulated_ET_Data_Start_S3)] = 0 
    Accumulated_P_Data_Start_S1[np.isnan(Accumulated_P_Data_Start_S1)] = 0
    Accumulated_P_Data_Start_S2[np.isnan(Accumulated_P_Data_Start_S2)] = 0 
    Accumulated_P_Data_Start_S3[np.isnan(Accumulated_P_Data_Start_S3)] = 0 
     
    # Calculate pasture as DOY 1 till 365
    Accumulated_T_Data_Past = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Past = np.ones(Per_Start.Size) * np.nan    
    Accumulated_DOY_Data_Past = np.ones(Per_Start.Size) * np.nan   
    Accumulated_ET_Data_Past = np.ones(Per_Start.Size) * np.nan   
    Accumulated_P_Data_Past = np.ones(Per_Start.Size) * np.nan       
    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)
        dekad = 35 # Always take end in pasture
        Accumulated_T_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 5] = Tcum.Data[int(year_diff * 36 + dekad), Season_Type.Data[year_diff, :, :] == 5] 
        Accumulated_ET0_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 5] = ET0cum.Data[int(year_diff * 36 + dekad), Season_Type.Data[year_diff, :, :] == 5] 
        Accumulated_DOY_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 5] = 365
        Accumulated_ET_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 5] = ETcum.Data[int(year_diff * 36 + dekad), Season_Type.Data[year_diff, :, :] == 5] 
        Accumulated_P_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 5] = Pcum.Data[int(year_diff * 36 + dekad), Season_Type.Data[year_diff, :, :] == 5] 
        
    Accumulated_T_Data_Past[np.isnan(Accumulated_T_Data_Past)] = 0
    Accumulated_T_Data_Per[np.isnan(Accumulated_T_Data_Per)] = 0
    Accumulated_ET0_Data_Past[np.isnan(Accumulated_ET0_Data_Past)] = 0
    Accumulated_ET0_Data_Per[np.isnan(Accumulated_ET0_Data_Per)] = 0
    Accumulated_DOY_Data_Past[np.isnan(Accumulated_DOY_Data_Past)] = 0
    Accumulated_DOY_Data_Per[np.isnan(Accumulated_DOY_Data_Per)] = 0
    Accumulated_ET_Data_Past[np.isnan(Accumulated_ET_Data_Past)] = 0
    Accumulated_ET_Data_Per[np.isnan(Accumulated_ET_Data_Per)] = 0   
    Accumulated_P_Data_Past[np.isnan(Accumulated_P_Data_Past)] = 0
    Accumulated_P_Data_Per[np.isnan(Accumulated_P_Data_Per)] = 0   
        
    # Add all seasons to one map
    Accumulated_T_Data = Accumulated_T_Data_Start_S1 + Accumulated_T_Data_Start_S2 + Accumulated_T_Data_Start_S3 + Accumulated_T_Data_Per + Accumulated_T_Data_Past
    Accumulated_T_Data[Accumulated_T_Data==0] = np.nan
    Accumulated_ET0_Data = Accumulated_ET0_Data_Start_S1 + Accumulated_ET0_Data_Start_S2 + Accumulated_ET0_Data_Start_S3 + Accumulated_ET0_Data_Per + Accumulated_ET0_Data_Past
    Accumulated_ET0_Data[Accumulated_ET0_Data==0] = np.nan
    Accumulated_DOY_Data = Accumulated_DOY_Data_Start_S1 - Accumulated_DOY_Data_End_S1 + Accumulated_DOY_Data_Start_S2 - Accumulated_DOY_Data_End_S2 + Accumulated_DOY_Data_Start_S3 - Accumulated_DOY_Data_End_S3 + Accumulated_DOY_Data_Per + Accumulated_DOY_Data_Past
    Accumulated_DOY_Data[Accumulated_DOY_Data==0] = np.nan    
    Accumulated_ET_Data = Accumulated_ET_Data_Start_S1 + Accumulated_ET_Data_Start_S2 + Accumulated_ET_Data_Start_S3 + Accumulated_ET_Data_Per + Accumulated_ET_Data_Past
    Accumulated_ET_Data[Accumulated_ET_Data==0] = np.nan    
    Accumulated_P_Data = Accumulated_P_Data_Start_S1 + Accumulated_P_Data_Start_S2 + Accumulated_P_Data_Start_S3 + Accumulated_P_Data_Per + Accumulated_P_Data_Past
    Accumulated_P_Data[Accumulated_P_Data==0] = np.nan    
    
    # Add Season 1 to one map
    Accumulated_T_Data_S1 = Accumulated_T_Data_Start_S1 
    Accumulated_T_Data_S1[Accumulated_T_Data_S1==0] = np.nan
    Accumulated_ET0_Data_S1 = Accumulated_ET0_Data_Start_S1
    Accumulated_ET0_Data_S1[Accumulated_ET0_Data_S1==0] = np.nan
    Accumulated_DOY_Data_S1 = Accumulated_DOY_Data_Start_S1 - Accumulated_DOY_Data_End_S1
    Accumulated_DOY_Data_S1[Accumulated_DOY_Data_S1==0] = np.nan    
    Accumulated_ET_Data_S1 = Accumulated_ET_Data_Start_S1
    Accumulated_ET_Data_S1[Accumulated_ET_Data_S1==0] = np.nan    
    Accumulated_P_Data_S1 = Accumulated_P_Data_Start_S1
    Accumulated_P_Data_S1[Accumulated_P_Data_S1==0] = np.nan   
    
    # Add Season 2 to one map
    Accumulated_T_Data_S2 = Accumulated_T_Data_Start_S2 
    Accumulated_T_Data_S2[Accumulated_T_Data_S2==0] = np.nan
    Accumulated_ET0_Data_S2 = Accumulated_ET0_Data_Start_S2
    Accumulated_ET0_Data_S2[Accumulated_ET0_Data_S2==0] = np.nan
    Accumulated_DOY_Data_S2 = Accumulated_DOY_Data_Start_S2 - Accumulated_DOY_Data_End_S2
    Accumulated_DOY_Data_S2[Accumulated_DOY_Data_S2==0] = np.nan    
    Accumulated_ET_Data_S2 = Accumulated_ET_Data_Start_S2
    Accumulated_ET_Data_S2[Accumulated_ET_Data_S2==0] = np.nan    
    Accumulated_P_Data_S2 = Accumulated_P_Data_Start_S2
    Accumulated_P_Data_S2[Accumulated_P_Data_S2==0] = np.nan    
    
    # Add Season 3 to one map
    Accumulated_T_Data_S3 = Accumulated_T_Data_Start_S3 
    Accumulated_T_Data_S3[Accumulated_T_Data_S3==0] = np.nan
    Accumulated_ET0_Data_S3 = Accumulated_ET0_Data_Start_S3
    Accumulated_ET0_Data_S3[Accumulated_ET0_Data_S3==0] = np.nan
    Accumulated_DOY_Data_S3 = Accumulated_DOY_Data_Start_S3 - Accumulated_DOY_Data_End_S3
    Accumulated_DOY_Data_S3[Accumulated_DOY_Data_S3==0] = np.nan    
    Accumulated_ET_Data_S3 = Accumulated_ET_Data_Start_S3
    Accumulated_ET_Data_S3[Accumulated_ET_Data_S3==0] = np.nan        
    Accumulated_P_Data_S3 = Accumulated_P_Data_Start_S3
    Accumulated_P_Data_S3[Accumulated_P_Data_S3==0] = np.nan        
    
    # Add Season Perennial to one map
    Accumulated_T_Data_Per = Accumulated_T_Data_Per 
    Accumulated_T_Data_Per[Accumulated_T_Data_Per==0] = np.nan
    Accumulated_ET0_Data_Per = Accumulated_ET0_Data_Per
    Accumulated_ET0_Data_Per[Accumulated_ET0_Data_Per==0] = np.nan
    Accumulated_DOY_Data_Per = Accumulated_DOY_Data_Per - Accumulated_DOY_Data_Per
    Accumulated_DOY_Data_Per[Accumulated_DOY_Data_Per==0] = np.nan    
    Accumulated_ET_Data_Per = Accumulated_ET_Data_Per
    Accumulated_ET_Data_Per[Accumulated_ET_Data_Per==0] = np.nan     
    Accumulated_P_Data_Per = Accumulated_P_Data_Per
    Accumulated_P_Data_Per[Accumulated_P_Data_Per==0] = np.nan     
    
    ################## Calculate AquaCrop water use efficiency #############################
    
    AquaCrop_Water_Use_Efficiency_Data = 1000 * (Accumulated_Biomass_Production.Data/(10 * Accumulated_DOY_Data * Accumulated_T_Data/Accumulated_ET0_Data))

    # Write in DataCube
    AquaCrop_Water_Use_Efficiency = DataCube.Rasterdata_Empty()
    AquaCrop_Water_Use_Efficiency.Data = AquaCrop_Water_Use_Efficiency_Data.clip(0,100) * MASK
    AquaCrop_Water_Use_Efficiency.Projection = ET.Projection
    AquaCrop_Water_Use_Efficiency.GeoTransform = ET.GeoTransform
    AquaCrop_Water_Use_Efficiency.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    AquaCrop_Water_Use_Efficiency.Size = AquaCrop_Water_Use_Efficiency_Data.shape
    AquaCrop_Water_Use_Efficiency.Variable = "AquaCrop Water Use Efficiency"
    AquaCrop_Water_Use_Efficiency.Unit = "kg-m-2"
    
    del AquaCrop_Water_Use_Efficiency_Data
    
    AquaCrop_Water_Use_Efficiency.Save_As_Tiff(os.path.join(output_folder_L3, "AquaCrop_Water_Use_Efficiency", "All"))    

    # Season 1
    AquaCrop_Water_Use_Efficiency_Data_S1 = 1000 * (Accumulated_Biomass_Production_S1.Data/(10 * Accumulated_DOY_Data_S1 * Accumulated_T_Data_S1/Accumulated_ET0_Data_S1))

    # Write in DataCube
    AquaCrop_Water_Use_Efficiency_S1 = DataCube.Rasterdata_Empty()
    AquaCrop_Water_Use_Efficiency_S1.Data = AquaCrop_Water_Use_Efficiency_Data_S1.clip(0,100) * MASK
    AquaCrop_Water_Use_Efficiency_S1.Projection = ET.Projection
    AquaCrop_Water_Use_Efficiency_S1.GeoTransform = ET.GeoTransform
    AquaCrop_Water_Use_Efficiency_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    AquaCrop_Water_Use_Efficiency_S1.Size = AquaCrop_Water_Use_Efficiency_Data_S1.shape
    AquaCrop_Water_Use_Efficiency_S1.Variable = "AquaCrop Water Use Efficiency Season 1"
    AquaCrop_Water_Use_Efficiency_S1.Unit = "kg-m-2"
    
    del AquaCrop_Water_Use_Efficiency_Data_S1
    
    AquaCrop_Water_Use_Efficiency_S1.Save_As_Tiff(os.path.join(output_folder_L3, "AquaCrop_Water_Use_Efficiency", "S1"))    

   # Season 2
    AquaCrop_Water_Use_Efficiency_Data_S2 = 1000 * (Accumulated_Biomass_Production_S2.Data/(10 * Accumulated_DOY_Data_S2 * Accumulated_T_Data_S2/Accumulated_ET0_Data_S2))

    # Write in DataCube
    AquaCrop_Water_Use_Efficiency_S2 = DataCube.Rasterdata_Empty()
    AquaCrop_Water_Use_Efficiency_S2.Data = AquaCrop_Water_Use_Efficiency_Data_S2.clip(0,100) * MASK
    AquaCrop_Water_Use_Efficiency_S2.Projection = ET.Projection
    AquaCrop_Water_Use_Efficiency_S2.GeoTransform = ET.GeoTransform
    AquaCrop_Water_Use_Efficiency_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    AquaCrop_Water_Use_Efficiency_S2.Size = AquaCrop_Water_Use_Efficiency_Data_S2.shape
    AquaCrop_Water_Use_Efficiency_S2.Variable = "AquaCrop Water Use Efficiency Season 2"
    AquaCrop_Water_Use_Efficiency_S2.Unit = "kg-m-2"
    
    del AquaCrop_Water_Use_Efficiency_Data_S2
    
    AquaCrop_Water_Use_Efficiency_S2.Save_As_Tiff(os.path.join(output_folder_L3, "AquaCrop_Water_Use_Efficiency", "S2"))    

   # Season 3
    AquaCrop_Water_Use_Efficiency_Data_S3 = 1000 * (Accumulated_Biomass_Production_S3.Data/(10 * Accumulated_DOY_Data_S3 * Accumulated_T_Data_S3/Accumulated_ET0_Data_S3))

    # Write in DataCube
    AquaCrop_Water_Use_Efficiency_S3 = DataCube.Rasterdata_Empty()
    AquaCrop_Water_Use_Efficiency_S3.Data = AquaCrop_Water_Use_Efficiency_Data_S3.clip(0,100) * MASK
    AquaCrop_Water_Use_Efficiency_S3.Projection = ET.Projection
    AquaCrop_Water_Use_Efficiency_S3.GeoTransform = ET.GeoTransform
    AquaCrop_Water_Use_Efficiency_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    AquaCrop_Water_Use_Efficiency_S3.Size = AquaCrop_Water_Use_Efficiency_Data_S3.shape
    AquaCrop_Water_Use_Efficiency_S3.Variable = "AquaCrop Water Use Efficiency Season 3"
    AquaCrop_Water_Use_Efficiency_S3.Unit = "kg-m-2"
    
    del AquaCrop_Water_Use_Efficiency_Data_S3
    
    AquaCrop_Water_Use_Efficiency_S3.Save_As_Tiff(os.path.join(output_folder_L3, "AquaCrop_Water_Use_Efficiency", "S3"))    

   # Season Perennial
    AquaCrop_Water_Use_Efficiency_Data_Per = 1000 * (Accumulated_Biomass_Production_Per.Data/(10 * Accumulated_DOY_Data_Per * Accumulated_T_Data_Per/Accumulated_ET0_Data_Per))

    # Write in DataCube
    AquaCrop_Water_Use_Efficiency_Per = DataCube.Rasterdata_Empty()
    AquaCrop_Water_Use_Efficiency_Per.Data = AquaCrop_Water_Use_Efficiency_Data_Per.clip(0,100) * MASK
    AquaCrop_Water_Use_Efficiency_Per.Projection = ET.Projection
    AquaCrop_Water_Use_Efficiency_Per.GeoTransform = ET.GeoTransform
    AquaCrop_Water_Use_Efficiency_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    AquaCrop_Water_Use_Efficiency_Per.Size = AquaCrop_Water_Use_Efficiency_Data_Per.shape
    AquaCrop_Water_Use_Efficiency_Per.Variable = "AquaCrop Water Use Efficiency Season Perennial"
    AquaCrop_Water_Use_Efficiency_Per.Unit = "kg-m-2"
    
    del AquaCrop_Water_Use_Efficiency_Data_Per
    
    AquaCrop_Water_Use_Efficiency_Per.Save_As_Tiff(os.path.join(output_folder_L3, "AquaCrop_Water_Use_Efficiency", "Perennial"))    

    ######################### Calculate Gross Biomass Water Productivity - Decade #########################
    GBWP_Decade_Data = Actual_Biomass_Production.Data/(10 * ET.Data)
    
    # Write in DataCube
    GBWP_Decade = DataCube.Rasterdata_Empty()
    GBWP_Decade.Data = GBWP_Decade_Data * MASK
    GBWP_Decade.Projection = ET.Projection
    GBWP_Decade.GeoTransform = ET.GeoTransform
    GBWP_Decade.Ordinal_time = ET.Ordinal_time
    GBWP_Decade.Size = GBWP_Decade_Data.shape
    GBWP_Decade.Variable = "Gross Biomass Water Productivity"
    GBWP_Decade.Unit = "kg-m-3"
    
    del GBWP_Decade_Data
    
    GBWP_Decade.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Decade"))         
    
    ######################### Calculate Gross Biomass Water Productivity - Accumulated #########################
    GBWP_Accumulated_Data = (Accumulated_Biomass_Production.Data)/(10 * Accumulated_ET_Data)
    
    # Write in DataCube
    GBWP_Season = DataCube.Rasterdata_Empty()
    GBWP_Season.Data = GBWP_Accumulated_Data * MASK
    GBWP_Season.Projection = ET.Projection
    GBWP_Season.GeoTransform = ET.GeoTransform
    GBWP_Season.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    GBWP_Season.Size = GBWP_Accumulated_Data.shape
    GBWP_Season.Variable = "Gross Biomass Water Productivity Season"
    GBWP_Season.Unit = "kg-m-3"
    
    del GBWP_Accumulated_Data
    
    GBWP_Season.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Season", "All"))           

    # Season 1
    GBWP_Accumulated_Data_S1 = (Accumulated_Biomass_Production_S1.Data)/(10 * Accumulated_ET_Data_S1)
    
    # Write in DataCube
    GBWP_Season_S1 = DataCube.Rasterdata_Empty()
    GBWP_Season_S1.Data = GBWP_Accumulated_Data_S1 * MASK
    GBWP_Season_S1.Projection = ET.Projection
    GBWP_Season_S1.GeoTransform = ET.GeoTransform
    GBWP_Season_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    GBWP_Season_S1.Size = GBWP_Accumulated_Data_S1.shape
    GBWP_Season_S1.Variable = "Gross Biomass Water Productivity Season 1"
    GBWP_Season_S1.Unit = "kg-m-3"
    
    del GBWP_Accumulated_Data_S1
    
    GBWP_Season_S1.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Season", "S1"))           

    # Season 2
    GBWP_Accumulated_Data_S2 = (Accumulated_Biomass_Production_S2.Data)/(10 * Accumulated_ET_Data_S2)
    
    # Write in DataCube
    GBWP_Season_S2 = DataCube.Rasterdata_Empty()
    GBWP_Season_S2.Data = GBWP_Accumulated_Data_S2 * MASK
    GBWP_Season_S2.Projection = ET.Projection
    GBWP_Season_S2.GeoTransform = ET.GeoTransform
    GBWP_Season_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    GBWP_Season_S2.Size = GBWP_Accumulated_Data_S2.shape
    GBWP_Season_S2.Variable = "Gross Biomass Water Productivity Season 2"
    GBWP_Season_S2.Unit = "kg-m-3"
    
    del GBWP_Accumulated_Data_S2
    
    GBWP_Season_S2.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Season", "S2"))         

    # Season 3
    GBWP_Accumulated_Data_S3 = (Accumulated_Biomass_Production_S3.Data)/(10 * Accumulated_ET_Data_S3)
    
    # Write in DataCube
    GBWP_Season_S3 = DataCube.Rasterdata_Empty()
    GBWP_Season_S3.Data = GBWP_Accumulated_Data_S3 * MASK
    GBWP_Season_S3.Projection = ET.Projection
    GBWP_Season_S3.GeoTransform = ET.GeoTransform
    GBWP_Season_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    GBWP_Season_S3.Size = GBWP_Accumulated_Data_S3.shape
    GBWP_Season_S3.Variable = "Gross Biomass Water Productivity Season 3"
    GBWP_Season_S3.Unit = "kg-m-3"
    
    del GBWP_Accumulated_Data_S3
    
    GBWP_Season_S3.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Season", "S3"))         

    # Season Perennial
    GBWP_Accumulated_Data_Per = (Accumulated_Biomass_Production_Per.Data)/(10 * Accumulated_ET_Data_Per)
    
    # Write in DataCube
    GBWP_Season_Per = DataCube.Rasterdata_Empty()
    GBWP_Season_Per.Data = GBWP_Accumulated_Data_Per * MASK
    GBWP_Season_Per.Projection = ET.Projection
    GBWP_Season_Per.GeoTransform = ET.GeoTransform
    GBWP_Season_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    GBWP_Season_Per.Size = GBWP_Accumulated_Data_Per.shape
    GBWP_Season_Per.Variable = "Gross Biomass Water Productivity Season Perennial"
    GBWP_Season_Per.Unit = "kg-m-3"
    
    del GBWP_Accumulated_Data_Per
    
    GBWP_Season_Per.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Season", "Perennial"))         

    ######################### Calculate amount of days season - Accumulated #########################
    DOY_Accumulated_Data = Accumulated_DOY_Data_S1 + Accumulated_DOY_Data_S2 + Accumulated_DOY_Data_S3 + Accumulated_DOY_Data_Per
    
    # Write in DataCube
    DOY_Accumulated = DataCube.Rasterdata_Empty()
    DOY_Accumulated.Data = DOY_Accumulated_Data * MASK
    DOY_Accumulated.Projection = ET.Projection
    DOY_Accumulated.GeoTransform = ET.GeoTransform
    DOY_Accumulated.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    DOY_Accumulated.Size = DOY_Accumulated_Data.shape
    DOY_Accumulated.Variable = "Amount Of Days Season"
    DOY_Accumulated.Unit = "days"
    
    del DOY_Accumulated_Data
    
    DOY_Accumulated.Save_As_Tiff(os.path.join(output_folder_L3, "Days_Season", "All"))           

    # Season 1
    DOY_Accumulated_Data_S1 = Accumulated_DOY_Data_S1
    
    # Write in DataCube
    DOY_Accumulated_S1 = DataCube.Rasterdata_Empty()
    DOY_Accumulated_S1.Data = DOY_Accumulated_Data_S1 * MASK
    DOY_Accumulated_S1.Projection = ET.Projection
    DOY_Accumulated_S1.GeoTransform = ET.GeoTransform
    DOY_Accumulated_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    DOY_Accumulated_S1.Size = DOY_Accumulated_Data_S1.shape
    DOY_Accumulated_S1.Variable = "Amount Of Days Season 1"
    DOY_Accumulated_S1.Unit = "days"
    
    del DOY_Accumulated_Data_S1
    
    DOY_Accumulated_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Days_Season", "S1"))           

    # Season 2
    DOY_Accumulated_Data_S2 = Accumulated_DOY_Data_S2
    
    # Write in DataCube
    DOY_Accumulated_S2 = DataCube.Rasterdata_Empty()
    DOY_Accumulated_S2.Data = DOY_Accumulated_Data_S2 * MASK
    DOY_Accumulated_S2.Projection = ET.Projection
    DOY_Accumulated_S2.GeoTransform = ET.GeoTransform
    DOY_Accumulated_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    DOY_Accumulated_S2.Size = DOY_Accumulated_Data_S2.shape
    DOY_Accumulated_S2.Variable = "Amount Of Days Season 2"
    DOY_Accumulated_S2.Unit = "days"
    
    del DOY_Accumulated_Data_S2
    
    DOY_Accumulated_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Days_Season", "S2"))           
   
    # Season 3
    DOY_Accumulated_Data_S3 = Accumulated_DOY_Data_S3
    
    # Write in DataCube
    DOY_Accumulated_S3 = DataCube.Rasterdata_Empty()
    DOY_Accumulated_S3.Data = DOY_Accumulated_Data_S3 * MASK
    DOY_Accumulated_S3.Projection = ET.Projection
    DOY_Accumulated_S3.GeoTransform = ET.GeoTransform
    DOY_Accumulated_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    DOY_Accumulated_S3.Size = DOY_Accumulated_Data_S3.shape
    DOY_Accumulated_S3.Variable = "Amount Of Days Season 3"
    DOY_Accumulated_S3.Unit = "days"
    
    del DOY_Accumulated_Data_S3
    
    DOY_Accumulated_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Days_Season", "S3"))           

    # Season Perennial
    DOY_Accumulated_Data_Per = Accumulated_DOY_Data_Per
    
    # Write in DataCube
    DOY_Accumulated_Per = DataCube.Rasterdata_Empty()
    DOY_Accumulated_Per.Data = DOY_Accumulated_Data_Per * MASK
    DOY_Accumulated_Per.Projection = ET.Projection
    DOY_Accumulated_Per.GeoTransform = ET.GeoTransform
    DOY_Accumulated_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    DOY_Accumulated_Per.Size = DOY_Accumulated_Data_Per.shape
    DOY_Accumulated_Per.Variable = "Amount Of Days Season Perennial"
    DOY_Accumulated_Per.Unit = "days"
    
    del DOY_Accumulated_Data_Per
    
    DOY_Accumulated_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Days_Season", "Perennial"))         

    ################################# Calculate Mean Yield Fresh Grass over every AEZ per year #################################
    L3_AEZ_ET = dict()
    AEZ.Data = AEZ.Data.astype(np.int)
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        L3_AEZ_ET[int(AEZ_ID)] = np.nanpercentile(np.where(AEZ.Data == AEZ_ID, ET.Data, np.nan), 99, axis=(1,2))
        
    ET_target_Data = np.ones(Actual_Biomass_Production.Size) * np.nan
    for AEZ_ID in np.unique(AEZ.Data[~np.isnan(AEZ.Data)]):
        ET_target_Data = np.where(AEZ.Data == AEZ_ID, L3_AEZ_ET[int(AEZ_ID)][:, None, None], ET_target_Data)   
        
    ######################### Calculate Gross Biomass Water Productivity - Target #########################
    GBWP_Target_Data = Target_Biomass_Production.Data/(10 * ET_target_Data) 
    
    # Write in DataCube
    GBWP_Target = DataCube.Rasterdata_Empty()
    GBWP_Target.Data = GBWP_Target_Data * MASK
    GBWP_Target.Projection = ET.Projection
    GBWP_Target.GeoTransform = ET.GeoTransform
    GBWP_Target.Ordinal_time = ET.Ordinal_time
    GBWP_Target.Size = GBWP_Target_Data.shape
    GBWP_Target.Variable = "Gross Biomass Water Productivity Target"
    GBWP_Target.Unit = "kg-m-3"
    
    del GBWP_Target_Data
    
    GBWP_Target.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Target"))     
    
    ######################### Calculate Gross Biomass Water Productivity - Gap #########################
    GBWP_Gap_Data = GBWP_Decade.Data - GBWP_Target.Data
    GBWP_Gap_Data = GBWP_Gap_Data.clip(-10000, 0)
    
    # Write in DataCube
    GBWP_Gap = DataCube.Rasterdata_Empty()
    GBWP_Gap.Data = GBWP_Gap_Data * MASK
    GBWP_Gap.Projection = ET.Projection
    GBWP_Gap.GeoTransform = ET.GeoTransform
    GBWP_Gap.Ordinal_time = ET.Ordinal_time
    GBWP_Gap.Size = GBWP_Gap_Data.shape
    GBWP_Gap.Variable = "Gross Biomass Water Productivity Gap"
    GBWP_Gap.Unit = "kg-m-3"
    
    del GBWP_Gap_Data
    
    GBWP_Gap.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Gap"))     

    ######################### Calculate Gross Biomass Water Productivity - Improvement Required #########################
    GBWP_Improvements_Required_Data = (GBWP_Target.Data - GBWP_Decade.Data)/GBWP_Decade.Data * 100

    # Write in DataCube
    GBWP_Improvements_Required = DataCube.Rasterdata_Empty()
    GBWP_Improvements_Required.Data = GBWP_Improvements_Required_Data * MASK
    GBWP_Improvements_Required.Projection = ET.Projection
    GBWP_Improvements_Required.GeoTransform = ET.GeoTransform
    GBWP_Improvements_Required.Ordinal_time = ET.Ordinal_time
    GBWP_Improvements_Required.Size = GBWP_Improvements_Required_Data.shape
    GBWP_Improvements_Required.Variable = "Gross Biomass Water Productivity Improvement Required"
    GBWP_Improvements_Required.Unit = "Percentage"
    
    del GBWP_Improvements_Required_Data
    
    GBWP_Improvements_Required.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Improvement_Required"))     
    
    ######################### Calculate Normalized Gross Biomass Water Productivity Maximum Per TBP #########################
    Total_years = int(np.ceil(ET0.Size[0]/36))
    Mean_Long_Term_ET0_Data = np.ones([36, ET0.Size[1], ET0.Size[2]]) * np.nan
    
    for dekad in range(0,36):
        IDs = np.array(range(0, Total_years)) * 36 + dekad  
        IDs_good = IDs[IDs<=ET0.Size[0]]
        Mean_Long_Term_ET0_Data[dekad, :, :] = np.nanmean(ET0.Data[IDs_good,:,:], axis = 0) 
   
    Normalized_GBWP_Max_Per_TBP_Data = 5.7 * ET0.Data/np.tile(Mean_Long_Term_ET0_Data, (Total_years, 1, 1))

    # Write in DataCube
    Normalized_GBWP_Max_Per_TBP = DataCube.Rasterdata_Empty()
    Normalized_GBWP_Max_Per_TBP.Data = Normalized_GBWP_Max_Per_TBP_Data * MASK
    Normalized_GBWP_Max_Per_TBP.Projection = ET.Projection
    Normalized_GBWP_Max_Per_TBP.GeoTransform = ET.GeoTransform
    Normalized_GBWP_Max_Per_TBP.Ordinal_time = ET.Ordinal_time
    Normalized_GBWP_Max_Per_TBP.Size = Normalized_GBWP_Max_Per_TBP_Data.shape
    Normalized_GBWP_Max_Per_TBP.Variable = "Normalized Gross Biomass Water Productivity Maximum per TBP"
    Normalized_GBWP_Max_Per_TBP.Unit = "kg-m-3"
    
    del Normalized_GBWP_Max_Per_TBP_Data
    
    Normalized_GBWP_Max_Per_TBP.Save_As_Tiff(os.path.join(output_folder_L3, "Normalized_GBWP_Max_Per_TBP"))  
    
    ######################### Calculate Normalized Gross Biomass Water Productivity Minimum Per TBP #########################
    Normalized_GBWP_Min_Per_TBP_Data = 1.7 * ET0.Data/np.tile(Mean_Long_Term_ET0_Data, (Total_years, 1, 1))

    # Write in DataCube
    Normalized_GBWP_Min_Per_TBP = DataCube.Rasterdata_Empty()
    Normalized_GBWP_Min_Per_TBP.Data = Normalized_GBWP_Min_Per_TBP_Data * MASK
    Normalized_GBWP_Min_Per_TBP.Projection = ET.Projection
    Normalized_GBWP_Min_Per_TBP.GeoTransform = ET.GeoTransform
    Normalized_GBWP_Min_Per_TBP.Ordinal_time = ET.Ordinal_time
    Normalized_GBWP_Min_Per_TBP.Size = Normalized_GBWP_Min_Per_TBP_Data.shape
    Normalized_GBWP_Min_Per_TBP.Variable = "Normalized Gross Biomass Water Productivity Minimum per TBP"
    Normalized_GBWP_Min_Per_TBP.Unit = "kg-m-3"
    
    del Normalized_GBWP_Min_Per_TBP_Data
    
    Normalized_GBWP_Min_Per_TBP.Save_As_Tiff(os.path.join(output_folder_L3, "Normalized_GBWP_Min_Per_TBP"))      
    
    ########################## Calculate Water Productivity Score #########################
    Water_Productivity_Score_Data = 9 * (GBWP_Decade.Data * ET0.Data/np.tile(Mean_Long_Term_ET0_Data, (Total_years, 1, 1)) - Normalized_GBWP_Min_Per_TBP.Data)/(Normalized_GBWP_Max_Per_TBP.Data - Normalized_GBWP_Min_Per_TBP.Data) + 1

    # Write in DataCube
    Water_Productivity_Score = DataCube.Rasterdata_Empty()
    Water_Productivity_Score.Data = Water_Productivity_Score_Data * MASK
    Water_Productivity_Score.Projection = ET.Projection
    Water_Productivity_Score.GeoTransform = ET.GeoTransform
    Water_Productivity_Score.Ordinal_time = ET.Ordinal_time
    Water_Productivity_Score.Size = Water_Productivity_Score_Data.shape
    Water_Productivity_Score.Variable = "Water Productivity Score Data"
    Water_Productivity_Score.Unit = "-"
    
    del Water_Productivity_Score_Data
    
    Water_Productivity_Score.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Productivity_Score"))      
    
    ########################## Calculate Water Productivity #########################
    Water_Productivity_Data = (Yield.Data)/(10 * Accumulated_ET_Data)       
    
    # Write in DataCube
    Water_Productivity = DataCube.Rasterdata_Empty()
    Water_Productivity.Data = Water_Productivity_Data * MASK
    Water_Productivity.Projection = ET.Projection
    Water_Productivity.GeoTransform = ET.GeoTransform
    Water_Productivity.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Water_Productivity.Size = Water_Productivity_Data.shape
    Water_Productivity.Variable = "Water Productivity"
    Water_Productivity.Unit = "kg-m-3"
    
    del Water_Productivity_Data
    
    Water_Productivity.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Productivity", "All"))       

    # Season 1
    Water_Productivity_Data_S1 = (Yield_S1.Data)/(10 * Accumulated_ET_Data_S1)       
    
    # Write in DataCube
    Water_Productivity_S1 = DataCube.Rasterdata_Empty()
    Water_Productivity_S1.Data = Water_Productivity_Data_S1 * MASK
    Water_Productivity_S1.Projection = ET.Projection
    Water_Productivity_S1.GeoTransform = ET.GeoTransform
    Water_Productivity_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Water_Productivity_S1.Size = Water_Productivity_Data_S1.shape
    Water_Productivity_S1.Variable = "Water Productivity Season 1"
    Water_Productivity_S1.Unit = "kg-m-3"
    
    del Water_Productivity_Data_S1
    
    Water_Productivity_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Productivity", "S1"))      

    # Season 2
    Water_Productivity_Data_S2 = (Yield_S2.Data)/(10 * Accumulated_ET_Data_S2)       
    
    # Write in DataCube
    Water_Productivity_S2 = DataCube.Rasterdata_Empty()
    Water_Productivity_S2.Data = Water_Productivity_Data_S2 * MASK
    Water_Productivity_S2.Projection = ET.Projection
    Water_Productivity_S2.GeoTransform = ET.GeoTransform
    Water_Productivity_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Water_Productivity_S2.Size = Water_Productivity_Data_S2.shape
    Water_Productivity_S2.Variable = "Water Productivity Season 2"
    Water_Productivity_S2.Unit = "kg-m-3"
    
    del Water_Productivity_Data_S2
    
    Water_Productivity_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Productivity", "S2"))     

    # Season 3
    Water_Productivity_Data_S3 = (Yield_S3.Data)/(10 * Accumulated_ET_Data_S3)       
    
    # Write in DataCube
    Water_Productivity_S3 = DataCube.Rasterdata_Empty()
    Water_Productivity_S3.Data = Water_Productivity_Data_S3 * MASK
    Water_Productivity_S3.Projection = ET.Projection
    Water_Productivity_S3.GeoTransform = ET.GeoTransform
    Water_Productivity_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Water_Productivity_S3.Size = Water_Productivity_Data_S3.shape
    Water_Productivity_S3.Variable = "Water Productivity Season 3"
    Water_Productivity_S3.Unit = "kg-m-3"
    
    del Water_Productivity_Data_S3
    
    Water_Productivity_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Productivity", "S3"))    

    # Season Perennial
    Water_Productivity_Data_Per = (Yield_Per.Data)/(10 * Accumulated_ET_Data_Per)       
    
    # Write in DataCube
    Water_Productivity_Per = DataCube.Rasterdata_Empty()
    Water_Productivity_Per.Data = Water_Productivity_Data_Per * MASK
    Water_Productivity_Per.Projection = ET.Projection
    Water_Productivity_Per.GeoTransform = ET.GeoTransform
    Water_Productivity_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Water_Productivity_Per.Size = Water_Productivity_Data_Per.shape
    Water_Productivity_Per.Variable = "Water Productivity Season Perennial"
    Water_Productivity_Per.Unit = "kg-m-3"
    
    del Water_Productivity_Data_Per
    
    Water_Productivity_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Productivity", "Perennial"))    

    ########################## Save Accumulated ET  ##########################

    # Write in DataCube
    Accumulated_ET = DataCube.Rasterdata_Empty()
    Accumulated_ET.Data = Accumulated_ET_Data * MASK
    Accumulated_ET.Projection = ET.Projection
    Accumulated_ET.GeoTransform = ET.GeoTransform
    Accumulated_ET.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET.Size = Accumulated_ET_Data.shape
    Accumulated_ET.Variable = "Accumulated ET"
    Accumulated_ET.Unit = "mm"
    
    Accumulated_ET.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET", "All"))    

    # Write in DataCube Season 1
    Accumulated_ET_S1 = DataCube.Rasterdata_Empty()
    Accumulated_ET_S1.Data = Accumulated_ET_Data_S1 * MASK
    Accumulated_ET_S1.Projection = ET.Projection
    Accumulated_ET_S1.GeoTransform = ET.GeoTransform
    Accumulated_ET_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET_S1.Size = Accumulated_ET_Data_S1.shape
    Accumulated_ET_S1.Variable = "Accumulated ET Season 1"
    Accumulated_ET_S1.Unit = "mm"
    
    Accumulated_ET_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET", "S1"))    

    # Write in DataCube Season 2
    Accumulated_ET_S2 = DataCube.Rasterdata_Empty()
    Accumulated_ET_S2.Data = Accumulated_ET_Data_S2 * MASK
    Accumulated_ET_S2.Projection = ET.Projection
    Accumulated_ET_S2.GeoTransform = ET.GeoTransform
    Accumulated_ET_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET_S2.Size = Accumulated_ET_Data_S2.shape
    Accumulated_ET_S2.Variable = "Accumulated ET Season 2"
    Accumulated_ET_S2.Unit = "mm"
    
    Accumulated_ET_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET", "S2"))    

    # Write in DataCube Season 3
    Accumulated_ET_S3 = DataCube.Rasterdata_Empty()
    Accumulated_ET_S3.Data = Accumulated_ET_Data_S3 * MASK
    Accumulated_ET_S3.Projection = ET.Projection
    Accumulated_ET_S3.GeoTransform = ET.GeoTransform
    Accumulated_ET_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET_S3.Size = Accumulated_ET_Data_S3.shape
    Accumulated_ET_S3.Variable = "Accumulated ET Season 3"
    Accumulated_ET_S3.Unit = "mm"
    
    Accumulated_ET_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_ET_Per = DataCube.Rasterdata_Empty()
    Accumulated_ET_Per.Data = Accumulated_ET_Data_Per * MASK
    Accumulated_ET_Per.Projection = ET.Projection
    Accumulated_ET_Per.GeoTransform = ET.GeoTransform
    Accumulated_ET_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET_Per.Size = Accumulated_ET_Data_Per.shape
    Accumulated_ET_Per.Variable = "Accumulated ET Season Perennial"
    Accumulated_ET_Per.Unit = "mm"
    
    Accumulated_ET_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET", "Perennial")) 

    ########################## Save Accumulated T  ##########################

    # Write in DataCube
    Accumulated_T = DataCube.Rasterdata_Empty()
    Accumulated_T.Data = Accumulated_T_Data * MASK
    Accumulated_T.Projection = ET.Projection
    Accumulated_T.GeoTransform = ET.GeoTransform
    Accumulated_T.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_T.Size = Accumulated_T_Data.shape
    Accumulated_T.Variable = "Accumulated T"
    Accumulated_T.Unit = "mm"
    
    Accumulated_T.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T", "All"))    

    # Write in DataCube Season 1
    Accumulated_T_S1 = DataCube.Rasterdata_Empty()
    Accumulated_T_S1.Data = Accumulated_T_Data_S1 * MASK
    Accumulated_T_S1.Projection = ET.Projection
    Accumulated_T_S1.GeoTransform = ET.GeoTransform
    Accumulated_T_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_T_S1.Size = Accumulated_T_Data_S1.shape
    Accumulated_T_S1.Variable = "Accumulated T Season 1"
    Accumulated_T_S1.Unit = "mm"
    
    Accumulated_T_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T", "S1"))    

    # Write in DataCube Season 2
    Accumulated_T_S2 = DataCube.Rasterdata_Empty()
    Accumulated_T_S2.Data = Accumulated_T_Data_S2 * MASK
    Accumulated_T_S2.Projection = ET.Projection
    Accumulated_T_S2.GeoTransform = ET.GeoTransform
    Accumulated_T_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_T_S2.Size = Accumulated_T_Data_S2.shape
    Accumulated_T_S2.Variable = "Accumulated T Season 2"
    Accumulated_T_S2.Unit = "mm"
    
    Accumulated_T_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T", "S2"))    

    # Write in DataCube Season 3
    Accumulated_T_S3 = DataCube.Rasterdata_Empty()
    Accumulated_T_S3.Data = Accumulated_T_Data_S3 * MASK
    Accumulated_T_S3.Projection = ET.Projection
    Accumulated_T_S3.GeoTransform = ET.GeoTransform
    Accumulated_T_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_T_S3.Size = Accumulated_T_Data_S3.shape
    Accumulated_T_S3.Variable = "Accumulated T Season 3"
    Accumulated_T_S3.Unit = "mm"
    
    Accumulated_T_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_T_Per = DataCube.Rasterdata_Empty()
    Accumulated_T_Per.Data = Accumulated_T_Data_Per * MASK
    Accumulated_T_Per.Projection = ET.Projection
    Accumulated_T_Per.GeoTransform = ET.GeoTransform
    Accumulated_T_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_T_Per.Size = Accumulated_T_Data_Per.shape
    Accumulated_T_Per.Variable = "Accumulated T Season Perennial"
    Accumulated_T_Per.Unit = "mm"
    
    Accumulated_T_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T", "Perennial")) 

    ########################## Save Accumulated ET0  ##########################

    # Write in DataCube
    Accumulated_ET0 = DataCube.Rasterdata_Empty()
    Accumulated_ET0.Data = Accumulated_ET0_Data * MASK
    Accumulated_ET0.Projection = ET.Projection
    Accumulated_ET0.GeoTransform = ET.GeoTransform
    Accumulated_ET0.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET0.Size = Accumulated_ET0_Data.shape
    Accumulated_ET0.Variable = "Accumulated ET0"
    Accumulated_ET0.Unit = "mm"
    
    Accumulated_ET0.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0", "All"))    

    # Write in DataCube Season 1
    Accumulated_ET0_S1 = DataCube.Rasterdata_Empty()
    Accumulated_ET0_S1.Data = Accumulated_ET0_Data_S1 * MASK
    Accumulated_ET0_S1.Projection = ET.Projection
    Accumulated_ET0_S1.GeoTransform = ET.GeoTransform
    Accumulated_ET0_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET0_S1.Size = Accumulated_ET0_Data_S1.shape
    Accumulated_ET0_S1.Variable = "Accumulated ET0 Season 1"
    Accumulated_ET0_S1.Unit = "mm"
    
    Accumulated_ET0_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0", "S1"))    

    # Write in DataCube Season 2
    Accumulated_ET0_S2 = DataCube.Rasterdata_Empty()
    Accumulated_ET0_S2.Data = Accumulated_ET0_Data_S2 * MASK
    Accumulated_ET0_S2.Projection = ET.Projection
    Accumulated_ET0_S2.GeoTransform = ET.GeoTransform
    Accumulated_ET0_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET0_S2.Size = Accumulated_ET0_Data_S2.shape
    Accumulated_ET0_S2.Variable = "Accumulated ET0 Season 2"
    Accumulated_ET0_S2.Unit = "mm"
    
    Accumulated_ET0_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0", "S2"))    

    # Write in DataCube Season 3
    Accumulated_ET0_S3 = DataCube.Rasterdata_Empty()
    Accumulated_ET0_S3.Data = Accumulated_ET0_Data_S3 * MASK
    Accumulated_ET0_S3.Projection = ET.Projection
    Accumulated_ET0_S3.GeoTransform = ET.GeoTransform
    Accumulated_ET0_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET0_S3.Size = Accumulated_ET0_Data_S3.shape
    Accumulated_ET0_S3.Variable = "Accumulated ET0 Season 3"
    Accumulated_ET0_S3.Unit = "mm"
    
    Accumulated_ET0_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_ET0_Per = DataCube.Rasterdata_Empty()
    Accumulated_ET0_Per.Data = Accumulated_ET0_Data_Per * MASK
    Accumulated_ET0_Per.Projection = ET.Projection
    Accumulated_ET0_Per.GeoTransform = ET.GeoTransform
    Accumulated_ET0_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET0_Per.Size = Accumulated_ET0_Data_Per.shape
    Accumulated_ET0_Per.Variable = "Accumulated ET0 Season Perennial"
    Accumulated_ET0_Per.Unit = "mm"
    
    Accumulated_ET0_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0", "Perennial")) 

    ########################## Save Accumulated P  ##########################

    # Write in DataCube
    Accumulated_P = DataCube.Rasterdata_Empty()
    Accumulated_P.Data = Accumulated_P_Data * MASK
    Accumulated_P.Projection = ET.Projection
    Accumulated_P.GeoTransform = ET.GeoTransform
    Accumulated_P.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_P.Size = Accumulated_P_Data.shape
    Accumulated_P.Variable = "Accumulated P"
    Accumulated_P.Unit = "mm"
    
    Accumulated_P.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P", "All"))    

    # Write in DataCube Season 1
    Accumulated_P_S1 = DataCube.Rasterdata_Empty()
    Accumulated_P_S1.Data = Accumulated_P_Data_S1 * MASK
    Accumulated_P_S1.Projection = ET.Projection
    Accumulated_P_S1.GeoTransform = ET.GeoTransform
    Accumulated_P_S1.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_P_S1.Size = Accumulated_P_Data_S1.shape
    Accumulated_P_S1.Variable = "Accumulated P Season 1"
    Accumulated_P_S1.Unit = "mm"
    
    Accumulated_P_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P", "S1"))    

    # Write in DataCube Season 2
    Accumulated_P_S2 = DataCube.Rasterdata_Empty()
    Accumulated_P_S2.Data = Accumulated_P_Data_S2 * MASK
    Accumulated_P_S2.Projection = ET.Projection
    Accumulated_P_S2.GeoTransform = ET.GeoTransform
    Accumulated_P_S2.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_P_S2.Size = Accumulated_P_Data_S2.shape
    Accumulated_P_S2.Variable = "Accumulated P Season 2"
    Accumulated_P_S2.Unit = "mm"
    
    Accumulated_P_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P", "S2"))    

    # Write in DataCube Season 3
    Accumulated_P_S3 = DataCube.Rasterdata_Empty()
    Accumulated_P_S3.Data = Accumulated_P_Data_S3 * MASK
    Accumulated_P_S3.Projection = ET.Projection
    Accumulated_P_S3.GeoTransform = ET.GeoTransform
    Accumulated_P_S3.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_P_S3.Size = Accumulated_P_Data_S3.shape
    Accumulated_P_S3.Variable = "Accumulated P Season 3"
    Accumulated_P_S3.Unit = "mm"
    
    Accumulated_P_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_P_Per = DataCube.Rasterdata_Empty()
    Accumulated_P_Per.Data = Accumulated_P_Data_Per * MASK
    Accumulated_P_Per.Projection = ET.Projection
    Accumulated_P_Per.GeoTransform = ET.GeoTransform
    Accumulated_P_Per.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_P_Per.Size = Accumulated_P_Data_Per.shape
    Accumulated_P_Per.Variable = "Accumulated P Season Perennial"
    Accumulated_P_Per.Unit = "mm"
    
    Accumulated_P_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P", "Perennial")) 

    ######################### Add trends ##########################################################
    
    # Set time
    T = np.arange(len(Dates_Years)) 
    
    # Calculate trend ET
    trend_year = ((np.sum(np.where(np.isnan(Accumulated_ET.Data),0,1),axis = 0) * np.nansum(Accumulated_ET.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET_Change_In_Time_Data = trend_year / np.nanmean(Accumulated_ET.Data, axis = 0) * 100
    
    trend_year_S1 = ((np.sum(np.where(np.isnan(Accumulated_ET_S1.Data),0,1),axis = 0) * np.nansum(Accumulated_ET_S1.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET_S1.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET_S1.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET_Change_In_Time_Data_S1 = trend_year_S1 / np.nanmean(Accumulated_ET_S1.Data, axis = 0) * 100 
    
    trend_year_S2  = ((np.sum(np.where(np.isnan(Accumulated_ET_S2.Data),0,1),axis = 0) * np.nansum(Accumulated_ET_S2.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET_S2.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET_S2.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET_Change_In_Time_Data_S2 = trend_year_S2 / np.nanmean(Accumulated_ET_S2.Data, axis = 0) * 100     
    
    trend_year_S3 = ((np.sum(np.where(np.isnan(Accumulated_ET_S3.Data),0,1),axis = 0) * np.nansum(Accumulated_ET_S3.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET_S3.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET_S3.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET_Change_In_Time_Data_S3 = trend_year_S3 / np.nanmean(Accumulated_ET_S3.Data, axis = 0) * 100
    
    trend_year_Per = ((np.sum(np.where(np.isnan(Accumulated_ET_Per.Data),0,1),axis = 0) * np.nansum(Accumulated_ET_Per.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET_Per.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET_Per.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET_Change_In_Time_Data_Per = trend_year_Per / np.nanmean(Accumulated_ET_Per.Data, axis = 0) * 100

    # Calculate trend T
    trend_year = ((np.sum(np.where(np.isnan(Accumulated_T.Data),0,1),axis = 0) * np.nansum(Accumulated_T.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_T.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_T.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    T_Change_In_Time_Data = trend_year / np.nanmean(Accumulated_T.Data, axis = 0) * 100
    
    trend_year_S1 = ((np.sum(np.where(np.isnan(Accumulated_T_S1.Data),0,1),axis = 0) * np.nansum(Accumulated_T_S1.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_T_S1.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_T_S1.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    T_Change_In_Time_Data_S1 = trend_year_S1 / np.nanmean(Accumulated_T_S1.Data, axis = 0) * 100 
    
    trend_year_S2  = ((np.sum(np.where(np.isnan(Accumulated_T_S2.Data),0,1),axis = 0) * np.nansum(Accumulated_T_S2.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_T_S2.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_T_S2.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    T_Change_In_Time_Data_S2 = trend_year_S2 / np.nanmean(Accumulated_T_S2.Data, axis = 0) * 100     
    
    trend_year_S3 = ((np.sum(np.where(np.isnan(Accumulated_T_S3.Data),0,1),axis = 0) * np.nansum(Accumulated_T_S3.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_T_S3.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_T_S3.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    T_Change_In_Time_Data_S3 = trend_year_S3 / np.nanmean(Accumulated_T_S3.Data, axis = 0) * 100
    
    trend_year_Per = ((np.sum(np.where(np.isnan(Accumulated_T_Per.Data),0,1),axis = 0) * np.nansum(Accumulated_T_Per.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_T_Per.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_T_Per.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    T_Change_In_Time_Data_Per = trend_year_Per / np.nanmean(Accumulated_T_Per.Data, axis = 0) * 100

    # Calculate trend ET0
    trend_year = ((np.sum(np.where(np.isnan(Accumulated_ET0.Data),0,1),axis = 0) * np.nansum(Accumulated_ET0.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET0.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET0.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET0_Change_In_Time_Data = trend_year / np.nanmean(Accumulated_ET0.Data, axis = 0) * 100
    
    trend_year_S1 = ((np.sum(np.where(np.isnan(Accumulated_ET0_S1.Data),0,1),axis = 0) * np.nansum(Accumulated_ET0_S1.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET0_S1.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET0_S1.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET0_Change_In_Time_Data_S1 = trend_year_S1 / np.nanmean(Accumulated_ET0_S1.Data, axis = 0) * 100 
    
    trend_year_S2  = ((np.sum(np.where(np.isnan(Accumulated_ET0_S2.Data),0,1),axis = 0) * np.nansum(Accumulated_ET0_S2.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET0_S2.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET0_S2.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET0_Change_In_Time_Data_S2 = trend_year_S2 / np.nanmean(Accumulated_ET0_S2.Data, axis = 0) * 100     
    
    trend_year_S3 = ((np.sum(np.where(np.isnan(Accumulated_ET0_S3.Data),0,1),axis = 0) * np.nansum(Accumulated_ET0_S3.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET0_S3.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET0_S3.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET0_Change_In_Time_Data_S3 = trend_year_S3 / np.nanmean(Accumulated_ET0_S3.Data, axis = 0) * 100
    
    trend_year_Per = ((np.sum(np.where(np.isnan(Accumulated_ET0_Per.Data),0,1),axis = 0) * np.nansum(Accumulated_ET0_Per.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_ET0_Per.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_ET0_Per.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    ET0_Change_In_Time_Data_Per = trend_year_Per / np.nanmean(Accumulated_ET0_Per.Data, axis = 0) * 100


    # Calculate trend P
    trend_year = ((np.sum(np.where(np.isnan(Accumulated_P.Data),0,1),axis = 0) * np.nansum(Accumulated_P.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_P.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_P.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    P_Change_In_Time_Data = trend_year / np.nanmean(Accumulated_P.Data, axis = 0) * 100
    
    trend_year_S1 = ((np.sum(np.where(np.isnan(Accumulated_P_S1.Data),0,1),axis = 0) * np.nansum(Accumulated_P_S1.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_P_S1.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_P_S1.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    P_Change_In_Time_Data_S1 = trend_year_S1 / np.nanmean(Accumulated_P_S1.Data, axis = 0) * 100 
    
    trend_year_S2  = ((np.sum(np.where(np.isnan(Accumulated_P_S2.Data),0,1),axis = 0) * np.nansum(Accumulated_P_S2.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_P_S2.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_P_S2.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    P_Change_In_Time_Data_S2 = trend_year_S2 / np.nanmean(Accumulated_P_S2.Data, axis = 0) * 100     
    
    trend_year_S3 = ((np.sum(np.where(np.isnan(Accumulated_P_S3.Data),0,1),axis = 0) * np.nansum(Accumulated_P_S3.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_P_S3.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_P_S3.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    P_Change_In_Time_Data_S3 = trend_year_S3 / np.nanmean(Accumulated_P_S3.Data, axis = 0) * 100
    
    trend_year_Per = ((np.sum(np.where(np.isnan(Accumulated_P_Per.Data),0,1),axis = 0) * np.nansum(Accumulated_P_Per.Data * T[:,None,None], axis = 0)) - (np.nansum(Accumulated_P_Per.Data, axis = 0) * np.nansum(T[:,None,None], axis = 0)))/((np.sum(np.where(np.isnan(Accumulated_P_Per.Data),0,1),axis = 0)* np.nansum(T[:,None,None] * T[:,None,None], axis = 0)) - (np.nansum(T[:,None,None], axis = 0) * np.nansum(T[:,None,None], axis = 0))) 
    P_Change_In_Time_Data_Per = trend_year_Per / np.nanmean(Accumulated_P_Per.Data, axis = 0) * 100

    ########################## Save Accumulated ET trend ##########################

    # Write in DataCube
    Accumulated_ET_Trend = DataCube.Rasterdata_Empty()
    Accumulated_ET_Trend.Data = ET_Change_In_Time_Data * MASK
    Accumulated_ET_Trend.Projection = ET.Projection
    Accumulated_ET_Trend.GeoTransform = ET.GeoTransform
    Accumulated_ET_Trend.Ordinal_time = None
    Accumulated_ET_Trend.Size = ET_Change_In_Time_Data.shape
    Accumulated_ET_Trend.Variable = "Accumulated ET Trend"
    Accumulated_ET_Trend.Unit = "Percentage-year-1"
    
    Accumulated_ET_Trend.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET_Trend", "All"))    

    # Write in DataCube Season 1
    Accumulated_ET_Trend_S1 = DataCube.Rasterdata_Empty()
    Accumulated_ET_Trend_S1.Data = ET_Change_In_Time_Data_S1 * MASK
    Accumulated_ET_Trend_S1.Projection = ET.Projection
    Accumulated_ET_Trend_S1.GeoTransform = ET.GeoTransform
    Accumulated_ET_Trend_S1.Ordinal_time = None
    Accumulated_ET_Trend_S1.Size = ET_Change_In_Time_Data_S1.shape
    Accumulated_ET_Trend_S1.Variable = "Accumulated ET Trend Season 1"
    Accumulated_ET_Trend_S1.Unit = "Percentage-year-1"
    
    Accumulated_ET_Trend_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET_Trend", "S1"))    

    # Write in DataCube Season 2
    Accumulated_ET_Trend_S2 = DataCube.Rasterdata_Empty()
    Accumulated_ET_Trend_S2.Data = ET_Change_In_Time_Data_S2 * MASK
    Accumulated_ET_Trend_S2.Projection = ET.Projection
    Accumulated_ET_Trend_S2.GeoTransform = ET.GeoTransform
    Accumulated_ET_Trend_S2.Ordinal_time = None
    Accumulated_ET_Trend_S2.Size = ET_Change_In_Time_Data_S2.shape
    Accumulated_ET_Trend_S2.Variable = "Accumulated ET Trend Season 2"
    Accumulated_ET_Trend_S2.Unit = "Percentage-year-1"
    
    Accumulated_ET_Trend_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET_Trend", "S2"))    

    # Write in DataCube Season 3
    Accumulated_ET_Trend_S3 = DataCube.Rasterdata_Empty()
    Accumulated_ET_Trend_S3.Data = ET_Change_In_Time_Data_S3 * MASK
    Accumulated_ET_Trend_S3.Projection = ET.Projection
    Accumulated_ET_Trend_S3.GeoTransform = ET.GeoTransform
    Accumulated_ET_Trend_S3.Ordinal_time = None
    Accumulated_ET_Trend_S3.Size = ET_Change_In_Time_Data_S3.shape
    Accumulated_ET_Trend_S3.Variable = "Accumulated ET Trend Season 3"
    Accumulated_ET_Trend_S3.Unit = "Percentage-year-1"
    
    Accumulated_ET_Trend_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET_Trend", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_ET_Trend_Per = DataCube.Rasterdata_Empty()
    Accumulated_ET_Trend_Per.Data = ET_Change_In_Time_Data_Per * MASK
    Accumulated_ET_Trend_Per.Projection = ET.Projection
    Accumulated_ET_Trend_Per.GeoTransform = ET.GeoTransform
    Accumulated_ET_Trend_Per.Ordinal_time = None
    Accumulated_ET_Trend_Per.Size = ET_Change_In_Time_Data_Per.shape
    Accumulated_ET_Trend_Per.Variable = "Accumulated ET Trend Season Perennial"
    Accumulated_ET_Trend_Per.Unit = "Percentage-year-1"
    
    Accumulated_ET_Trend_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET_Trend", "Perennial")) 

    ########################## Save Accumulated T trend ##########################

    # Write in DataCube
    Accumulated_T_Trend = DataCube.Rasterdata_Empty()
    Accumulated_T_Trend.Data = T_Change_In_Time_Data * MASK
    Accumulated_T_Trend.Projection = ET.Projection
    Accumulated_T_Trend.GeoTransform = ET.GeoTransform
    Accumulated_T_Trend.Ordinal_time = None
    Accumulated_T_Trend.Size = T_Change_In_Time_Data.shape
    Accumulated_T_Trend.Variable = "Accumulated T Trend"
    Accumulated_T_Trend.Unit = "Percentage-year-1"
    
    Accumulated_T_Trend.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T_Trend", "All"))    

    # Write in DataCube Season 1
    Accumulated_T_Trend_S1 = DataCube.Rasterdata_Empty()
    Accumulated_T_Trend_S1.Data = T_Change_In_Time_Data_S1 * MASK
    Accumulated_T_Trend_S1.Projection = ET.Projection
    Accumulated_T_Trend_S1.GeoTransform = ET.GeoTransform
    Accumulated_T_Trend_S1.Ordinal_time = None
    Accumulated_T_Trend_S1.Size = T_Change_In_Time_Data_S1.shape
    Accumulated_T_Trend_S1.Variable = "Accumulated T Trend Season 1"
    Accumulated_T_Trend_S1.Unit = "Percentage-year-1"
    
    Accumulated_T_Trend_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T_Trend", "S1"))    

    # Write in DataCube Season 2
    Accumulated_T_Trend_S2 = DataCube.Rasterdata_Empty()
    Accumulated_T_Trend_S2.Data = T_Change_In_Time_Data_S2 * MASK
    Accumulated_T_Trend_S2.Projection = ET.Projection
    Accumulated_T_Trend_S2.GeoTransform = ET.GeoTransform
    Accumulated_T_Trend_S2.Ordinal_time = None
    Accumulated_T_Trend_S2.Size = T_Change_In_Time_Data_S2.shape
    Accumulated_T_Trend_S2.Variable = "Accumulated T Trend Season 2"
    Accumulated_T_Trend_S2.Unit = "Percentage-year-1"
    
    Accumulated_T_Trend_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T_Trend", "S2"))    

    # Write in DataCube Season 3
    Accumulated_T_Trend_S3 = DataCube.Rasterdata_Empty()
    Accumulated_T_Trend_S3.Data = T_Change_In_Time_Data_S3 * MASK
    Accumulated_T_Trend_S3.Projection = ET.Projection
    Accumulated_T_Trend_S3.GeoTransform = ET.GeoTransform
    Accumulated_T_Trend_S3.Ordinal_time = None
    Accumulated_T_Trend_S3.Size = T_Change_In_Time_Data_S3.shape
    Accumulated_T_Trend_S3.Variable = "Accumulated T Trend Season 3"
    Accumulated_T_Trend_S3.Unit = "Percentage-year-1"
    
    Accumulated_T_Trend_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T_Trend", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_T_Trend_Per = DataCube.Rasterdata_Empty()
    Accumulated_T_Trend_Per.Data = T_Change_In_Time_Data_Per * MASK
    Accumulated_T_Trend_Per.Projection = ET.Projection
    Accumulated_T_Trend_Per.GeoTransform = ET.GeoTransform
    Accumulated_T_Trend_Per.Ordinal_time = None
    Accumulated_T_Trend_Per.Size = T_Change_In_Time_Data_Per.shape
    Accumulated_T_Trend_Per.Variable = "Accumulated T Trend Season Perennial"
    Accumulated_T_Trend_Per.Unit = "Percentage-year-1"
    
    Accumulated_T_Trend_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_T_Trend", "Perennial")) 

    ########################## Save Accumulated ET0 trend ##########################

    # Write in DataCube
    Accumulated_ET0_Trend = DataCube.Rasterdata_Empty()
    Accumulated_ET0_Trend.Data = ET0_Change_In_Time_Data * MASK
    Accumulated_ET0_Trend.Projection = ET.Projection
    Accumulated_ET0_Trend.GeoTransform = ET.GeoTransform
    Accumulated_ET0_Trend.Ordinal_time = None
    Accumulated_ET0_Trend.Size = ET0_Change_In_Time_Data.shape
    Accumulated_ET0_Trend.Variable = "Accumulated Trend ET0"
    Accumulated_ET0_Trend.Unit = "Percentage-year-1"
    
    Accumulated_ET0_Trend.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0_Trend", "All"))    

    # Write in DataCube Season 1
    Accumulated_ET0_Trend_S1 = DataCube.Rasterdata_Empty()
    Accumulated_ET0_Trend_S1.Data = ET0_Change_In_Time_Data_S1 * MASK
    Accumulated_ET0_Trend_S1.Projection = ET.Projection
    Accumulated_ET0_Trend_S1.GeoTransform = ET.GeoTransform
    Accumulated_ET0_Trend_S1.Ordinal_time = None
    Accumulated_ET0_Trend_S1.Size = ET0_Change_In_Time_Data_S1.shape
    Accumulated_ET0_Trend_S1.Variable = "Accumulated ET0 Trend Season 1"
    Accumulated_ET0_Trend_S1.Unit = "Percentage-year-1"
    
    Accumulated_ET0_Trend_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0_Trend", "S1"))    

    # Write in DataCube Season 2
    Accumulated_ET0_Trend_S2 = DataCube.Rasterdata_Empty()
    Accumulated_ET0_Trend_S2.Data = ET0_Change_In_Time_Data_S2 * MASK
    Accumulated_ET0_Trend_S2.Projection = ET.Projection
    Accumulated_ET0_Trend_S2.GeoTransform = ET.GeoTransform
    Accumulated_ET0_Trend_S2.Ordinal_time = None
    Accumulated_ET0_Trend_S2.Size = ET0_Change_In_Time_Data_S2.shape
    Accumulated_ET0_Trend_S2.Variable = "Accumulated ET0 Trend Season 2"
    Accumulated_ET0_Trend_S2.Unit = "Percentage-year-1"
    
    Accumulated_ET0_Trend_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0_Trend", "S2"))    

    # Write in DataCube Season 3
    Accumulated_ET0_Trend_S3 = DataCube.Rasterdata_Empty()
    Accumulated_ET0_Trend_S3.Data = ET0_Change_In_Time_Data_S3 * MASK
    Accumulated_ET0_Trend_S3.Projection = ET.Projection
    Accumulated_ET0_Trend_S3.GeoTransform = ET.GeoTransform
    Accumulated_ET0_Trend_S3.Ordinal_time = None
    Accumulated_ET0_Trend_S3.Size = ET0_Change_In_Time_Data_S3.shape
    Accumulated_ET0_Trend_S3.Variable = "Accumulated ET0 Trend Season 3"
    Accumulated_ET0_Trend_S3.Unit = "Percentage-year-1"
    
    Accumulated_ET0_Trend_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0_Trend", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_ET0_Trend_Per = DataCube.Rasterdata_Empty()
    Accumulated_ET0_Trend_Per.Data = ET0_Change_In_Time_Data_Per * MASK
    Accumulated_ET0_Trend_Per.Projection = ET.Projection
    Accumulated_ET0_Trend_Per.GeoTransform = ET.GeoTransform
    Accumulated_ET0_Trend_Per.Ordinal_time = None
    Accumulated_ET0_Trend_Per.Size = ET0_Change_In_Time_Data_Per.shape
    Accumulated_ET0_Trend_Per.Variable = "Accumulated ET0 Trend Season Perennial"
    Accumulated_ET0_Trend_Per.Unit = "Percentage-year-1"
    
    Accumulated_ET0_Trend_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET0_Trend", "Perennial")) 

    ########################## Save Accumulated P trend ##########################

    # Write in DataCube
    Accumulated_P_Trend = DataCube.Rasterdata_Empty()
    Accumulated_P_Trend.Data = P_Change_In_Time_Data * MASK
    Accumulated_P_Trend.Projection = ET.Projection
    Accumulated_P_Trend.GeoTransform = ET.GeoTransform
    Accumulated_P_Trend.Ordinal_time = None
    Accumulated_P_Trend.Size = P_Change_In_Time_Data.shape
    Accumulated_P_Trend.Variable = "Accumulated P Trend"
    Accumulated_P_Trend.Unit = "Percentage-year-1"
    
    Accumulated_P_Trend.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P_Trend", "All"))    

    # Write in DataCube Season 1
    Accumulated_P_Trend_S1 = DataCube.Rasterdata_Empty()
    Accumulated_P_Trend_S1.Data = P_Change_In_Time_Data_S1 * MASK
    Accumulated_P_Trend_S1.Projection = ET.Projection
    Accumulated_P_Trend_S1.GeoTransform = ET.GeoTransform
    Accumulated_P_Trend_S1.Ordinal_time = None
    Accumulated_P_Trend_S1.Size = P_Change_In_Time_Data_S1.shape
    Accumulated_P_Trend_S1.Variable = "Accumulated P Trend Season 1"
    Accumulated_P_Trend_S1.Unit = "Percentage-year-1"
    
    Accumulated_P_Trend_S1.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P_Trend", "S1"))    

    # Write in DataCube Season 2
    Accumulated_P_Trend_S2 = DataCube.Rasterdata_Empty()
    Accumulated_P_Trend_S2.Data = P_Change_In_Time_Data_S2 * MASK
    Accumulated_P_Trend_S2.Projection = ET.Projection
    Accumulated_P_Trend_S2.GeoTransform = ET.GeoTransform
    Accumulated_P_Trend_S2.Ordinal_time = None
    Accumulated_P_Trend_S2.Size = P_Change_In_Time_Data_S2.shape
    Accumulated_P_Trend_S2.Variable = "Accumulated P Trend Season 2"
    Accumulated_P_Trend_S2.Unit = "Percentage-year-1"
    
    Accumulated_P_Trend_S2.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P_Trend", "S2"))    

    # Write in DataCube Season 3
    Accumulated_P_Trend_S3 = DataCube.Rasterdata_Empty()
    Accumulated_P_Trend_S3.Data = P_Change_In_Time_Data_S3 * MASK
    Accumulated_P_Trend_S3.Projection = ET.Projection
    Accumulated_P_Trend_S3.GeoTransform = ET.GeoTransform
    Accumulated_P_Trend_S3.Ordinal_time = None
    Accumulated_P_Trend_S3.Size = P_Change_In_Time_Data_S3.shape
    Accumulated_P_Trend_S3.Variable = "Accumulated P Trend Season 3"
    Accumulated_P_Trend_S3.Unit = "Percentage-year-1"
    
    Accumulated_P_Trend_S3.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P_Trend", "S3"))    

    # Write in DataCube Season Perennial
    Accumulated_P_Trend_Per = DataCube.Rasterdata_Empty()
    Accumulated_P_Trend_Per.Data = P_Change_In_Time_Data_Per * MASK
    Accumulated_P_Trend_Per.Projection = ET.Projection
    Accumulated_P_Trend_Per.GeoTransform = ET.GeoTransform
    Accumulated_P_Trend_Per.Ordinal_time = None
    Accumulated_P_Trend_Per.Size = P_Change_In_Time_Data_Per.shape
    Accumulated_P_Trend_Per.Variable = "Accumulated P Trend Season Perennial"
    Accumulated_P_Trend_Per.Unit = "Percentage-year-1"
    
    Accumulated_P_Trend_Per.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_P_Trend", "Perennial")) 

    return()