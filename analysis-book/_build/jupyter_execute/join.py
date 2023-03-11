#!/usr/bin/env python
# coding: utf-8

# # Join Tutorial
# 
# Join points to closest BBL shapes tutorial.

# # Importing Libraries

# In[1]:


import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import geopandas as gpd
import fiona
from fiona.crs import from_epsg
import geoplot
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
import datetime
import statsmodels.api as sm

plt.rcParams['savefig.facecolor'] = 'white'
get_ipython().run_line_magic('matplotlib', 'inline')


# Printing versions of Python modules and packages with **watermark** - the IPython magic extension.

# In[2]:


get_ipython().run_line_magic('load_ext', 'watermark')


# In[3]:


get_ipython().run_line_magic('watermark', '-v -p numpy,pandas,geopandas,geoplot,fiona,matplotlib.pyplot,seaborn')


# Documention for installing watermark: https://github.com/rasbt/watermark

# # Retrieve Data

# In[4]:


path = 'https://raw.githubusercontent.com/mebauer/nyc-311-street-flooding/main/data/\
street-flooding-complaints.csv'

df = pd.read_csv(path, low_memory=False)
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.longitude, df.latitude, crs=4263))

gdf = gdf.dropna(subset=['longitude']).reset_index(drop=True)
gdf = gdf.to_crs(2263)

print(gdf.shape)
gdf.head()


# In[5]:


gdf.plot()


# In[6]:


path = '~/Downloads/nyc_mappluto_22v3_1_fgdb/MapPLUTO_22v3_1.gdb'
pluto_gdf = gpd.read_file(path, rows=500)

pluto_gdf = pluto_gdf.to_crs(2263)

print(pluto_gdf.shape)
pluto_gdf.head()


# In[7]:


pluto_gdf.plot()


# In[8]:


pluto_gdf.sindex


# In[9]:


offset = 200
bbox = gdf.bounds + [-offset, -offset, offset, offset]

bbox.head()


# In[10]:


hits = bbox.apply(lambda row: list(pluto_gdf.sindex.intersection(row)), axis=1)

print(hits.shape)
hits.head()


# In[11]:


tmp = pd.DataFrame(
        {
        # index of points table
        "pt_idx": np.repeat(hits.index, hits.apply(len)),

        # ordinal position of line - access via iloc later
        "line_i": np.concatenate(hits.values)
        }
)

print(tmp.shape)
tmp.head()


# In[12]:


# Join back to the lines on line_i; we use reset_index() to 
# give us the ordinal position of each line
tmp = tmp.join(pluto_gdf.reset_index(drop=True), on="line_i")

tmp.head()


# In[13]:


# Join back to the original points to get their geometry
# rename the point geometry as "point"
tmp = tmp.join(gdf.geometry.rename("point"), on="pt_idx")

# Convert back to a GeoDataFrame, so we can do spatial ops
tmp = gpd.GeoDataFrame(tmp, geometry="geometry", crs=gdf.crs)

tmp.head()


# In[14]:


tmp["snap_dist"] = tmp.geometry.distance(gpd.GeoSeries(tmp.point))

tmp.head()


# In[15]:


# Discard any lines that are greater than tolerance from points
tmp = tmp.loc[tmp.snap_dist <= offset]

# Sort on ascending snap distance, so that closest goes to top
tmp = tmp.sort_values(by=["snap_dist"])

tmp.head()


# In[16]:


# group by the index of the points and take the first, which is the
# closest line 
closest = tmp.groupby("pt_idx").first()

# construct a GeoDataFrame of the closest lines
closest = gpd.GeoDataFrame(closest, geometry="geometry")

closest.head()


# In[17]:


# Join back to the original points:
updated_points = gdf.join(closest.drop(columns=['geometry']))

updated_points.head()


# In[18]:


updated_points.describe()


# In[19]:


updated_points['unique_key'].is_unique


# In[ ]:




