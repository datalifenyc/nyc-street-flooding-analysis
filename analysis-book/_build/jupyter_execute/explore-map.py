#!/usr/bin/env python
# coding: utf-8

# # Explore Map

# ## Import Libraries

# ### External Libraries

# In[1]:


import geopandas as gpd


# ### External Libraries

# ## Define Variables

# In[2]:


nyc_street_flooding_input = 'data/street-flooding/clean_street-flood-complaints_rows-all.geojson'


# ## Get Clean Data

# In[3]:


street_flooding_gdf = gpd.read_file(nyc_street_flooding_input)


# ## View Complaints on OpenStreetMap

# In[4]:


street_flooding_gdf['geometry'] = street_flooding_gdf.geometry


# In[5]:


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


# ## Convert `datetime64` data type to string
# 
# `datetime64` needs to be converted to string before viewing using 
# `GeoPandas.explore()`, otherwise the following error will appear: 
# `Object of type Timestamp is not JSON serializable`

# In[6]:


# created_date, resolution_action_updated_date, closed_date

street_flooding_gdf['created_date'] = street_flooding_gdf['created_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['resolution_action_updated_date'] = street_flooding_gdf['resolution_action_updated_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['closed_date'] = street_flooding_gdf['closed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')


# In[7]:


street_flooding_gdf[popup_columns].explore('borough')


# ## References
# 
# [ENH: explore(): skip if fields/index are Timestamp #2378 | geopandas > Issues](https://github.com/geopandas/geopandas/issues/2378)

# 
