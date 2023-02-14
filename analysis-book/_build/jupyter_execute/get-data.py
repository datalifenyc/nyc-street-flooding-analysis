#!/usr/bin/env python
# coding: utf-8

# # Get Data

# ## Import Libraries

# ### Built-in Libraries

# In[ ]:





# ### External Libraries

# In[1]:


import geopandas as gpd


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
# | API Endpoints | [JSON](https://data.cityofnewyork.us/resource/erm2-nwe9.json)<br>[GeoJSON](https://data.cityofnewyork.us/resource/erm2-nwe9.geojson)<br>[CSV](https://data.cityofnewyork.us/resource/erm2-nwe9.csv) |
# | `complaint_type` | Sewer |
# | `descriptor` | Street Flooding (SJ) |

# ### Define Variables

# In[2]:


NYC_OPEN_DATA_311_API_JSON = 'https://data.cityofnewyork.us/resource/erm2-nwe9.json?descriptor=Street%20Flooding%20(SJ)'
NYC_OPEN_DATA_311_API_GEOJSON = 'https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?descriptor=Street%20Flooding%20(SJ)'
NYC_OPEN_DATA_311_API_CSV = 'https://data.cityofnewyork.us/resource/erm2-nwe9.csv?descriptor=Street Flooding (SJ)'


# ### Download 311 Service Complaints for `Street Flooding (SJ)`

# In[3]:


street_flooding_gdf = gpd.read_file(NYC_OPEN_DATA_311_API_GEOJSON, driver='GeoJSON')


# ### Preview Street Flooding Data

# In[4]:


street_flooding_gdf.head(10)


# In[ ]:




