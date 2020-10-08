"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-04 21:51:25
 * @modify date 2020-10-07 20:38:12
 * @desc [
    Contains auxiliary methods for table class.

    TODO: 
    - Will need to add other length counting methods for stri/dicts. 
    - May like to create self.c_len() methods for such
    - Integrate aligned list when passing initial keys. cntrl search "left".

    TODO:
    - In the future, create "type" dict for columns. 
        - If the column is int, then automatically format right?
        - if column is float, automatically format on decimal
        - if str, automatically format left.
        - once this is done, can remove special formatting for the records column (only ints).
 ]
 */
"""

##########
# Imports
##########
import os
import math

try:
    from script_objects import Union, Tuple

except ModuleNotFoundError:
    from .script_objects import Union, Tuple

##########
# Auxiliary methods for the TableInfo class
##########

class Aux_TblInfo():
    """Contains aux methods & constants for the TblInfo class."""
    ALLOWED_TERM_WIDTH = 0.70
    indent = int((1 - ALLOWED_TERM_WIDTH) * 10)
    records_key = '#'
    h_line = '-'
    markdown = False
    mdfile = None


    def __init__(self):
        """Attributes are instantiated in TblInfo() class."""
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
    def _set_width_attrs(self,) -> None:
        """Calls Width methods to set width attributes in class."""
        self._add_records_col_width()
        self._set_width_cols_total()
        self._set_non_col_space()
        self._set_final_colwidths_dict()

    def _add_records_col_width(self) -> None:
        """Adds records column width to self._width_per_col"""
        widths = self.width_per_col
        widths[self.records_key] = len(str(self.records))
        self.width_per_col = widths

    def _set_width_cols_total(self) -> None:
        """Sets total column space used."""
        self.width_cols_total = sum(self.width_per_col.values())
    
    def _set_non_col_space(self) -> None:
        """Sets the total table width."""
        self.non_col_space = (       # Don't include end columns
            (self.num_cols * 2 - 2) * self.num_spaces + 
            (self.num_cols - 2) * len(self.col_sep)
        )


    def _set_final_colwidths_dict(self) -> dict:
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
                col_padding =  prop_col_width[k] + int(prop_extra_padding)
                if col_padding > self.width_per_col[k]:
                    col_padding = self.width_per_col[k]     # not longer than needed

                prop_col_width[k] = col_padding

            return prop_col_width


        ## get_col_width_dict() parent
        allowed_width = os.get_terminal_size().columns * self.ALLOWED_TERM_WIDTH
        if self.width_cols_total + self.non_col_space <= allowed_width:
           return
        
        ## Get proportional column widths
        prop_col_width = {k : get_col_prop_width(v, allowed_width) for k, v in self.width_per_col.items()}
        prop_col_width = pad_col_prop_width(prop_col_width, allowed_width)

        self.width_per_col = prop_col_width

        return


    ##########
    # Printing
    ##########
    def _print(self, *args) -> None:
        """Custom print w/ no separation/end chars."""
        if self.markdown:
            self.mdfile.write(*args)
        else:   
            print(*args, sep = '', end = '') 

    
    def _print_col_delim(self) -> None:
        """Prints column delimiters: num_spaces, col_sep, num_spaces
        
        If no col_sep, prints num_spaces."""
        if len(self.col_sep) == 0:
            self._print(self.num_spaces) * ' '
        else:
            self._print(self.num_spaces * ' ', self.col_sep, self.num_spaces * ' ')
    
    def _print_cell(self, val: str, col: str, left: bool = True, indent: bool = False):
        """Print cell contents

        Args:
            val (str): Value in cell
            col (str): Column of printing
            left (bool, optional): Print left aligned. Otherwise right aligned. Defaults to True.
            indent (bool, optional): Print initial indent for row. Defaults to False.
        """
        if indent:
            self._print_indent()
        if left:
            self._print(val)
            self._fill_space(val, col)
        else:
            self._fill_space(val, col)
            self._print(val)


    def _print_indent(self):
        """Prints table indent."""
        self._print(self.indent * ' ')


    def _print_headers(self, custom_func: object = None) -> None:
        """Prints headers. Can pass custom function to call on headers

        Args:
            custom_func (object, optional): Func to format headers. Defaults to None.
        """
        for i in range(len(self.tbl_keys)):
            key = self.tbl_keys[i]
            header = custom_func(key) if custom_func else key

            left = True if i > 0 else False
            indent = True if i == 0 else False
            self._print_cell(header, key, left = left, indent = indent)

            if i == len(self.tbl_keys) - 1:
                self._print('\n')
            else:
                self._print_col_delim()
        return
    

    def _print_horizontal_line(self) -> None:
        """Prints horizontal lines on the table."""
        for k in self.tbl_keys:
            col_width = self.width_per_col[k]

            if k == self.records_key:
                self._print_indent()
            self._print( self.h_line * col_width)

            if k == self.tbl_keys[-1]:
                self._print('\n')
            else:
                self._print_col_delim()
    
    
    def _print_records(self) -> None:
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
                ## If already printed.
                if row_records[k][r] == -1:
                    indent = True if k == self.records_key else False
                    self._print_cell('', k, indent= indent)
                    if k == self.tbl_keys[-1]:
                        self._print('\n')
                    else:
                        self._print_col_delim()
                    continue
                
                ## Print cell
                low, upp = row_records[k][r]     ## Ranges
                val = row_records[k][v][low:upp]
                left = True if k != self.records_key else False
                indent = True if k == self.records_key else False
                self._print_cell(val, k, left, indent)

                if k == self.tbl_keys[-1]:
                    self._print('\n')
                else:
                    self._print_col_delim()
                    
                ## Check done printing
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
            while num_printed != len(self.tbl_keys):
                row_records, num_printed = print_row(row_records, num_printed)
        
        self._print('\n' * 2)
        return None


    ##########
    # Spacing
    ##########
    def _fill_space(self, value: Union[int, str], col: str) -> None:
        """Prints space to fill column according to value length and column length.

        Args:
            value (Union[int, str]): int or string
            col (str): key to length of widths_per_col
        """
        col_len = self.width_per_col[col]
        _fill_space = col_len - len(str(value))
        self._print(' ' * _fill_space)
        return
    

    ##########
    # Markdown
    ##########

    def _markdown_on(self, markdown: bool, md_filename: str):
        """If markdown, sets up markdown attributes."""
        self.markdown = False
        if markdown:
            if not md_filename:
                raise Exception("Must pass `md_filename` to append table to.")
            self.markdown = True
            self.mdfile = open(md_filename, 'a')
        return
    
    def _markdown_off(self, md_filename: str) -> None:
        """If markdown, shutsdown markdown attributes."""
        if not self.markdown: return

        self.markdown = False
        self.mdfile.close()

