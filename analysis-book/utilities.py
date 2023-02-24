"""
Module: Basic multi-use functions
"""

# Import Libraries

## Standard Libraries
from datetime import datetime as dt
from pathlib import Path

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
    return Path(file_name).exists()

## Function: `main`
def main():
    pass

# Run
if __name__ == '__main__':
    main()

