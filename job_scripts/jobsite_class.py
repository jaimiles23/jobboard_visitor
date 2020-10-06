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
    flag_can_open = True

    print_attr = (
        'ident',
        'name',
        ## ADD ALL OF THESE BELOW
        'flag_opened',
        'sites',
        'queue_index',
        'queue_priority',
        'searched_queue',
    )


    @classmethod
    def print_opened_all_sites(cls) -> None:
        """Prints message that all websites have been opened if flag_can_open

        Changes flag_can_open to false.
        """
        if JobSite.flag_can_open:
            print(f"- Opened {cls.sites_opened} / {cls.max_sites_opened}")
        JobSite.flag_can_open = False
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

        print(f"{JobSite.jobsite_queue=}")
        print(f"{JobSite.used_jobsites=}")


        for index, ident in JobSite.used_jobsites:
            removed = sum(1 if (num < index) else 0 for num in indices_used)
            del JobSite.jobsite_queue[index - removed]
            indices_used.add(index)

            ## Add to end of list
            JobSite.jobsite_queue.append(ident)

        print(f"{JobSite.jobsite_queue=}")
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
                print(f"{num=}")
                int(num)
                return helper(arr, l, r, num)
            except:
                return -1   # delete non int values


        ## Start Cleaning Queue
        if len(JobSite.jobsite_queue) == len(all_jobsites):
            return
        
        ## sort job ids to look through
        jobsite_ids = [jobsite.ident for jobsite in all_jobsites]
        jobsite_ids.sort()
        print(f"{jobsite_ids=}")
        print(f"{JobSite.jobsite_queue=}")

        ## remove unnecessary items from queue
        removed = 0
        for i in range(len(JobSite.jobsite_queue)):
            binsearch_results = bin_search(jobsite_ids, 0, len(jobsite_ids) - 1, JobSite.jobsite_queue[i - removed])
            
            if binsearch_results == -1:
                print(f"- id ({JobSite.jobsite_queue[i - removed]=}) not located - removed")
                del JobSite.jobsite_queue[i - removed]
                removed += 1


        print(f"{jobsite_ids=}")
        print(f"{JobSite.jobsite_queue=}")

        ## update queue indices
        print("- update queue indices.")
        for job in all_jobsites:
            job.queue_index = job.get_queue_index()
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
        queue_priority (int): (1/queue_priority) of queue to search.
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
    queue_priority: int
    jobboard: bool
    organization: bool
    country: str
    state: str
    city: str


    ## Custom methods
    def __post_init__(self):
        """Called at end of __init__ by dataclass."""
        self.queue_index = self.get_queue_index()


    ##########
    # Instance methods
    ##########
    def get_queue_index(self) -> int:
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


    def set_flag_open(self) -> bool:
        """Returns self.flag_open to determine if url should be opened.
        """
        flag_open = (
            (JobSite.max_sites_opened > JobSite.sites_opened) and
            (self.queue_index <= math.ceil(len( JobSite.jobsite_queue) / self.queue_priority))
        )
        if flag_open:
            JobSite.sites_opened += 1
        self.flag_open = flag_open
    

    def open_websites(self) -> None:
        """Opens the website if self.flag_open.
        
        Appends tuple of index & id to used_jobsites to change queue later.
        """
        if JobSite.sites_opened == JobSite.max_sites_opened:
            JobSite.print_opened_all_sites()
            return None
        elif JobSite.sites_opened + len(self.urls) > JobSite.max_sites_opened:
            self.print_exceeds_site_count(flag_open= False)
            return None
        
        for url in self.urls:
            self.set_flag_open()
            self.print_queue_info(self.flag_open)
            if self.flag_open:
                pass
                # webbrowser.open(url)
            
        if self.flag_open:
            JobSite.used_jobsites.append( (self.queue_index, self.ident))
        return None
    

    def print_site_info(self, flag_open: bool, details: str) -> None:
        """Prints information about the website, including if opened & details.

        Args:
            flag_open (bool): Prints if website was opened.
            details (str): Extra details to include
        """
        opened_dict = {
            True    :   "opened",
            False   :   "not opened"
        }
        print(f"""- {self.name} ({self.ident}) 
    {details}
    status: {opened_dict[flag_open]}
    sites opened: {JobSite.sites_opened} / {JobSite.max_sites_opened}""")
        return None
        

    def print_exceeds_site_count(self, flag_open: bool) -> None:
        """Prints message that number of URLs to open exceeds available webpages.

        Args:
            flag_open (bool): if website was opened.
        """
        details = f"\t{len(self.urls)} websites - exceeds {JobSite.max_sites_opened} websites."
        self.print_site_info(flag_open, details)
    

    def print_queue_info(self, flag_open: bool) -> None:
        """Prints information about whether the site was opened or not.

        Args:
            flag_open (bool): if website was opened.
        """
        details = f"Q_index: {self.queue_index}, \
priority_Q: {self.queue_priority}, \
seached first {math.ceil(len( JobSite.jobsite_queue) / self.queue_priority)}"
        self.print_site_info(flag_open, details)
