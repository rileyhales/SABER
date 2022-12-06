import geopandas as gpd
import pandas as pd
from functools import reduce

clay_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_clay.gpkg',layer='middle_east_clay')
coarse_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_coarse.gpkg',layer='middle_east_coarse')
landcover = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_landcover.gpkg')
sand_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_sand.gpkg',layer='middle_east_sand')
silt_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_silt.gpkg',layer='middle_east_silt')
slope_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_slope.gpkg',layer='middle_east_slope')

data_frames = [clay_df, coarse_df,landcover, silt_df, slope_df,sand_df]

for df in data_frames:
    print(df.columns)

middle_east_merged = reduce(lambda left,right:pd.merge(left,right,on=['OBJECTID','GridID','HydroID','NextDownID','CatType','COMID','Shape_Leng','Shape_Area','Tot_Drain_','geometry'],how='outer'),data_frames)

print(middle_east_merged.columns)

hist_list =[]

for column in middle_east_merged:
    if column[:5] == 'HISTO':
        hist_list.append(column)

middle_east_merged['HIST_TOTAL'] = middle_east_merged[hist_list].sum(axis=1)

for column in hist_list:
    middle_east_merged[column] = middle_east_merged[column] / middle_east_merged['HIST_TOTAL']

middle_east_merged.drop(columns=['HIST_TOTAL','OBJECTID','GridID','HydroID','NextDownID','Shape_Area','Shape_Leng','CatType'], inplace=True)

middle_east_merged.to_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_merged.gpkg')






# for prop in ['clay', 'coarse', 'sand', 'silt', 'slope']:
#     for gpkg in glob.glob(f'/Users/jonahdundas/data/SABER/Region Stats/*/*_{prop}.gpkg'):
#         gdf = gpd.read_file(gpkg)
#         gdf.columns = [f'{prop}{x}' if x.startswith('_') else x for x in gdf.columns]
#         gdf.to_file(gpkg)


# for name in glob.glob('/Users/jonahdundas/data/SABER/Region Stats/*/*.gpkg'):
#     if name[-14:] == 'catchment.gpkg':
#         dest = name.replace('-geoglows-catchment.gpkg','.gpkg')
#         os.rename(name, dest)

