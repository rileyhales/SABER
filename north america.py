import geopandas as gpd
import pandas as pd
from functools import reduce

clay_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_clay.gpkg',layer='north_america_clay')
coarse_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_coarse.gpkg',layer='north_america_coarse')
landcover = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_landcover.gpkg')
sand_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_sand.gpkg',layer='north_america_sand')
silt_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_silt.gpkg',layer='north_america_silt')
slope_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_slope.gpkg',layer='north_america_slope')

data_frames = [clay_df, coarse_df,landcover, silt_df, slope_df,sand_df]

for df in data_frames:
    print(df.columns)

north_america_merged = reduce(lambda left,right:pd.merge(left,right,on=['OBJECTID','GridID','HydroID','NextDownID','CatType','COMID','Shape_Leng','Shape_Area','Tot_Drain_','geometry'],how='outer'),data_frames)

print(north_america_merged.columns)

hist_list =[]

for column in north_america_merged:
    if column[:5] == 'HISTO':
        hist_list.append(column)

north_america_merged['HIST_TOTAL'] = north_america_merged[hist_list].sum(axis=1)

for column in hist_list:
    north_america_merged[column] = north_america_merged[column] / north_america_merged['HIST_TOTAL']

north_america_merged.drop(columns=['HIST_TOTAL','OBJECTID','GridID','HydroID','NextDownID','Shape_Area','Shape_Leng','CatType'], inplace=True)

north_america_merged.to_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_merged.gpkg')






# for prop in ['clay', 'coarse', 'sand', 'silt', 'slope']:
#     for gpkg in glob.glob(f'/Users/jonahdundas/data/SABER/Region Stats/*/*_{prop}.gpkg'):
#         gdf = gpd.read_file(gpkg)
#         gdf.columns = [f'{prop}{x}' if x.startswith('_') else x for x in gdf.columns]
#         gdf.to_file(gpkg)


# for name in glob.glob('/Users/jonahdundas/data/SABER/Region Stats/*/*.gpkg'):
#     if name[-14:] == 'catchment.gpkg':
#         dest = name.replace('-geoglows-catchment.gpkg','.gpkg')
#         os.rename(name, dest)

