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

import warnings
from dataclasses import dataclass

try:
	from .script_objects import (Any, DataFrame, DataFrames, Iterator, Series,
	                             Union)
except:
	from script_objects import Any, DataFrame, DataFrames, Iterator, Series, Union


## warnings
WARN_STACK = 2
WARN_LEN = 'length'
WARN_KEYS = 'keys'
WARN_ATTR = 'class_attr'

##
UserDefinedClass = object


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



##########
# Warnings
##########
@dataclass
class TblEntryWarning(UserWarning):
	"""Class to show warnings about table entries."""

	##### Init
	"""Uses the warn_type (str) to determine what warning message to call.

	Args:
		entry (Union[dict, Iterator[Any], UserDefinedClass]): information to record.
		tbl_info (dict): table holding information.
		show_values (bool, optional): show value assignment. Defaults to False.
		stack (int, optional): number of lines to go back. Defaults to WARN_STACK.
	"""
	warn_type: str
	entry: Union[dict, Iterator[Any], UserDefinedClass]
	tbl_info: dict
	show_values: bool = False
	stack: int = WARN_STACK

	def __post_init__(self):
		warn_dict = {
			WARN_LEN		:	self.warn_entry_length,
			WARN_KEYS		:	self.warn_entry_keys,
			WARN_ATTR	:	self.warn_entry_attr,
		}
		warn_dict[self.warn_type]()


	##### Warning messages
	def warn_entry_length(self):
		"""Shows warning that iterator length does not match keys length."""
		warning_message = ""
		warnings.warn(warning_message)
		
		# https://pymotw.com/2/warnings/ - use stack to show number of lines to move up.


	def warn_entry_keys(self):
		"""Shows warning that entry.keys do not match table.keys."""
		warning_message = ""
		warnings.warn(warning_message)


	def warn_entry_attr(self):
		"""Shows warning that entry attributes do not match table.keys."""
		warning_message = ""
		warnings.warn(warning_message)
