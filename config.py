from datetime import datetime

CURR_YEAR = datetime.now().year

SEMESTER_DICT = {'Semester 1': '16',
                 'Semester 2': '95',
                 'Semester 3': '134'}

MY_IDC_HOME = 'https://my.idc.ac.il/'

MOODLE_MAIN_PAGE = 'http://moodle.idc.ac.il/{}/my/index.php?lang={}'

COURSE_MAIN_PAGE = 'http://moodle.idc.ac.il/{}/course/view.php?id={}'

COURSE_NEW_ITEMS_PAGE = 'http://moodle.idc.ac.il/{}/blocks/idc_news/full_list.php?courseid={}'