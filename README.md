# Jobboard Visitor
![](https://toonclips.com/600/cartoon-boy-knocking-on-a-door-by-toonaday-6729.jpg)

## About
This program systematically opens job boards from a priority-based queue. Jobboards are stored in `jobboard_info.xlsx` with other relevant information.


## Motivation

### Progressive Careers
I created this program to accomodate my specific career interest to work in a progressive data capacity; I want to use my interdisciplinary experience in research, education, and technology to empower others. However, it can be challenging to find these types of jobs without knowing what jobboards to visit.

There are 2 broad categories of jobboards:
1. **General Jobboards**
   
General Jobboards contain jobs for a wide range of industries and experience levels. These are often household names including: [Indeed](https://www.indeed.com/), [Glassdoor](http://glassdoor.com/), and [Monster](https://www.monster.com/). 

2. **Niche Jobboards**
   
Niche Jobboards focus on a specific industry or specialist. Socially-motivated organizations will post their opportunities on niche, progressive jobboards including: [Idealist](https://www.idealist.org/), [Humentum](https://jobs.humentum.org/), and [National Non-Profits](https://nationalnonprofits.org/).


Posting opportunities on niche jobboards makes sense at an organization level; you are directing your message to a specific demographic of jobseekers. However, this strategy creates obstacles for early-mid level career job-seekers who are interested in various opportunities and fields. [SimplyCareer](http://simplycareer.com/job-site-directory/) maintains a helpful directory of various industry specific jobboards.

However, jobboards like Indeed have normalized job seekers to one-stop shops that accomodate their career interests. I created this program to systematically check various progressive jobboards & organizations to help me find "the right one, eventually."

![](https://i.imgur.com/JH9jQki.jpg)


### Job Searching: The Life Long Adventure

Additionally, I want to acknowledge job searching as a life-long adventure. Fewer and fewer people stay with the same organization their whole life. In fact, many of the opportunities that I am interested in are contract positions. <!-- This is especialy true in technological roles, where it's often encouraged for people to switch jobs every 3-4 years to seek new skills, different responsibilities, and better compensation.  -->As such, any automation pertaining to job searching is likely to pay dividends over time. In later career seeking, I may be interested to automate job searching on a single site, as demonstrated [here](https://realpython.com/beautiful-soup-web-scraper-python/).


### Re-visiting Organizations

Looking for jobs is an enlightening process; it's likely you will fall in love with an organization that doesn't have a position available for you. This script can also be used to periodically revisit organization websites to check for available career opportunities.


## To use
To use this repository, reference the [How to.md](https://github.com/jaimiles23/jobboard_visitor/blob/main/job_files/How%20to.md) file.

_Example Usage_:
![Example usage](https://i.imgur.com/3SkMJkz.jpg)

## TODO
- [ ] Add logic flag so only updated `Jobboards.md` if the job_queue is modified - because new jobs are added to the list.
- [ ] Change script to use PathLib library instead of absolute file paths - this way, new users won't need to change filename constants.
- [ ] Fix geography in **jobboards.xlsx** - Doesn't make sense to store country, state, & city separately.
  - [ ] Create relational table with unique rows containing `country`, `city`, `state`
  - [ ] Update **jobboards.xlsx** with relational table primary ids
  - [ ] Remove `country`, `city`, `state` references from script.
  - [ ] Test
- [ ] Create data visualization of location of jobboard reaches.
  - [ ] e.g., density in California, DC, etc.,

