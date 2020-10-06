"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 21:51:25
 * @modify date 2020-10-05 16:02:55
 * @desc [
    Contains auxiliary methods for table class.

    NOTE: Will need to add other length counting methods for stri/dicts. 
    May like to create self.c_len() methods for such
 ]
 */
"""

##########
# Imports
##########

import os
import math
from constants import ALLOWED_TERM_WIDTH
from custom_objects import Table, Union


##########
# Auxiliary methods for the TableInfo class
##########
class TableInfo_AuxMethods():
    records_key = '#'

    def __init__(self):
        self.records = 0
        self.keys = []
        self.num_cols = len(self.keys) + 1   # records column
        self.width_per_col = {}

        self.col_sep = '|'
        self.num_spaces = 3


    ##########
    # Width Methods
    ##########
    def set_width_attrs(self,) -> None:
        """Calls Width methods to set width attributes in class.
        """
        self.add_records_col_width()
        self.set_total_col_space()
        self.set_total_tbl_width()
        self.set_final_colwidths_dict()

    def add_records_col_width(self) -> None:
        """Adds records column width to self._width_per_col"""
        widths = self.width_per_col
        widths[self.records_key] = len(str(self.records))
        self.width_per_col = widths

    def set_total_col_space(self) -> None:
        """Sets total column space used."""
        self.width_cols_total = sum(self.width_per_col.values())
    
    def set_total_tbl_width(self) -> None:
        """Sets the total table width."""
        non_col_space = (       # Don't include end columns
            (self.num_cols * 2 - 2) * self.num_spaces + 
            (self.num_cols - 2) * len(self.col_sep)
        )
        self.width_tbl_total = self.width_cols_total + non_col_space


    def set_final_colwidths_dict(self) -> dict:
        """Returns dictionary with width for each columns

        Returns:
            dict: {col_name: width}
        
        Aux functions:
            - get_width(): returns space used for table or columns
            - get_col_prop_width(): returns proportion for each column
        """

        def get_col_prop_width(col_width: int, allowed_width: int) -> int:
            """Returns new column width for table. Proprortionate to longest entry."""
            EXTRA_WIDTH_ALLOWANCE = 1.5
            if col_width < (allowed_width // (self.num_cols * EXTRA_WIDTH_ALLOWANCE)):
                return col_width
            return int((col_width / self.width_tbl_total) * allowed_width)
        
        
        ## get_col_width_dict(tbl_info)
        allowed_width = int(os.get_terminal_size().columns * ALLOWED_TERM_WIDTH)
        if self.width_tbl_total <= allowed_width:
           return
        
        ## Get proportional column widths
        prop_col_width = {k : get_col_prop_width(v, allowed_width) for k, v in self.width_per_col.items()}
        self.width_per_col = prop_col_width
        return
        
        
    ##########
    # Row Height
    ##########
    def set_row_heights(self) -> dict:
        """Returns dictionary of maximum height required for each row.

        Args:
            col_widths (dict): dict of column widths 

        Returns:
            dict: [description]
        """
        def get_max_row_height(row: int) -> int:
            """Returns max height required for each row."""
            max_height = 1
            for k in self.keys:
                cell_len, col_len = len(str(getattr(self, k)[row])), self.width_per_col[k]
                row_col_height = math.ceil(cell_len / col_len)

                if row_col_height > max_height:
                    max_height = row_col_height
            return max_height

        self.row_heights = {r: get_max_row_height(r) for r in range(self.records)}
    

    ##########
    # Printing
    ##########
    def c_print(self, *args) -> None:
        """Custom print w/ no separation/end chars.
        """
        print(args, sep = '', end = '')
    
    def print_col_delim(self) -> None:
        """Prints column delimiters: num_spaces, col_sep, num_spaces
        
        If no col_sep, prints num_spaces.
        """
        if len(self.col_sep) == 0:
            self.c_print(self.num_spaces)
        else:
            self.c_print(self.num_spaces * ' ', self.col_sep, self.num_spaces * ' ')

    def print_headers(self, custom_func: object = None) -> None:
        """Prints headers. Can pass custom function to call on headers

        Args:
            custom_func (object, optional): Func to format headers. Defaults to None.
        """
        for h in ([self.records_key] + self.keys[:-1]):
            header = custom_func(h) if custom_func else h
            self.c_print(header, self.fill_space(h, h))
            self.print_col_delim()
        
        last_col = self.keys[-1]
        header = custom_func(last_col) if custom_func else last_col
        self.c_print(header, self.fill_space(last_col, last_col, newline=True))
        return
        

    ##########
    # Spacing
    ##########
    def fill_space(self, value: Union[int, str], col: str, newline: bool = False) -> None:
        """Prints space to fill column according to value length and column length.

        Args:
            value (Union[int, str]): int or string
            col (str): key to length of widths_per_col
            newline (bool): indicates if should show new line.
        """
        col_len = self.width_per_col[col]
        fill_space = col_len - len(str(value))
        self.c_print(' ' * fill_space)
        if newline: print()
    





