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

from script_objects import Any, Iterator, Union, UserDefinedClass


##########
# Warnings
##########
@dataclass
class TblEntryWarning(UserWarning):
	"""Class to show warnings about table entries."""
	## Warning keys
	WARN_LEN = 'length'
	WARN_KEYS = 'keys'
	WARN_ATTR = 'class_attr'

	## Messages
	MSG_ITERATOR = "Iterator length did not match Table fields."
	MSG_CLASS = "Class Attributes did not contain all Table fields."
	MSG_DICT = "Dictionary did not contain all Table fields."

	##### Init
	"""Uses the warn_type (str) to determine what warning message to call.

	Args:
		entry (Union[dict, Iterator[Any], UserDefinedClass]): information to record.
		tbl_info (dict): table holding information.
		show_values (bool, optional): show value assignment. Defaults to False.
	"""
	warn_type: str
	entry: Union[dict, Iterator[Any], UserDefinedClass]
	show_values: bool = False

	def __post_init__(self):
		warn_dict = {
			self.WARN_LEN		:	self.MSG_ITERATOR,
			self.WARN_KEYS		:	self.MSG_CLASS,
			self.WARN_ATTR		:	self.MSG_DICT,
		}
		self.msg = warn_dict[self.warn_type]
		

	def warn_message(self):
		"""Shows warning that iterator length does not match keys length.
		
		if show_values, prints value assignment.
		"""
		if self.show_values:
			msg_val_assignment = ['\nFields assigned values as follow:']
			for k, v in self.entry:
				val_msg = f"\t- {k} : {v}\n"
				msg_val_assignment.append(val_msg)
			warning_message = ''.join(msg_val_assignment)
		else:
			warning_message = ''
		
		warnings.warn(warning_message)
		# https://pymotw.com/2/warnings/ - use stack to show number of lines to move up.

