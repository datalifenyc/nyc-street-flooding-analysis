#!/usr/bin/env python
# coding: utf-8

# # Street Flooding & MapPLUTO
# 
# Merge the NYC Street Flooding service requests dataset with MapPluto

# ## Import Libraries

# ### Standard Libraries

# In[1]:


import os
import json


# ### Custom Libraries

# In[2]:


from utilities import (
    check_file_exists as cfe
)


# ### External Libraries

# In[3]:


import geopandas as gpd
import pandas as pd
import fiona


# ## Define Variables

# ### Input Files

# In[4]:


data_stats_json_input = 'data/data-stats.json'


# ### Output Files

# In[5]:


nyc_street_flooding_gdf_columns_output = 'data/nyc_street_flooding_gdf_columns.txt'
pluto_gdf_columns_output = 'data/pluto_gdf_columns.txt'

current_script_path = os.path.realpath(os.path.curdir)

merge_flood_mappluto_output_ofgdb =  'data/merge/nyc-street-flooding-mappluto.gdb'
merge_flood_mappluto_output_geojson =  'data/merge/nyc-street-flooding-mappluto.geojson'
# pluto_geojson = 'data/PLUTO/pluto_22v3_1.geojson'
# pluto_geojson_full_path = f'{current_script_path}/{pluto_geojson}'


# ### NYC Street Flooding Complaints

# In[6]:


nyc_street_flooding_geojson = 'data/street-flooding/street-flood-complaints_rows-all.geojson'


# ### MapPLUTO

# In[7]:


map_pluto_gdb_folder = 'data/PLUTO/MapPLUTO_22v3_1_water_included.gdb'


# In[8]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using gdb file type"', "map_pluto_shp_folder  = 'data/PLUTO/MapPLUTO_22v3_1_water_included.shp'\n")


# ## Combine `Street Flooding Complaints` and `MapPLUTO` Datasets

# ### Read `Street Flooding Complaints`

# In[9]:


street_flooding_gdf = gpd.read_file(
    nyc_street_flooding_geojson, 
    driver = 'GeoJSON', 
    rows = 500
)


# In[10]:


sfc_size = len(street_flooding_gdf)
print(f'# of Street Flooding Complaints: {sfc_size}')


# #### Save `Street Flooding Complaints` Column Names to `nyc_street_flooding_gdf_columns.txt`
# 
# {cite}`hule2021listtofile`

# In[11]:


street_flooding_columns = street_flooding_gdf.columns.tolist()


# In[12]:


with open(f'{current_script_path}/{nyc_street_flooding_gdf_columns_output}', 'w') as write_f:
    for column in street_flooding_columns:
        write_f.write(f'{column}\n')


# #### Check Index

# In[13]:


street_flooding_gdf.index


# #### Set `unique_key` as Index

# In[14]:


street_flooding_gdf.set_index('unique_key', inplace = True)


# #### Verify Index Change

# In[15]:


street_flooding_gdf.index


# ### Read `MapPluto`
# 
# Time to read gdb folder: ~`37m`

# In[16]:


pluto_gdf = gpd.read_file(
    map_pluto_gdb_folder, 
    file = 'FileGDB', 
    # rows = 15
)


# #### Save `Pluto` Column Names to `pluto_gdf_columns.txt`
# 
# {cite}`hule2021listtofile`

# In[17]:


pluto_columns = pluto_gdf.columns.tolist()


# In[18]:


with open(f'{current_script_path}/{pluto_gdf_columns_output}', 'w') as write_f:
    for column in pluto_columns:
        write_f.write(f'{column}\n')


# ### Check EPSG CRS codes before merging, to ensure proper alignment
# 
# EPSG (European Petroleum Survey Group) Geodetic Parameter Dataset is a respository of coordinate reference systems and transformations datasets, managed by the International Association of Oil and Gas Producers (IOGP). It is widely used in Geographic Information Systems (GIS) to define and describe the spatial reference systems of geographic data. {cite}`wiki2019epsgregistry`
# 
# CRS (Coordinate Reference System) is used to define and describe the spatial reference systems of geographic data. The CRS defines the origin, scale, and orientation of the coordinate system, as well as how the coordinates are mapped onto a flat surface such as a map or a computer screen. {cite}`cain2013crs`

# EPSG: 4326

# In[19]:


street_flooding_gdf.crs


# In[20]:


pluto_gdf.crs


# ### Convert Pluto to EPSG code: 4326

# In[21]:


pluto_4326_gdf = pluto_gdf.to_crs(4326)


# #### Verify Conversion

# In[22]:


pluto_4326_gdf.crs


# ### Join #1: BBL

# #### Check data type of join column

# In[23]:


street_flooding_gdf['bbl'].dtype


# In[24]:


pluto_4326_gdf['BBL'].dtype


# #### Convert `Street Flooding` GeoDataFrame's `bbl` column from `object` to `float`.

# In[25]:


street_flooding_gdf['BBL'] = street_flooding_gdf['bbl'].astype(float)


# #### Left Join on `BBL`

# ##### Create column to store index before merge
# 
# {cite}`son2019keepindex`

# In[26]:


street_flooding_gdf['unique_key'] = street_flooding_gdf.index


# In[27]:


street_flooding_pluto_gdf = pd.merge(
    street_flooding_gdf,
    pluto_4326_gdf,
    on = 'BBL',
    how = 'left'
)


# #### Preview Results of `BBL` Join

# ##### Check index

# In[28]:


street_flooding_pluto_gdf.index


# ##### Set `unique_key` as index

# In[29]:


street_flooding_pluto_gdf.set_index('unique_key', inplace = True)


# ##### Verify index change

# In[30]:


street_flooding_gdf.index


# ##### List attributes in a 5 column grid

# In[31]:


all_columns = street_flooding_pluto_gdf.columns.tolist()


# In[32]:


chunks = [all_columns[x:x + 5] for x in range(0, len(all_columns), 5)]


# In[33]:


attribute_grid = pd.DataFrame(chunks)


# In[34]:


attribute_grid


# In[35]:


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

# In[36]:


street_flooding_pluto_gdf[preview_columns].head(10)


# ##### View most recent service requests

# In[37]:


street_flooding_pluto_gdf[preview_columns].tail(10)


# #### Check % Join by BBL

# In[38]:


def pct_join(gdf: gpd.GeoDataFrame, column_check: str) -> dict:
    gdf_join_info = dict()
    df_size = len(gdf)
    # None does not return the NaN count
    # missing_column_check_count = len(gdf[gdf[column_check] == None])
    missing_column_check_count = gdf[column_check].isna().sum()

    gdf_join_info['df_size'] = df_size
    gdf_join_info['match_count'] = df_size - missing_column_check_count
    gdf_join_info[f'missing_{(column_check)}_count'] = missing_column_check_count
    gdf_join_info['pct_join'] = round((df_size - missing_column_check_count) / df_size * 100, 2)
    gdf_join_info['pct_missing'] = round(missing_column_check_count / df_size * 100, 2)

    return gdf_join_info


# In[39]:


bbl_join_stats_dict = pct_join(street_flooding_pluto_gdf, 'geometry_y')
bbl_join_stats_dict


# ### Join #2: Spatial Join
# 
# {cite}`ramsey2018postgisspatial`

# #### Split DataFrame Into BBL Matches and Non-matches

# ##### BBL matches

# In[40]:


street_flooding_pluto_bbl_match_gdf = \
    street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] != None]


# BBL match GeoDataFrame info

# In[41]:


street_flooding_pluto_bbl_match_gdf.info()


# Verify match count

# In[42]:


match_count = bbl_join_stats_dict['df_size'] - \
    bbl_join_stats_dict['missing_geometry_y_count']

match_count == \
    len(street_flooding_pluto_bbl_match_gdf)


# #### Add BBL match count to JSON file

# In[43]:


with open(data_stats_json_input, 'r') as read_json:
    data_stats = json.load(read_json)


# In[44]:


print(data_stats)


# In[45]:


data_stats['street_flood_mappluto_bbl'] = len(street_flooding_pluto_bbl_match_gdf)


# In[46]:


print(data_stats)


