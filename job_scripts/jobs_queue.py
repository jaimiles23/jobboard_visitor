"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-09-29 20:37:50
 * @modify date 2020-10-06 17:03:43
 * @desc [
    Class that contains pickle support methods for jobs
 ]
 */
"""

##########
# Imports 
##########

import pickle

from . import constants
from .script_objects import JobIDs, List, Tuple, All_JobSites


##########
# Pickle class 
##########

class JobQueue(object):
    """Methods to load & save the job queue."""
    ##########
    # Constants
    ##########
    filename_pickle = constants.FILENAME_PICKLE

    ##########
    # Init
    ##########
    def __init__(self, all_jobsites: All_JobSites):
        self.job_queue = self.load_queue( all_jobsites)


    ##########
    # Load Queue
    ##########
    def load_queue(self, all_jobsites: All_JobSites) -> object:
        """Loads pickle file

        Returns:
            object: returns pickle file, dict
        """
        try: 
            saved_job_queue = pickle.load( open(self.filename_pickle, 'rb'))  
        except:
            saved_job_queue = list()
        
        return self.clean_queue(saved_job_queue, all_jobsites)


    def clean_queue(self, job_queue: list, all_jobsites: All_JobSites) -> None:
        """Cleans job queue of objects that match instantiated JobSites.

        Args:
            job_queue (list): Job queue
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
        if len(job_queue) == len(all_jobsites):
            return
        

        print("- Cleaning queue of non-existent jobs")
        ## Sort job ids to look through
        jobsite_ids = [jobsite.ident for jobsite in all_jobsites]
        jobsite_ids.sort()

        ## Remove unnecessary items from queue
        removed = 0
        for i in range(len(job_queue)):
            binsearch_results = bin_search(jobsite_ids, 0, len(jobsite_ids) - 1, job_queue[i - removed])
            if binsearch_results == -1:
                print(f"\t- id ({job_queue[i - removed]=}) not located - removed")
                del job_queue[i - removed]
                removed += 1

        ## Update queue indices
        for job in all_jobsites:
            job.Q_index = job.get_Q_index()
        print("- Updated queue.")
        return


    ##########
    # Save Job Queue
    ##########
    def save_queue(self, used_jobs: List[Tuple[int, int]]) -> None:
        """Saves dictionary to pickle file.
        """
        new_job_queue = JobQueue.get_new_queue(self.job_queue, used_jobs)

        pickle.dump( new_job_queue, open(self.filename_pickle, 'wb'))
        return

    @staticmethod
    def get_new_queue(
        job_queue: list,
        used_jobs: List[Tuple[int, int]],
        ) -> JobIDs:
        """Returns new queue to save in pickle file.

        Returns:
            JobIDs: representing queue of jobsite IDs
        """
        indices_used = set()
        for index, ident in used_jobs:
            removed = sum(1 if (num < index) else 0 for num in indices_used)
            del job_queue[index - removed]
            indices_used.add(index)

            job_queue.append(ident)
        return job_queue


    

