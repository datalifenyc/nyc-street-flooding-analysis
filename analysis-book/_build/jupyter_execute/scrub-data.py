#!/usr/bin/env python
# coding: utf-8

# # Clean Data

# ## Import Libraries

# ### External Libraries

# In[1]:


import geopandas as gpd


# ### External Libraries

# ## Define Variables

# In[2]:


nyc_street_flooding_input = 'data/street-flood-complaints_rows-all.geojson'
nyc_street_flooding_output = 'data/clean_street-flood-complaints_rows-all.geojson'


# ## Get Original Data

# In[3]:


street_flooding_gdf = gpd.read_file(nyc_street_flooding_input)


# ## Set `unique_key` as Index

# In[4]:


street_flooding_gdf.set_index('unique_key', inplace=True)


# ## Remove Rows With Missing `geometry`

# In[5]:


street_flooding_gdf.dropna(subset = ['geometry'], inplace = True)


# ## Preview Street Flooding Data

# In[6]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].head(10)


# In[7]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].tail(10)


# ## Save Clean Dataset

# In[8]:


street_flooding_gdf.to_file(nyc_street_flooding_output, driver='GeoJSON')

