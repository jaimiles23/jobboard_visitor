"""
/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 21:25:45
 * @modify date 2020-10-04 21:25:45
 * @desc [
    Contains TableInfo class for storing using information
 ]
 */
 """
##########
# Initialize table
##########

from constants import WARN_ATTR, WARN_KEYS, WARN_LEN, WARN_STACK
from custom_errors import TblEntryWarning
from custom_objects import Any, Iterator, Table, Union, UserDefinedClass

##########
# TableInfo Class
##########

class TableInfo(object):
	"""Custom object to store user information"""

	##########
	# Init
	##########
	def __init__(self, tbl_keys: Union[dict, Iterator[Any]]):
		"""Initializes TableInfo objects with attributes based on TableInfo keys.

		Args:
			tbl_keys (Union[dict, Iterator[Any]]): List of attributes to create
		"""
		if not isinstance(tbl_keys, dict) and not hasattr(tbl_keys, '__iter__'):
			raise Exception("Initialization TableInfo must be type: List, Tuple, or Dictionary.")

		tbl_keys = tbl_keys if hasattr(tbl_keys, '__iter__') else list(tbl_keys.keys())
		self.__keys = tbl_keys
		self.__records = 0

		for k in self.__keys:
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
		"""
		def is_userdefinedclass(cls):
			return str(cls).startswith('<class ')

		## add_entry
		flag_show_warning, warn_type = False, None
		entry_num = self.records + 1
		
		## Convert user defined object to dict
		if is_userdefinedclass(entry):
			attr_dict = {}
			for k in self.__keys:
				try: val = getattr(entry, k)
				except AttributeError: val = None
				finally: attr_dict[k][entry_num] = val

			entry = attr_dict		# Add to tbl_info w/ dict method
			if None in attr_dict.values():
				flag_show_warning, warn_type = True, WARN_ATTR
		
		## Set Table Info from dict
		if isinstance(entry, dict):	
			if entry.keys() != self.__keys:
				flag_show_warning, warn_type = True, WARN_KEYS
			
			for k in self.__keys:
				try: val = entry[k]
				except KeyError: val = None
				finally: 
					tbl_info = getattr(self, k)
					tbl_info.append(val)
					setattr(self, k, tbl_info)
		
		## Set Table Info from list
		elif hasattr(entry, '__iter__'):
			if len(entry) != len(self.__keys):
				flag_show_warning, warn_type = True, WARN_LEN

			for i in range(len(self.__keys)):
				val = entry[i] if i < len(entry) else None
				tbl_info = getattr(self, self.__keys[i])
				tbl_info.append(val)
				setattr(self, k, tbl_info)

		# Show any warnings
		if flag_show_warning:
			TblEntryWarning(
				warn_type= warn_type, entry= entry, tbl_info= tbl_info, show_values= show_warn_vals)
		
		## Increment number of records
		self.__records += 1
		return None


	##########
	# Print information
	##########
	def print_info(
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
		- Uses auxiliary methods in "aux" module.
	"""
	col_sep = col_sep if v_lines else ''




