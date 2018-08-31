from datetime import datetime

CURR_YEAR = datetime.now().year

SEMESTER_DICT = {'1': '16',   # Semester 1
                 '2': '95',   # Semester 2
                 '3': '134'}  # Semester 3

MY_IDC_HOME = 'https://my.idc.ac.il/'

MOODLE_MAIN_PAGE = 'http://moodle.idc.ac.il/{}/my/index.php?lang={}'  # Year, language

COURSE_MAIN_PAGE = 'http://moodle.idc.ac.il/{}/course/view.php?id={}'  # Year, Course code

COURSE_NEW_ITEMS_PAGE = 'http://moodle.idc.ac.il/{}/blocks/idc_news/full_list.php?courseid={}'  # Course code
