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
from .class_jobboard import JobBoard
from .script_objects import all_jobboards, DataFrame, DataFrames, Tuple

##########
# Load from Excel
##########

def load_dataframes(
	filename: str = constants.FILENAME_JOBBOARDS, 
	sheetnames: Tuple[str] = constants.SHEETNAMES
	) -> DataFrames:
	"""Loads JobBoard data from xlsx file with `file_name`.

	Args:
		filename (str): csv to read.

	Returns:
		DataFrames: tuple of pandas data frames.
	"""

	df_JobBoards, df_countries, df_states, df_cities = (
		pd.read_excel( filename, sheet, index_col = 0) for sheet in sheetnames
		)
	return (df_JobBoards, df_countries, df_states, df_cities)


def get_df_jobboards() -> DataFrame:
	"""Returns cleaned JobBoard dataframe

	Returns:
		DataFrame: Cleaned dataframe of JobBoard information
	"""
	df_JobBoards, df_countries, df_states, df_cities = load_dataframes()

	## Get countries
	df_location_keys = (df_countries, df_states, df_cities)
	df_JobBoards = locations.get_str_locations(df_JobBoards, df_location_keys)

	## Urls to lists
	df_JobBoards = transform_col.transform_col_to_list_type(df_JobBoards)

	return df_JobBoards
