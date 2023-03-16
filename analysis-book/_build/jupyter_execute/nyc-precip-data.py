#!/usr/bin/env python
# coding: utf-8

# # NOAA ASOS/AWOS
# ## NOAA Automated Surface/Weather Observing Systems (ASOS/AWOS)
# ### Precipitation Data (Hourly) from 2010 to 2020, NYC, New York (Central Park, 40.779, -73.96925)
# 
# Author: Mark Bauer

# Dataset: Automated Surface/Weather Observing Systems (ASOS/AWOS)  
# ASOS Mainpage: https://www.ncei.noaa.gov/products/land-based-station/automated-surface-weather-observing-systems  
# User guide: https://www.weather.gov/media/asos/aum-toc.pdf
# 
# 
# Data retrieved from:  
# Iowa State University Environmental Mesonet: https://mesonet.agron.iastate.edu/request/asos/hourlyprecip.phtml?network=NY_ASOS  
# Station data: https://mesonet.agron.iastate.edu/sites/site.php?station=NYC&network=NY_ASOS  
# 
# 
# 
# Iowa Environmental Mesonet (IEM) Computed Hourly Precipitation Totals
# > The IEM attempts to take the METAR reports of precipitation and then provide just the hourly precipitation totals. These totals are not for the true hour (00 to 59 after), but for the hour between the standard METAR reporting time, typically :53 or :54 after. The timestamps displayed are in Central Daylight/Standard Time and for the hour the precipitation fell. So a value for 5 PM would roughly represent the period between 4:53 and 5:53 PM.

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


# path = 'https://mesonet.agron.iastate.edu/cgi-bin/request/hourlyprecip.py?network=NY_ASOS&station=NYC\
# &year1=2010&month1=1&day1=1&year2=2020&month2=12&day2=31&lalo=1&st=1&tz=America%2FNew_York'

# df = pd.read_csv(path)
# df.to_csv('data/hourlyprecip-nyc.csv', index=False)


# In[5]:


ls data/


# # Read in Data

# In[6]:


df = pd.read_csv('data/hourlyprecip-nyc.csv')

print(df.shape)
df.head()


# In[7]:


df.info()


# In[8]:


df.describe()


# In[9]:


# to date_time
df['date_time'] = pd.to_datetime(df['valid'], infer_datetime_format=True)
df = df.sort_values(by='date_time').reset_index(drop=True)

df.head(10)


# In[10]:


fig, axs = plt.subplots(1, 2, figsize=(8, 4))

sns.histplot(df['precip_in'],
             ax=axs[0])
axs[0].set_title('distribution of depths')

# removing zeros
sns.histplot(data=df.loc[df['precip_in'] > 0],
             x='precip_in',
             ax=axs[1])
axs[1].set_title('distribution of depths (exclude zeros)')

fig.tight_layout()


# In[11]:


fig, axs = plt.subplots(1, 2, figsize=(8, 4))

sns.boxplot(x=df["precip_in"],
             ax=axs[0])
axs[0].set_title('distribution of depths')

# removing zeros
sns.boxplot(data=df.loc[df["precip_in"] > 0],
             x='precip_in',
             ax=axs[1])
axs[1].set_title('distribution of depths (exclude zeros)')

fig.tight_layout()


# In[12]:


# highest values
fig, ax = plt.subplots(figsize=(8, 6))

(df
 .sort_values(by='precip_in', ascending=False)
 .loc[:, ['valid', 'precip_in']]
 .head()
 .sort_values(by='precip_in')
 .plot
 .barh(x='valid', y='precip_in', ax=ax)
)

plt.title('Highest Hourly Precipitation (Central Park, NYC)\n')
plt.ylabel('Date (Hourly)\n')
plt.xlabel('\nInches')
plt.tight_layout()


# Nice tutorial about resampling: https://www.earthdatascience.org/courses/use-data-open-source-python/use-time-series-data-in-python/date-time-types-in-pandas-python/resample-time-series-data-pandas-python/

