"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-09-29 21:08:40
 * @modify date 2020-10-03 19:49:18
 * @desc [
    Contains job site class to contain job information

    TODO:
    - Consider making jobsite class methods inherited from an aux object.
 ]
 */
"""

##########
# Imports
##########

import math
import webbrowser
from dataclasses import dataclass

from . import constants
from .jobs_queue import JobQueue
from .script_objects import JobIDs, List, Tuple, All_JobSites


##########
# Jobsite class
##########

@dataclass
class JobSite(object):

    ## Class vars
    jobsite_queue = JobQueue.load_queue()     
    used_jobsites = list()

    max_sites_opened = constants.MAX_SITES_OPENED
    sites_opened = 0
    flag_show_opened_max_sites = True

    attrs_to_print = (
        'ident',
        'name',
        'flag_opened',
        'num_sites',
        'Q_index',
        # 'Q_priority',
        # 'checked_jobs_in_Q',
    )

    @classmethod
    def print_opened_all_sites(cls) -> None:
        """Prints message that all websites have been opened if flag_show_opened_max_sites

        Changes flag_show_opened_max_sites to false.
        """
        if not JobSite.flag_show_opened_max_sites:
            print(f"- Opened {cls.sites_opened} / {cls.max_sites_opened}")
        JobSite.flag_show_opened_max_sites = True
        return


    @classmethod
    def reset_class_vars(cls) -> Tuple[list, list, int, int]:
        """Resets JobSite constant variables. 

        This accounts for when the script is run in loop during testing.
        """
        JobSite.jobsite_queue = JobQueue.load_queue()
        JobSite.used_jobsites = list()
        JobSite.sites_opened = 0


    @classmethod
    def get_new_queue(cls) -> JobIDs:
        """Returns new queue to use

        Returns:
            JobIDs: representing queue of jobsite IDs

        NOTE:
            - removed calculated w/ set math to change index for O(N) time complexity.
        """
        indices_used = set()
        for index, ident in JobSite.used_jobsites:
            removed = sum(1 if (num < index) else 0 for num in indices_used)
            del JobSite.jobsite_queue[index - removed]
            indices_used.add(index)

            ## Add to end of list
            JobSite.jobsite_queue.append(ident)
        return JobSite.jobsite_queue
    

    @classmethod
    def clean_queue(cls, all_jobsites: All_JobSites) -> None:
        """Cleans job queue of objects that match instantiated JobSites.

        Args:
            all_jobsites (All_JobSites): list of instantiated job sites
        
        Calls auxiliary bin_search function to locate un-used jobsites.
        """
        def bin_search(arr: list, l: int, r: int, num: int) -> int:
            """Binary search in array to locate number

            Args:
                arr (list): items to search
                l (int): left bound
                r (int): right bound
                num (int): num to find

            Returns:
                int: index of num, or -1 if number doesn't exist.
            """
            def helper(arr: list, l: int, r: int, num: int) -> int:
                """Aux recursive function."""
                mid = (l + r) // 2
                if r < l: return -1
                elif arr[mid] == num: return mid
                elif arr[mid] > num: return helper(arr, l, mid - 1, num)
                else: return helper(arr, mid + 1, r, num)
            
            try:
                int(num)
                return helper(arr, l, r, num)
            except:
                return -1   # delete non int values


        ## Start Cleaning Queue
        if len(JobSite.jobsite_queue) == len(all_jobsites):
            return
        
        print("- Cleaning queue of non-existent jobs")
        ## sort job ids to look through
        jobsite_ids = [jobsite.ident for jobsite in all_jobsites]
        jobsite_ids.sort()

        ## remove unnecessary items from queue
        removed = 0
        for i in range(len(JobSite.jobsite_queue)):
            binsearch_results = bin_search(jobsite_ids, 0, len(jobsite_ids) - 1, JobSite.jobsite_queue[i - removed])
            
            if binsearch_results == -1:
                print(f"\t- id ({JobSite.jobsite_queue[i - removed]=}) not located - removed")
                del JobSite.jobsite_queue[i - removed]
                removed += 1

        ## update queue indices
        for job in all_jobsites:
            job.Q_index = job.get_Q_index()
        print("- Updated queue.")
        return 


    ##########
    # Init
    ##########
    """Initialize instance of JobSites. Uses record info from df_jobsites

    Args:
        id (int): Unique ID
        name (str): jobsite name
        urls (List[str]): jobsite urls to open
        description (str): Description of organization
        Q_priority (int): (1/Q_priority) of queue to search.
        jobboard (bool): indicates if jobboard
        organization (bool): indicates if a specific org
        country (str): country location
        state (str): state location
        city (str): city location
    """
    ## Args
    ident : int     # identification
    name: str
    urls: List[str]
    description: str
    Q_priority: int
    jobboard: bool
    organization: bool
    country: str
    state: str
    city: str


    ## Custom methods
    def __post_init__(self):
        """Called at end of __init__ by dataclass."""
        self.Q_index = self.get_Q_index()

        ## Init flags
        self.flag_opened = False
        if isinstance(self.urls, str):
            self.num_sites = 1
        else:
            self.num_sites = len(self.urls)
        return


    ##########
    # Instance methods
    ##########
    def get_Q_index(self) -> int:
        """Returns index of jobsite instance in queue. If not in queue, adds to end.

        Returns:
            int: index in job queues
        """
        for i in range(len( JobSite.jobsite_queue)):
            if JobSite.jobsite_queue[i] == self.ident:
                return i
        
        return self.create_new_index()
    

    def create_new_index(self) -> int:
        """Creates new index in job_queue for jobboard.

        Returns:
            int: index of jobboard in queue.
        """
        index = len(JobSite.jobsite_queue)
        JobSite.jobsite_queue.append(self.ident)
        print(f"- Adding {self.name} ({self.ident}) to job queue at index {index}")
        return index


    def set_checked_jobs_in_Q(self) -> None:
        """sets how many items were checks first in queue for this jobsite."""
        self.checked_jobs_in_Q = math.ceil(len( JobSite.jobsite_queue) / self.Q_priority)
        return


    def set_flag_opened(self) -> bool:
        """Returns self.flag_opened to determine if url should be opened.
        """
        flag_opened = (
            (JobSite.max_sites_opened > JobSite.sites_opened) and
            (self.Q_index <= self.checked_jobs_in_Q)
        )
        if flag_opened:
            JobSite.sites_opened += 1
        self.flag_opened = flag_opened
        return
    

    def open_websites(self) -> None:
        """Opens the website if self.flag_opened.
        
        Appends tuple of index & id to used_jobsites to change queue later.
        """
        self.set_checked_jobs_in_Q()

        if JobSite.sites_opened == JobSite.max_sites_opened:
            JobSite.print_opened_all_sites()
            return
        elif JobSite.sites_opened + len(self.urls) > JobSite.max_sites_opened:
            self.checked_jobs_in_Q = "too many sites."
            return
        
        self.set_flag_opened()

        if self.flag_opened:
            for url in self.urls: 
                pass 
                # webbrowser.open(url)  
                # self.print_queue_info(self.flag_opened)
            
        if self.flag_opened:
            JobSite.used_jobsites.append( (self.Q_index, self.ident))
        return None
    

