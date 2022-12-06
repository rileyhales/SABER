import geopandas as gpd
import pandas as pd
from functools import reduce

clay_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_clay.gpkg')
coarse_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_coarse.gpkg',layer='australia_coarse')
landcover = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_landcover.gpkg')
sand_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_sand.gpkg',layer='australia_sand')
silt_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_silt.gpkg',layer='australia_silt')
slope_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_slope.gpkg',layer='australia_slope')

data_frames = [clay_df, coarse_df,landcover, silt_df, slope_df,sand_df]

# for df in data_frames:
#     print(df.columns)

australia_merged = reduce(lambda left,right:pd.merge(left,right,on=['OBJECTID','GridID','CatType','HydroID','NextDownID','Shape_Leng','COMID','Shape_Area','Tot_Drain_','geometry'],how='outer'),data_frames)

# print(australia_merged.columns)

hist_list =[]

for column in australia_merged:
    if column[:5] == 'HISTO':
        hist_list.append(column)

australia_merged['HIST_TOTAL'] = australia_merged[hist_list].sum(axis=1)

for column in hist_list:
    australia_merged[column] = australia_merged[column] / australia_merged['HIST_TOTAL']

australia_merged.drop(columns=['HIST_TOTAL','OBJECTID','GridID','HydroID','NextDownID','Shape_Area','Shape_Leng','CatType'], inplace=True)

australia_merged.to_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_merged.gpkg')






# for prop in ['clay', 'coarse', 'sand', 'silt', 'slope']:
#     for gpkg in glob.glob(f'/Users/jonahdundas/data/SABER/Region Stats/*/*_{prop}.gpkg'):
#         gdf = gpd.read_file(gpkg)
#         gdf.columns = [f'{prop}{x}' if x.startswith('_') else x for x in gdf.columns]
#         gdf.to_file(gpkg)


# for name in glob.glob('/Users/jonahdundas/data/SABER/Region Stats/*/*.gpkg'):
#     if name[-14:] == 'catchment.gpkg':
#         dest = name.replace('-geoglows-catchment.gpkg','.gpkg')
#         os.rename(name, dest)

