"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 20:13:18
 * @modify date 2020-10-04 20:13:18
 * @desc [
    Method to print table information
 ]
 */
"""

##########
# Imports
##########

import math
import os

from constants import ALLOWED_TERM_WIDTH, TBL_RECORD_KEY, TBL_STRCT_KEY
from custom_objects import Any, List, Table


##########
# Print table information
##########

def print_tbl(
	tbl_info: object,
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
	
	NOTE:
		- Let user's pass an alignment function too!??, can be dict of keys & alignment. This will be helpful for markdown adaptation as well.
	"""
	## print_tbl(tbl_info)
	col_sep = col_sep if v_lines else ''		# to calc col_width
	col_widths: dict = get_col_width_dict(tbl_info, num_spaces, col_sep)

	tbl_width: int = get_width(col_widths, num_spaces, col_sep, total_table=True)
	col_heights: dict = get_row_heights(tbl_info, col_widths)
	
	print(col_widths)
	print(col_heights)

	print_header(tbl_info, col_widths, col_sep, num_spaces, row_sep) 


	# def transform_rows(tbl_info: object ) -> dict:
	# 	"""Transform values to a dictionary. This way, can print on multiple lines in terminal if required."""
	# 	pass


##########
# Aux method
##########

def only_print(*args):
		print(*args, sep = '', end = '')
		return




def get_row_heights(tbl_info: object col_widths: dict) -> dict:
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

	print(tbl_info[TBL_RECORD_KEY])
	return {r: get_max_row_height(r) for r in tbl_info[TBL_RECORD_KEY]}


def print_col_sep(col_sep: str, num_spaces: int) -> None:
	""""prints column separators.

	Args:
		col_sep (str): Character used to separate columns
		num_spaces (int): Number of spaces before & after col_sep.
	"""
	only_print(num_spaces * ' ', col_sep, num_spaces * ' ')
	return None
	

def get_headers(tbl_info: dict) -> list:
	"""returns table headers."""
	headers = [k for k in tbl_info.keys() if k != TBL_STRCT_KEY]
	return headers


def print_header(
	tbl_info: dict, 
	col_widths: dict,
	col_sep: str,
	num_spaces: int,
	row_sep: str = '-'
	) -> None:
	"""Prints header table

	Args:
		tbl_info (dict): Table information.
		col_widths (dict): Width of each column.
		col_sep (str): Char separating columns
		num_spaces (int): Num spaces before & after each col_sep
		row_sep (str, optional): Character to separate rows. Defaults to '-'.
	"""
	headers = get_headers(tbl_info)
	print(headers)
	tbl_ends = (0, len(headers) - 1)

	for i in range(len(headers)):
		if i not in tbl_ends:
			print_col_sep(col_sep, num_spaces)
		h = headers[i]
		only_print(h, ' ' * col_widths[h] - len(h))
	return None


##########
# Test
##########

def test_print_tbl() -> None:
	"""Tests print table."""
	test_dicts = (
		{1: {1:1, 2:2}, 2: {1:1, 2:2}, 3: {1:1, 2:2}, 4: {1:1, 2:2}, 5: {1:1, 2:2}, '#': [1, 2], '__keys': [1, 2, 3, 4, 5]},
	)
	for test in test_dicts:
		print_tbl(test)


test_print_tbl()
