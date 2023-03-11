#!/usr/bin/env python
# coding: utf-8

# # Street Flooding & MapPLUTO
# 
# Merge the NYC Street Flooding service requests dataset with MapPluto

# ## Import Libraries

# ### Standard Libraries

# In[1]:


import os


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

# ### Output Files

# In[4]:


nyc_street_flooding_gdf_columns_output = 'data/nyc_street_flooding_gdf_columns.txt'
pluto_gdf_columns_output = 'data/pluto_gdf_columns.txt'

current_script_path = os.path.realpath(os.path.curdir)
pluto_geojson = 'data/PLUTO/pluto_22v3_1.geojson'
pluto_geojson_full_path = f'{current_script_path}/{pluto_geojson}'


# ### NYC Street Flooding Complaints

# In[5]:


nyc_street_flooding_geojson = 'data/street-flooding/street-flood-complaints_rows-all.geojson'


# ### MapPLUTO

# In[6]:


map_pluto_gdb_folder = 'data/PLUTO/MapPLUTO_22v3_1_water_included.gdb'


# In[7]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using gdb file type"', "map_pluto_shp_folder  = 'data/PLUTO/MapPLUTO_22v3_1_water_included.shp'\n")


# ## Combine `Street Flooding Complaints` and `MapPLUTO` Datasets

# ### Read `Street Flooding Complaints`

# In[8]:


street_flooding_gdf = gpd.read_file(nyc_street_flooding_geojson)


# In[9]:


sfc_size = len(street_flooding_gdf)
print(f'# of Street Flooding Complaints: {sfc_size}')


# #### Save `Street Flooding Complaints` Column Names to `nyc_street_flooding_gdf_columns.txt`
# 
# {cite}`hule2021listtofile`

# In[10]:


street_flooding_columns = street_flooding_gdf.columns.tolist()


# In[11]:


with open(f'{current_script_path}/{nyc_street_flooding_gdf_columns_output}', 'w') as write_f:
    for column in street_flooding_columns:
        write_f.write(f'{column}\n')


# #### Check Index

# In[12]:


street_flooding_gdf.index


# #### Set `unique_key` as Index

# In[13]:


street_flooding_gdf.set_index('unique_key', inplace = True)


# #### Verify Index Change

# In[14]:


street_flooding_gdf.index


# ### Read `MapPluto`
# 
# Time to read gdb folder: ~`42m`

# In[15]:


if cfe(pluto_geojson_full_path) == False:
    print('PLUTO geojson file has not been created. Getting data from gdb folder....')
    pluto_gdf = gpd.read_file(map_pluto_gdb_folder)
    pluto_gdf.to_file(pluto_geojson_full_path, driver='GeoJSON')
else:
    pluto_gdf = gpd.read_file(pluto_geojson_full_path, driver='GeoJSON')


# In[16]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using gdb file type"', 'pluto_shp_gdf = gpd.read_file(map_pluto_shp_folder)\n')


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


# In[38]:


type(street_flooding_pluto_gdf)


# In[39]:


len(street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] == None])


# #### Check % Join by BBL

# In[40]:


def pct_join(gdf: gpd.GeoDataFrame) -> dict:
    gdf_join_info = dict()
    df_size = len(gdf)
    missing_geometry_y_count = len(gdf[gdf['geometry_y'] == None])

    gdf_join_info['df_size'] = df_size
    gdf_join_info['missing_geometry_y_count'] = missing_geometry_y_count
    gdf_join_info['pct_join'] = (df_size - missing_geometry_y_count) / df_size * 100
    gdf_join_info['pct_missing'] = missing_geometry_y_count / df_size * 100

    return gdf_join_info


# In[41]:


bbl_join_stats_dict = pct_join(street_flooding_pluto_gdf)
bbl_join_stats_dict


# ### Join #2: Spatial Join
# 
# {cite}`ramsey2018postgisspatial`

# #### Split DataFrame Into BBL Matches and Non-matches

# ##### BBL matches

# In[42]:


street_flooding_pluto_bbl_match_gdf = \
    street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] != None]


# In[79]:


output_match_folder = 'data/merge/'
file_name_geojson = 'street_flooding_pluto_bbl_match.geojson'
file_name_shp = 'street_flooding_pluto_bbl_match.shp'


# Save Match to geojson

# In[80]:


street_flooding_pluto_bbl_match_gdf.to_file(f'{output_match_folder}{file_name_geojson}', driver='GeoJSON')


# Save Match to Shapefile

# In[81]:


street_flooding_pluto_bbl_match_gdf.to_file(f'{output_match_folder}{file_name_shp}')


# Verify match count

# In[43]:


match_count = bbl_join_stats_dict['df_size'] - \
    bbl_join_stats_dict['missing_geometry_y_count']

match_count == \
    len(street_flooding_pluto_bbl_match_gdf)


# ##### BBL mismatches

# In[44]:


street_flooding_pluto_bbl_mismatch_gdf = \
    street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] == None]


# Only extract the street flooding columns before rejoining with sjoin

# In[45]:


street_flooding_pluto_bbl_mismatch_copy_gdf = \
    street_flooding_pluto_bbl_mismatch_gdf.copy()


# Rename `geometry_x` column back to original name, `geometry`

# In[46]:


street_flooding_pluto_bbl_mismatch_copy_gdf.rename(columns = {"geometry_x": "geometry"}, inplace = True)


# Copy index as column, `unique_key`

# In[47]:


street_flooding_pluto_bbl_mismatch_copy_gdf['unique_key'] = street_flooding_pluto_bbl_mismatch_copy_gdf.index


# In[48]:


street_flooding_pluto_bbl_mismatch_copy_gdf.info()


# Verify mismatch count

# In[49]:


bbl_join_stats_dict['missing_geometry_y_count'] == \
    len(street_flooding_pluto_bbl_mismatch_copy_gdf)


# Copy only the street flooding columns

# In[50]:


street_flooding_bbl_no_match_gdf = \
    street_flooding_pluto_bbl_mismatch_copy_gdf[street_flooding_columns].copy()


# #### Perform `sjoin`
# 
# {cite}`ramsey2018postgisspatial,fleischmann2021spatialjoin`

# Set active geometry

# In[51]:


street_flooding_bbl_no_match_gdf.set_geometry('geometry', inplace = True)


# In[52]:


street_flooding_map_pluto_sjoin_gdf = (
    gpd.sjoin(
        street_flooding_bbl_no_match_gdf,
        pluto_4326_gdf,
        how = 'left',
        predicate = 'within'
    )
)


# In[53]:


list_of_columns = street_flooding_map_pluto_sjoin_gdf.columns.tolist()


# In[54]:


list_of_columns


# In[55]:


preview_columns


# In[74]:


preview_columns_sjoin = [
    'borough',
    'Borough',
    'created_date', 
    'street_name', 
    'bbl', 
    'ZipCode', 
    'geometry',
    'TaxMap']


# In[57]:


street_flooding_map_pluto_sjoin_gdf[preview_columns_sjoin].head(10)


# In[58]:


street_flooding_map_pluto_sjoin_gdf[preview_columns_sjoin].tail(10)


# In[59]:


nan_count = street_flooding_map_pluto_sjoin_gdf['Borough'].isna().sum()
nan_count


# #### Perform `sjoin_nearest`
# 
# {cite}`ramsey2018postgisspatial,fleischmann2021spatialjoin`

# In[ ]:





# In[60]:


"""street_flooding_bbl_no_match_gdf.crs = 'epsg:3035'
street_flooding_bbl_no_match_gdf.to_crs('4326', inplace = True)"""


# In[61]:


"""pluto_4326_gdf.crs = 'epsg:3035'
pluto_4326_gdf.to_crs('4326', inplace = True)"""


# In[62]:


"""street_flooding_bbl_no_match_gdf.crs"""


# In[63]:


"""street_flooding_bbl_no_match_gdf.geometry"""


# In[64]:


"""pluto_4326_gdf.crs"""


# In[65]:


"""pluto_4326_gdf.geometry"""


# In[66]:


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

# In[67]:


"""street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('32610'),
        pluto_4326_gdf.to_crs('32610'),
        # how = 'inner',
        distance_col = 'distances'
    )
)"""


# In[85]:


# temp
sfbnmg10 = street_flooding_bbl_no_match_gdf.iloc[:10,:].copy()


# In[86]:


# temp
len(sfbnmg10)


# In[87]:


# temp
p4g10 = pluto_4326_gdf.iloc[:50,:].copy()


# In[88]:


# temp
len(p4g10)


# In[89]:


# temp
street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('2263'),
        pluto_4326_gdf.to_crs('2263'),
        how = 'left',
        distance_col = 'distance'
    )
)


# In[68]:


street_flooding_map_pluto_sjoin_nearest_gdf = (
    gpd.sjoin_nearest(
        street_flooding_bbl_no_match_gdf.to_crs('3857'),
        pluto_4326_gdf.to_crs('3857'),
        how = 'left',
        distance_col = 'distance'
    )
)


# In[69]:


street_flooding_map_pluto_sjoin_nearest_gdf.columns


# In[82]:


len(pluto_4326_gdf)


# In[75]:


preview_columns_sjoin.append('distance')


# In[90]:


# temp
street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin].head(10)


# In[76]:


street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin].head(10)


# In[77]:


street_flooding_map_pluto_sjoin_nearest_gdf[preview_columns_sjoin].tail(10)


# In[78]:


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




