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

import sys
import pandas as pd

from job_scripts import (constants, custom_errors, df_methods,
                         jobboard_instances, locations)
from job_scripts.queue_methods import QueueMethods
from job_scripts.jobboard_class import JobBoard
from job_scripts.tableinfo import TableInfo
from job_scripts.script_objects import Tuple


##########
# Main
##########

def main():
    """
    Opens jobsite URLS.
        1. Manage jobboard attr options
		2. Load and clean jobsite jobsite data frame
		3. Creates jobsite instances from dataframe
        4. Opens jobsites
        5. Save new job queue
	"""
    ##### System Arguments
    """
    Allows users to pass options through the Run Dialog box (win + r).
        - boards: shows jobboards
        - orgs: shows organizations
    
    NOTE:
    option_jobboardattr = class attr, instance attr
    """
    option_jobboardattr : Tuple[ Tuple[ str, str]] = (
        ("boards", "jobboard"),
        ("orgs", "organization"),
    )
    available_options = [option[0] for option in option_jobboardattr]
    options = {key: True for key in sys.argv if key in available_options}

    if len(options.keys()) > 0:
        for o in available_options:
            if o not in options:
                options[o] = False
    else:
        options = {key: True for key in available_options}
    print(options)
    for k, v in options.items():
        setattr(JobBoard, k, v)


    ##### Steps conducted
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
        jobboard.open_websites(option_jobboardattr)
        tbl.add_entry(jobboard, user_object=True)
    
    markdown = False
    md_filename = r"C:\Users\Jai\Documents\github\job_visitor\test.md"
    tbl.print_info(markdown= markdown, md_filename= md_filename, show_records_col= False)

    JobBoard.print_num_opened_sites()
    
    ## 5
    print(header, steps[5])
    QueueMethods.save_queue( JobBoard.job_queue, JobBoard.used_jobsites)


## Main
if __name__ == "__main__":
    main()

