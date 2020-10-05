"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-09-29 20:37:50
 * @modify date 2020-10-02 20:47:31
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

##########
# Pickle class 
##########

class JobQueue(object):
    
    ## Constant
    filename_pickle = constants.FILENAME_PICKLE

    ## Pickle Methods
    @classmethod
    def load_queue(cls) -> object:
        """Loads pickle file

        Returns:
            object: returns pickle file, dict
        """
        try: 
            saved_queues = pickle.load( open(cls.filename_pickle, 'rb'))
            
        except:
            saved_queues = list()
        
        return saved_queues


    @classmethod
    def save_queue(cls, queue_new: list) -> None:
        """Saves dictionary to pickle file.
        """
        pickle.dump( queue_new, open(cls.filename_pickle, 'wb'))
        return
