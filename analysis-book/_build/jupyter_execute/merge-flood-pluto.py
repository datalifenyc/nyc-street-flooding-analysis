#!/usr/bin/env python
# coding: utf-8

# # Street Flooding & MapPLUTO
# 
# Merge the NYC Street Flooding service requests dataset with MapPluto

# ## Import Libraries

# ### Standard Libraries

# In[ ]:


import os


# ### Custom Libraries

# In[ ]:


from utilities import (
    check_file_exists as cfe
)


# ### External Libraries

# In[ ]:


import geopandas as gpd
import pandas as pd


# ## Define Variables

# ### Output Files

# In[ ]:


nyc_street_flooding_gdf_columns_output = 'data/nyc_street_flooding_gdf_columns.txt'
pluto_gdf_columns_output = 'data/pluto_gdf_columns.txt'

current_script_path = os.path.realpath(os.path.curdir)
# pluto_geojson = 'data/PLUTO/pluto_22v3_1.geojson'
# pluto_geojson_full_path = f'{current_script_path}/{pluto_geojson}'


# ### NYC Street Flooding Complaints

# In[ ]:


nyc_street_flooding_geojson = 'data/street-flooding/street-flood-complaints_rows-all.geojson'


# ### MapPLUTO

# In[ ]:


map_pluto_gdb_folder = 'data/PLUTO/MapPLUTO_22v3_1_water_included.gdb'


# In[ ]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using gdb file type"', "map_pluto_shp_folder  = 'data/PLUTO/MapPLUTO_22v3_1_water_included.shp'\n")


# ## Combine `Street Flooding Complaints` and `MapPLUTO` Datasets

# ### Read `Street Flooding Complaints`

# In[ ]:


street_flooding_gdf = gpd.read_file(
    nyc_street_flooding_geojson, 
    driver='GeoJSON', 
    rows=3
)


# In[ ]:


sfc_size = len(street_flooding_gdf)
print(f'# of Street Flooding Complaints: {sfc_size}')


# #### Save `Street Flooding Complaints` Column Names to `nyc_street_flooding_gdf_columns.txt`
# 
# {cite}`hule2021listtofile`

# In[ ]:


street_flooding_columns = street_flooding_gdf.columns.tolist()


# In[ ]:


with open(f'{current_script_path}/{nyc_street_flooding_gdf_columns_output}', 'w') as write_f:
    for column in street_flooding_columns:
        write_f.write(f'{column}\n')


# #### Check Index

# In[ ]:


street_flooding_gdf.index


# #### Set `unique_key` as Index

# In[ ]:


street_flooding_gdf.set_index('unique_key', inplace = True)


# #### Verify Index Change

# In[ ]:


street_flooding_gdf.index


# ### Read `MapPluto`
# 
# Time to read gdb folder: ~`42m`

# In[ ]:


pluto_gdf = gpd.read_file(
    map_pluto_gdb_folder, 
    file = 'FileGDB', 
    # rows = 15
)


# #### Save `Pluto` Column Names to `pluto_gdf_columns.txt`
# 
# {cite}`hule2021listtofile`

# In[ ]:


pluto_columns = pluto_gdf.columns.tolist()


# In[ ]:


with open(f'{current_script_path}/{pluto_gdf_columns_output}', 'w') as write_f:
    for column in pluto_columns:
        write_f.write(f'{column}\n')


# ### Check EPSG CRS codes before merging, to ensure proper alignment
# 
# EPSG (European Petroleum Survey Group) Geodetic Parameter Dataset is a respository of coordinate reference systems and transformations datasets, managed by the International Association of Oil and Gas Producers (IOGP). It is widely used in Geographic Information Systems (GIS) to define and describe the spatial reference systems of geographic data. {cite}`wiki2019epsgregistry`
# 
# CRS (Coordinate Reference System) is used to define and describe the spatial reference systems of geographic data. The CRS defines the origin, scale, and orientation of the coordinate system, as well as how the coordinates are mapped onto a flat surface such as a map or a computer screen. {cite}`cain2013crs`

# EPSG: 4326

# In[ ]:


street_flooding_gdf.crs


# In[ ]:


pluto_gdf.crs


# ### Convert Pluto to EPSG code: 4326

# In[ ]:


pluto_4326_gdf = pluto_gdf.to_crs(4326)


# #### Verify Conversion

# In[ ]:


pluto_4326_gdf.crs


# ### Join #1: BBL

# #### Check data type of join column

# In[ ]:


street_flooding_gdf['bbl'].dtype


# In[ ]:


pluto_4326_gdf['BBL'].dtype


# #### Convert `Street Flooding` GeoDataFrame's `bbl` column from `object` to `float`.

# In[ ]:


street_flooding_gdf['BBL'] = street_flooding_gdf['bbl'].astype(float)


# #### Left Join on `BBL`

# ##### Create column to store index before merge
# 
# {cite}`son2019keepindex`

