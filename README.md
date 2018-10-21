# scroodle
> Moodle scraper for IDC Herzliya. Automatically collects new assignments and information from current semester's courses

Do you find yourself browsing [IDC Moodle](http://moodle.idc.ac.il/2018/my/index.php?lang=en) every couple of hours, every day, clicking through each course and scrolling until the end of time, just to check whether new assignments or announcements are up?

<img src="readme_gif.gif">

No more! :books: 

## Table of contents
 - [Introduction](#introduction)
 - [Installation](#installation)
 - [Usage](#usage)
 - [Techy details](#techy-details)
 - [A new file named my_creds.ini was created! Help!!](#a-new-file-named-my_creds.ini-was-created!-Help!!)
 - [License](#license)
 - [Feedback](#feedback)

## Introduction

**scroodle** is a small, easy-to-use Python program that does the 'hard job' for you, so you don't have to! Insert your Moodle username and password, and get all the recent homeworks, announcments and resources from *your* current semester's courses in no time!
What's worse than spending your Friday morning scrolling through Moodle?

## Installation

Do you like [PyPi](https://pypi.org/)? I've got some good news for you! You can use the package easily using the following command:
```sh
pip install scroodle
```
That is, assuming you have [pip](https://pypi.org/project/pip/) already installed on your machine.
You can check out the project's page on PyPi [here](https://pypi.org/project/scroodle/).

You may also install the package in a different way;
Note that in this case, the first two steps are first-time only!

Clone the git repository to your local machine.
```sh
git clone https://github.com/tsehori/scroodle.git
```

Then, install the dependencies from requirements.txt:
```sh
pip install -r requirements.txt
```

To use the program, make sure that your current directory in the command line is *scroodle*, then:
```sh
python main.py
```
And just follow the program's instructions!

## Usage
After installing scroodle (as described [above](#installation)), go to the folder \scroodle\scroodle, wherever you've downloaded it. *scroodle* doesn't have any system arguments (no [argparser](https://docs.python.org/3/library/argparse.html) integrated in scroodle); you just run `python main.py` (or `python3 main.py`), and scroodle will tell you what to do next!

## Techy details
*scroodle* is my first practical Python project, in which I have incorporated many standard and third-party libraries. *scroodle* was actually built from my own frustration with the existing system, and solved a problem for at least one person I know of (me!).
In this section, I'll try to briefly address and explain the main libraries used in the program, and explain what use do they give for *scroodle*.

 - [*RoboBrowser*](https://github.com/jmcarp/robobrowser), a 3rd party library I've found in GitHub. Essentially, RoboBrowser allows to browse the web without a standalone web browser; it is capable of entering pages, filling forms and submitting them, etc. Furthermore, I think it's best ability is how it incorporates the wonderful library [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/); BS allows for "easy" web scraping, which is useful especially in cases where a website does not have a proper API.

## A new file named my_creds.ini was created! Help!!
Not to worry; this file saves your preferences, such as desired language and semester, and your username, shall you want it. In the next time the program runs, it won't have to ask for these details.
In case you don't want these detailes to be saved -- just delete the file. :innocent:

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Technical overview
Throughout structuring and developing *scroodle*, I have run into some challenges. This is one of my first medium-sized Python project, in which I tried to implement best practices and 'Pythonic' code; using diverse Python libraries (both from the standard library and 3rd party), using virtualenv to create an isolated Python environment, that allowed me to work on scroodle independent from other projects and repositories, etc.

Moreover, during the project, I incorporated some of Git's main functionalities: initializing the git repository and pushing it remotely into GitHub, adding relevant parts to each commit, documenting all commits explicitly, branching, pull requesting, etc.

- We start by initializing a [ConfigParser](https://docs.python.org/3/library/configparser.html) for my_creds.ini, and we try reading it.
If this file doesn't exist, we create it and ask the user for his desired language and current semester. Those are saved automatically in my_creds.ini.
- The user is asked for a username. It can be either saved or not saved in my_creds.ini; it's up to the user.
- The password is asked. It is not saved.
- We initialize a connection with the browser using [RoboBrowser](https://github.com/jmcarp/robobrowser), and in the function init_connection, we log into the user's Moodle. We also create a [dataframe](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas-dataframe).
- In the fucntion get_courses_codes, we get the current's semester course codes (sort of unique IDs), used later to browse to their corresponding webpages.
- For each course, using the function add_course_new_info, we fetch all the course's new information using RoboBrowser. You may notice that those web-scraping parts are kind of similar to [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/); you are right. RoboBrowser is built upon it, and in many cases they have identical syntax.
- We now have a dataframe containing all the information. We can print it out!
- If the user wants to view\download some of the new information, he can do it. In function download_requested_items, we use Python's convinient [webbrowser](https://docs.python.org/2/library/webbrowser.html) to open the browser and access the links.
