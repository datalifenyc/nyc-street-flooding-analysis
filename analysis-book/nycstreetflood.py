"""
Module
------
Download NYC Open Data 311 Service Request data for Street Flooding (SJ) from 
NYC Open Data website.

Data Sources(s)
---------------

Notes
-----

References
----------
"""

# Import Libraries

## Standard Libraries
import os
from typing import List

## Custom Libraries
from utilities import (
    get_current_date as gcd,
    check_file_exists as cfe
)

## External Libraries
import geopandas as gpd
import pandas as pd

# Define Classes & Functions

## Class: `StreetFlood`
class StreetFlood:

    # Define Class Methods
    
    ## Method: Initialize
    def __init__(self) -> None:
        pass

    ## Method: `get_street_flooding_data`
    def get_street_flooding_data(self, file_type: str = 'geojson') -> None:
        """
        Functionality
        -------------
        Get NYC Open Data 311 Service Requests dataset with descriptor: Street Flooding (SJ)

        Parameters
        ----------
            file_type (str, optional): download data as <json|geojson|csv>. Defaults to 'geojson'.

        Returns
        -------
            (None)
        """
        df_size = -1
        file_size = 10000
        limit = file_size
        current_file = 0
        current_script_path = os.path.realpath(__file__)
        current_script_dir = os.path.dirname(current_script_path)
        output_prefix = f'{current_script_dir}/data/street-flood-complaints'
        file_name_output = self.get_output_file_name(output_prefix, limit, df_size, current_file, file_type)
        new_files_list = []
        if cfe(file_name_output) == True:
            print(f'Street flooding dataset has already been download for {gcd()}.')
        else:
            while df_size != 0:
                street_flooding_df = gpd.read_file(self.get_api_endpoint(limit, current_file), driver='GeoJSON')
                df_size = len(street_flooding_df)
                if df_size == 0:
                    break
                else:
                    file_name_output = self.get_output_file_name(output_prefix, limit, df_size, current_file, file_type)
                    new_files_list.append(file_name_output)
                    street_flooding_df.to_file(file_name_output)
                    print(f'Save file {current_file + 1}: {file_name_output}')
                    current_file += 1
                    
            # Merge downloaded geojson files into 1 file
            self.merge_geojson_files(output_prefix, new_files_list, file_type)

    ## Method: `get_api_endpoint`       
    def get_api_endpoint(self, limit: int, current_file: int) -> str:
        """
        Functionality
        -------------
        Returns the API Endpoint for the NYC Street Flooding dataset

        Parameters
        ----------
            limit (int): max number of rows to return per file
            current_file (int): current file count for downloads larger than the 
            file limit

        Returns
        -------
            (str): URL for NYC Street Flooding dataset
        """
        offset = limit * current_file
        return f'https://data.cityofnewyork.us/resource/erm2-nwe9.geojson?descriptor=Street%20Flooding%20(SJ)&$limit={limit}&$offset={offset}&$order=unique_key'

    # Method: `get_output_file_name`
    def get_output_file_name(self, output_prefix: str, limit: int, df_size: int, current_file: int, file_type: str) -> str:
        """
        Functionality
        -------------
        Returns the file name for the current dataset in the form:
        <output_prefix>_rows-<start_num>_<end_num>_dt-<current_date>.<file_ext>

        Parameters
        ----------
            output_prefix (str): <file_path>/<file_name_beginning>
            limit (int): max number of rows to return per file
            current_file (int): current file count for downloads larger than the 
            file limit
            file_type (str): file format of saved dataset as <json|geojson|csv>

        Returns
        -------
            (str): name of street flooding dataset save file
        """
        start_num = 1 + (limit * current_file)
        end_num = -1 + start_num + df_size
        return f'{output_prefix}_rows-{start_num :06d}-{end_num :06d}_dt-{gcd()}.{file_type}'

    # Method: `merge_geojson_files`
    def merge_geojson_files(self, output_prefix: str, new_files_list: List = [], file_type: str = 'geojson') -> None:
        """
        Functionality
        -------------
        ### Merge `.geojson` Files Into a Single GeoPandas Dataframe

        Parameters
        ----------
            None

        Returns
            (None)
        """
        # List of currently downloaded nyc street flooding geojson files
        geojson_file_list = new_files_list
        # print(geojson_file_list)

        geojson_df_list = list()

        for geojson_file in geojson_file_list:
            geojson_file_df = gpd.read_file(geojson_file, driver='GeoJSON')
            geojson_df_list.append(geojson_file_df)

        # Merge complete dataset
        street_flooding_gdf = pd.concat(geojson_df_list)

        # Save file
        street_flooding_gdf.to_file(f'{output_prefix}_rows-all.{file_type}')

        print(f'Geojson files have been merged.')

## Function: `main`
def main():
    print(f'Downloading Latest Street Flooding Dataset...\n')
    download = StreetFlood()
    download.get_street_flooding_data()
    print(f'\nDownload Complete')

# Run
if __name__ == '__main__':
    main()