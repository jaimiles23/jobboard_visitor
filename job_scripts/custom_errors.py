"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-02 15:24:06
 * @modify date 2020-10-02 15:24:06
 * @desc [
    Defines custom errors in this script.
 ]
 */
"""

##########
# Imports
##########

try:
	from .script_objects import (Any, DataFrame, DataFrames, Iterator, Series,
	                             Union)
except:
	from script_objects import Any, DataFrame, DataFrames, Iterator, Series, Union


##########
# Incompatible Data
##########

class IncompatibleData(Exception):
	"""Class to show incompatible data type."""
	def __init__(self, val: Any, id_series: Series, column: str, row: int) -> None:
		"""Displays Error message with incompatible data location

		Args:
			val (Any): value that raised error
			id_series (Series): Series of IDs
			column (str): Column of dataframe
			row (int): row of data
		"""
		message = f"Invalid value: [{val}] in column: {column} with id {id_series[row]}"
		super().__init__(message)
		return

