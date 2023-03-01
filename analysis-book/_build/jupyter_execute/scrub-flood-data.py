#!/usr/bin/env python
# coding: utf-8

# # Clean Data
# 
# ![clean-merge-data](img/scrub-process-diagram.png)

# ## Import Libraries

# ### External Libraries

# In[1]:


import geopandas as gpd


# ### External Libraries

# ## Define Variables

# In[2]:


nyc_street_flooding_input = 'data/street-flooding/street-flood-complaints_rows-all.geojson'
nyc_street_flooding_output = 'data/street-flooding/clean_street-flood-complaints_rows-all.geojson'


# ## Get Original Data

# In[3]:


street_flooding_gdf = gpd.read_file(nyc_street_flooding_input)


# ## Before Count

# In[4]:


street_flooding_complaints_before_count = len(street_flooding_gdf)
print(f'There were {street_flooding_complaints_before_count:,} street flooding complaints from 2010 to the present.')


# ## Set `unique_key` as Index

# In[5]:


street_flooding_gdf.set_index('unique_key', inplace=True)


# ## Remove Rows With Missing `geometry`

# In[6]:


street_flooding_gdf.dropna(subset = ['geometry'], inplace = True)


# ## After Count

# In[7]:


street_flooding_complaints_after_count = len(street_flooding_gdf)
print(f'There were {street_flooding_complaints_after_count:,} street flooding complaints after rows with missing geometry have been removed.')


# ## Preview Street Flooding Data

# In[8]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].head(10)


# In[9]:


street_flooding_gdf[['created_date', 'borough', 'bbl', 'geometry']].tail(10)


# ## Save Clean Dataset

# In[10]:


street_flooding_gdf.to_file(nyc_street_flooding_output, driver='GeoJSON')

