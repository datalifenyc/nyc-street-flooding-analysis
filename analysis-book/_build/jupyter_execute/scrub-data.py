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


# ## Convert `datetime64` data type to string

# In[4]:


# created_date, resolution_action_updated_date, closed_date

street_flooding_gdf['created_date'] = street_flooding_gdf['created_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['resolution_action_updated_date'] = street_flooding_gdf['resolution_action_updated_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
street_flooding_gdf['closed_date'] = street_flooding_gdf['closed_date'].dt.strftime('%Y-%m-%d %H:%M:%S')


# ## Set `unique_key` as Index

# In[5]:


street_flooding_gdf.set_index('unique_key', inplace=True)


# ## Remove Rows With Missing `geometry`

# In[6]:


street_flooding_gdf.dropna(subset = ['geometry'], inplace = True)


# ## Preview Street Flooding Data

# In[7]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].head(10)


# In[8]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].tail(10)


# ## Save Clean Dataset

# In[9]:


street_flooding_gdf.to_file(nyc_street_flooding_output, driver='GeoJSON')

