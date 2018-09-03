# scroodle
> Moodle scraper for IDC Herzliya. Automatically collects new assignments and information from current semester's courses

Do you find yourself browsing [IDC Moodle](http://moodle.idc.ac.il/2018/my/index.php?lang=en) every couple of hours, every day, clicking through each course and scrolling until the end of time, just to check whether new assignments or announcements are up?

<img src="readme_gif.gif">

No more! :books: 

## What is it?

**scroodle** is a small, easy-to-use Python program that does the 'hard job' for you, so you don't have to! Insert your Moodle username and password, and get all the recent homeworks, announcments and resources from *your* current semester's courses in no time!
What's worse than spending your Friday morning scrolling through Moodle?

## How to install it?
The first two steps are first-time only!

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
