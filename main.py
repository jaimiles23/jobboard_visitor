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
from job_scripts import constants


##########
# Main
##########

def main():
    """
    Opens jobsite URLS.
        1. Manage jobboard attr options
		2. Load and clean jobsite jobsite data frame
		3. Creates jobsite instances from dataframe
        4. Sort queue to match jobboards.
        5. Opens jobsites
        6. Save new job queue
	"""
    ##### System Arguments
    """
    Allows users to pass options through the Run Dialog box (win + r).
        - boards: shows jobboards
        - orgs: shows organizations
    
    NOTE:
    option_jobboardattr = class attr, instance attr
    """
    ## Only open boards/orgs
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
    for k, v in options.items():
        setattr(JobBoard, k, v)
    
    
    ##### Steps conducted
    steps = {
        1   :   "Load & Clean Jobboard Dataframe",
        2   :   "Create Jobboard Instances from Dataframe",
        3   :   "Clean QueueMethods",
        4   :   "Sort Jobboards to Match Queue",
        5   :   "Open Jobboards in Queue",
        6   :   "Print results & write to table.",
        7   :   "Save New Job Queue",
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
    all_jobboards = sorted(all_jobboards, key = lambda x: JobBoard.job_queue.index(x.ident))


    ## 5
    print(header, steps[5])

    ## Check if provided numbers of sites to open.
    num_to_open = constants.MAX_SITES_TO_OPEN
    for a in sys.argv:
        try:
            num_to_open = int(a)
        except:
            pass
    JobBoard.MAX_SITES_TO_OPEN = num_to_open


    ## Create Table objects to store attr info
    tbl_print = TableInfo( JobBoard.attrs_to_print)
    tbl_md = TableInfo( JobBoard.attrs_for_md)

    ## Open sites
    for jobboard in all_jobboards:
        jobboard.open_websites(option_jobboardattr)
        tbl_print.add_entry(jobboard, user_object=True)
        tbl_md.add_entry(jobboard, user_object=True)
    

    ## 6
    print(header, steps[6])

    tbl_print.print_info(show_records_col= False)
    JobBoard.print_num_opened_sites()

    tbl_md.print_info(
        markdown= True,
        md_filename= constants.FILENAME_MD
    )
    

    ## 7
    print(header, steps[7])
    QueueMethods.save_queue( JobBoard.job_queue, JobBoard.used_jobsites)


## Main
if __name__ == "__main__":
    main()

