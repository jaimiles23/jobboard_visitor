"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 21:51:25
 * @modify date 2020-10-05 16:02:55
 * @desc [
    Contains auxiliary methods for table class.

    NOTE: Will need to add other length counting methods for stri/dicts. 
    May like to create self.c_len() methods for such

    NOTE: integrate aligned list when passing initial keys. cntrl search "left".
 ]
 */
"""

##########
# Imports
##########

import os
import math
from constants import ALLOWED_TERM_WIDTH
from custom_objects import Table, Union, Dict, Tuple


##########
# Auxiliary methods for the TableInfo class
##########
class TableInfo_AuxMethods():
    indent = 3 * ' '
    records_key = '#'
    h_line = '-'


    def __init__(self):
        self.records = 0
        self.keys = []
        self.tbl_keys = self.keys + [self.records_key]

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
    # def set_row_heights(self) -> dict:
    #     """Returns dictionary of maximum height required for each row.

    #     Args:
    #         col_widths (dict): dict of column widths 

    #     Returns:
    #         dict: [description]
    #     """
    #     def get_max_row_height(row: int) -> int:
    #         """Returns max height required for each row."""
    #         max_height = 1
    #         for k in self.keys:
    #             cell_len, col_len = len(str(getattr(self, k)[row])), self.width_per_col[k]
    #             row_col_height = math.ceil(cell_len / col_len)

    #             if row_col_height > max_height:
    #                 max_height = row_col_height
    #         return max_height

    #     self.row_heights = {r: get_max_row_height(r) for r in range(self.records)}
    

    ##########
    # Printing
    ##########
    def c_print(self, *args) -> None:
        """Custom print w/ no separation/end chars.
        """
        print(*args, sep = '', end = '')
    

    def print_col_delim(self) -> None:
        """Prints column delimiters: num_spaces, col_sep, num_spaces
        
        If no col_sep, prints num_spaces.
        """
        if len(self.col_sep) == 0:
            self.c_print(self.num_spaces) * ' '
        else:
            self.c_print(self.num_spaces * ' ', self.col_sep, self.num_spaces * ' ')
    

    def print_cell(self, val: str, col: str, left: bool = True, indent: bool = False):
        """Print cell contents

        Args:
            val (str): Value in cell
            col (str): Column of printing
            left (bool, optional): Print left aligned. Otherwise right aligned. Defaults to True.
            indent (bool, optional): Print initial indent for row. Defaults to False.
        """
        if indent:
            self.print_indent()
        if left:
            self.c_print(val)
            self.fill_space(val, col)
        else:
            self.fill_space(val, col)
            self.c_print(val)


    def print_indent(self):
        """Prints table indent."""
        self.c_print(self.indent)


    def print_headers(self, custom_func: object = None) -> None:
        """Prints headers. Can pass custom function to call on headers

        Args:
            custom_func (object, optional): Func to format headers. Defaults to None.
        """
        for i in range(len(self.tbl_keys)):
            key = self.tbl_keys[i]
            header = custom_func(key) if custom_func else key

            left = True if i > 0 else False
            indent = True if i == 0 else False
            self.print_cell(header, key, left = left, indent = indent)

            if i == len(self.tbl_keys) - 1:
                print()
            else:
                self.print_col_delim()
        return
    

    def print_horizontal_line(self) -> None:
        """Prints horizontal lines on the table."""
        for k in self.tbl_keys:
            col_width = self.width_per_col[k]

            if k == self.records_key:
                self.print_indent()
            self.c_print( self.h_line * col_width)

            if k == self.tbl_keys[-1]:
                print()
            else:
                self.print_col_delim()
    

    def print_records(self) -> None:
        """Prints table records for table.
        
        Aux functions:
            - print_row
        
        Notes:
            - v, r constants for 'values' and 'range'
            - range of -1 indicates finished printing value.
        """
        def print_row(row_records: dict, num_printed: int) -> Tuple[ dict, int]:
            """Prints values for rows without extending outside column."""
            for k in self.tbl_keys:
                ## Already printed
                if row_records[k][r] == -1:
                    indent = True if k == self.records_key else False
                    self.print_cell('', k, indent= indent)
                    self.print_col_delim()
                    continue
                
                ## Print val & Spaces
                low, upp = row_records[k][r]     ## Ranges
                val = row_records[k][v][low:upp]
                left = True if k != self.records_key else False
                indent = True if k == self.records_key else False
                self.print_cell(val, k, left, indent)

                if k != self.tbl_keys[-1]:
                    self.print_col_delim()
                else:
                    print()

                ## Check finished printing
                if upp == len(row_records[k][v]):
                    num_printed += 1
                    row_records[k][r] = -1
                    continue
                
                ## Update range
                low = upp
                if (upp + self.width_per_col[k]) < len(row_records[k][v]):
                    upp = upp + self.width_per_col[k]
                else:
                    upp = len(row_records[k][v])
                row_records[k][r] = (low, upp)
                
            return row_records, num_printed


        ## Main function
        v, r = 'val', 'range'
        for i in range(self.records):
            row_records = {k : {} for k in self.tbl_keys}

            # get records for row
            for k in self.tbl_keys:     
                val = str(i + 1) if (k == self.records_key) else str(getattr(self, k)[i])
                upp = len(val) if len(val) <= self.width_per_col[k] else self.width_per_col[k]
                row_records[k][v], row_records[k][r] = val, (0, upp)
            
            # print row
            num_printed = 0
            while num_printed != len(self.tbl_keys):       # not realllyyyyyy O(N**2)
                row_records, num_printed = print_row(row_records, num_printed)
        return None


    ##########
    # Spacing
    ##########
    def fill_space(self, value: Union[int, str], col: str) -> None:
        """Prints space to fill column according to value length and column length.

        Args:
            value (Union[int, str]): int or string
            col (str): key to length of widths_per_col
        """
        col_len = self.width_per_col[col]
        fill_space = col_len - len(str(value))
        self.c_print(' ' * fill_space)
        return
