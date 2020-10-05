"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 21:51:25
 * @modify date 2020-10-04 21:51:25
 * @desc [
    Contains auxiliary methods for table class.
 ]
 */
"""

##########
# Imports
##########
import os
from constants import ALLOWED_TERM_WIDTH


##########
# Column widths
##########
class TableInfo_AuxMethods():
    def __init__(self):
        self.__keys = []


    def get_width(
        self, 
        col_widths: dict, 
        num_spaces: int, 
        col_sep: str,
        total_table: bool = False,
        ) -> int:
        """Returns int representing the width of either the (total table, or the sum of columns)

        Args:
            col_widths (dict): Length of columns withs,
            num_spaces (int): Number of spaces b/w column chars
            col_sep (str): Character separating columns.
            table (bool, optional): Specify return length of entire table. Otherwise, returns length of columns.

        Returns:
            int: Length of table or columns.
        """
        total_col_space = sum(col_widths.values())
        num_cols = len(col_widths.keys())
        non_col_space = (num_cols*2 - 2) * num_spaces + (num_cols-2) * len(col_sep)		# don't include @ far left&right
        if total_table:
            return total_col_space + non_col_space
        return total_col_space


    def get_col_widths_dict(
        self,
        num_spaces: int,
        col_sep: str
        ) -> dict:
        """Returns dictionary with width for each columns
        
        Args:
            num_spaces (int): Number of spaces between each column separator
            col_sep (str): Character to separate columns

        Returns:
            dict: {col_name: width}
        
        Aux functions:
            - get_col_widths(): returns max length for each column.
            - get_width(): returns space used for table or columns
            - get_col_prop_width(): returns proportion for each column
        """
        def get_col_widths(self, info: list, allowed_width: int) -> int:
            """returns maximum width for each column."""
            max_col_width = len(max( (str(v) for v in getattr(self, info)), key = len))
            return max_col_width if max_col_width < allowed_width else allowed_width	

        def get_col_prop_width(col_width: int) -> int:
            """Returns new column width for table. Proprortionate to longest entry."""
            EXTRA_WIDTH_ALLOWANCE = 1.5
            if col_width < (allowed_col_width // (num_cols * EXTRA_WIDTH_ALLOWANCE)):
                return col_width
            return int((col_width / tbl_width) * allowed_col_width)
        
        
        ## get_col_width_dict(tbl_info)
        allowed_width = int(os.get_terminal_size().columns * ALLOWED_TERM_WIDTH)
        col_widths = { k: get_col_widths(self, k, allowed_width) for k in self.__keys}
        tbl_width = self.get_width(col_widths, num_spaces, col_sep, total_table=True)

        # print(tbl_width, allowed_width)
        if tbl_width <= allowed_width:
            return col_widths
        
        allowed_col_width = self.get_width(col_widths, num_spaces, col_sep, total_table=False)
        num_cols = len(col_widths.keys())
        prop_col_width = {k : get_col_prop_width(v) for k, v in col_widths.items()}
        return prop_col_width
        
        
##########
# Row Height
##########
        