# In[13]:


# Resample to hourly precip max and save as new dataframe
one_hour = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('1H')
    .max()
)

one_hour.describe()


# In[14]:


# Resample to hourly precip max and save as new dataframe
six_hour = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('6H')
    .max()
)

six_hour.describe()


# In[15]:


fig, axs = plt.subplots(1, 2, figsize=(10, 4))

sns.lineplot(data=one_hour, legend=False, palette=('tab:blue', ), ax=axs[0])
sns.lineplot(data=six_hour, legend=False, palette=('tab:blue', ), ax=axs[1])

axs[0].legend(labels=['1-Hour Max'])
axs[1].legend(labels=['6-Hour Max'])

for ax in axs.flat:
    ax.set_xlabel('')
    ax.set_ylabel('Depth (Inches)')

fig.tight_layout()


# # Read in NYC 311 Street Flooding Complaints

# In[16]:


path = 'https://raw.githubusercontent.com/mebauer/nyc-311-street-flooding/\
main/data/street-flooding-complaints.csv'

complaints_df = pd.read_csv(path, low_memory=False)

print(complaints_df.shape)
complaints_df.head()


# In[17]:


complaints_df.info()


# In[18]:


complaints_df['descriptor'].value_counts()


# In[19]:


# to date_time
complaints_df['date_time'] = pd.to_datetime(complaints_df['created_date'], infer_datetime_format=True)
complaints_df = complaints_df.sort_values(by='date_time').reset_index(drop=True)

complaints_df.head()


# # Hourly Max Depth vs. Hourly Complaint Counts

# In[20]:


# Resample to daily precip max and save as new dataframe
hour_max = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('1H')
    .max()
)

hour_max.describe()


# In[21]:


hour_max.loc[hour_max['precip_in'] > 0, ['rain_flag']] = 1
hour_max['rain_flag'] = hour_max['rain_flag'].fillna(0)
hour_max['rain_flag'] = hour_max['rain_flag'].astype(int)

hour_max.describe()


# In[22]:


# Resample to daily precip max and save as new dataframe
complaints_hourly = (
    complaints_df
    .set_index('date_time')[['unique_key']]
    .resample('1H')
    .count()
    .rename(columns={'unique_key':'count'})
)

complaints_hourly.head()


# In[23]:


merged_df = (
    hour_max
    .merge(complaints_hourly,
           left_index=True,
           right_index=True,
           how='left')
)

merged_df['count'] = merged_df['count'].fillna(0).astype(int)
merged_df['precip_in'] = merged_df['precip_in'].fillna(0)

merged_df.describe()


# In[24]:


complaint_and_rain = len(
    merged_df
    .loc[(merged_df['count'] > 0)
         & (merged_df['rain_flag'] == 1)]
)

complaint_and_norain = len(
    merged_df
    .loc[(merged_df['count'] > 0)
         & (merged_df['rain_flag'] == 0)]
)

nocomplaint_and_rain = len(
    merged_df
    .loc[(merged_df['count'] == 0)
         & (merged_df['rain_flag'] == 1)]
)

nocomplaint_and_norain = len(
    merged_df
    .loc[(merged_df['count'] == 0)
         & (merged_df['rain_flag'] == 0)]
)


print('Total hours: {:,}\n-----'.format(len(merged_df)))
print('There were complaints and it rained: {:,}'.format(complaint_and_rain))
print('There were complaints but it didnt rain: {:,}'.format(complaint_and_norain))
print('There were no complaints but it did rain: {:,}'.format(nocomplaint_and_rain))
print('There were no complaints and it didnt rain: {:,}'.format(nocomplaint_and_norain))


# In[25]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.scatterplot(data=merged_df, x="precip_in", y="count", ax=ax, alpha=.3)

plt.title('Hourly Total 311 Street Flooding Complaints vs. Precip 1-Hour Max (Inches)')
plt.xlabel('1-Hour Max (Inches)')
plt.ylabel('Total Count')

plt.tight_layout()


# In[26]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.regplot(data=merged_df, x="precip_in", y="count", ax=ax)

plt.title('Total Hourly 311 Street Flooding Complaints vs. Precip 1-Hour Max (Inches)')
plt.xlabel('1-Hourl Max (Inches)')
plt.ylabel('Total Count')

plt.tight_layout()


# In[27]:


merged_df.corr(method='pearson')


# In[28]:


merged_df.corr(method='spearman')


# In[29]:


Y = merged_df['count']
X = merged_df['precip_in']
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results = model.fit()
print(results.summary())


# # Total Daily Depth vs. Daily Complaint Counts

# In[30]:


# Resample to daily precip max and save as new dataframe
daily_total = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('D')
    .sum()
)

daily_total.describe()


# In[31]:


fig, ax = plt.subplots(figsize=(6, 4))

sns.lineplot(data=daily_total, legend=False, palette=('tab:blue', ), ax=ax)

ax.legend(labels=['Daily Total'])
ax.set_xlabel('')
ax.set_ylabel('Depth (Inches)')

plt.tight_layout()


# In[32]:


daily_total.loc[daily_total['precip_in'] > 0, ['rain_flag']] = 1
daily_total['rain_flag'] = daily_total['rain_flag'].fillna(0)
daily_total['rain_flag'] = daily_total['rain_flag'].astype(int)

daily_total['precip_in'] = daily_total['precip_in'].fillna(0)

daily_total.head()


# In[33]:


complaints_daily = (
    complaints_df
    .set_index('date_time')[['unique_key']]
    .resample('D')
    .count()
    .rename(columns={'unique_key':'count'})
)

complaints_daily.head()


# In[34]:


merged_df = (
    daily_total
    .merge(complaints_daily,
           left_index=True,
           right_index=True,
           how='left')
)

merged_df['count'] = merged_df['count'].fillna(0).astype(int)
merged_df['precip_in'] = merged_df['precip_in'].fillna(0)

merged_df.head()


# In[35]:


complaint_and_rain = len(
    merged_df
    .loc[(merged_df['count'] > 0)
         & (merged_df['rain_flag'] == 1)]
)

complaint_and_norain = len(
    merged_df
    .loc[(merged_df['count'] > 0)
         & (merged_df['rain_flag'] == 0)]
)

nocomplaint_and_rain = len(
    merged_df
    .loc[(merged_df['count'] == 0)
         & (merged_df['rain_flag'] == 1)]
)

nocomplaint_and_norain = len(
    merged_df
    .loc[(merged_df['count'] == 0)
         & (merged_df['rain_flag'] == 0)]
)


print('Total days: {:,}\n-----'.format(len(merged_df)))
print('There were complaints and it rained: {:,}'.format(complaint_and_rain))
print('There were complaints but it didnt rain: {:,}'.format(complaint_and_norain))
print('There were no complaints but it did rain: {:,}'.format(nocomplaint_and_rain))
print('There were no complaints and it didnt rain: {:,}'.format(nocomplaint_and_norain))


# In[36]:


fig, axs = plt.subplots(1, 2, figsize=(10, 4))

sns.lineplot(data=merged_df, x=merged_df.index, y='precip_in', legend=False, palette=('tab:blue', ), ax=axs[0])
sns.lineplot(data=merged_df, x=merged_df.index, y='count', legend=False, palette=('tab:blue', ), ax=axs[1])

axs[0].legend(labels=['Daily Precip Total Depth'])
axs[1].legend(labels=['Daily Complaints'])

axs[0].set_ylabel('Depth (Inches)')
axs[1].set_ylabel('Count')

[ax.set_xlabel('') for ax in axs.flat]
    
fig.tight_layout()


# In[37]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.scatterplot(data=merged_df, x="precip_in", y="count", ax=ax, alpha=.3)

plt.title('Daily 311 Street Flooding Complaints vs. Daily Total Depth (Inches)')
plt.xlabel('Total Depth (Inches)')
plt.ylabel('Count')

plt.tight_layout()


# In[38]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.regplot(data=merged_df, x="precip_in", y="count", ax=ax)

plt.title('Daily 311 Street Flooding Complaints vs. Daily Total Depth (Inches)')
plt.xlabel('Total Depth (Inches)')
plt.ylabel('Count')

plt.tight_layout()


# In[39]:


merged_df.corr(method='pearson')


# In[40]:


merged_df.corr(method='spearman')


# In[41]:


Y = merged_df['count']
X = merged_df['precip_in']
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results = model.fit()
print(results.summary())


# # Weekly Total Depth vs. Weekly Complaint Counts

# In[42]:


# Resample to daily precip max and save as new dataframe
week_total = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('W')
    .sum()
)

week_total.describe()


# In[43]:


week_total.loc[week_total['precip_in'] > 0, ['rain_flag']] = 1
week_total['rain_flag'] = week_total['rain_flag'].fillna(0)
week_total['rain_flag'] = week_total['rain_flag'].astype(int)

week_total['precip_in'] = week_total['precip_in'].fillna(0)

week_total.describe()


# In[44]:


# Resample to daily precip max and save as new dataframe
complaints_weekly = (
    complaints_df
    .set_index('date_time')[['unique_key']]
    .resample('W')
    .count()
    .rename(columns={'unique_key':'count'})
)

complaints_weekly.head()


# In[45]:


merged_df = (
    week_total
    .merge(complaints_weekly,
           left_index=True,
           right_index=True,
           how='left')
)

merged_df['count'] = merged_df['count'].fillna(0).astype(int)
merged_df['precip_in'] = merged_df['precip_in'].fillna(0)

merged_df.describe()


# In[46]:


complaint_and_rain = len(
    merged_df
    .loc[(merged_df['count'] > 0)
         & (merged_df['rain_flag'] == 1)]
)

complaint_and_norain = len(
    merged_df
    .loc[(merged_df['count'] > 0)
         & (merged_df['rain_flag'] == 0)]
)

nocomplaint_and_rain = len(
    merged_df
    .loc[(merged_df['count'] == 0)
         & (merged_df['rain_flag'] == 1)]
)

nocomplaint_and_norain = len(
    merged_df
    .loc[(merged_df['count'] == 0)
         & (merged_df['rain_flag'] == 0)]
)


print('Total weeks: {:,}\n-----'.format(len(merged_df)))
print('There were complaints and it rained: {:,}'.format(complaint_and_rain))
print('There were complaints but it didnt rain: {:,}'.format(complaint_and_norain))
print('There were no complaints but it did rain: {:,}'.format(nocomplaint_and_rain))
print('There were no complaints and it didnt rain: {:,}'.format(nocomplaint_and_norain))


# In[47]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.scatterplot(data=merged_df, x="precip_in", y="count", ax=ax, alpha=.3)

plt.title('Total Weekly 311 Street Flooding Complaints vs. Total Weekly Depth (Inches)')
plt.xlabel('Total Depth (Inches)')
plt.ylabel('Count')

plt.tight_layout()


# In[48]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.regplot(data=merged_df, x="precip_in", y="count", ax=ax)

plt.title('Total Weekly 311 Street Flooding Complaints vs. Total Weekly Depth (Inches)')
plt.xlabel('Total Depth (Inches)')
plt.ylabel('Count')

plt.tight_layout()


# In[49]:


merged_df.corr(method='pearson')


# In[50]:


merged_df.corr(method='spearman')


# In[51]:


Y = merged_df['count']
X = merged_df['precip_in']
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results = model.fit()
print(results.summary())


# In[ ]:




