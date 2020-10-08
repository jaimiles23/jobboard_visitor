"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-02 17:30:31
 * @modify date 2020-10-02 19:47:18
 * @desc [
    Creates JobSite instances from df_jobsites.
 ]
 */
"""

##########
# Imports
##########

from .constants import (COL_CITY, COL_COUNTRY, COL_DESCRIPT, COL_ID,
                       COL_JOBBOARD, COL_NAME, COL_ORG, COL_QUEUE_PRIORITY,
                       COL_STATE, COL_URLS)
from .jobboard_class import JobBoard
from .script_objects import all_jobboards, DataFrame


##########
# Create instances
##########

def create_jobboard_instances(df: DataFrame) -> all_jobboards:
    """Creates list of All JobSites from df_jobsites

    Args:
        df (DataFrame): Dataframe to create JobSite instances

    Returns:
        all_jobboards: List of all JobSite Instances
    """
    all_jobboards: list = []

    for i in range(len(df)):
        jobsite = JobBoard(
            ident = df.index[i],
            name = df[COL_NAME].iloc[i],
            urls = df[COL_URLS].iloc[i],
            description = df[COL_DESCRIPT].iloc[i],
            Q_priority= df[COL_QUEUE_PRIORITY].iloc[i],
            jobboard = df[COL_JOBBOARD].iloc[i],
            organization = df[COL_JOBBOARD].iloc[i],
            country = df[COL_COUNTRY].iloc[i],
            state = df[COL_STATE].iloc[i],
            city = df[COL_CITY].iloc[i],
        )
        all_jobboards.append(jobsite)
    return all_jobboards






