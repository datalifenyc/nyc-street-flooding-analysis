#!/usr/bin/env python
# coding: utf-8

# # Street Flooding Complaints (SFC)

# ## Source: 311 Service Requests from 2010 to Present

# ### About
# 
# | Key | Value |
# | --- | ----- |
# | URL | https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9 |
# | Description | All 311 Service Requests from 2010 to present. |
# | Updated | 2023-02-15 |
# | Update Frequency | Daily |
# | Views | 440K+ |
# | Data Provided by | [311](https://data.cityofnewyork.us/browse?Dataset-Information_Agency=311), DoITT |
# | Category | [Social Services](https://data.cityofnewyork.us/browse?category=Social+Services) |
# | API Docs | https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9 |
# | API Endpoints<br />(sample size: `10`) | [JSON](https://data.cityofnewyork.us/resource/erm2-nwe9.json?$limit=10&descriptor=Street%20Flooding%20(SJ))<br>[GeoJSON](https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?$limit=10&descriptor=Street%20Flooding%20(SJ))<br>[CSV](https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=10&descriptor=Street%20Flooding%20(SJ)) |
# | `complaint_type` | Sewer |
# | `descriptor` | Street Flooding (SJ) |

# ## Import Libraries

# ### Built-in Libraries

# In[1]:


# import json
import os
from datetime import datetime as dt
from pathlib import Path


# ### External Libraries

# In[2]:


import pyproj
import geopandas as gpd
import pandas as pd
# import geojson as gj


# ### Define Variables
# 
# Default limit = 1000 
# 

# In[3]:


get_ipython().run_cell_magic('script', 'echo skip', "NYC_OPEN_DATA_311_API_JSON = 'https://data.cityofnewyork.us/resource/erm2-nwe9.json?descriptor=Street%20Flooding%20(SJ)'\nNYC_OPEN_DATA_311_API_GEOJSON = 'https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?descriptor=Street%20Flooding%20(SJ)'\nNYC_OPEN_DATA_311_API_CSV = 'https://data.cityofnewyork.us/resource/erm2-nwe9.csv?descriptor=Street%20Flooding%20(SJ)'\n")


# ### Download 311 Service Complaints for `Street Flooding (SJ)`

# #### Define prefix for output variable

# In[4]:


get_ipython().run_cell_magic('script', 'echo skip', "output_prefix = 'data/street_flood-complaints.'\n")


# #### Save `.json` data locally

# In[5]:


get_ipython().run_cell_magic('script', 'echo skip', "street_flooding_jdf = pd.read_json(NYC_OPEN_DATA_311_API_JSON)\nstreet_flooding_jdf.to_json(output_prefix + 'json')\n")


# #### Save `.geojson` data locally

# In[6]:


get_ipython().system('python nycstreetflood.py')


# ### Save `.csv` data locally

# In[7]:


get_ipython().run_cell_magic('script', 'echo skip', "street_flooding_cdf = pd.read_csv(NYC_OPEN_DATA_311_API_CSV)\nstreet_flooding_cdf.to_csv(output_prefix + 'csv')\n")


# ### View Street Flooding Metadata

# In[8]:


nyc_street_flooding_geojson = 'data/street-flood-complaints_rows-all.geojson'
street_flooding_gdf = gpd.read_file(nyc_street_flooding_geojson)


# In[9]:


street_flooding_gdf.info()


# ### Convert `datetime64` data type to string

# In[10]:


# created_date, resolution_action_updated_date, closed_date

street_flooding_gdf['created_date'] = street_flooding_gdf['created_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['resolution_action_updated_date'] = street_flooding_gdf['resolution_action_updated_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['closed_date'] = street_flooding_gdf['closed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')


# ### Set `unique_key` as Index

# In[11]:


street_flooding_gdf.set_index('unique_key', inplace=True)


# ### Remove Rows With Missing `geometry`

# In[12]:


street_flooding_gdf.dropna(subset = ['geometry'], inplace = True)


# ### Preview Street Flooding Data

# In[13]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].head(10)


# ### View on Map

# In[14]:


street_flooding_gdf['geometry'] = street_flooding_gdf.geometry


# In[15]:


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


# In[16]:


street_flooding_gdf[popup_columns].explore('borough')


# ## References
# 
# ### Python Standard Library
# 
# #### Format
# 
# [How to pad zeros to a String in Python | Python Engineer](https://www.python-engineer.com/posts/pad-zeros-string/)  
# Contributer: [@Patrick Loeber](https://patloeber.com)
# 
# #### Date and Time
# 
# [datetime — Basic date and time types | Python > Documentation](https://docs.python.org/3/library/datetime.html)
# 
# #### File & Path I/O
# 
# [pathlib — Object-oriented filesystem paths | Python > Documentation](https://docs.python.org/3/library/pathlib.html)
# 
# ### GeoPandas
# 
# #### User Guide
# 
# [Reading and Writing Files | GoePandas - Documentation - User Guide](https://geopandas.org/en/stable/docs/user_guide/io.html)
# 
# [Merging Data | GeoPandas - Documentation - User Guide](https://geopandas.org/en/stable/docs/user_guide/mergingdata.html)
# 
# #### API Reference
# 
# [geopandas.GeoDataFrame.to_file | GeoPandas API reference](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.to_file.html)
# 
# ### Jupyter Notebook
# 
# #### Magic (%%) Commands
# 
# [How to (intermittently) skip certain cells when running IPython notebook? | stackoverflow](https://stackoverflow.com/questions/19309287/how-to-intermittently-skip-certain-cells-when-running-ipython-notebook)  
# Contributor: [@Mark](https://stackoverflow.com/users/420385/mark)
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
# ### Socrata API
# 
# [Paging through Data | Socrata - Documentation](https://dev.socrata.com/docs/paging.html)
# 

# 
