#!/usr/bin/env python
# coding: utf-8

# # Investigating the correlation between high precipitation events and 311 street flooding complaints in New York City
# Author: Mark Bauer  
# 
# ## Objective: Ground-truthing 311 street flooding complaints to actual precipitation levels.
# 
# The NYC 311 is a fantastic system to alert the City of non-emergency services such as garbage and trash removal, noise levels, dirty sidewalks, etc. Department of Environmental Protection (DEP) is tasked with responding to 311's Street Flooding complaints. While 311 is not directly intended to measure and observe flooding events, studies show that 311 street flooding complaints might be linked to actual flooding and have the potential to reveal areas that require greater sewer maintenence and resources.
# 
# This analysis is designed to test the hypothesis that 311 Street Flooding Complaints are correlated with high precipitation events in Central Park, NYC from 2010 to 2020.
# 
# ## Links   
# NYC 311: https://portal.311.nyc.gov/  
# About NYC 311: https://portal.311.nyc.gov/about-nyc-311/  
# Street Flooding Complaint Form: https://portal.311.nyc.gov/article/?kanumber=KA-02198

# # Data Sources
# 
# ## 1) 311 Steet Flooding Complaints
# 
# 311 Service Requests from 2010 to Present: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
# 
# 
# ## 2) NOAA Automated Surface/Weather Observing Systems (ASOS/AWOS)
# Precipitation Data (Hourly) from 2010 to 2020, NYC, New York (Central Park, 40.779, -73.96925)
# 
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


import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import chi2_contingency
import datetime
import fiona

plt.rcParams['savefig.facecolor'] = 'white'
get_ipython().run_line_magic('matplotlib', 'inline')


# Printing versions of Python modules and packages with **watermark** - the IPython magic extension.

# In[2]:


get_ipython().run_line_magic('load_ext', 'watermark')


# In[3]:


get_ipython().run_line_magic('watermark', '-v -p numpy,pandas,geopandas,geoplot,fiona,matplotlib.pyplot,seaborn')


# Documention for installing watermark: https://github.com/rasbt/watermark

# # Retrieve Data

# Saving the data locally to my directory.

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

print('rows: {:,}\ncolumns: {}'.format(df.shape[0], df.shape[1]))
df.head()


# In[7]:


# My usual sanity checks of the dataframe
df.info()


# In[8]:


df.describe()


# In[9]:


# to date_time
df['date_time'] = pd.to_datetime(df['valid'], infer_datetime_format=True)
df = df.sort_values(by='date_time').reset_index(drop=True)

# sanity check
df.head(10)


# In[10]:


fig, axs = plt.subplots(1, 2, figsize=(8, 4))

sns.histplot(df['precip_in'], ax=axs[0])
axs[0].set_title('distribution of depths')

# removing zeros
sns.histplot(data=df.loc[df['precip_in'] > 0], x='precip_in', ax=axs[1])
axs[1].set_title('distribution of depths (exclude zeros)')

fig.tight_layout()


# In[11]:


fig, axs = plt.subplots(1, 2, figsize=(8, 4))

sns.boxplot(x=df["precip_in"], ax=axs[0])
axs[0].set_title('distribution of depths')

# removing zeros
sns.boxplot(data=df.loc[df["precip_in"] > 0], x='precip_in', ax=axs[1])
axs[1].set_title('distribution of depths (exclude zeros)')

fig.tight_layout()


# In[12]:


# highest values by date_time in NYC

fig, ax = plt.subplots(figsize=(8, 6))

(df
 .sort_values(by='precip_in', ascending=False)
 .loc[:, ['valid', 'precip_in']]
 .head()
 .sort_values(by='precip_in')
 .plot.barh(x='valid', y='precip_in', ax=ax, legend=False)
)

plt.title('Highest Hourly Precipitation 2010 to 2020 (Central Park, NYC)')
plt.ylabel('Date (Hourly)')
plt.xlabel('Inches')
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

# sanity check
one_hour.describe()


# In[14]:


# Resample to 6-hour precip max and save as new dataframe
six_hour = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('6H')
    .max()
)

# sanity check
six_hour.describe()


# # Compare 1-Hour and 6-Hour max precipitation

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


# The plots generally follow the same trend, so we can use one of them to represent our actual precipitation group. Specifically, these intervals can represent our Flash Flooding group.

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


# only one 311 descriptor in this dataset - street flooding
complaints_df['descriptor'].value_counts()


# In[19]:


# to date_time
complaints_df['date_time'] = pd.to_datetime(complaints_df['created_date'], infer_datetime_format=True)
complaints_df = complaints_df.sort_values(by='date_time').reset_index(drop=True)

# sanity check
complaints_df.head()


# # 6-Hour Max Depth vs. 6-Hour Complaint Counts

# In[20]:


# Resample to 6-hour precip max and save as new dataframe
hour_six_max = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('6H')
    .max()
)

hour_six_max['precip_in'] = hour_six_max['precip_in'].fillna(0)

hour_six_max.loc[hour_six_max['precip_in'] > 0, ['rain_flag']] = 1
hour_six_max['rain_flag'] = hour_six_max['rain_flag'].fillna(0)
hour_six_max['rain_flag'] = hour_six_max['rain_flag'].astype(int)

# sanity check
hour_six_max.describe()


# In[21]:


# Resample to 6-hour complaint count and save as new dataframe
complaints_hourly = (
    complaints_df
    .set_index('date_time')[['unique_key']]
    .resample('6H')
    .count()
    .rename(columns={'unique_key':'count'})
)

complaints_hourly['count'] = complaints_hourly['count'].fillna(0)

complaints_hourly.loc[complaints_hourly['count'] > 0, 'complaint_flag'] = 1
complaints_hourly['complaint_flag'] = complaints_hourly['complaint_flag'].fillna(0)
complaints_hourly['complaint_flag'] = complaints_hourly['complaint_flag'].astype(int)

complaints_hourly.describe()


# In[22]:


# merge both datasets on date_time
merged_df = (
    hour_six_max
    .merge(complaints_hourly,
           left_index=True,
           right_index=True,
           how='left')
)

merged_df['count'] = merged_df['count'].fillna(0).astype(int)
merged_df['complaint_flag'] = merged_df['complaint_flag'].fillna(0).astype(int)

# sanity check
merged_df.describe()


# # Qualitative Analysis - 311 Complaint vs. Rain Event

# In[23]:


print('Total 6-hour intervals: {:,}\n-----'.format(len(merged_df)))
print('Normalize all')

pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'], margins=True).round(2)


# In[24]:


print('Total 6-hour intervals: {:,}\n-----'.format(len(merged_df)))
print('Normalize by row')

pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'], normalize='index').round(2)


# In[25]:


crosstab = pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'])
stat, p, dof, expected = chi2_contingency(crosstab)

# interpret p-value
alpha = 0.05
print("p value is " + str(p))
if p <= alpha:
    print('Dependent (reject H0)')
else:
    print('Independent (H0 holds true)')


# ## Highest Event

# In[26]:


merged_df.sort_values(by='precip_in', ascending=False).head(1)


# In[27]:


fig, ax1 = plt.subplots(figsize=(8, 6))
ax2 = ax1.twinx()

sns.lineplot(data=merged_df, 
             x=merged_df.index,
             y='precip_in',
             label='precip_in', 
             color='tab:blue',
             ax=ax1)

sns.lineplot(data=merged_df, 
             x=merged_df.index,
             y='count',
             label='complaints', 
             color='tab:red',
             ax=ax2)

ax1.set_xlim([datetime.date(2018, 8, 8), datetime.date(2018, 8, 14)])

ax1.legend(loc=2)
ax2.legend(loc=1)

event = merged_df.sort_values(by='precip_in', ascending=False).head(1).index[0]
plt.title('Highest 6-Hour Max Depth: {}'.format(event))

plt.tight_layout()


# # Quantitative Analysis - Linear Regression

# In[28]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.regplot(data=merged_df, x="precip_in", y="count", ax=ax)

plt.title('Count of 6-Hour 311 Street Flooding Complaints vs. Precip 6-Hour Max (Inches)')
plt.xlabel('6-Hour Max (Inches)')
plt.ylabel('6-Hour Total Count')

plt.tight_layout()


# In[29]:


merged_df.corr(method='pearson')


# In[30]:


merged_df.corr(method='spearman')


# In[31]:


Y = merged_df['count']
X = merged_df['precip_in']
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results = model.fit()
print(results.summary())


# In[32]:


print('Parameters:\n{}'.format(results.params.round(4)))
print('\nR2: {}'.format(results.rsquared.round(4)))


# # Total Daily Depth vs. Daily Complaint Counts

# In[33]:


# Resample to daily precip sum and save as new dataframe
daily_total = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('D')
    .sum()
)

daily_total['precip_in'] = daily_total['precip_in'].fillna(0)

daily_total.loc[daily_total['precip_in'] > 0, ['rain_flag']] = 1
daily_total['rain_flag'] = daily_total['rain_flag'].fillna(0)
daily_total['rain_flag'] = daily_total['rain_flag'].astype(int)

# sanity check
daily_total.describe()


# In[34]:


# Resample to daily complaint count and save as new dataframe
complaints_daily = (
    complaints_df
    .set_index('date_time')[['unique_key']]
    .resample('D')
    .count()
    .rename(columns={'unique_key':'count'})
)

complaints_daily['count'] = complaints_daily['count'].fillna(0).astype(int)

complaints_daily.loc[complaints_daily['count'] > 0, 'complaint_flag'] = 1
complaints_daily['complaint_flag'] = complaints_daily['complaint_flag'].fillna(0)
complaints_daily['complaint_flag'] = complaints_daily['complaint_flag'].astype(int)

complaints_daily.describe()


# In[35]:


# merge dataframes on date_time
merged_df = (
    daily_total
    .merge(complaints_daily,
           left_index=True,
           right_index=True,
           how='left')
)

merged_df['count'] = merged_df['count'].fillna(0)
merged_df['complaint_flag'] = merged_df['complaint_flag'].fillna(0)

merged_df.head()


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


# # Qualitative Analysis - 311 Complaint vs. Rain Event

# In[37]:


print('Total daily intervals: {:,}\n-----'.format(len(merged_df)))
print('Normalize all')

pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'], margins=True).round(2)


# In[38]:


print('Total daily intervals: {:,}\n-----'.format(len(merged_df)))
print('Normalize by row')

pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'], normalize='index').round(2)


# In[39]:


crosstab = pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'])
stat, p, dof, expected = chi2_contingency(crosstab)

# interpret p-value
alpha = 0.05
print("p value is " + str(p))
if p <= alpha:
    print('Dependent (reject H0)')
else:
    print('Independent (H0 holds true)')


# ## Highest Event

# In[40]:


merged_df.sort_values(by='precip_in', ascending=False).head(1)


# In[41]:


fig, ax1 = plt.subplots(figsize=(8, 6))
ax2 = ax1.twinx()

sns.lineplot(data=merged_df, 
             x=merged_df.index,
             y='precip_in',
             label='precip_in', 
             color='tab:blue',
             ax=ax1)

sns.lineplot(data=merged_df, 
             x=merged_df.index,
             y='count',
             label='complaints', 
             color='tab:red',
             ax=ax2)

ax1.set_xlim([datetime.date(2011, 8, 7), datetime.date(2011, 8, 21)])
ax2.set_xlim([datetime.date(2011, 8, 7), datetime.date(2011, 8, 21)])

ax1.legend(loc=2)
ax2.legend(loc=1)

event = str(merged_df.sort_values(by='precip_in', ascending=False).head(1).index[0])[:-9]
plt.title('Highest Daily Depth Amount: {}'.format(event))

plt.tight_layout()


# # Quantitative Analysis - Linear Regression

# In[42]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.regplot(data=merged_df, x="precip_in", y="count", ax=ax)

plt.title('Daily 311 Street Flooding Complaints vs. Daily Total Depth (Inches)')
plt.xlabel('Total Depth (Inches)')
plt.ylabel('Count')

plt.tight_layout()


# In[43]:


merged_df.corr(method='pearson')


# In[44]:


merged_df.corr(method='spearman')


# In[45]:


Y = merged_df['count']
X = merged_df['precip_in']
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results = model.fit()
print(results.summary())


# In[46]:


print('Parameters:\n{}'.format(results.params.round(4)))
print('\nR2: {}'.format(results.rsquared.round(4)))


# # Weekly Total Depth vs. Weekly Complaint Counts

