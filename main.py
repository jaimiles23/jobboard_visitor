#! python3

"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-09-29 16:00:33
 * @modify date 2020-10-03 17:32:30
 * @desc [
    Contains data for job websites of interest.
 ]
 */
"""


##########
# Imports
##########

import pandas as pd

from job_scripts import (constants, custom_errors, df_methods,
                         jobsite_instances, locations)
from job_scripts.jobs_queue import JobQueue
from job_scripts.jobsite_class import JobSite
from job_scripts.tableinfo import TableInfo


##########
# Main
##########

def main():
    """Opens jobsite URLS.

		1. Load and clean jobsite jobsite data frame
		2. Creates jobsite instances from dataframe
        3. Opens jobsites
        4. Save new job queue
	"""
    steps = {
        1   :   "Load & Clean JobSite Dataframe",
        2   :   "Create JobSite Instances from Dataframe",
        3   :   "Open JobSites in Queue",
        4   :   "Save new job queue"
    }
    header = '#' * 5
    ## 1
    print(header, steps[1])
    df_jobsites = df_methods.get_df_jobsites()

    ## 2
    print(header, steps[2])
    all_jobsites = jobsite_instances.create_jobsite_instances(df_jobsites)

    ## 3
    print(header, steps[3])

    tbl = TableInfo( JobSite.attrs_to_print)
    JobSite.clean_queue(all_jobsites)
    for jobsite in all_jobsites:
        tbl.add_entry(jobsite, user_object=True)
        jobsite.open_websites()
    
    tbl.print_info()
        
    ## 4
    print(header, steps[4])
    JobQueue.save_queue( JobSite.get_new_queue())

    JobSite.reset_class_vars()          # reset for testing purposes


if __name__ == "__main__":
    main()

