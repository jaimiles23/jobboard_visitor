"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 20:15:35
 * @modify date 2020-10-04 20:15:35
 * @desc [
    Tests for printing functions
 ]
 */
"""

##########
# Imports
##########

from add_entry import add_tbl_entry
from init_table import init_tbl
from print_tbl import print_tbl


##########
# Tests
##########

def test_init_tbl() -> bool:
	"""Tests table init working as intended."""
	print_test_header("Initialize table tests")
	keys_results = (
		(
			['info'], 
			{'info': {}, '#': [], 'keys': ['info']}
			),
		(
			['test', 'info'],
			{'test': {}, 'info': {}, '#': [], 'keys': ['test', 'info']}
		),
		(
			[1,2,3,4,5],
			{1: {}, 2: {}, 3: {}, 4: {}, 5: {}, '#': [], 'keys': [1, 2, 3, 4, 5]}
		),
		(
			[],
			{'#': [], 'keys': []}
		)
	)
	for k, r in keys_results:
		try:
			assert init_tbl(k) == r
		except:
			print( init_tbl(k), r)
			raise Exception()
	print('done')


def test_print_tbl() -> None:
	"""Tests print table."""
	print_test_header("print tables")
	test_dicts = (
		{1: {1:1, 2:2}, 2: {1:1, 2:2}, 3: {1:1, 2:2}, 4: {1:1, 2:2}, 5: {1:1, 2:2}, '#': [1, 2], 'keys': [1, 2, 3, 4, 5]},
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
	# test_init_tbl()

	test_print_tbl()


if __name__ == "__main__":
	main()

