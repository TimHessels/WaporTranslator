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

def main(Start_year_analyses, End_year_analyses, output_folder):

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
    ET = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET), Formats.ET, Dates, Conversion = Conversions.ET, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET', Product = 'WAPOR', Unit = 'mm/day')
    T = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.T), Formats.T, Dates, Conversion = Conversions.T, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'T', Product = 'WAPOR', Unit = 'mm/day')
    ET0 = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.ET0), Formats.ET0, Dates, Conversion = Conversions.ET0, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'ET0', Product = 'WAPOR', Unit = 'mm/day')
    Actual_Biomass_Production = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Actual_Biomass_Production), Formats.Actual_Biomass_Production, Dates, Conversion = Conversions.Actual_Biomass_Production, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Actual Biomass Production', Product = '', Unit = 'kg/ha/d')
    NPPcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_NPP), Formats.Cumulative_NPP, Dates, Conversion = Conversions.Cumulative_NPP, Variable = 'Cumulated NPP', Product = '', Unit = 'mm/decade')      
    Crop_S1_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_Start_S1), Formats.Season_Start_S1, list(Dates_Years), Conversion = Conversions.Season_Start_S1, Variable = 'Season 1 Start', Product = '', Unit = 'DOY')
    Crop_S2_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_Start_S2), Formats.Season_Start_S2, list(Dates_Years), Conversion = Conversions.Season_Start_S2, Variable = 'Season 2 Start', Product = '', Unit = 'DOY')
    Crop_S1_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S1), Formats.Season_End_S1, list(Dates_Years), Conversion = Conversions.Season_End_S1, Variable = 'Season 1 End', Product = '', Unit = 'DOY')
    Crop_S2_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Season_End_S2), Formats.Season_End_S2, list(Dates_Years), Conversion = Conversions.Season_End_S2, Variable = 'Season 2 End', Product = '', Unit = 'DOY')
    Per_Start = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Perenial_Start), Formats.Perenial_Start, list(Dates_Years), Conversion = Conversions.Perenial_Start, Variable = 'Perenial Start', Product = '', Unit = 'DOY')
    Per_End = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Perenial_End), Formats.Perenial_End, list(Dates_Years), Conversion = Conversions.Perenial_End, Variable = 'Perenial End', Product = '', Unit = 'DOY')
    ET0cum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_ET0), Formats.Cumulative_ET0, Dates, Conversion = Conversions.Cumulative_ET0, Variable = 'Cumulated ET0', Product = '', Unit = 'mm/decade')      
    ETcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_ET), Formats.Cumulative_ET, Dates, Conversion = Conversions.Cumulative_ET, Variable = 'Cumulated ET', Product = '', Unit = 'mm/decade')      
    Tcum = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Cumulative_T), Formats.Cumulative_T, Dates, Conversion = Conversions.Cumulative_T, Variable = 'Cumulated T', Product = '', Unit = 'mm/decade')      
    AEZ = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.AEZ), Formats.AEZ, Dates, Conversion = Conversions.AEZ, Variable = 'Surface Runoff Coefficient', Product = '', Unit = '-')  
    CropType = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.CropType), Formats.CropType, list(Dates_Years), Conversion = Conversions.CropType, Variable = 'CropType', Product = '', Unit = '-')
    CropClass = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.CropClass), Formats.CropClass, list(Dates_Years), Conversion = Conversions.CropClass, Variable = 'CropClass', Product = '', Unit = '-')
    Accumulated_Biomass_Production = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Accumulated_Biomass_Production), Formats.Accumulated_Biomass_Production, list(Dates_Years), Conversion = Conversions.Accumulated_Biomass_Production, Variable = 'Accumulated Biomass Production', Product = '', Unit = 'ton/ha/season')
    Target_Biomass_Production = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Target_Biomass_Production), Formats.Target_Biomass_Production, Dates, Conversion = Conversions.Target_Biomass_Production, Example_Data = example_file, Mask_Data = example_file, gap_filling = 1, reprojection_type = 2, Variable = 'Target Biomass Production', Product = '', Unit = 'kg/ha/d')
    Yield = DataCube.Rasterdata_tiffs(os.path.join(output_folder, Paths.Yield), Formats.Yield, list(Dates_Years), Conversion = Conversions.Yield, Variable = 'Yield', Product = '', Unit = 'ton/ha')
    
    ######################## Calculate days in each dekads #################################
    Days_in_Dekads = np.append(ET.Ordinal_time[1:] - ET.Ordinal_time[:-1], 11)

    ################################# Calculate Crop Season and LU #################################
    Season_Type = L3_Food.Calc_Crops(CropType, CropClass, MASK)

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

    ######################### Calculate AquaCrop Water Use Efficiency ########################

    # Calculate cummulative ET and ET0 over the seasons
    DOYcum = np.ones(Tcum.Size) * Days_in_Dekads[:, None, None]
    DOYcum = DOYcum.cumsum(axis = 0)    
    
    # For perenial crop clip the season at start and end year
    Accumulated_T_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_T_Data_End = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_End = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_End = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_Start = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_End = np.ones(Per_Start.Size) * np.nan
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

        for dekad in range(0,37):
            Accumulated_T_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = NPPcum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
            Accumulated_ET0_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad]= ET0cum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
            Accumulated_DOY_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = DOYcum[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
            Accumulated_ET_Data_End[year_diff, Per_End.Data[year_diff, :, :] == dekad] = ETcum.Data[int(year_diff * 36 + dekad-1), Per_End.Data[year_diff, :, :] == dekad] 
    
    Accumulated_T_Data_Per =  Accumulated_T_Data_End - Accumulated_T_Data_Start
    Accumulated_ET0_Data_Per =  Accumulated_ET0_Data_End - Accumulated_ET0_Data_Start
    Accumulated_DOY_Data_Per =  Accumulated_DOY_Data_End - Accumulated_DOY_Data_Start
    Accumulated_ET_Data_Per =  Accumulated_ET_Data_End - Accumulated_ET_Data_Start
    
    # For other crops (double and single) take the start and end of the seasons
    Accumulated_T_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_T_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_End_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_DOY_Data_End_S2 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_Start_S1 = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET_Data_Start_S2 = np.ones(Per_Start.Size) * np.nan
    
    if not np.isnan(np.nanmean(Crop_S1_End.Data)):
        for Date_Year in Dates_Years:
            year_diff = int(Date_Year.year - Dates_Years[0].year)
            for dekad in range(0,int(np.nanmax(Crop_S2_End.Data))):
                Accumulated_T_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = Tcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_T_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = Tcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_ET0_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = ET0cum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_ET0_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = ET0cum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_End_S1[year_diff, Crop_S1_Start.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad)), Crop_S1_Start.Data[year_diff, :, :] == dekad] 
                Accumulated_DOY_Data_End_S2[year_diff, Crop_S2_Start.Data[year_diff, :, :] == dekad] = DOYcum[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_Start.Data[year_diff, :, :] == dekad] 
                Accumulated_ET_Data_Start_S1[year_diff, Crop_S1_End.Data[year_diff, :, :] == dekad] = ETcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad)), Crop_S1_End.Data[year_diff, :, :] == dekad] 
                Accumulated_ET_Data_Start_S2[year_diff, Crop_S2_End.Data[year_diff, :, :] == dekad] = ETcum.Data[np.minimum(NPPcum.Size[0]-1, int(year_diff * 36 + dekad-1)), Crop_S2_End.Data[year_diff, :, :] == dekad] 
    
    Accumulated_T_Data_Start_S1[np.isnan(Accumulated_T_Data_Start_S1)] = 0
    Accumulated_T_Data_Start_S2[np.isnan(Accumulated_T_Data_Start_S2)] = 0 
    Accumulated_ET0_Data_Start_S1[np.isnan(Accumulated_ET0_Data_Start_S1)] = 0
    Accumulated_ET0_Data_Start_S2[np.isnan(Accumulated_ET0_Data_Start_S2)] = 0 
    Accumulated_DOY_Data_Start_S1[np.isnan(Accumulated_DOY_Data_Start_S1)] = 0
    Accumulated_DOY_Data_Start_S2[np.isnan(Accumulated_DOY_Data_Start_S2)] = 0 
    Accumulated_DOY_Data_End_S1[np.isnan(Accumulated_DOY_Data_End_S1)] = 0
    Accumulated_DOY_Data_End_S2[np.isnan(Accumulated_DOY_Data_End_S2)] = 0 
    Accumulated_ET_Data_Start_S1[np.isnan(Accumulated_ET_Data_Start_S1)] = 0
    Accumulated_ET_Data_Start_S2[np.isnan(Accumulated_ET_Data_Start_S2)] = 0 
     
    # Calculate pasture as DOY 1 till 365
    Accumulated_T_Data_Past = np.ones(Per_Start.Size) * np.nan
    Accumulated_ET0_Data_Past = np.ones(Per_Start.Size) * np.nan    
    Accumulated_DOY_Data_Past = np.ones(Per_Start.Size) * np.nan   
    Accumulated_ET_Data_Past = np.ones(Per_Start.Size) * np.nan   
    for Date_Year in Dates_Years:
        year_diff = int(Date_Year.year - Dates_Years[0].year)
        dekad = 35 # Always take end in pasture
        Accumulated_T_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 4] = Tcum.Data[int(year_diff * 36 + dekad), Season_Type.Data[year_diff, :, :] == 4] 
        Accumulated_ET0_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 4] = ET0cum.Data[int(year_diff * 36 + dekad), Season_Type.Data[year_diff, :, :] == 4] 
        Accumulated_DOY_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 4] = 365
        Accumulated_ET_Data_Past[year_diff, Season_Type.Data[year_diff, :, :] == 4] = ETcum.Data[int(year_diff * 36 + dekad), Season_Type.Data[year_diff, :, :] == 4] 
        
    Accumulated_T_Data_Past[np.isnan(Accumulated_T_Data_Past)] = 0
    Accumulated_T_Data_Per[np.isnan(Accumulated_T_Data_Per)] = 0
    Accumulated_ET0_Data_Past[np.isnan(Accumulated_ET0_Data_Past)] = 0
    Accumulated_ET0_Data_Per[np.isnan(Accumulated_ET0_Data_Per)] = 0
    Accumulated_DOY_Data_Past[np.isnan(Accumulated_DOY_Data_Past)] = 0
    Accumulated_DOY_Data_Per[np.isnan(Accumulated_DOY_Data_Per)] = 0
    Accumulated_ET_Data_Past[np.isnan(Accumulated_ET_Data_Past)] = 0
    Accumulated_ET_Data_Per[np.isnan(Accumulated_ET_Data_Per)] = 0   
    
    # Add all seasons to one map
    Accumulated_T_Data = Accumulated_T_Data_Start_S1 + Accumulated_T_Data_Start_S2 + Accumulated_T_Data_Per + Accumulated_T_Data_Past
    Accumulated_T_Data[Accumulated_T_Data==0] = np.nan
    Accumulated_ET0_Data = Accumulated_ET0_Data_Start_S1 + Accumulated_ET0_Data_Start_S2 + Accumulated_ET0_Data_Per + Accumulated_ET0_Data_Past
    Accumulated_ET0_Data[Accumulated_ET0_Data==0] = np.nan
    Accumulated_DOY_Data = Accumulated_DOY_Data_Start_S1 - Accumulated_DOY_Data_End_S1 + Accumulated_DOY_Data_Start_S2 - Accumulated_DOY_Data_End_S2 + Accumulated_DOY_Data_Per + Accumulated_DOY_Data_Past
    Accumulated_DOY_Data[Accumulated_DOY_Data==0] = np.nan    
    Accumulated_ET_Data = Accumulated_ET_Data_Start_S1 + Accumulated_ET_Data_Start_S2 + Accumulated_ET_Data_Per + Accumulated_ET_Data_Past
    Accumulated_ET_Data[Accumulated_ET_Data==0] = np.nan    
    
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
    
    AquaCrop_Water_Use_Efficiency.Save_As_Tiff(os.path.join(output_folder_L3, "AquaCrop_Water_Use_Efficiency"))    

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
    
    GBWP_Season.Save_As_Tiff(os.path.join(output_folder_L3, "GBWP_Season"))           

    ################################# Calculate Mean Yield Fresh Grass over every AEZ per year #################################
    L3_AEZ_ET = dict()
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
    
    Water_Productivity.Save_As_Tiff(os.path.join(output_folder_L3, "Water_Productivity"))       
    
    '''
    # Write in DataCube
    Accumulated_ET = DataCube.Rasterdata_Empty()
    Accumulated_ET.Data = Accumulated_ET_Data * MASK
    Accumulated_ET.Projection = ET.Projection
    Accumulated_ET.GeoTransform = ET.GeoTransform
    Accumulated_ET.Ordinal_time = np.array(list(map(lambda i : i.toordinal(), Dates_Years)))
    Accumulated_ET.Size = Accumulated_ET_Data.shape
    Accumulated_ET.Variable = "Accumulated ET"
    Accumulated_ET.Unit = "mm"
    
    Accumulated_ET.Save_As_Tiff(os.path.join(output_folder_L3, "Accumulated_ET"))    
    '''    
    
    return()