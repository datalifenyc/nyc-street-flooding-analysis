"""
Module
------
Basic multi-use functions

Notes
-----

References
----------

# Python Documentation

zipfile — Work with ZIP archives
https://docs.python.org/3/library/zipfile.html

io — Core tools for working with streams
https://docs.python.org/3/library/io.html

urllib.request — Extensible library for opening URLs
https://docs.python.org/3/library/urllib.request.html#module-urllib.request

os.path — Common pathname manipulations
https://docs.python.org/3/library/os.path.html

# GitHub

Download and extract a ZIP file in Python | hantoine/download_and_unzip.py
https://gist.github.com/hantoine/c4fc70b32c2d163f604a8dc2a050d5f6

"""

# Import Libraries

## Standard Libraries
from datetime import datetime as dt
from pathlib import Path
from urllib.request import urlopen as uo
from io import BytesIO as bio
from zipfile import ZipFile as zf
import os

# Define Functions

## Function: `get_current_date`
def get_current_date() -> str:
    """
    Functionality
    -------------
    Returns current date in format <YYYY-MM-DD>

    Parameters
    ----------

    Returns
    -------
        (str): current date
    """
    return dt.now().strftime('%Y-%m-%d')

## Function: `check_file_exists`
def check_file_exists(file_name: str) -> bool:
    """
    Funtionality
    ------------
    Returns `True` if file exists

    Parameters
    ----------
        file_name (str): file name to check

    Returns
    -------
        (bool): `True` if file exits
    """
    return os.path.exists(file_name)

## Function: `download_unzip`
def download_unzip(zip_url: str, output_folder: str) -> None:
    """
    Functionality
    -------------
    Download and extract zip files

    Parameters
    ----------
        zip_url (str): URL of data file
        output_folder (str): Location to safe and extract data file contents

    Returns
    -------
        (None)
    """
    response = uo(zip_url)
    data_zip = zf(bio(response.read()))
    data_zip.extractall(path = output_folder)

## Function: `main`
def main():
    pass

# Run
if __name__ == '__main__':
    main()

