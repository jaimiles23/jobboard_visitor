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
                         jobboard_instances, locations)
from job_scripts.queue_methods import QueueMethods
from job_scripts.jobboard_class import JobBoard
from job_scripts.tableinfo import TableInfo


##########
# Main
##########

def main():
    """
    Opens jobsite URLS.
		1. Load and clean jobsite jobsite data frame
		2. Creates jobsite instances from dataframe
        3. Opens jobsites
        4. Save new job queue
	"""
    steps = {
        1   :   "Load & Clean JobSite Dataframe",
        2   :   "Create JobSite Instances from Dataframe",
        3   :   "Clean QueueMethods",
        4   :   "Open JobSites in Queue",
        5   :   "Save New Job Queue"
    }
    header = '>' * 3
    
    ## 1
    print(header, steps[1])
    df_jobsites = df_methods.get_df_jobboards()

    ## 2
    print(header, steps[2])
    all_jobboards = jobboard_instances.create_jobboard_instances(df_jobsites)

    ## 3
    print(header, steps[3])
    JobBoard.job_queue = QueueMethods.clean_queue(JobBoard.job_queue, all_jobboards)

    ## 4
    print(header, steps[4])

    tbl = TableInfo( JobBoard.attrs_to_print)
    for jobboard in all_jobboards:
        jobboard.open_websites()
        tbl.add_entry(jobboard, user_object=True)
    
    markdown = True
    show_records = True
    guess_align = True
    md_filename = 'test.md'
    tbl.print_info(markdown= markdown, md_filename= md_filename, show_records_col= show_records, guess_alignment=guess_align)
    
    ## 5
    print(header, steps[5])
    QueueMethods.save_queue( JobBoard.job_queue, JobBoard.used_jobsites)


## Main
if __name__ == "__main__":
    main()

