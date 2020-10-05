"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-10-02 15:25:27
 * @modify date 2020-10-02 15:25:27
 * @desc [
    Script constants
 ]
 */
"""
##########
# CSV INFO
##########

FILENAME_JOBSITES = r"C:\Users\Jai\Documents\github\job_visitor\jobboard_info.xlsx"
SHEETNAMES = (
	"job_sites",
	"country",
	"state",
	"city"
)

DELIMITER_LOC = ','
DELIMITER_URL = '\n'

##########
# JobSite 
##########
MAX_SITES_OPENED = 8


##########
# Column names
##########

COL_ID = 'id'       # NOTE: This is index column
COL_NAME = 'name'
COL_URLS = "urls"
COL_DESCRIPT = 'description'
COL_QUEUE_PRIORITY = 'queue_priority'
COL_JOBBOARD = 'jobboard'
COL_ORG = 'organization'
COL_COUNTRY = 'country'
COL_STATE = 'state'
COL_CITY = 'city'


##########
# DF & Dict Keys
##########

AUX_DF_KEYS = (
    COL_COUNTRY,
    COL_STATE,
    COL_CITY
)


##########
# PICKLE 
##########

FILENAME_PICKLE = r"C:\Users\Jai\Documents\github\job_visitor\job_queue.pkl"