# ##### BBL mismatches
# 
# Before rejoining with sjoin, extract the street flooding rows that did not 
# match by BBL. 

# In[47]:


street_flooding_pluto_bbl_mismatch_gdf = \
    street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] == None]


# Rename `geometry_x` column back to original name, `geometry`

# In[56]:


street_flooding_pluto_bbl_mismatch_gdf_prejoin = \
    street_flooding_pluto_bbl_mismatch_gdf.copy()


# In[57]:


street_flooding_pluto_bbl_mismatch_gdf_prejoin.rename(columns = {'geometry_x': 'geometry'}, inplace = True)


# Copy index as column, `unique_key`

# In[58]:


street_flooding_pluto_bbl_mismatch_gdf_prejoin['unique_key'] = street_flooding_pluto_bbl_mismatch_gdf_prejoin.index


# BBL mismatch GeoDataFrame info

# In[59]:


street_flooding_pluto_bbl_mismatch_gdf_prejoin.info()


# Verify mismatch count

# In[60]:


bbl_join_stats_dict['missing_geometry_y_count'] == \
    len(street_flooding_pluto_bbl_mismatch_gdf_prejoin)


# Copy only the street flooding columns

# In[61]:


street_flooding_bbl_no_match_gdf = \
    street_flooding_pluto_bbl_mismatch_gdf_prejoin[street_flooding_columns].copy()


# #### Perform `sjoin`
# 
# __Note:__ `sjoin` is skipped because the remaining street flooding complaint locations did no match the MapPluto dataset. `sjoin_nearest` will be used instead. _[consider revisiting]_
# 
# {cite}`ramsey2018postgisspatial,fleischmann2021spatialjoin`

# Set active geometry

# In[62]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using `sjoin_nearest`"', "street_flooding_bbl_no_match_gdf.set_geometry('geometry', inplace = True)\n")


# In[64]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using `sjoin_nearest`"', "street_flooding_map_pluto_sjoin_gdf = (\n    gpd.sjoin(\n        street_flooding_bbl_no_match_gdf,\n        pluto_4326_gdf,\n        # pluto_4326_gdf_copy_si_only,\n        how = 'left',\n        # predicate = 'intersects'\n    )\n)\n")


# In[65]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using `sjoin_nearest`"', "preview_columns_sjoin = [\n    'borough',\n    'Borough',\n    'created_date', \n    'street_name', \n    'bbl', \n    'ZipCode', \n    'geometry',\n    'TaxMap'\n]\n")


# In[66]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using `sjoin_nearest`"', 'street_flooding_map_pluto_sjoin_gdf[preview_columns_sjoin].head(10)\n')


# In[67]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using `sjoin_nearest`"', 'street_flooding_map_pluto_sjoin_gdf[preview_columns_sjoin].tail(10)\n')


# In[68]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using `sjoin_nearest`"', "nan_count = street_flooding_map_pluto_sjoin_gdf['Borough'].isna().sum()\nnan_count\n")


# #### Perform `sjoin_nearest`
# 
# {cite}`ramsey2018postgisspatial,fleischmann2021spatialjoin`
# 
# Use Projected CRS for `gpd.sjoin_nearest`
# 
# New York, Long Island (EPSG: 2263)
# 
# Mercator (EPSG: 3857)
# 
# 1. Google Maps
# 2. Open Street Maps
# 3. Stamen Maps
# 
# {cite}`frazier2020crsinr`

# Set active geometry

# In[69]:


street_flooding_bbl_no_match_gdf.set_geometry('geometry', inplace = True)


# Implement [`geopandas.sjoin_nearest`](https://geopandas.org/en/stable/docs/reference/api/geopandas.sjoin_nearest.html)

# In[70]:


street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        # Convert CRS to EPSG: 2263
        street_flooding_bbl_no_match_gdf.to_crs('2263'),
        pluto_4326_gdf.to_crs('2263'),
        how = 'left',
        # max_distance = 100,
        distance_col = 'distance'
    )
)


# ##### Preview `sjoin_nearest` results

# Check index

# In[71]:


street_flooding_map_pluto_sjoin_nearest_gdf.index


# Select columns to preview

# In[72]:


preview_columns_sjoin_nearest_list = [
    'borough',
    'Borough',
    'created_date', 
    'street_name', 
    'bbl', 
    'ZipCode', 
    'geometry',
    'TaxMap'
]


# In[73]:


street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin_nearest_list].head()


# In[74]:


street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin_nearest_list].tail()


# Check number of street flooding complaint locations that did not match after 
# the `sjoin_nearest` implementation

# In[75]:


nan_count = street_flooding_map_pluto_sjoin_nearest_gdf['Borough'].isna().sum()
nan_count


# In[76]:


sjoin_nearest_stats_dict = \
    pct_join(street_flooding_map_pluto_sjoin_nearest_gdf, 'Borough')
sjoin_nearest_stats_dict


# ### Merge `BBL` and `sjoin_nearest` GeoPandas DataFrames

# #### Confirm Both DataFrame Columns Match

# ##### Street Flooding MapPluto `BBL` column count

# In[77]:


street_flooding_pluto_bbl_columns_list = street_flooding_pluto_bbl_match_gdf.columns.tolist()


# In[78]:


street_flooding_pluto_bbl_columns_count = len(street_flooding_pluto_bbl_columns_list)


# In[79]:


print(f'Street Flooding MapPluto BBL column count: {street_flooding_pluto_bbl_columns_count}')


# ##### Street Flooding MapPluto `sjoin_nearest` column count

# In[80]:


street_flooding_map_pluto_sjoin_nearest_columns_list = street_flooding_map_pluto_sjoin_nearest_gdf.columns.tolist()


# In[81]:


street_flooding_map_pluto_sjoin_nearest_columns_count = len(street_flooding_map_pluto_sjoin_nearest_columns_list)


# In[82]:


print(f'Street Flooding MapPluto sjoin_nearest column count: {street_flooding_map_pluto_sjoin_nearest_columns_count}')


# ##### Compare columns

# In[83]:


bbl_only = set(street_flooding_pluto_bbl_columns_list) - set(street_flooding_map_pluto_sjoin_nearest_columns_list)
bbl_only


# In[84]:


sjoin_nearest_only = set(street_flooding_map_pluto_sjoin_nearest_columns_list) - set(street_flooding_pluto_bbl_columns_list)
sjoin_nearest_only


# ##### Verify index is the unique_key

# In[85]:


street_flooding_pluto_bbl_match_gdf.index


# In[86]:


street_flooding_map_pluto_sjoin_nearest_gdf.index


# ##### DataFrame column transform

# BBL match DataFrame

# In[87]:


street_flooding_pluto_bbl_match_gdf_pretransform = \
    street_flooding_pluto_bbl_match_gdf.copy()


# In[88]:


street_flooding_pluto_bbl_match_gdf_pretransform.rename(columns = {'geometry_x': 'geometry'}, inplace = True)


# In[89]:


street_flooding_pluto_bbl_match_gdf_pretransform.drop(columns = ['geometry_y'], inplace = True)


# In[90]:


street_flooding_pluto_bbl_match_gdf_pretransform['unique_key'] = street_flooding_pluto_bbl_match_gdf_pretransform.index


# `sjoin_nearest` match DataFrame

# In[91]:


street_flooding_map_pluto_sjoin_nearest_gdf_pretransform = \
    street_flooding_map_pluto_sjoin_nearest_gdf.copy()


# In[92]:


street_flooding_map_pluto_sjoin_nearest_gdf_pretransform.drop(columns = ['distance', 'index_right'], inplace = True)


# ##### Re-compare columns

# In[93]:


street_flooding_pluto_bbl_match_gdf_pretransform_columns_list = street_flooding_pluto_bbl_match_gdf_pretransform.columns.tolist()


# In[94]:


street_flooding_map_pluto_sjoin_nearest_gdf_pretransform_columns_list = street_flooding_map_pluto_sjoin_nearest_gdf_pretransform.columns.tolist()


# BBL match only

# In[95]:


bbl_recheck_only = set(street_flooding_pluto_bbl_match_gdf_pretransform_columns_list) - set(street_flooding_map_pluto_sjoin_nearest_gdf_pretransform_columns_list)
bbl_recheck_only


