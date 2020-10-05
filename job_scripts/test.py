""""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-09-29 21:08:40
 * @modify date 2020-09-30 21:25:09
 * @desc [
    Contains job site class to contain job information
 ]
 */
"""

##########
# Imports
##########

import webbrowser
from dataclasses import dataclass
from typing import List

from .jobs_queue import JobQueue

##########
# Jobsite class
##########

@dataclass
class JobSite(object):

    ## Constants
    saved_queue = JobQueue.load_queue()     ## ADD FILENAME TO CONSTANTS
    used_sites = list()

    ## Get next queue
    @classmethod
    def get_new_queue(cls) -> list:
        """Returns new queue to use

        Returns:
            list: new website queue
        
        NOTE: Could use sets, but don't to preserve order. Thus, O(N**2)
        """
        front_of_queue = list()
        for site in JobSite.saved_queue:
            if site not in JobSite.used_sites:
                front_of_queue.append(site)
        
        return front_of_queue + JobSite.used_sites


    ##########
    # Init
    ##########
    def __init__(
        self,
        identification: int,
        name: str,
        urls: List[str],
        description: str,
        queue_priority: int,
        jobboard: bool,
        organization: bool,
        country: str,
        state: str,
        city: str
    ):
        """Initialize instance of JobSites. Uses record info from df_jobsites

        Args:
            id (int): Unique ID
            name (str): Name of
            urls (List[str]): jobsite urls to open
            description (str): Description of organization
            queue_priority (int): (1/queue_priority) of queue to search.
            jobboard (bool): indicates if jobboard
            organization (bool): indicates if a specific org
            country (str): country location
            state (str): state location
            city (str): city location
        """

        self.id = identification
        self.name = name
        self.urls = urls
        self.description = description
        self.queue_priority = 

        self.name = name
        self.urls = urls
        self.description = description
        self.priority = priority

        if not self.check_in_queue():
            self.add_to_queue()

        self.show = self.get_flag_show()

        self.move_to_back_of_queue()
    

    def check_in_queue(self) -> bool:
        """Checks that self.name in queue.
        """
        if self.name in JobSite.saved_queue:
            return True
        return False
    

    def add_to_queue(self) -> None:
        """Adds self.name to queue.
        """
        JobSite.saved_queue.append(self.name)


    def get_flag_show(self) -> bool:
        """Returns self.show.

        Checks if times_opened matches show_x_times self variables.
        """
        flag_show = False
        for i in range( len( JobSite.saved_queue) // self.priority):
            if JobSite.saved_queue[i] == self.name:
                flag_show = True
                return flag_show
        return flag_show
    

    def move_to_back_of_queue(self) -> None:
        """Moves job_site name to back of saved queue if show.
        """
        if self.show:
            JobSite.used_sites.append(self.name)
        return 


    def open_site(self) -> None:
        """Opens the website if self.show."""
        if self.show:
            for url in self.urls:
                webbrowser.open(url)
        return


