"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 13:03:19
 * @modify date 2020-10-04 14:24:25
 * @desc [
	Modules contains methods relevant to printing table information. Provides methods to:
		- Initialize the table strucutre
		- Add entry to table
		- Print the table

NOTE: Also include method to write the table to a markdown file - can be used for hackerrank.
 ]
 */
"""


##########
# Imports
##########

import math
from typing import Any, Iterator, Union
import os

from custom_errors import TblEntryWarning


##########
# Constants
##########

## table
TBL_STRCT_KEY = '__keys'
TBL_RECORD_KEY = '#'

## allowed space on terminal
ALLOWED_TERM_WIDTH = 0.98


## warnings
WARN_STACK = 2
WARN_LEN = 'length'
WARN_KEYS = 'keys'
WARN_ATTR = 'class_attr'


##########
# Objects
##########

UserDefinedClass = object
Table = dict


##########
# Initialize table
##########

def init_tbl( tbl_keys: Union[dict, Iterator[Any]]) -> Table:
	"""Returns Table (dict) with passed keys.

	Args:
		tbl_keys (Union[ dict, Iterator[Any]): Used to create dictionary key.

	Returns:
		Table: Returns dictionary with key structure

	Notes:
		- Table structure is stored in reserved '__keys' dictionary key.
		- Allows duplicates passed as tbl_keys.
	"""
	if not isinstance(tbl_keys, dict) and not hasattr(tbl_keys, '__iter__'):
		raise Exception("Initialization table must be type: List, Tuple, or Dictionary.")

	tbl_keys = tbl_keys if hasattr(tbl_keys, '__iter__') else tbl_keys.keys()
	tbl_keys.insert(0, TBL_RECORD_KEY)
	return { k  :dict() for k in tbl_keys}


##########
# Add table information
##########

def add_tbl_entry(
	tbl_info: Table, 
	entry: Union[dict, Iterator[Any], UserDefinedClass],
	show_warning: bool = True,
	show_warn_vals: bool = False
	) -> Table:
	"""Dictionary representing table holding information.

	Args:
		tbl_info (Table): dictionary that holds information
		entry (Union[dict, Iterator[Any], UserDefinedClass]): Info to add to table.
		show_warning (bool, optional): show warnings when adding entry. Defaults to True.
		show_warn_vals (bool, optional): show value assignments in warning. Defaults to False.

	Returns:
		Table: Table dictionary with updated entry.
	
	Auxiliary methods:
		is_userdefinedclass(): returns boolean if object is a user defined class.
	"""
	def is_userdefinedclass(cls):
		return str(cls).startswith('<class ')


	flag_show_warning, warn_type = False, None
	entry_num = len(tbl_info[ TBL_RECORD_KEY])
	
	if is_userdefinedclass(entry):
		attr_dict = {}
		for k in tbl_info.keys():
			try: val = getattr(entry, k)
			except AttributeError: val = None
			finally: attr_dict[k][entry_num] = val

		entry = attr_dict		# Add to tbl_info w/ dict method
		if None in attr_dict.values():
			flag_show_warning, warn_type = True, WARN_ATTR
	
	if isinstance(entry, dict):	
		if entry.keys() != tbl_info.keys():
			flag_show_warning, warn_type = True, WARN_KEYS
		
		for k in tbl_info.keys():
			try: val = entry[k]
			except KeyError: val = None
			finally: tbl_info[k][entry_num] = val
	
	elif hasattr(entry, '__iter__'):
		if len(entry) != len(tbl_info.keys()):
			flag_show_warning, warn_type = True, WARN_LEN
			
		i = 0
		for k in tbl_info.keys():
			val = entry[i] if i < len(entry) else None
			tbl_info[k][entry_num] = val
			i += 1

	if flag_show_warning:
		TblEntryWarning(warn_type= warn_type, entry= entry, tbl_info= tbl_info, show_values= show_warn_vals)
	
	return tbl_info


##########
# Print table information
##########

def print_tbl(
	tbl_info: Table, 
	num_spaces: int = 3,
	h_lines: bool = False,
	v_lines: bool = True,
	row_sep: str = '-',
	col_sep: str = '|'
	) -> None:
	"""Prints table information in pretty format.

	Args:
		tbl_info (Table): dict of info to print.
		num_spaces (int, optional): spaces to put b/w table columns.. Defaults to 3.
		h_lines (bool, optional): Should print horizontal lines. Defaults to False.
		v_lines (bool, optional): Should print column lines. Defaults to True.
		row_sep (str, optional): print character between rows. Defaults to '-'.
		col_sep (str, optional): print character between columns. Defaults to '|'.

	Auxiliary functions:
		- get_col_width_dict(): returns dict, col : width
		- get_max_row_height(): returns max height of each row
	
	NOTE:
		- Let user's pass an alignment function too!??, can be dict of keys & alignment. This will be helpful for markdown adaptation as well.
	"""
	def p(*args):
		print(*args, sep = '', end = '')
		return

	## Aux functions
	def get_col_width_dict(tbl_info: Table) -> dict:
		"""Returns dictionary with width for each column.
		
		Aux functions:
			- get_col_widths(): returns max length for each column.
			- get_width(): returns space used for table or columns
			- get_col_prop_width(): returns proportion for each column
			- print_headers(): prints table headers

		Notes:
			- Checks that combined columns widths are less than terminal size.
			- If greater than terminal size, re-structures widths to be proportional to longest length.
		"""
		## Aux funcs
		def get_col_widths(column: dict, allowed_width: int) -> int:
			"""returns maximum width for each column."""
			max_col_width = len(max( (str(v) for v in column.values()), key = len))
			return max_col_width if max_col_width < allowed_width else allowed_width
		

		def get_width(column_widths: dict, table: bool = False, columns: bool = False) -> int:
			"""Returns int representing the amount of space.
			Two bool args to determine if return table space, or allowed_column spaces.
			"""
			total_col_space = sum(column_widths.values())
			num_cols = len(column_widths.keys())
			non_col_space = (num_cols*2 - 2) * num_spaces + (num_cols-2) * len(col_sep)		# don't include @ far left&right
			if table: 	return total_col_space + non_col_space
			if columns: return total_col_space - non_col_space
			raise Exception()

	
		def get_col_prop_width(col_width: int, num_columns: int) -> int:
			"""Returns new column width for table. Proprortionate to longest entry."""
			if col_width < (allowed_col_width // num_columns):
				return col_width
			return int((col_width / tbl_width) * allowed_col_width)
			

		## get_col_width_dict(tbl_info)
		allowed_width = int(os.get_terminal_size().columns * ALLOWED_TERM_WIDTH)
		column_widths = { k: get_col_widths(tbl_info[k], allowed_width) for k in tbl_info.keys()}
		tbl_width = get_width(column_widths, table=True)

		# print(tbl_width, allowed_width)
		if tbl_width <= allowed_width:
			return column_widths
		
		allowed_col_width = get_width(column_widths, columns= True)
		prop_col_width = {k : get_col_prop_width(v, len(column_widths.keys())) for k, v in column_widths.items()}
		# print(prop_col_width)
		return prop_col_width
	

	def get_row_heights(tbl_info: Table, col_widths: dict) -> dict:
		"""Returns dictionary of maximum height required for each row."""
		def get_max_row_height(row: int) -> int:
			"""Returns max height required for each row."""
			max_height = 1
			for k in tbl_info.keys():
				row_col_len = len(str(tbl_info[k][row]))
				col_len = col_widths[k]

				row_col_height = math.ceil(row_col_len/col_len)
				if row_col_height > max_height:
					max_height = row_col_height
			return max_height
	
		tbl_key = tbl_info[TBL_STRCT_KEY][0]
		return {r: get_max_row_height(r) for r in tbl_info[tbl_key].keys()}
	

	def print_col_sep(col_sep = col_sep):
		"""prints column separators."""
		p(num_spaces * ' ', col_sep, num_spaces * ' ')
		return
		

	def get_headers(tbl_info: dict) -> list:
		"""returns table headers."""
		headers = [k for k in tbl_info.keys()]
		headers.insert(0, '#')
		return headers


	def print_header(tbl_info: dict, col_widths: dict, row_sep: str = '-') -> None:
		"""Prints the table headers."""
		headers = get_headers(tbl_info)
		print(headers)
		ends = (0, len(headers) - 1)

		for i in range(len(headers)):
			if i not in ends:
				print_col_sep()
			h = headers[i]
			p(h, ' ' * col_widths[h] - len(h))

		for h in headers:
			p(row_sep * col_widths[h])

		return None
				


	## print_tbl(tbl_info)
	col_sep = col_sep if v_lines else ''		# to calc col_width
	col_widths: dict = get_col_width_dict(tbl_info)
	col_heights: dict = get_row_heights(tbl_info, col_widths)
	
	print(col_widths)
	print(col_heights)

	print_header(tbl_info, col_widths)



	
	
	
	# def transform_rows(tbl_info: Table, ) -> dict:
	# 	"""Transform values to a dictionary. This way, can print on multiple lines in terminal if required."""
	# 	pass







##########
# Tests
##########

def test_init_tbl() -> bool:
	"""Tests table init working as intended."""
	print_test_header("Initialize table tests")
	keys_results = (
		(['info'], {'info':{}}),
		(['test', 'info'], {'test':{}, 'info':{}}),
		([1,2,3,4,5], {1:{}, 2:{}, 3:{}, 4:{}, 5:{}}),
		([], {}),
	)
	for k, r in keys_results:
		assert init_tbl(k) == r


def test_print_tbl() -> None:
	"""Tests print table."""
	print_test_header("print tables")
	test_dicts = (
		{'a': {1:'asdf', 2:'vcadva'}, 'b':{1:'asdf', 2:1}},
		{'a': {1:1, 2:2}, 'b':{1:3, 2:4}},
		{'a': {1:1, 2:2, 3:3}, 'b':{1:3, 2:'a'*999, 3:3}}
	)
	for test in test_dicts:
		print_tbl(test)


def print_test_header(text: str):
	header = '#' * 10
	spacing = '\n'
	print(spacing, header,spacing, header[0], text,spacing, header, spacing)


##########
# Main
##########

def main():
	test_init_tbl()

	test_print_tbl()


if __name__ == "__main__":
	main()