# `sjoin_nearest` match only

# In[96]:


sjoin_nearest_only = set(street_flooding_map_pluto_sjoin_nearest_gdf_pretransform_columns_list) - set(street_flooding_pluto_bbl_match_gdf_pretransform_columns_list)
sjoin_nearest_only


# #### Implement [Merge](https://geopandas.org/en/stable/docs/user_guide/mergingdata.html)

# ##### Set active geometry

# In[97]:


street_flooding_pluto_bbl_match_gdf_pretransform.set_geometry(col = 'geometry', inplace = True)
street_flooding_map_pluto_sjoin_nearest_gdf_pretransform.set_geometry(col = 'geometry', inplace = True)


# In[98]:


street_flooding_mappluto_gdf_merge_gdf = pd.concat([street_flooding_pluto_bbl_match_gdf_pretransform.to_crs('2263'), street_flooding_map_pluto_sjoin_nearest_gdf_pretransform.to_crs('2263')])


# ##### Preview Results

# In[99]:


street_flooding_mappluto_gdf_merge_gdf.info()


# In[100]:


preview_columns_merge_list = [
    'borough',
    'Borough',
    'created_date', 
    'street_name', 
    'bbl', 
    'ZipCode', 
    'geometry',
    'Tract2010',
    'TaxMap'
]


# In[101]:


street_flooding_mappluto_gdf_merge_gdf[preview_columns_merge_list].head()


# In[102]:


street_flooding_mappluto_gdf_merge_gdf[preview_columns_merge_list].tail()


# ##### Check total missing joins

# In[103]:


nan_count = street_flooding_mappluto_gdf_merge_gdf['Borough'].isna().sum()
nan_count


# In[104]:


street_flooding_mappluto_gdf_merge_stats_dict = \
    pct_join(street_flooding_mappluto_gdf_merge_gdf, 'Borough')
street_flooding_mappluto_gdf_merge_stats_dict


# __Note__ Revisit None vs NaN count.
# 
# Reference: 
# 
# [pandas GroupBy columns with NaN (missing) values](https://stackoverflow.com/questions/18429491/pandas-groupby-columns-with-nan-missing-values)

# In[105]:


street_flooding_mappluto_gdf_merge_gdf.groupby(['Borough'], dropna = False)['Borough'].count()


# In[106]:


len(street_flooding_mappluto_gdf_merge_gdf)


# #### Save Final Merge Match Count to JSON file

# In[107]:


data_stats['street_flood_mappluto_sjoin_nearest'] = \
    street_flooding_mappluto_gdf_merge_stats_dict['match_count']


# In[108]:


print(data_stats)


# In[109]:


data_stats_json = {}
for key, value in data_stats.items():
    data_stats_json[key] = int(value)


# In[110]:


with open(data_stats_json_input, 'w') as write_json:
    json.dump(data_stats_json, write_json, indent = 4)


# ### Save Merged Dataset 
# 
# Reference:
# 
# [`geopandas.GeoDataFrame.to_file`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html)

# #### Check supported driver options

# In[111]:


fiona.supported_drivers


# #### Confirm output folder exists

# In[112]:


if not os.path.exists('data/merge'):
    print('Creating new folder for merged streeet flooding and MapPluto dataset: "data/merge"')
    os.makedirs('data/merge')
else:
    print('"data/merge" folder already exists')


# #### Reindex Merged GeoPandas DataFrame

# In[113]:


street_flooding_mappluto_gdf_to_save = street_flooding_mappluto_gdf_merge_gdf.copy()


# In[114]:


street_flooding_mappluto_gdf_to_save.index.rename('orig_unique_key', inplace = True)


# #### Save as `.gdb` using `OpenFileGDB` driver

# In[115]:


street_flooding_mappluto_gdf_to_save.to_file(merge_flood_mappluto_output_ofgdb, driver = 'OpenFileGDB', crs = 'EPSG:2263')


# #### Save as `.geojson` using `GeoJSON` driver

# In[116]:


street_flooding_mappluto_gdf_to_save.to_file(merge_flood_mappluto_output_geojson, driver = 'GeoJSON', crs = 'EPSG:2263')