# In[47]:


# Resample to weekly precip sum and save as new dataframe
week_total = (
    df
    .set_index('date_time')[['precip_in']]
    .resample('W')
    .sum()
)

week_total['precip_in'] = week_total['precip_in'].fillna(0)

week_total.loc[week_total['precip_in'] > 0, ['rain_flag']] = 1
week_total['rain_flag'] = week_total['rain_flag'].fillna(0)
week_total['rain_flag'] = week_total['rain_flag'].astype(int)

# sanity check
week_total.describe()


# In[48]:


# Resample to weekly complaint counts and save as new dataframe
complaints_weekly = (
    complaints_df
    .set_index('date_time')[['unique_key']]
    .resample('W')
    .count()
    .rename(columns={'unique_key':'count'})
)

complaints_weekly['count'] = complaints_weekly['count'].fillna(0)

complaints_weekly.loc[complaints_weekly['count'] > 0, 'complaint_flag'] = 1
complaints_weekly['complaint_flag'] = complaints_weekly['complaint_flag'].fillna(0)
complaints_weekly['complaint_flag'] = complaints_weekly['complaint_flag'].astype(int)

complaints_weekly.describe()


# In[49]:


# merge on date_time
merged_df = (
    week_total
    .merge(complaints_weekly,
           left_index=True,
           right_index=True,
           how='left')
)

merged_df['count'] = merged_df['count'].fillna(0).astype(int)
merged_df['complaint_flag'] = merged_df['complaint_flag'].fillna(0)

# sanity check
merged_df.describe()


# # Qualitative Analysis - 311 Complaint vs. Rain Event

# In[50]:


print('Total weekly intervals: {:,}\n-----'.format(len(merged_df)))
print('Normalize all')

pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'], margins=True).round(2)


# In[51]:


print('Total weekly intervals: {:,}\n-----'.format(len(merged_df)))
print('Normalize by row')

pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'], normalize='index').round(2)


# In[52]:


crosstab = pd.crosstab(merged_df['complaint_flag'], merged_df['rain_flag'])
stat, p, dof, expected = chi2_contingency(crosstab)

# interpret p-value
alpha = 0.05
print("p value is " + str(p))
if p <= alpha:
    print('Dependent (reject H0)')
else:
    print('Independent (H0 holds true)')


# ## Highest Event

# In[53]:


merged_df.sort_values(by='precip_in', ascending=False).head(1)


# In[54]:


fig, ax1 = plt.subplots(figsize=(8, 6))
ax2 = ax1.twinx()

sns.lineplot(data=merged_df, 
             x=merged_df.index,
             y='precip_in',
             label='precip_in', 
             color='tab:blue',
             ax=ax1)

sns.lineplot(data=merged_df, 
             x=merged_df.index,
             y='count',
             label='complaints', 
             color='tab:red',
             ax=ax2)

ax1.set_xlim([datetime.date(2011, 6, 14), datetime.date(2011, 10, 14)])
myFmt = mdates.DateFormatter('%m-%d\n%Y')
ax1.xaxis.set_major_formatter(myFmt)

ax1.legend(loc=2)
ax2.legend(loc=1)

event = str(merged_df.sort_values(by='precip_in', ascending=False).head(1).index[0])[:-9]
plt.title('Highest Weekly Depth Amount: {}'.format(event))

plt.tight_layout()


# # Quantitative Analysis - Linear Regression

# In[55]:


fig, ax = plt.subplots(figsize=(8, 6))

sns.regplot(data=merged_df, x="precip_in", y="count", ax=ax)

plt.title('Total Weekly 311 Street Flooding Complaints vs. Total Weekly Depth (Inches)')
plt.xlabel('Total Depth (Inches)')
plt.ylabel('Count')

plt.tight_layout()


# In[56]:


merged_df.corr(method='pearson')


# In[57]:


merged_df.corr(method='spearman')


# In[58]:


Y = merged_df['count']
X = merged_df['precip_in']
X = sm.add_constant(X)

model = sm.OLS(Y,X)
results = model.fit()
print(results.summary())


# In[59]:


print('Parameters:\n{}'.format(results.params.round(4)))
print('\nR2: {}'.format(results.rsquared.round(4)))


# In[ ]:




