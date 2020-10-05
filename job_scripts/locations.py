""""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-02 15:23:28
 * @modify date 2020-10-02 16:58:38
 * @desc [
    Script to get string location data from data frame.
 ]
 */
"""

##########
# Imports
##########

import pandas as pd

from . import constants
from . import custom_errors
from .script_objects import DataFrame, DataFrames, List, Series, Union

##########
# Get locations
##########

def get_str_locations(df_jobsites: DataFrame, df_location_keys: DataFrames) -> DataFrame:
	"""Returns df_jobsites with location columns transformed into strings.

	Args:
		df_jobsite (Dataframe): master df to manipulate and return.
		df_location_keys (DataFrames): Respectively: countries, states, and cities.

	Returns:
		DataFrame: jobsites, with locations as strings.
	
	Auxiliary methods:
		1. get_int_list() - returns list of int locations to get str locations
		1. parse_val_for_strloc() - map over column to get string
	"""
	def parse_val_for_strloc(
		location_value: Union[int, str, List[str]], 
		int_str_key: dict,
		id_series: Series,
		column: str,
		row: str,
		) -> Union[str, List[str]]:
		"""Parses the value(s) and transforms it to string location(s).

		Args:
			location_value (Union[str, List[str]]): representing location or multiple locations
			int_str_key (dict): dict to convert int value to str
			id_series (Series): row ids
			column (str): data column
			row (str): row used

		Returns:
			Union[str, List[str]]: Location, or list of locations.
		
		Auxiliary function:
			get_int_list(): Returns List[int] from List[str].
		"""

		def get_int_list(
			location_values: str, 
			DELIMITER_LOC: str,
			id_series: Series,
			column: str,
			row: int
			) -> List[int]:
			"""Returns list of integers from string of int locations

			Args:
				location_values (str): List of locations, represented as str integers
				DELIMITER_LOC (str): string to separate locations ints by
				id_series (Series): Identify row id
				column (str): Column accessed
				row (int): Row of data

			Returns:
				List[int]: List of integers that map to locations
			
			NOTE:
			In the case that data is not properly input, raises an IncompatibleData Error 
			that indicates the column and row_id.
			"""
			location_values = location_values.replace(' ', '').split(DELIMITER_LOC)
			locations_ints = list()
			for val in location_values:
				try:
					val = int(val)
					locations_ints.append(val)
				except ValueError:
					if val == '':
						continue
					raise custom_errors.IncompatibleData(val, id_series, column, row)

			return locations_ints


		if isinstance(location_value, (int)):
			return int_str_key[location_value]
		
		location_strs = [int_str_key[i] for i in 
			get_int_list(location_value, constants.DELIMITER_LOC, id_series, column, row)] 
		return location_strs


	location_df_keys = (
		(df_location_keys[0], constants.AUX_DF_KEYS[0]),     # Country
		(df_location_keys[1], constants.AUX_DF_KEYS[1]),     # State
		(df_location_keys[2], constants.AUX_DF_KEYS[2]),     # City
	)
	for df, key in location_df_keys:
		# print(df.to_dict(), key, sep = "\n")
		int_str_dict = df.to_dict()[key]
		df_jobsites[key] = pd.Series([
			parse_val_for_strloc(df_jobsites[key].iloc[i], int_str_dict, df_jobsites.index, key, i)
				for i in range(len(df_jobsites[key]))])

	return df_jobsites
