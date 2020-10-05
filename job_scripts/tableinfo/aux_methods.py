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
from custom_objects import Table


##########
# Auxiliary methods for the TableInfo class
##########
class TableInfo_AuxMethods():
    def __init__(self):
        self.records = 0
        self.keys = []
        self.num_cols = len(self.keys) + 1   # records column
        self.width_per_col = {}
        

    ##########
    # Width Methods
    ##########
    def set_total_col_space(self) -> None:
        """Sets total column space used."""
        self.width_cols_total = sum(self.width_per_col.values())
    
    def set_total_tbl_width(
        self,
        num_spaces: int,
        col_sep: str,
    ) -> None:
        """Sets the total table width.

        Args:
            num_spaces (int): number of spaces b/w tbl sep
            col_sep (str): char to separate columns
        """
        non_col_space = (       # Don't include end columns.
            (self.num_cols * 2 - 2) * num_spaces + 
            (self.num_cols - 2) * len(col_sep)
        )
        self.width_tbl_total

    def get_width(
        self, 
        num_spaces: int, 
        col_sep: str,
        total_table: bool = False,
        ) -> int:
        """Returns int representing the width of either the (total table, or the sum of columns)

        Args:
            num_spaces (int): Number of spaces b/w column chars
            col_sep (str): Character separating columns.
            table (bool, optional): Specify return length of entire table. Otherwise, returns length of columns.

        Returns:
            int: Length of table or columns.
        """
        non_col_space = (       # Don't include end columns.
            (self.num_cols * 2 - 2) * num_spaces + 
            (self.num_cols - 2) * len(col_sep)
        )
        return total_col_space + non_col_space


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
            - get_width(): returns space used for table or columns
            - get_col_prop_width(): returns proportion for each column
        """

        def get_col_prop_width(col_width: int) -> int:
            """Returns new column width for table. Proprortionate to longest entry."""
            EXTRA_WIDTH_ALLOWANCE = 1.5
            if col_width < (allowed_col_width // (self.num_cols * EXTRA_WIDTH_ALLOWANCE)):
                return col_width
            return int((col_width / tbl_width) * allowed_col_width)
        
        
        ## get_col_width_dict(tbl_info)
        allowed_width = int(os.get_terminal_size().columns * ALLOWED_TERM_WIDTH)
        tbl_width = self.get_width(num_spaces, col_sep, total_table=True)
        if tbl_width <= allowed_width:
            return self.width_per_col
        
        ## Get proportional column widths
        allowed_col_width = self.get_width(num_spaces, col_sep, total_table=False)
        prop_col_width = {k : get_col_prop_width(v) for k, v in self.width_per_col.items()}
        return prop_col_width
        
        
    ##########
    # Row Height
    ##########
    def get_row_heights(self, col_widths: dict) -> dict:
        """Returns dictionary of maximum height required for each row.

        Args:
            col_widths (dict): dict of column widths 

        Returns:
            dict: [description]
        """
        def get_max_row_height(row: int) -> int:
            """Returns max height required for each row."""
            max_height = 1
            for k in tbl_info.keys():
                row_col_len = len(str(tbl_info[k][row]))
                col_len = col_widths[k]

                row_col_height = math.ceil(row_col_len/col_len)
                if row_col_height > max_height:
                    max_height = row_col_height
            return max_height

        print(tbl_info[TBL_RECORD_KEY])
        return {r: get_max_row_height(r) for r in tbl_info[TBL_RECORD_KEY]}
