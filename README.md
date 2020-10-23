# Jobboard Visitor
![](https://toonclips.com/600/cartoon-boy-knocking-on-a-door-by-toonaday-6729.jpg)

## Purpose
This program facilitates job searching by systematically opening job boards from a priority-based queue. Jobboards are stored in `jobboard_info.xlsx` with other relevant information.


## Motivation

### Progressive Careers
I initially created this program to accomodate my specific career interest to work in a progressive data capacity; I want to contribute my interdisciplinary experience in research and technology to empower others. This may entail a career in consulting, program evaluation, or progressive data analytics. It can be challenging to find this interest on well-established job boards like Indeed, Glassdoor, and Monster.com. Socially-motivated organizations will post their opportunities on various progressive jobboards or their own internal site. For example:
- [Idealist](https://www.idealist.org/)
- [Humentum](https://jobs.humentum.org/)
- [National Non-Profits](https://nationalnonprofits.org/)

While this hiring strategy makes sense at an organizational level, it creates obstacles for early-mid level career job-seekers who are not yet married to a single career. Job seekers today are normalized to one-stop shop jobboards that accomodate their career interests. I created this program to systematically check progressive jobboards/organizations to help me find "the right one, eventually."

![](https://i.imgur.com/JH9jQki.jpg)


### Job Searching: The Life Long Adventure

Additionally, I want to acknowledge job searching as a life-long adventure. Fewer and fewer people stay with the same organization their whole life. <!-- This is especialy true in technological roles, where it's often encouraged for people to switch jobs every 3-4 years to seek new skills, different responsibilities, and better compensation.  -->As such, any automation pertaining to job searching is likely to pay dividends over time. In later career seeking, I may be interested to automate job searching on a single site, as demonstrated [here](https://realpython.com/beautiful-soup-web-scraper-python/).


### Re-visiting Organizations

Looking for jobs is an enlightening process; it's likely you will fall in love with an organization that don't have a position available for you. For instance, I am interested in monitoring & evaluation positions with USAID. This program can be used to systematically check USAID and other organizations for available career options.


## To use
To use this repository, reference the [Create Batch File.md](https://github.com/jaimiles23/jobboard_visitor/blob/main/create_batch_file.md) file.


## TODO
- [ ] Fix geography in **jobboards.xlsx** - Doesn't make sense to store country, state, & city separately.
  - [ ] Create relational table with unique rows containing `country`, `city`, `state`
  - [ ] Update **jobboards.xlsx** with relational table primary ids
  - [ ] Remove `country`, `city`, `state` references from script.
  - [ ] Test
- [ ] Create data visualization of location of jobboard reaches.
  - [ ] e.g., density in California, DC, etc.,