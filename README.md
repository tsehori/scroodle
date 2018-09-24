# scroodle
> Moodle scraper for IDC Herzliya. Automatically collects new assignments and information from current semester's courses

Do you find yourself browsing [IDC Moodle](http://moodle.idc.ac.il/2018/my/index.php?lang=en) every couple of hours, every day, clicking through each course and scrolling until the end of time, just to check whether new assignments or announcements are up?

<img src="readme_gif.gif">

No more! :books: 

## What is it?

**scroodle** is a small, easy-to-use Python program that does the 'hard job' for you, so you don't have to! Insert your Moodle username and password, and get all the recent homeworks, announcments and resources from *your* current semester's courses in no time!
What's worse than spending your Friday morning scrolling through Moodle?

## How to install it?

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

## A new file named my_crdeds.ini was created! Help!!
Not to worry; this file saves your preferences, such as desired language and semester, and your username, shall you want it. In the next time the program runs, it won't have to ask for these details.
In case you don't want these detailes to be saved -- just delete the file. :innocent:

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Technical overview
In this section, I will try to brifely address the code's in-and-out.
- We start by initializing a [ConfigParser](https://docs.python.org/3/library/configparser.html) for my_creds.ini, and we try reading it.
If this file doesn't exist, we create it and ask the user for his desired language and current semester. Those are saved automatically in my_creds.ini.
- The user is asked for a username. It can be either saved or not saved in my_creds.ini; it's up to the user.
- The password is asked. It is not saved.
- We initialize a connection with the browser using [RoboBrowser](https://github.com/jmcarp/robobrowser), and in the function init_connection, we log into the user's Moodle. We also create a [dataframe](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html#pandas-dataframe).
- In the fucntion get_courses_codes, we get the current's semester course codes (sort of unique IDs), used later to browse to their corresponding webpages.
- For each course, using the function add_course_new_info, we fetch all the course's new information using RoboBrowser. You may notice that those web-scraping parts are kind of similar to [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/); you are right. RoboBrowser is built upon it, and in many cases they have identical syntax.
- We now have a dataframe containing all the information. We can print it out!
- If the user wants to view\download some of the new information, he can do it. In function download_requested_items, we use Python's convinient [webbrowser](https://docs.python.org/2/library/webbrowser.html) to open the browser and access the links.
