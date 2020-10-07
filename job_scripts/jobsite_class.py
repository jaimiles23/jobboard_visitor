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
    jobsite_queue = JobQueue.load_queue()   # TODO: Change this to a passed arg in open_wbesite()
    # NOTE: NOT CLASS ATTR.
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
    

