"""
/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 21:25:45
 * @modify date 2020-10-05 14:58:33
 * @desc [
    Contains TableInfo class. Stores & Prints information.
 ]
 */
 """
##########
# Initialize table
##########

from aux_methods import TableInfo_AuxMethods
from constants import WARN_ATTR, WARN_KEYS, WARN_LEN, WARN_STACK
from custom_errors import TblEntryWarning
from custom_objects import Any, Iterator, Table, Union, UserDefinedClass


##########
# TableInfo Class
##########

class TableInfo(TableInfo_AuxMethods):
	"""Custom object to store user information"""

	##########
	# Init
	##########
	def __init__(self, tbl_keys: Union[dict, Iterator[Any]]):
		"""Initializes TableInfo objects with attributes based on TableInfo keys.

		Args:
			tbl_keys (Union[dict, Iterator[Any]]): List of attributes to create.
		
		NOTE:
			- In the future, may be interested to explore creating flexible getter/setter
			methods for string-defined attributes?
				- This will simplify the code of appending the value to the list,
				and can include update col_lengths value in this method.
		"""
		if not isinstance(tbl_keys, dict) and not hasattr(tbl_keys, '__iter__'):
			raise Exception("Initialization TableInfo must be type: List, Tuple, or Dictionary.")
		tbl_keys = tbl_keys if hasattr(tbl_keys, '__iter__') else list(tbl_keys.keys())
		
		self.records = 0
		self.keys = tbl_keys
		self.width_per_col = {k:0 for k in tbl_keys}

		for k in self.keys:
			setattr(self, k, list())
		return None
	

	##########
	# Add Entry
	##########
	def add_entry(
		self,
		entry: Union[dict, Iterator[Any], UserDefinedClass],
		show_warning: bool = True,
		show_warn_vals: bool = False
	) -> None:
		"""Adds entry to table class holding information

		Args:
			entry (Union[dict, Iterator[Any], UserDefinedClass]): Info to add to table.
			show_warning (bool, optional): Show warnings when adding entry. Defaults to True.
			show_warn_vals (bool, optional): Show value assignments in warning. Defaults to False.

		Returns:
			Table: Table dictionary with updated entry.
		
		Auxiliary methods:
			- is_userdefinedclass(): returns boolean if object is a user defined class.
			- convert_class_to_dict(): converts class to dict
			- convert_iter_to_dict(): convert iter to dict
		"""
		def is_userdefinedclass(cls):
			return str(cls).startswith('<class ')
		
		def convert_class_to_dict(entry: UserDefinedClass) -> dict:
			attr_dict = {}
			for k in self.keys:
				try: val = getattr(entry, k)
				except AttributeError: val = None
				finally: attr_dict[k] = val
			return attr_dict
		
		def convert_iter_to_dict(entry: Iterator) -> dict:
			iter_dict = {}
			for i in range(len(self.keys)):
				val = entry[i] if i < len(entry) else None
				iter_dict[self.keys[i]] = val
			return iter_dict


		##### add_entry main method()
		flag_show_warning, warn_type = False, None
		
		## Convert user defined object to dict
		if is_userdefinedclass(entry):
			entry_dict = convert_class_to_dict(entry)
			if None in entry.values():
				flag_show_warning, warn_type = True, WARN_ATTR
		
		## Convert Iterable to dict
		elif hasattr(entry, '__iter__'):
			entry_dict = convert_iter_to_dict(entry)
			if len(entry) != len(self.keys):
				flag_show_warning, warn_type = True, WARN_LEN
		
		elif isinstance(entry, dict):
			entry_dict = entry
			if entry.keys() != self.keys:
				flag_show_warning, warn_type = True, WARN_KEYS

		## Add attribute info
		for k in self.keys:
			val = entry_dict.get(k, None)
			tbl_info = getattr(self, k) + [val]
			setattr(self, k, tbl_info)
		
		# Show any warnings
		if flag_show_warning:
			TblEntryWarning(
				warn_type= warn_type, entry= entry, tbl_info= tbl_info, show_values= show_warn_vals)
		
		## Wrap-up
		self.records += 1
		self.update_col_lengths(entry_dict)
		return None
	

	def update_col_lengths(self, entry_dict) -> None:
		"""Updates the column lengths if entry_dict[k] is > than entry.

		Args:
			entry_dict (dict): values to compare to current column lengths.
		"""
		for k in self.keys:
			val = entry_dict.get(k, 0)
			val = val if val else 0
			if val > self.width_per_col[k]:
				self.width_per_col[k] = val
		return None
	

	def add_entries(self, entries: Iterator) -> None:
		"""Calls add_entry() method on list.

		Args:
			entries (Iterator): Iterable of entries to add.
		"""
		for entry in entries:
			self.add_entry(entry)
		return None


	##########
	# Print information
	##########
	def print_info(
		self,
		num_spaces: int = 3,
		row_sep: str = '-',
		col_sep: str = '|', 
		h_lines: bool = False,
		v_lines: bool = False,
		column_alignment: Union[dict, None] = {}
	):
		"""Prints information stored in the table.

		Args:
			num_spaces (int, optional): Number of spaces b/w col separator. Defaults to 3.
			row_sep (str, optional): Char to separate rows. Defaults to '-'.
			col_sep (str, optional): Char to separate cols. Defaults to '|'.
			h_lines (bool, optional): Print lines b/w rows. Defaults to False.
			v_lines (bool, optional): Print lines b/w columns. Defaults to False.
			column_alignment (Union[dict, None], optional): colname: (l,r,c) alignment. Defaults to None.
		
		Note:
			- Uses auxiliary methods in "aux_methods" module.
		"""
		col_sep = col_sep if v_lines else ''
		col_widths: dict = self.get_col_widths_dict(num_spaces, col_sep)
	





##########
# Test
##########

keys = ['a', 'b']
tbl = TableInfo(keys)
print(tbl.__dict__)
tbl.add_entry([1,2])
print(tbl.a, tbl.b)
tbl.add_entry([3,5])
print(tbl.a, tbl.b)

add = [{'a':1, 'b':8}, {'a':2, 'b':20}]
tbl.add_entries(add)
print(tbl.a, tbl.b)
print(tbl.width_per_col)
