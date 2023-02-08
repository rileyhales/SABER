import geopandas as gpd
import pandas as pd

# read in each region's final geopackage
africa = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/africa/africa_merged.gpkg')
australia = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/australia/australia_merged.gpkg')
central_america = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/central america/central_america_merged.gpkg')
central_asia = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/central asia/central_asia_merged.gpkg')
east_asia = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/east asia/east_asia_merged.gpkg')
europe = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/europe/europe_merged.gpkg')
islands = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/islands/islands_merged.gpkg')
japan = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/japan/japan_merged.gpkg')
middle_east = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/middle east/middle_east_merged.gpkg')
north_america = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/north america/north_america_merged.gpkg')
south_america = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/south america/south_america_merged.gpkg')
south_asia = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/south asia/south_asia_merged.gpkg')
west_asia = gpd.read_file('/Users/jonahdundas/data/SABER/Region Stats/west asia/west_asia_merged.gpkg')

# make a list of each region's variable name
df = [africa, australia, central_america, central_asia, east_asia, europe, islands, japan, middle_east, north_america, south_america, south_asia, west_asia]

# concatenate all the regions into one global dataset
all_regions = pd.concat(df)

# export as both a geopackage and a csv file
all_regions.to_file('/Users/jonahdundas/data/SABER/Region Stats/all_regions.gpkg')
all_regions.drop(columns=['geometry'],inplace=True)
all_regions.to_csv('/Users/jonahdundas/data/SABER/Region Stats/all_regions.csv')
