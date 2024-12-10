import json
import pandas as pd
import geopandas as gpd

# Esri endpoint for USA states data
url = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_States_Generalized/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

# Read the data as a GeoDataFrame and lower-case the column headers
src_gdf = gpd.read_file(url).to_crs('EPSG:4326')
src_gdf.columns = src_gdf.columns.str.lower()

# Re-project to a suitable projected CRS (e.g., EPSG:3857 for Web Mercator or another local projection)
projected_gdf = src_gdf.to_crs(epsg=3857)

# Compute centroids in the projected CRS
projected_gdf['centroid'] = projected_gdf.geometry.centroid

# Convert centroids to geographic CRS for latitude/longitude extraction
centroid_gdf = projected_gdf.set_geometry('centroid').to_crs(epsg=4326)

# Extract latitude and longitude
projected_gdf['lat'] = centroid_gdf.geometry.y.round(4)
projected_gdf['lon'] = centroid_gdf.geometry.x.round(4)

# Slim down the GeoDataFrame to just the data we need
keep_cols = ['state_name', 'state_fips', 'sub_region', 'state_abbr',
             'population', 'pop_sqmi', 'sqmi', 'lat', 'lon']

df = projected_gdf[keep_cols].sort_values('state_name').copy()

df.to_json('./data/usa_states_regions.json', indent=4, orient='records')