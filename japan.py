import geopandas as gpd
import pandas as pd
from functools import reduce

clay_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/Japan/japan_clay.gpkg')
coarse_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/Japan/japan_coarse.gpkg')
landcover = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/Japan/japan_landcover.gpkg')
sand_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/Japan/japan_sand.gpkg')
silt_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/Japan/japan_silt.gpkg')
slope_df = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/Japan/japan_slope.gpkg')

data_frames = [clay_df, coarse_df,landcover, silt_df, slope_df, sand_df]

japan_merged = reduce(lambda left,right:pd.merge(left,right,on=['COMID','Shape_Area','Tot_Drain_','geometry'],how='outer'),data_frames)


hist_list =[]

for column in japan_merged:
    if column[:5] == 'HISTO':
        hist_list.append(column)

japan_merged['HIST_TOTAL'] = japan_merged[hist_list].sum(axis=1)

for column in hist_list:
    japan_merged[column] = japan_merged[column] / japan_merged['HIST_TOTAL']

japan_merged.drop(columns=['HIST_TOTAL','Shape_Area'], inplace=True)

japan_merged.to_file('/Users/jonahdundas/data/SABER/Region Stats/Japan/japan_merged.gpkg')






# for prop in ['clay', 'coarse', 'sand', 'silt', 'slope']:
#     for gpkg in glob.glob(f'/Users/jonahdundas/data/SABER/Region Stats/*/*_{prop}.gpkg'):
#         gdf = gpd.read_file(gpkg)
#         gdf.columns = [f'{prop}{x}' if x.startswith('_') else x for x in gdf.columns]
#         gdf.to_file(gpkg)


# for name in glob.glob('/Users/jonahdundas/data/SABER/Region Stats/*/*.gpkg'):
#     if name[-14:] == 'catchment.gpkg':
#         dest = name.replace('-geoglows-catchment.gpkg','.gpkg')
#         os.rename(name, dest)

