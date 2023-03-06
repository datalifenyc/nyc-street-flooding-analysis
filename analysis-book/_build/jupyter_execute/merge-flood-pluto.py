#!/usr/bin/env python
# coding: utf-8

# # Merge Street Flooding & MapPLUTO

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


# In[ ]:


get_ipython().run_cell_magic('script', 'echo "[skip] Reason: using gdb file type"', 'pluto_shp_gdf = gpd.read_file(map_pluto_shp_folder)\n')


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


# In[ ]:


type(street_flooding_pluto_gdf)


# In[ ]:


len(street_flooding_pluto_gdf[street_flooding_pluto_gdf['geometry_y'] == None])


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


pct_join(street_flooding_pluto_gdf)


# ### Join #2: Spatial Join
# 
# {cite}`ramsey2018postgisspatial`

# In[ ]:


"""street_flooding_map_pluto_df = (
    gpd.sjoin_nearest(
        street_flooding_gdf.to_crs(4326),
        map_pluto_gdf.to_crs(4326),
        distance_col = 'distance_between'
    ).reset_index(drop = True)
)"""


# In[ ]:


"""street_flooding_map_pluto_shp_df = (
    gpd.sjoin(
        street_flooding_gdf,
        pluto_shp_gdf.to_crs(4326),
        how = 'inner',
        predicate = 'within'
    ).reset_index(drop = True)
)
"""


# In[ ]:


# nan_count = street_flood_pluto_gdf['geometry_y'].isna().sum()


# In[ ]:




