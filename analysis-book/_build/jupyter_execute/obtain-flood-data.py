#!/usr/bin/env python
# coding: utf-8

# # Street Flooding Complaints (SFC)

# ## Import Libraries

# ### Built-in Libraries

# In[1]:


import json
# import requests
# import csv


# ### External Libraries

# In[2]:


import pyproj
import geopandas as gpd
import pandas as pd
# import geojson as gj


# ## 311 Service Requests from 2010 to Present

# ### About
# 
# | Key | Value |
# | --- | ----- |
# | URL | https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9 |
# | Description | All 311 Service Requests from 2010 to present. |
# | Updated | 2023-02-13 |
# | Views | 440K+ |
# | Data Provided by | [311](https://data.cityofnewyork.us/browse?Dataset-Information_Agency=311), DoITT |
# | Category | [Social Services](https://data.cityofnewyork.us/browse?category=Social+Services) |
# | API Docs | https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9 |
# | API Endpoints<br />(sample size: `10`) | [JSON](https://data.cityofnewyork.us/resource/erm2-nwe9.json?$limit=10&descriptor=Street%20Flooding%20(SJ))<br>[GeoJSON](https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?$limit=10&descriptor=Street%20Flooding%20(SJ))<br>[CSV](https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=10&descriptor=Street%20Flooding%20(SJ)) |
# | `complaint_type` | Sewer |
# | `descriptor` | Street Flooding (SJ) |

# ### Define Variables
# 
# Default limit = 1000 
# 
# [Ref: Paging through Data](https://dev.socrata.com/docs/paging.html)

# In[3]:


NYC_OPEN_DATA_311_API_JSON = 'https://data.cityofnewyork.us/resource/erm2-nwe9.json?descriptor=Street%20Flooding%20(SJ)'
NYC_OPEN_DATA_311_API_GEOJSON = 'https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?descriptor=Street%20Flooding%20(SJ)'
NYC_OPEN_DATA_311_API_CSV = 'https://data.cityofnewyork.us/resource/erm2-nwe9.csv?descriptor=Street%20Flooding%20(SJ)'


# ### Download 311 Service Complaints for `Street Flooding (SJ)`

# #### Define prefix for output variable

# In[4]:


output_prefix = 'data/street_flood-complaints.'


# #### Save `.json` data locally

# In[5]:


street_flooding_jdf = pd.read_json(NYC_OPEN_DATA_311_API_JSON)
street_flooding_jdf.to_json(output_prefix + 'json')


# #### Save `.geojson` data locally

# In[6]:


street_flooding_gdf = gpd.read_file(NYC_OPEN_DATA_311_API_GEOJSON, driver='GeoJSON')
street_flooding_gdf.to_file(output_prefix + 'geojson')


# #### Save `.csv` data locally

# In[7]:


street_flooding_cdf = pd.read_csv(NYC_OPEN_DATA_311_API_CSV)
street_flooding_cdf.to_csv(output_prefix + 'csv')


# ### View Street Flooding Metadata

# In[8]:


street_flooding_gdf.info()


# ### Convert `datetime64` data type to string

# In[9]:


# created_date, resolution_action_updated_date, closed_date

street_flooding_gdf['created_date'] = street_flooding_gdf['created_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['resolution_action_updated_date'] = street_flooding_gdf['resolution_action_updated_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['closed_date'] = street_flooding_gdf['closed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')


# ### Set `unique_key` as Index

# In[10]:


street_flooding_gdf.set_index('unique_key', inplace=True)


# ### Remove Rows With Missing `geometry`

# In[11]:


street_flooding_gdf.dropna(subset = ['geometry'], inplace = True)


# ### Preview Street Flooding Data

# In[12]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].head(10)


# ### View on Map

# In[13]:


street_flooding_gdf['geometry'] = street_flooding_gdf.geometry


# In[14]:


popup_columns = [
    'geometry',
    'created_date',
    'incident_address',
    'city',
    'incident_zip',
    'borough',
    'bbl',
    'status',
]


# In[15]:


street_flooding_gdf[popup_columns].explore('borough')


# ## References
# 
# ### GeoPandas
# 
# [Reading and Writing Files | GoePandas Documentation](https://geopandas.org/en/stable/docs/user_guide/io.html)
# 
# ### pyproj
# 
# [On fresh Conda installation of PyProj: pyproj unable to set database path. _pyproj_global_context_initialize()](https://stackoverflow.com/questions/69630630/on-fresh-conda-installation-of-pyproj-pyproj-unable-to-set-database-path-pypr)
# 
# #### Fix
# 
# Un-install pyproj
# 
# `conda remove --force pyproj`
# 
# Re-install pyproj via `pip` instead of `conda`
# 
# `pip install pyproj`
# 

# 
