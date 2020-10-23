"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-02 16:26:36
 * @modify date 2020-10-02 16:55:23
 * @desc [
    Auxiliary function to transform urls column into list data.
 ]
 */
"""

##########
# Imports
##########

import pandas as pd

from . import constants
from .script_objects import DataFrame

##########
# URL as List
##########

def transform_col_to_list_type(df: DataFrame, colname: str = constants.COL_URLS, delimiter: str = constants.DELIMITER_URL) -> DataFrame:
    """Returns dataframe with column transformed to list

    Args:
        df_jobsites (DataFrame): dataframe to transform
        colname (str, optional): name of column to make list data. Defaults to constants.COL_URLS.
        delimiter (str, optional): delimiter to separate into list data. Defaults to constants.DELIMITER_URL

    Returns:
        DataFrame: passed df with colname trasnformed to list
    """
    def get_list(data: str, delimiter: str) -> list:
        """Returns cleaned list from passed data

        Args:
            data (str): passed string data
            delimiter (str): split data at

        Returns:
            list: list containing data, split at delimiter
        """
        data_list = [x.strip().lower() for x in data.split(delimiter)]
        return data_list
        

    df[colname] = [ get_list(df[colname].iloc[i], delimiter) for i in range(len(df[colname]))]
    return df
