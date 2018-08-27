import pandas as pd
from datetime import datetime
from robobrowser import RoboBrowser
from tabulate import tabulate
import my_creds
import config

PREFERRED_LANG = 'en'  # 'en' or 'he'
CURRENT_SEMESTER = 'Semester 2'  # 'Semester 1', 'Semester 2' or 'Semester 3'


def init_connection(browser):
    """Initializes connection with Moodle website and
       log ins with user credentials
    :param: browser: RoboBrowser object
    """
    browser.open(config.MY_IDC_HOME)
    login_form = browser.get_form(id='auth_form')
    login_form['username'].value = my_creds.USERNAME
    login_form['password'].value = my_creds.PASSWORD
    browser.submit_form(login_form)


def get_courses_codes(browser):
    """
    :param: browser: RoboBrowser object
    :return: Courses codes for current semester
    """

    browser.open('http://moodle.idc.ac.il/2018/my/index.php?lang={}'
                 .format(PREFERRED_LANG))
    semester_form = browser.get_forms()[1]
    semester_form['coc-category'].value = \
        config.SEMESTER_DICT['{}'.format(CURRENT_SEMESTER)]
    all_courses_links = [url.get('href') for url in
                         [link.find('a') for link in browser.select(
                             ".coc-category-{}".format(
                                 config.SEMESTER_DICT[CURRENT_SEMESTER]))]]
    return [code.split('=')[1] for code in all_courses_links]


def get_course_name(code):
    """
    :param code: Course code (string)
    :return: Course name (string)
    """
    browser.open('http://moodle.idc.ac.il/2018/course/view.php?id={}'
                 .format(code))
    return browser.select('.page-header-headings')[0].h1.string


def add_course_new_info(main_df, course_name, num_last_items=3):
    """
    :param main_df: Either an empty dataframe or a dataframe containing previous
               courses information
    :param course_name: String
    :param num_last_items: Number of last items from each course
    :return: Dataframe with num_last_items information
    """
    browser.open('http://moodle.idc.ac.il/{}/blocks/idc_news/'
                 'full_list.php?courseid={}'.format(
                  datetime.now().year, courses_dict[course_name]))
    course_info = pd.read_html(str(browser.find('table')))[0]\
        .head(num_last_items)
    course_info['Course Name'] = course_name
    course_info['View'] = [item.get('href')
                           for item in browser.find('table')
                               .find_all('a')][:num_last_items]
    if len(main_df.index) == 0:  # If the dataframe is empty, initialize it
        main_df = course_info
    else:
        main_df = main_df.append(course_info, ignore_index=True)
    return main_df


if __name__ == '__main__':
    df = pd.DataFrame()
    browser = RoboBrowser(parser='html.parser')
    init_connection(browser=browser)
    course_codes = get_courses_codes(browser=browser)
    courses_dict = dict()

    for code in course_codes:
        courses_dict['{}'.format(get_course_name(code))] = code

    for course in courses_dict:
        df = add_course_new_info(df, course)

    # Sorting the dataframe by date
    df['Time'] = pd.to_datetime(df['Time']).apply(
        lambda x: x.strftime('%d/%m/%Y'))
    df['Time'] = pd.to_datetime(df['Time'])
    df.sort_values(by='Time', ascending=False, inplace=True)

    # Reordering the dataframe
    new_col_order = ['Time', 'Course Name', 'Text', 'Activity',
                     'Action', 'View']
    df = df[new_col_order]
    df.set_index(['Time'], inplace=True)
    print(tabulate(df, headers='keys', tablefmt='psql'))
