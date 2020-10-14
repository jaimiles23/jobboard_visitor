![](https://toonclips.com/600/cartoon-boy-knocking-on-a-door-by-toonaday-6729.jpg)
# Jobboard Visitor

- [Jobboard Visitor](#jobboard-visitor)
  - [Purpose](#purpose)
  - [Motivation](#motivation)
    - [Progressive Careers](#progressive-careers)
    - [Job Searching: The Life Long Adventure](#job-searching-the-life-long-adventure)
    - [Re-visiting Organizations](#re-visiting-organizations)
  - [How to use](#how-to-use)
    - [Clone repo](#clone-repo)
    - [Requirements](#requirements)
    - [Update jobboards](#update-jobboards)
    - [Change Constants](#change-constants)
    - [Batch script](#batch-script)
  - [TODO](#todo)

---

## Purpose
This program facilitates job searching by systematically opening job boards from a priority-based queue. Jobboard queue priority is stored in `jobboard_info.xlsx` with other relevant information.


## Motivation

### Progressive Careers
I initially created this program to accomodate my specific career interests; I want to contribute my interdisciplinary experience in program evaluation and technology to a progressive organization. This means that I am interested in a *progressive data* career where I use data to help others, e.g., data analytics with a non-profit.

It can be challenging to find progressive data jobs on well-established job boards like Indeed, Glassdoor, and Monster.com. Socially-motivated organizations will post their opportunities on their own internal site or various progressive jobboards. For example:
- [Idealist](https://www.idealist.org/)
- [Humentum](https://jobs.humentum.org/)
- [National Non-Profits](https://nationalnonprofits.org/)

 While this hiring strategy makes sense at an organizational level, it creates obstacles for early-mid level career job-seekers who are not yet married to a single career. Job seekers today are normalized to one-stop shop jobboards that accomodate their career interests. I created this program to systematically check progressive jobboards/organizations to help me find "the right one, eventually."

![](https://i.imgur.com/JH9jQki.jpg)


### Job Searching: The Life Long Adventure

Additionally, I want to acknowledge job searching as a life-long adventure. Fewer and fewer people stay with the same organization their whole life. <!-- This is especialy true in technological roles, where it's often encouraged for people to switch jobs every 3-4 years to seek new skills, different responsibilities, and better compensation.  -->As such, any automation pertaining to job searching is likely to pay dividends over time. In later career seeking, I may be interested to automate job searching on a single site, as demonstrated [here](https://realpython.com/beautiful-soup-web-scraper-python/).



### Re-visiting Organizations

Looking for jobs is an enlightening process; it's likely thaht you will discover organizations that don't have a position available for you. For instance, I am interested in monitoring & evaluation positions with USAID. This program can be used to systematically check USAID and other organizations for available career options.


## How to use
This section assume you are using a windows OS.

### Clone repo
This repository can be cloned using the following command:
```
git clone https://github.com/jaimiles23/jobboard_visitor.git
```

### Requirements
This program uses the pandas library to access and modify `jobboard_info.xlsx`.
```
python -m pip install -r requirements.txt
```
I do *not* recommend using a virtual environment for installing requirements. All users should have some version of pandas available on their standard python interpreter.


### Update jobboards
Changing the jobboards visited is easy! Simply update the `jobboard_info.xlsx` file. 

Below are the fields tracked  for each jobboard:
1. `id`: used to track the jobboard in the job_queue
2. `name`: name of the organization
3. `urls`: list of URLs to open for the organization
4. `description`: description of the organization
5. `queue_priority`: the jobboards priority in the job queue. This represents the fraction of the job queue to search for the job
   1. A job with priority 1 will always open
   2. A job with priority 2 will open if in the first half of the queue
   3. A job with priority 3 will open if in the first 3rd of the queue
   4. etc
6. `jobboard`: Boolean if is a jobboard
7. `organization`: Boolean if is a organization to directly apply to
8. `country`: integers representing the country location
9. `state`: integers representing the state(s) 
10. `city`: integers representing the city

*Notes*:
- When updating an existing entry or changing the id, delete the `job_queue.pkl` file to reset the job queue.
- Jobboards will not open if the `MAX_SITES` constant has already been reached.
- URLs are delimited by the new line character (alt + enter in Excel)
- Locations are represented by comma separated integers.
  - integer representations of locations can be found in the `country`, `state`, and `city` worksheets.
- You may safely add other columns without changing the program's functionality. The only required fields are:
  - id, URLs, and queue_priority


### Change Constants
The `constants.py` script contains constants in the script.

**Change the filename**
The first constant to change is the `FILENAME_JOBSITES`, which is located at the top of the script. Replace this string with the absolute path to `jobboard_info.xlsx`. Keep the 'r' prefix to process it as a raw string.

**Change number of jobboards to open**
This script limits the number of jobboards to process with the `MAX_SITES_OPENED` constant. The script will not process more than `MAX_SITES_OPENED` rows in the CSV.

**How to open all jobboards**
To open all jobboards in `jobboard_info.xlsx`, change the `queue_priority` variable of all to `1`, and change `MAX_SITES_OPENED = float('inf')` in `constants.py`


### Batch script
This repository contains a batch file, `jobs.bat`, that can run the program via the windows command line interface. To do so, complete the following 2 steps:
1. Change the file path
2. Modify your system path

**Changing the file path**

Currently, the .bat file reads as follows:
```
@python.exe @python.exe C:\Users\Jai\Documents\github\job_visitor\main.py %* & pause %* & pause
```
Right click the .bat file, click edit, and replace my file path with your own file path. Instructions on copying the file path can be found [here](https://www.howtogeek.com/670447/how-to-copy-the-full-path-of-a-file-on-windows-10/#:~:text=Find%20the%20file%20or%20folder,select%20%E2%80%9CCopy%20As%20Path.%E2%80%9D). 


**Modifying the system path**

To add the .bat file to your system path:
1. Enter the *start* menu
2. Search *Edit environment variables for your account*
3. Select *path* and click *edit*
4. Click *new*
5. Enter the path to the cloned github directory
   1. e.g, C:\Users\Jai\Documents\github\job_visitor
6. Click *OK*

**Use the batch script**

Now, you can type "jobs" into your start menu and run the batch file!

![](https://imgur.com/jwWRIa5.png)


## TODO
- [ ] Create separate file on how to use & create batch script with link to Readme
- [ ] Create MD table of current organizations 
  - [ ] May be interested to explore creating a map with geographic location of these opportunities (US only?)
- [ ] Complete jobboard printing & test with MD print 