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


nyc_street_flooding_input = 'data/clean_street-flood-complaints_rows-all.geojson'


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


# In[6]:


street_flooding_gdf[popup_columns].explore('borough')

