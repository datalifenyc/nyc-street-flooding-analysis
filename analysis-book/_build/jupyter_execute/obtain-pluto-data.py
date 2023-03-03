#!/usr/bin/env python
# coding: utf-8

# # PLUTO & MapPLUTO
# 
# In addition to the PLUTO and MapPLUTO datasets, NYC has a rich set of GIS metadata resources. {cite}`cityofnewyork`

# ## Source 1: NYC Open Data
# 
# ### Primary Land Use Tax Lot Output (PLUTO)
# 
# | Key | Value |
# | --- | ----- |
# | URL | https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-PLUTO-/64uk-42ks |
# | Description | Extensive land use and geographic data at the tax lot level in comma–separated values (CSV) file format. The PLUTO files contain more than seventy fields derived from data maintained by city agencies. |
# | Updated | 2022-08-23 |
# | Update Frequency | Every 6 months |
# | Views | 10.5K |
# | Data Provided by | [Department of City Planning (DCP)](https://data.cityofnewyork.us/browse?Dataset-Information_Agency=Department+of+City+Planning+%28DCP%29) |
# | Category | [City Government](https://data.cityofnewyork.us/browse?category=Social+Services) |
# | API Docs | https://dev.socrata.com/foundry/data.cityofnewyork.us/64uk-42ks |
# | API Endpoints<br />(sample size: `10`) | [JSON](https://data.cityofnewyork.us/resource/64uk-42ks.json?$limit=10)<br>[GeoJSON](https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?$limit=10)<br>[CSV](https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=10) |
# | Data Dictionary | [PLUTODD.pdf](https://data.cityofnewyork.us/api/views/64uk-42ks/files/0bef0427-36f5-4d8d-867a-84dfa2477b9c?download=true&filename=PLUTODD.pdf)
# | README | [PlutoReadme.pdf](https://data.cityofnewyork.us/api/views/64uk-42ks/files/ded66205-b6ef-4253-8b38-cc24b5fca8b6?download=true&filename=PlutoReadme.pdf) |
# 
# 
# ### MapPLUTO
# 
# | Key | Value |
# | --- | ----- |
# | URL | https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-Map-MapPLUTO-/f888-ni5f |
# | Description | Extensive land use and geographic data at the tax lot level in GIS format (ESRI Shapefile). Contains more than seventy fields derived from data maintained by city agencies, merged with tax lot features from the Department of Finance’s Digital Tax Map, clipped to the shoreline. |
# | Updated | 2022-12-21 |
# | Update Frequency | Quarterly |
# | Views | 6K+ |
# | Data Provided by | [Department of City Planning (DCP)](https://data.cityofnewyork.us/browse?Dataset-Information_Agency=Department+of+City+Planning+%28DCP%29) |
# | Category | [City Government](https://data.cityofnewyork.us/browse?category=Social+Services) |
# | Data Dictionary | [PLUTODD22v3.pdf](https://data.cityofnewyork.us/api/views/f888-ni5f/files/a5f455ae-002e-4e78-ae17-f3dcc59c236d?download=true&filename=PLUTODD22v3.pdf)
# | README | [PlutoReadme22v3.pdf](https://data.cityofnewyork.us/api/views/f888-ni5f/files/97ca6e86-32cc-46f1-b85c-8d01e17e1602?download=true&filename=PlutoReadme22v3.pdf) |

# ## Source 2: NYC Dept. of City Planning
# 
# ### PLUTO
# 
# | Key | Value |
# | --- | ----- |
# | URL | https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page |
# | Description | Extensive land use and geographic data at the tax lot level in comma–separated values (CSV) file format. The PLUTO files contain more than seventy fields derived from data maintained by city agencies. |
# | Release | 22v3.1 |
# | Date of Data | February 2023 |
# | Data Provided by | [Department of City Planning (DCP)](https://www.nyc.gov/site/planning/data-maps/open-data.page) |
# | Data Dictionary | [PLUTODD.pdf](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/PLUTODD.pdf) |
# | README | [PlutoReadme.pdf](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/PlutoReadme.pdf)
# | Download | [CSV](https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_pluto_22v3_1_csv.zip) |
# 
# ### MapPluto
# 
# | Key | Value |
# | --- | ----- |
# | URL | https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page |
# | Description | MapPLUTO merges PLUTO tax lot data with tax lot features from the Department of Finance’s Digital Tax Map (DTM) and is available as shoreline clipped and water included. It contains extensive land use and geographic data at the tax lot level in ESRI shapefile and File Geodatabase formats. |
# | Release | 22v3.1 |
# | Date of Data | February 2023 |
# | Data Provided by | [Department of City Planning (DCP)](https://www.nyc.gov/site/planning/data-maps/open-data.page) |
# | Metadata | [meta_mappluto.pdf](https://s-media.nyc.gov/agencies/dcp/assets/files/pdf/data-tools/bytes/meta_mappluto.pdf) |
# | Download | [MapPLUTO - Shoreline Clipped (FGDB)](https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_fgdb.zip)<br>[MapPLUTO - Water Included (FGDB)](https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_unclipped_fgdb.zip)<br>[MapPLUTO - Shoreline Clipped (Shapefile)](https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_shp.zip)<br>[MapPLUTO - Water Included (Shapefile)](https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_unclipped_shp.zip) |
# | REST API | [REST Endpoint](https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/MAPPLUTO/FeatureServer/0) |
# 

# ## Import Libraries

# ### External Libraries

# In[1]:


import fiona


# ## Define Variables
# 
# MapPLUTO - Water Included (FGDB)

# In[2]:


map_pluto_gdb_folder = 'data/PLUTO/MapPLUTO_22v3_1_water_included.gdb'


# ## Download `MapPLUTO` Dataset

# ### Save .gdb data locally to `data/PLUTO` folder

# In[3]:


get_ipython().system('python obtainplutodata.py')


# ## View MapPLUTO Metadata

# In[4]:


map_pluto_gdb = fiona.open(map_pluto_gdb_folder)


# In[5]:


map_pluto_gdb.driver


# In[6]:


map_pluto_gdb.schema


# In[7]:


map_pluto_gdb.crs


# ## References
# 
# ### Fiona
# 
# [Fiona | Fiona reads and writes geographic data files | GitHub](https://github.com/Toblerity/Fiona)
# 
# 
# `conda install -c conda-forge fiona`
# 
# or
# 
# `pip install fiona`
# 

# 
