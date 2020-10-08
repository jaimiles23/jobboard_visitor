"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 20:13:18
 * @modify date 2020-10-04 20:13:18
 * @desc [
    custom_errors related to printing
 ]
 */
"""

##########
# Imports
##########

import warnings
from dataclasses import dataclass

try:
	from script_objects import Any, Iterator, Union, UserDefinedClass
except:
	from .script_objects import Any, Iterator, Union, UserDefinedClass

##########
# Warnings
##########
@dataclass
class Tblentry_dictWarning(UserWarning):
	"""Class to show warnings about table entries."""
	## Warning keys
	WARN_LEN = 'length'
	WARN_KEYS = 'keys'
	WARN_ATTR = 'class_attr'

	## Messages
	MSG_ITERATOR = "Iterator length did not match Table fields."
	MSG_CLASS = "Class Attributes did not contain all Table fields."
	MSG_DICT = "Dictionary did not contain all Table fields."

	## Field assignment
	MSG_FIELD = '\nFields assigned values as follow:\n'

	##### Init
	"""Uses the warn_type (str) to determine what warning message to call.

	Args:
		entry_dict (Union[dict, Iterator[Any], UserDefinedClass]): information to record.
		tbl_info (dict): table holding information.
		show_values (bool, optional): show value assignment. Defaults to False.
	"""
	warn_type: str
	entry: Union[dict, Iterator[Any], UserDefinedClass]
	entry_dict: dict
	show_values: bool = False

	def __post_init__(self):
		warn_dict = {
			self.WARN_LEN		:	self.MSG_ITERATOR,
			self.WARN_KEYS		:	self.MSG_CLASS,
			self.WARN_ATTR		:	self.MSG_DICT,
		}
		self.msg = warn_dict[self.warn_type]
		self.warn_message()
		

	def warn_message(self):
		"""Shows warning that iterator length does not match keys length.
		
		if show_values, prints value assignment.
		"""
		warning_msg = [self.msg]
		if self.show_values:
			warning_msg += [self.MSG_FIELD]
			for k, v in self.entry_dict.items():
				val_msg = f"\t- {k} : {v}\n"
				warning_msg.append(val_msg)
			warning_msg = ''.join(warning_msg)
		
		warnings.warn(warning_msg)
		# https://pymotw.com/2/warnings/ - use stack to show number of lines to move up.