# In[ ]:


street_flooding_gdf['unique_key'] = street_flooding_gdf.index


# In[ ]:


street_flooding_pluto_gdf = pd.merge(
    street_flooding_gdf,
    pluto_4326_gdf,
    on = 'BBL',
    how = 'left'
)


# #### Preview Results of `BBL` Join

# ##### Check index

# In[ ]:


street_flooding_pluto_gdf.index


# ##### Set `unique_key` as index

# In[ ]:


street_flooding_pluto_gdf.set_index('unique_key', inplace = True)


# ##### Verify index change

# In[ ]:


street_flooding_gdf.index


# ##### List attributes in a 5 column grid

# In[ ]:


all_columns = street_flooding_pluto_gdf.columns.tolist()


# In[ ]:


chunks = [all_columns[x:x + 5] for x in range(0, len(all_columns), 5)]


# In[ ]:


attribute_grid = pd.DataFrame(chunks)


# In[ ]:


attribute_grid


# In[ ]:


preview_columns = [
    'created_date',
    'borough',
    'Borough',
    'street_name',
    'bbl',
    'ZipCode',
    'geometry_x',
    'geometry_y'
]


# ##### View oldest service requests

# In[ ]:


street_flooding_pluto_gdf[preview_columns].head(10)


# ##### View most recent service requests

# In[ ]:


street_flooding_pluto_gdf[preview_columns].tail(10)


# #### Check % Join by BBL

# In[ ]:


def pct_join(gdf: gpd.GeoDataFrame) -> dict:
    gdf_join_info = dict()
    df_size = len(gdf)
    missing_geometry_y_count = len(gdf[gdf['geometry_y'] == None])

    gdf_join_info['df_size'] = df_size
    gdf_join_info['missing_geometry_y_count'] = missing_geometry_y_count
    gdf_join_info['pct_join'] = (df_size - missing_geometry_y_count) / df_size * 100
    gdf_join_info['pct_missing'] = missing_geometry_y_count / df_size * 100

    return gdf_join_info


# In[ ]:


bbl_join_stats_dict = pct_join(street_flooding_pluto_gdf)
bbl_join_stats_dict


# ### Join #2: Spatial Join
# 
# {cite}`ramsey2018postgisspatial`

# #### Split DataFrame Into BBL Matches and Non-matches

# ##### BBL matches

# In[ ]:


street_flooding_pluto_bbl_match_gdf = \
    street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] != None]


# BBL match GeoDataFrame info

# In[ ]:


street_flooding_pluto_bbl_match_gdf.info()


# Verify match count

# In[ ]:


match_count = bbl_join_stats_dict['df_size'] - \
    bbl_join_stats_dict['missing_geometry_y_count']

match_count == \
    len(street_flooding_pluto_bbl_match_gdf)


# ##### BBL mismatches
# 
# Before rejoining with sjoin, extract the street flooding columns that did not 
# match by BBL. 

# In[ ]:


street_flooding_pluto_bbl_mismatch_gdf = \
    street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] == None]


# In[ ]:


# temp
street_flooding_pluto_bbl_mismatch_gdf.set_geometry(col='geometry_x', inplace=True)


# In[ ]:


# temp
street_flooding_pluto_bbl_mismatch_gdf[['geometry_x', 'borough']].explore('borough')


# In[ ]:


pluto_4326_gdf_copy = pluto_4326_gdf.copy()


# In[ ]:


pluto_4326_gdf_copy.set_geometry(col='geometry', inplace=True)


# In[ ]:


pluto_4326_gdf_copy['Borough'].unique


# In[ ]:


# pluto_4326_gdf_copy[['geometry', 'Borough']].explore('Borough')


# Rename `geometry_x` column back to original name, `geometry`

# In[ ]:


street_flooding_pluto_bbl_mismatch_gdf.rename(columns = {"geometry_x": "geometry"}, inplace = True)


# Copy index as column, `unique_key`

# In[ ]:


street_flooding_pluto_bbl_mismatch_gdf['unique_key'] = street_flooding_pluto_bbl_mismatch_gdf.index


# BBL mismatch GeoDataFrame info

# In[ ]:


street_flooding_pluto_bbl_mismatch_gdf.info()


# Verify mismatch count

# In[ ]:


bbl_join_stats_dict['missing_geometry_y_count'] == \
    len(street_flooding_pluto_bbl_mismatch_gdf)


# Copy only the street flooding columns

# In[ ]:


street_flooding_bbl_no_match_gdf = \
    street_flooding_pluto_bbl_mismatch_gdf[street_flooding_columns].copy()


# #### Perform `sjoin`
# 
# {cite}`ramsey2018postgisspatial,fleischmann2021spatialjoin`

# Set active geometry

# In[ ]:


street_flooding_bbl_no_match_gdf.set_geometry('geometry', inplace = True)


# In[ ]:


# pluto_4326_gdf[['geometry', 'Borough']].explore('Borough')


# In[ ]:


street_flooding_map_pluto_sjoin_gdf = (
    gpd.sjoin(
        street_flooding_bbl_no_match_gdf,
        pluto_4326_gdf,
        how = 'left',
        # predicate = 'intersects'
    )
)


# In[ ]:


preview_columns_sjoin = [
    'borough',
    'Borough',
    'created_date', 
    'street_name', 
    'bbl', 
    'ZipCode', 
    'geometry',
    'TaxMap']


# In[ ]:


street_flooding_map_pluto_sjoin_gdf[preview_columns_sjoin].head(10)


# In[ ]:


street_flooding_map_pluto_sjoin_gdf[preview_columns_sjoin].tail(10)


# In[ ]:


nan_count = street_flooding_map_pluto_sjoin_gdf['Borough'].isna().sum()
nan_count


# #### Perform `sjoin_nearest`
# 
# {cite}`ramsey2018postgisspatial,fleischmann2021spatialjoin`

# In[ ]:





# In[ ]:


"""street_flooding_bbl_no_match_gdf.crs = 'epsg:3035'
street_flooding_bbl_no_match_gdf.to_crs('4326', inplace = True)"""


# In[ ]:


"""pluto_4326_gdf.crs = 'epsg:3035'
pluto_4326_gdf.to_crs('4326', inplace = True)"""


# In[ ]:


"""street_flooding_bbl_no_match_gdf.crs"""


# In[ ]:


"""street_flooding_bbl_no_match_gdf.geometry"""


# In[ ]:


"""pluto_4326_gdf.crs"""


# In[ ]:


"""pluto_4326_gdf.geometry"""


# In[ ]:


"""street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('2957'),
        pluto_4326_gdf.to_crs('2957'),
        # how = 'inner',
        distance_col = 'distances'
    )
)
"""


# Use Projected CRS for `gpd.sjoin_nearest`
# 
# Mercator (EPSG: 3857)
# 
# 1. Google Maps
# 2. Open Street Maps
# 3. Stamen Maps
# 
# {cite}`frazier2020crsinr`

# In[ ]:


"""street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('32610'),
        pluto_4326_gdf.to_crs('32610'),
        # how = 'inner',
        distance_col = 'distances'
    )
)"""


# In[ ]:


# temp
sfbnmg10 = street_flooding_bbl_no_match_gdf.iloc[:10,:].copy()


# In[ ]:


# temp
len(sfbnmg10)


# In[ ]:


# temp
p4g10 = pluto_4326_gdf.iloc[:50,:].copy()


# In[ ]:


# temp
len(p4g10)


# In[ ]:


# temp
len(street_flooding_bbl_no_match_gdf)


# In[ ]:


# temp
len(pluto_4326_gdf)


# In[ ]:


street_flooding_bbl_no_match_gdf['geometry'].crs


# In[ ]:


street_flooding_bbl_no_match_gdf['geometry'].head()


# In[ ]:


pluto_4326_gdf['geometry'].crs


# In[ ]:


pluto_4326_gdf['geometry'].head()


# In[ ]:


# temp
street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('2263'),
        pluto_4326_gdf.to_crs('2263'),
        how = 'left',
        # distance_threshold = 100,
        distance_col = 'distance'
    )
)


# In[ ]:


# temp
street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('32617'),
        pluto_4326_gdf.to_crs('32617'),
        how = 'left',
        distance_threshold = 100,
        distance_col = 'distance'
    )
)


# In[ ]:


street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('3857'),
        pluto_4326_gdf.to_crs('3857'),
        how = 'left',
        distance_threshold = 100,
        distance_col = 'distance'
    )
)


# In[ ]:


# temp


# In[ ]:


street_flooding_map_pluto_sjoin_nearest_gdf.columns


# In[ ]:


len(pluto_4326_gdf)


# In[ ]:


preview_columns_sjoin.append('distance')


# In[ ]:


# temp 2263
street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin].head(10)


# In[ ]:


# temp 32617
street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin].head(10)


# In[ ]:


# 3857
street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin].head(10)


# In[ ]:


street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin].tail(10)


# In[ ]:


nan_count = street_flooding_map_pluto_sjoin_nearest_gdf['Borough'].isna().sum()
nan_count


# In[ ]:


"""street_flooding_map_pluto_df = (
    gpd.sjoin_nearest(
        street_flooding_gdf.to_crs(4326),
        map_pluto_gdf.to_crs(4326),
        distance_col = 'distance_between'
    ).reset_index(drop = True)
)"""


# In[ ]:


# nan_count = street_flood_pluto_gdf['geometry_y'].isna().sum()


# In[ ]:


"""pluto_gdf['geometry']"""


# In[ ]:


"""pluto_4326_gdf['geometry']"""


# In[ ]:


"""street_flooding_bbl_no_match_gdf['geometry']"""


# In[ ]:




