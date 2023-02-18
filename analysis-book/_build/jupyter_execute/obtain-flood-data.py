#!/usr/bin/env python
# coding: utf-8

# # Street Flooding Complaints (SFC)

# ## Import Libraries

# ### Built-in Libraries

# In[1]:


import json
import os


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


get_ipython().run_cell_magic('script', 'echo skip', "street_flooding_gdf = gpd.read_file(NYC_OPEN_DATA_311_API_GEOJSON, driver='GeoJSON')\nstreet_flooding_gdf.to_file(output_prefix + 'geojson')\n")


# In[7]:


def get_street_flooding_data(file_type: str = 'geojson') -> None:
    """_summary_

    Args:
        file_type (str, optional): _description_. Defaults to 'geojson'.
    """
    df_size = -1
    file_size = 10000
    limit = file_size
    current_file = 0
    output_prefix = 'data/street_flood-complaints'
    while df_size != 0:
        street_flooding_df = gpd.read_file(get_api_endpoint(limit, current_file), driver='GeoJSON')
        df_size = len(street_flooding_df)
        if df_size == 0:
            break
        else:
            file_name_output = get_output_file_name(output_prefix, limit, current_file, file_type)
            street_flooding_df.to_file(file_name_output)
            print(f'Save file {current_file + 1}: {file_name_output}')
            current_file += 1
        
def get_api_endpoint(limit: int, current_file: int) -> str:
    """_summary_

    Args:
        limit (int): _description_
        current_file (int): _description_

    Returns:
        str: _description_
    """
    offset = limit * current_file
    return f'https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?descriptor=Street%20Flooding%20(SJ)&$limit={limit}&$offset={offset}&$order=unique_key'

def get_output_file_name(output_prefix: str, limit: int, current_file: int, file_type: str):
    """_summary_

    Args:
        output_prefix (str): _description_
        limit (int): _description_
        current_file (int): _description_
        file_type (str): _description_

    Returns:
        _type_: _description_
    """
    start_num = 1 + (limit * current_file)
    end_num = (1 + current_file) * limit
    return f'{output_prefix}_{start_num :06d}_{end_num :06d}.{file_type}'


# In[8]:


get_ipython().run_cell_magic('script', 'echo skip', "output_prefix = 'data/street_flood-complaints'\nfile_size = 10000\nlimit = file_size\ncurrent_file = 0\nfile_type = 'geojson'\n\nget_output_file_name(output_prefix, limit, current_file, file_type)\n")


# In[9]:


get_ipython().run_cell_magic('script', 'echo "skip: refactor to check if already downloaded"', "get_street_flooding_data(file_type = 'geojson')\n")


# In[10]:


geojson_file_list = ['data/' + geojson_file for geojson_file in os.listdir('data/') if geojson_file.endswith('.geojson')]
# print(geojson_file_list)


# In[11]:


geojson_df_list = list()

for geojson_file in geojson_file_list:
    geojson_file_df = gpd.read_file(geojson_file, driver='GeoJSON')
    geojson_df_list.append(geojson_file_df)

street_flooding_gdf = pd.concat(geojson_df_list)


# #### Save `.csv` data locally

# In[12]:


get_ipython().run_cell_magic('script', 'echo skip', "street_flooding_cdf = pd.read_csv(NYC_OPEN_DATA_311_API_CSV)\nstreet_flooding_cdf.to_csv(output_prefix + 'csv')\n")


# ### View Street Flooding Metadata

# In[13]:


street_flooding_gdf.info()


# ### Convert `datetime64` data type to string

# In[14]:


# created_date, resolution_action_updated_date, closed_date

street_flooding_gdf['created_date'] = street_flooding_gdf['created_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['resolution_action_updated_date'] = street_flooding_gdf['resolution_action_updated_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['closed_date'] = street_flooding_gdf['closed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')


# ### Set `unique_key` as Index

# In[15]:


street_flooding_gdf.set_index('unique_key', inplace=True)


# ### Remove Rows With Missing `geometry`

# In[16]:


street_flooding_gdf.dropna(subset = ['geometry'], inplace = True)


# ### Preview Street Flooding Data

# In[17]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].head(10)


# ### View on Map

# In[18]:


street_flooding_gdf['geometry'] = street_flooding_gdf.geometry


# In[19]:


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


# In[20]:


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
