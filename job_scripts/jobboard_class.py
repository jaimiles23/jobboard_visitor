"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-09-29 21:08:40
 * @modify date 2020-10-03 19:49:18
 * @desc [
    Contains job site class to contain job information

    TODO:
    - Consider making jobsite class methods inherited from an auxiliary object.
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
from .queue_methods import QueueMethods
from .script_objects import JobIDs, List, Tuple, all_jobboards


##########
# Jobsite class
##########

@dataclass
class JobBoard(object):
    job_queue = QueueMethods.load_queue()
    flag_cleaned_queue = False
    used_jobsites = list()

    MAX_SITES_TO_OPEN = constants.MAX_SITES_TO_OPEN
    sites_opened = 0
    flag_show_opened_max_sites = True

    attrs_to_print = (
        'ident',
        'name',
        'flag_opened',
        'Q_index',
    )
    attrs_for_md = (
        'name_url',
        'description'
    )


    @classmethod
    def print_opened_all_sites(cls) -> None:
        """Prints message that all websites have been opened if flag_show_opened_max_sites

        Changes flag_show_opened_max_sites to false.
        """
        if not JobBoard.flag_show_opened_max_sites:
            print(f"- Opened {cls.sites_opened} / {cls.MAX_SITES_TO_OPEN}")
        JobBoard.flag_show_opened_max_sites = True
        return
    

    @classmethod
    def print_num_opened_sites(cls) -> None:
        """Prints message that opened x sites."""
        message = f"\t- Opened {cls.sites_opened} sites"
        print(message)


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

        ## For markdown
        self.name_url = f"[{self.name}]({self.urls[0]})"
        self.description = self.description.replace("\n", "")
        return


    ##########
    # Instance methods
    ##########
    def get_Q_index(self) -> int:
        """Returns index of jobsite instance in queue. If not in queue, adds to end.

        Returns:
            int: index in job queues
        """
        for i in range(len(self.job_queue)):
            if self.job_queue[i] == self.ident:
                return i
        
        return self.create_new_index()
    

    def create_new_index(self) -> int:
        """Creates new index in job_queue for jobboard.

        Returns:
            int: index of jobboard in queue.
        """
        index = len(self.job_queue)
        self.job_queue.append(self.ident)
        print(f"- Adding {self.name} ({self.ident}) to job queue at index {index}")
        return index


    def set_checked_jobs_in_Q(self, option_jobboardattr: Tuple[ Tuple[ str, str]]) -> None:
        """sets how many items were checks first in queue for this JobBoard."""
        for option_set in option_jobboardattr:  
            c_attr, _ = option_set
            if getattr(self, c_attr) == False:      # if an option is passed, search whole queue.
                self.checked_jobs_in_Q = len( self.job_queue)
                return

        self.checked_jobs_in_Q = math.ceil(len( self.job_queue) / self.Q_priority)
        return


    def set_flag_opened(self, option_jobboardattr: Tuple) -> bool:
        """Returns self.flag_opened to determine if url should be opened.
        """
        flag_opened = True

        for tup in option_jobboardattr:     # check if options were set for opening
            c_attr, i_attr = tup
            if getattr(self, c_attr) == False and getattr(self, i_attr):
                flag_opened = False

        if self.Q_index > self.checked_jobs_in_Q:
            flag_opened = False
        elif JobBoard.MAX_SITES_TO_OPEN < JobBoard.sites_opened + len(self.urls):
            flag_opened = False
            
        if flag_opened:
            JobBoard.sites_opened += len(self.urls)
        self.flag_opened = flag_opened
        return
    

    def open_websites(self, option_jobboardattr: Tuple[ Tuple[ str, str]]) -> None:
        """Opens the website if self.flag_opened. 
        Appends tuple of index & id to used_jobsites to change queue later.

        Args:
            option_jobboardattr (Tuple[ class attr, instance attr): Handles options
        """
        self.set_checked_jobs_in_Q(option_jobboardattr)

        if JobBoard.sites_opened == JobBoard.MAX_SITES_TO_OPEN:
            JobBoard.print_opened_all_sites()
            return
        elif JobBoard.sites_opened + len(self.urls) > JobBoard.MAX_SITES_TO_OPEN:
            self.checked_jobs_in_Q = "too many sites."
            return
        
        self.set_flag_opened(option_jobboardattr)

        if self.flag_opened:
            for url in self.urls: 
                    webbrowser.open(url)
            
        if self.flag_opened:
            JobBoard.used_jobsites.append( (self.Q_index, self.ident))
        return None
    

