# How to use
This file contains instructions on how to re-purpose this repository for your own job search. This section assumes you are using Windows OS.

## Clone repo
This repository can be cloned using the following command:
```
git clone https://github.com/jaimiles23/jobboard_visitor.git
```

## Requirements
This program uses the pandas library to access and modify `jobboard_info.xlsx`.
```
python -m pip install -r requirements.txt
```
<!-- I do *not* recommend using a virtual environment for installing requirements. All users should have some version of pandas available on their standard python interpreter. -->


## Update jobboards
Changing the jobboards visited is easy! Simply update the `jobboard_info.xlsx` file. 

Below are the fields tracked  for each jobboard:
1. `id`: used to track the jobboard in the job_queue
2. `name`: name of the organization
3. `urls`: list of URLs to open for the organization. This is new line delimited. You can enter a new line character with cntrl + enter
4. `description`: description of the organization
5. `queue_priority`: the jobboards priority in the job queue. This represents the fraction of the job queue to search for the job
   1. A job with priority 1 will always open (unless the maximum number of sites has been opened)
   2. A job with priority 2 will open if in the first half of the queue
   3. A job with priority 3 will open if in the first 3rd of the queue
   4. etc
6. `jobboard`: Boolean if is a jobboard. This is used for advanced searches with the keyword: "jobboard"
7. `organization`: Boolean if is a organization. This is used for advanced searches with the keyword "orgs"
8. `country`: integers representing the country location
9. `state`: integers representing the state(s) 
10. `city`: integers representing the city

***Notes***:
- Jobboards will not open if the `MAX_SITES` constant has already been reached.
- URLs are delimited by the new line character (alt + enter in Excel)
- Locations are represented by comma separated integers.
  - integer representations of locations can be found in the `country`, `state`, and `city` worksheets.
- You may safely add other columns without changing the program's functionality.
  - Keep existing columns


## Change Constants
You can change script constant values via the `constants.py` file in the job_scripts directory.

### Change the filenames
Change the 2 FILENAME constants:
- `FILENAME_JOBSITES`
- `FILENAME_MD`

Replace this string with the absolute path in your directory. Reference [Changing the file path](#Changing-the-file-path). Keep the 'r' prefix to process it as a raw string.

### Change number of jobboards to open
This script limits the number of jobboards to process with the `MAX_SITES_TO_OPEN` constant. The script will not process more than `MAX_SITES_TO_OPEN` rows in the CSV.

### How to open all jobboards
To open all jobboards in `jobboard_info.xlsx`, change the `queue_priority` variable of all to `1`, and change `MAX_SITES_TO_OPEN = float('inf')` in `constants.py`


## Batch script
This repository contains a batch file, `jobs.bat`, that can run the program via the windows command line interface. To do so, complete the following 2 steps:
1. Change the file path
2. Modify your system path

### Changing the file path

Currently, the .bat file reads as follows:
```
@python.exe @python.exe C:\Users\Jai\Documents\github\job_visitor\main.py %* & pause %* & pause
```
Right click the .bat file, click edit, and replace my file path with your own file path. Instructions on copying the file path can be found [here](https://www.howtogeek.com/670447/how-to-copy-the-full-path-of-a-file-on-windows-10/#:~:text=Find%20the%20file%20or%20folder,select%20%E2%80%9CCopy%20As%20Path.%E2%80%9D). 


### Modifying the system path

To add the .bat file to your system path:
1. Enter the *start* menu
2. Search *Edit environment variables for your account*
3. Select *path* and click *edit*
4. Click *new*
5. Enter the path to the cloned github directory
   1. e.g, C:\Users\Jai\Documents\github\job_visitor\job_files
6. Click *OK*

### Use the batch script**

Now, you can type "jobs" into your start menu and run the batch file. *Note*: This may be hidden under the collapsed "app" menu on the very first run.

 Alternatively, you can use the 'win' + 'r' shortcut to open the Run Dialog box. This allows you to input alternative options into the script, e.g., only open organization jobboards.
```
jobs orgs
```

![](https://i.imgur.com/GWfXXwk.png)