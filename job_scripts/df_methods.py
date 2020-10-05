"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-02 16:59:04
 * @modify date 2020-10-02 16:59:04
 * @desc [
	Contains methods to load script data frames.
 ]
 */
"""


##########
# Imports
##########

import pandas as pd

from . import constants
from . import custom_errors
from . import locations
from . import transform_col
from .jobsite_class import JobSite
from .script_objects import All_JobSites, DataFrame, DataFrames, Tuple

##########
# Load from Excel
##########

def load_dataframes(
	filename: str = constants.FILENAME_JOBSITES, 
	sheetnames: Tuple[str] = constants.SHEETNAMES
	) -> DataFrames:
	"""Loads jobsite data from xlsx file with `file_name`.

	Args:
		filename (str): csv to read.

	Returns:
		DataFrames: tuple of pandas data frames.
	"""

	df_jobsites, df_countries, df_states, df_cities = (
		pd.read_excel( filename, sheet, index_col = 0) for sheet in sheetnames
		)
	return (df_jobsites, df_countries, df_states, df_cities)


def get_df_jobsites() -> DataFrame:
	"""Returns cleaned jobsite dataframe

	Returns:
		DataFrame: Cleaned dataframe of jobsite information
	"""
	df_jobsites, df_countries, df_states, df_cities = load_dataframes()

	## Get countries
	df_location_keys = (df_countries, df_states, df_cities)
	df_jobsites = locations.get_str_locations(df_jobsites, df_location_keys)

	## Urls to lists
	df_jobsites = transform_col.transform_col_to_list_type(df_jobsites)

	return df_jobsites
