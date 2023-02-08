import geopandas as gpd
import pandas as pd
from functools import reduce

# read in all the geopackaages as pandas dataframes
clay_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_clay.gpkg',layer='africa_clay')
coarse_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_coarse.gpkg',layer='africa_coarse')
landcover = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_landcover.gpkg')
sand_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_sand.gpkg',layer='africa_sand')
silt_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_silt.gpkg',layer='africa_silt')
slope_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_slope.gpkg',layer='africa_slope')

# make a list of all the dataframe variable names
data_frames = [clay_df, coarse_df,landcover, silt_df, slope_df,sand_df]

# merge all the dataframes into one large dataframe containing all of the region's information
africa_merged = reduce(lambda left,right:pd.merge(left,right,on=['OBJECTID','GridID','HydroID','NextDownID','Shape_Leng','DrainLnID','Shape_Area','Tot_Drain_','geometry'],how='outer'),data_frames)

# make a list of all of the types of landcover found in the region (each landcover column name begins with "histo")
hist_list =[]
for column in africa_merged:
    if column[:5] == 'HISTO':
        hist_list.append(column)

# make a new column in the dataframe that finds the total pixel count for each catchment
africa_merged['HIST_TOTAL'] = africa_merged[hist_list].sum(axis=1)

# replace the pixel count values with the area percentage for each type of landcover
for column in hist_list:
    africa_merged[column] = africa_merged[column] / africa_merged['HIST_TOTAL']

# delete any columns that aren't important
africa_merged.drop(columns=['HIST_TOTAL','OBJECTID','GridID','HydroID','NextDownID','Shape_Area','Shape_Leng'], inplace=True)

# save the merged file as a new geopackage
africa_merged.to_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_merged.gpkg')






# for prop in ['clay', 'coarse', 'sand', 'silt', 'slope']:
#     for gpkg in glob.glob(f'/Users/jonahdundas/data/SABER/Region Stats/*/*_{prop}.gpkg'):
#         gdf = gpd.read_file(gpkg)
#         gdf.columns = [f'{prop}{x}' if x.startswith('_') else x for x in gdf.columns]
#         gdf.to_file(gpkg)


# for name in glob.glob('/Users/jonahdundas/data/SABER/Region Stats/*/*.gpkg'):
#     if name[-14:] == 'catchment.gpkg':
#         dest = name.replace('-geoglows-catchment.gpkg','.gpkg')
#         os.rename(name, dest)

