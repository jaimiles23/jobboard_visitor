"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 21:51:25
 * @modify date 2020-10-06 00:02:42
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
    indent = 3 * ' '        # TODO: Make indent a proportion of the window? e.g., 1 - 0.9 // 10?, so prop to window + final spacing?
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
        """Calls Width methods to set width attributes in class."""
        self.add_records_col_width()
        self.set_width_cols_total()
        self.set_non_col_space()
        self.set_final_colwidths_dict()

    def add_records_col_width(self) -> None:
        """Adds records column width to self._width_per_col"""
        widths = self.width_per_col
        widths[self.records_key] = len(str(self.records))
        self.width_per_col = widths

    def set_width_cols_total(self) -> None:
        """Sets total column space used."""
        self.width_cols_total = sum(self.width_per_col.values())
    
    def set_non_col_space(self) -> None:
        """Sets the total table width."""
        self.non_col_space = (       # Don't include end columns
            (self.num_cols * 2 - 2) * self.num_spaces + 
            (self.num_cols - 2) * len(self.col_sep)
        )


    def set_final_colwidths_dict(self) -> dict:
        """Returns dictionary with width for each columns

        Returns:
            dict: {col_name: width}
        
        Aux functions:
            - get_col_prop_width(): returns proportion for each column
            - pad_col_prop_width(): pads proportional width for each column
        """
        def get_col_prop_width(col_width: int, allowed_width: int) -> int:
            """Returns new column width for table. Proprortionate to longest entry.
            
            Note:
                - Cannot just use the columns proportion of the table, because single digit columns
                will receive too small of a width. Instead, must pad columns after.
            """
            prop_width = int(allowed_width // (self.num_cols))
            # print(col_width, tbl_prop, prop_width)
            
            if col_width < prop_width:
                return col_width
            return prop_width

        def pad_col_prop_width(prop_col_width: dict, allowed_width: int) -> dict:
            """Pads the proportional width of columns that are shorter than max length.
            
            1. Get extra padding & Columns to pad
            2. Get proportion of padding per column
            3. Add proportion of extra padding to each column.
            """
            extra_padding = allowed_width - (sum(prop_col_width[k] for k in self.tbl_keys))
            cols_to_pad = [k for k in self.tbl_keys if prop_col_width[k] < self.width_per_col[k]]

            tot_pad_needed = sum((self.width_per_col[k] for k in cols_to_pad))
            for k in cols_to_pad:
                prop_extra_padding = (self.width_per_col[k] / tot_pad_needed) * extra_padding
                prop_col_width[k] += int(prop_extra_padding)

            return prop_col_width


        ## get_col_width_dict(tbl_info)
        allowed_width = os.get_terminal_size().columns * ALLOWED_TERM_WIDTH

        ## TODO: TEST WITH MULTIPLE LONG COLUMNS, THEN DELETE PRINT
        print(allowed_width, self.width_cols_total)
        if self.width_cols_total + self.non_col_space <= allowed_width:
           return
        
        ## Get proportional column widths
        prop_col_width = {k : get_col_prop_width(v, allowed_width) for k, v in self.width_per_col.items()}
        print(prop_col_width)
        prop_col_width = pad_col_prop_width(prop_col_width, allowed_width)
        print(prop_col_width)
        
        print(sum(prop_col_width[k] for k in self.tbl_keys))
        self.width_per_col = prop_col_width

        return


    ##########
    # Printing
    ##########
    def c_print(self, *args) -> None:
        """Custom print w/ no separation/end chars.
        """
        print(*args, sep = '', end = '', flush=True)
    

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
                    if k == self.tbl_keys[-1]:
                        print()
                    else:
                        self.print_col_delim()
                    continue
                
                ## Print val & Spaces
                low, upp = row_records[k][r]     ## Ranges
                val = row_records[k][v][low:upp]
                left = True if k != self.records_key else False
                indent = True if k == self.records_key else False
                self.print_cell(val, k, left, indent)

                if k == self.tbl_keys[-1]:
                    print()
                else:
                    self.print_col_delim()
                    

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
