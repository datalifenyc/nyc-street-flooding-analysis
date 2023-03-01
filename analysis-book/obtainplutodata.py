"""
Module
------
Download MapPLUTO FGDB file from NYC Department of City Planning
website.

Data Source(s)
--------------

# NYC Department of City Planning

BYTES of the BIG APPLE™
https://www.nyc.gov/site/planning/data-maps/open-data.page#pluto

PLUTO and MapPLUTO
https://www.nyc.gov/site/planning/data-maps/open-data/dwn-pluto-mappluto.page

# NYC Open Data

Primary Land Use Tax Lot Output - Map (MapPLUTO)
https://data.cityofnewyork.us/City-Government/Primary-Land-Use-Tax-Lot-Output-Map-MapPLUTO-/f888-ni5f

Notes
-----
MapPLUTO - Primary Land Use Tax Lot Output - Map
FGDB - File Geodatabase

References
----------

# Python Documentation

os.path — Common pathname manipulations
https://docs.python.org/3/library/os.path.html

"""

# Import Libraries

## Standard Library
import os

## Custom Libraries
from utilities import (
    get_current_date as gcd,
    check_file_exists as cfe,
    download_unzip as du
)

# Define Variables

## Destination Folder
current_script_path = os.path.realpath(__file__)
current_script_dir = os.path.dirname(current_script_path)
output_folder_prefix = f'{current_script_dir}/data/PLUTO'

## PLUTO Release 22v3.1

### Format: csv
pluto_csv_url = 'https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_pluto_22v3_1_csv.zip'

## MapPLUTO Release 22v3.1

### Format: Shoreline Clipped (FGDB)
mappluto_shoreline_fgdb_url = 'https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_fgdb.zip'

### Format: Water Included (FGDB)
mappluto_water_fgdb_url = 'https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_unclipped_fgdb.zip'

### Format: Shoreline Clipped (Shapefile)
mappluto_shoreline_shapefile_url = 'https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_shp.zip'

### Format: Water Included (Shapefile)
mappluto_water_shapefile_url = 'https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nyc_mappluto_22v3_1_unclipped_shp.zip'

map_selection = {
    'none_csv': [
        # PLUTO (csv)
        ## data source url    
        pluto_csv_url,
        ## extracted file/folder name
        os.path.basename(pluto_csv_url).replace('_csv.zip', '.csv'),
        ## destination folder suffix
        ''
    ],
    'shoreline_fgdb': [
        # MapPLUTO Shoreline Clipped (FGDB)
        ## data source url 
        mappluto_shoreline_fgdb_url, 
        ## extracted file/folder name
        os.path.basename(mappluto_shoreline_fgdb_url).replace('fgdb.zip', 'shoreline_clipped.gdb').replace('nyc_mappluto', 'MapPLUTO'),
        # destination folder suffix
        ''
    ],
    'water_fgdb': [
        # MapPLUTO Water Included (FGDB)
        ## data source url     
        mappluto_water_fgdb_url, 
        ## extracted file/folder name
        os.path.basename(mappluto_water_fgdb_url).replace('unclipped_fgdb.zip', 'water_included.gdb').replace('nyc_mappluto', 'MapPLUTO'),
        # destination folder suffix
        ''
    ],
    'shoreline_shp': [
        # MapPLUTO Shoreline Clipped (Shapefile)
        ## data source url 
        mappluto_shoreline_shapefile_url,
        ## extracted file/folder name 
        os.path.basename(mappluto_shoreline_shapefile_url).replace('shp.zip', 'shoreline_clipped.shp').replace('nyc_mappluto', 'MapPLUTO'),
        # destination folder suffix
        ''
    ],
    'water_shp': [
        # MapPLUTO Water Included (Shapefile)
        # data source url 
        mappluto_water_shapefile_url, 
        # extracted file/folder name
        os.path.basename(mappluto_water_shapefile_url).replace('unclipped_shp.zip', 'water_included.shp').replace('nyc_mappluto', 'MapPLUTO'),
        # destination folder suffix
        ''
    ]
}

# Define Functions
def download_pluto(map_type: str = 'water', file_type: str = 'fgdb') -> None:
    """
    Functionality
    -------------
    Download PLUTO or MapPLUTO dataset from NYC Dept. of City Planning
    
    Parameters
    ----------
        map_type (str, optional): _description_. Defaults to 'water'.
            Options: none, shoreline, water
        file_type (str, optional): _description_. Defaults to 'fgdb'.
            Options: csv, fgdb, 

    Returns
    -------
        (None)
    """
    # Get key for map selection
    map_select = f'{map_type}_{file_type}'

    # Get url of map file
    pluto_download_url = map_selection[map_select][0]

    # Get folder name for destination map file
    pluto_download_folder_name = map_selection[map_select][1]

    # Define destination full path
    output_folder_file_name = f'{output_folder_prefix}/{pluto_download_folder_name}'

    # Do not download file if it already exists, otherwise download
    # print(f'{output_folder_file_name=}')
    print(f'Download latest PLUTO and MapPLUTO datasets...\n')

    if map_type == 'water':
        file_name_addon = '_unclipped'
    else:
        file_name_addon = ''

    match file_type:
        case 'fgdb':
            if cfe(output_folder_file_name) == True:
                print(f'Dataset: "{map_selection[map_select][1]}" already exists.\n')
            else:
                du(pluto_download_url, output_folder_prefix)
                os.rename(
                    f'{output_folder_prefix}/MapPLUTO_22v3_1{file_name_addon}.{file_type[-3:]}', 
                    output_folder_file_name
                )
                print(f'Dataset is available here: data/PLUTO/{pluto_download_folder_name}\n')
        case 'shp':
            if cfe(output_folder_file_name) == True:
                print(f'Dataset: "{map_selection[map_select][1]}" already exists.\n')
            else:
                os.mkdir(output_folder_file_name)
                du(pluto_download_url, output_folder_file_name)
                print(f'Dataset is available here: data/PLUTO/{pluto_download_folder_name}\n')
    print('SUCCESS.\n\nThe process has completed.')
    
## Function: `main`
def main():
    download_pluto('water', 'fgdb')

# Run
if __name__ =='__main__':
    main()