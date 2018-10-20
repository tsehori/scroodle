import pandas as pd
from robobrowser import RoboBrowser
import webbrowser
from tabulate import tabulate
import getpass
from pyfiglet import Figlet
import configparser
import config

# Both are initialized in main, after reading\writing my_creds.ini
CURRENT_SEMESTER = None
PREFERRED_LANG = None
PREFERRED_DISPLAY_FULL_URLS = None


def init_connection(browser, username, password):
    """Initializes connection with Moodle website and
       log ins with given user credentials
    :param: browser: RoboBrowser object
    :param username: The user's given username
    :param password: The user's given password
    """
    browser.open(config.MY_IDC_HOME)
    login_form = browser.get_form(id='auth_form')
    login_form['username'].value = username
    login_form['password'].value = password
    browser.submit_form(login_form)


def get_courses_codes(browser):
    """
    :param: browser: RoboBrowser object
    :return: Courses codes for current semester
    """
    browser.open(config.MOODLE_MAIN_PAGE.format(
        config.CURR_YEAR, PREFERRED_LANG))

    if config.CURR_YEAR < 2018:
        semester_form = browser.get_forms()[1]

        # The following has to be re-checked for 2019; once assignments
        # will be handed, it will be possible to check.
        semester_form['coc-category'].value = \
            config.SEMESTER_DICT[CURRENT_SEMESTER]
        all_courses_links = [url.get('href') for url in
                             [link.find('a') for link in browser.select(
                                 ".coc-category-{}".format(
                                      config.SEMESTER_DICT[CURRENT_SEMESTER]))]]
        return [code_in_link.split('=')[1]
                for code_in_link in all_courses_links]

    # At the moment, the Moodle page for 2019 apparently has no option
    # to choose a semester. This will be reviewed when second semester starts.
    all_courses_links = [url.get('href') for url in
                         [link.find('a') for link in browser.select(
                          "h3") if link.find('a') is not None]]
    return [code_in_link.split('=')[1] for code_in_link in all_courses_links]


def get_course_name(browser, course_code):
    """
    :param course_code: Course code (string)
    :return: Course name (string)
    """
    browser.open(config.COURSE_MAIN_PAGE.format(config.CURR_YEAR, course_code))
    return browser.select('.page-header-headings')[0].h1.string


def add_course_new_info(browser, main_df, course_name, courses_dict,
                        num_last_items=3):
    """
    :param main_df: Either an empty dataframe or a
           dataframe containing previous courses information
    :param course_name: String
    :param num_last_items: Number of last items from each course
    :return: Dataframe with num_last_items information
    """
    browser.open(config.COURSE_NEW_ITEMS_PAGE.format(
                  config.CURR_YEAR, courses_dict[course_name]))
    try:
        course_info = pd.read_html(str(browser.find('table')))[0] \
            .head(num_last_items)
    except ValueError:
        return pd.DataFrame()
    course_info['Course Name'] = course_name
    course_info['View'] = [a_tag.get('href')
                           for a_tag in browser.find('table')
                                .find_all('a')][:num_last_items]
    if len(main_df.index) == 0:  # If the dataframe is empty, initialize it
        main_df = course_info
    else:
        main_df = main_df.append(course_info, ignore_index=True)
    return main_df


def ask_for_username(creds_parser):
    """
    :param creds_parser: Configparser object from main program
    :return: Returns the username as entered by user and the possibly-
             modified configparser object
    """
    username = input('Type username (usually in the'
                     ' format firstname.lastname): ')
    save_flag = input('Should we save your '
                      'username for next time? y\\n: ') == 'y'
    if save_flag:
        print('Your username is being saved in file my_creds.ini.')
        creds_parser['CREDENTIALS'] = {}
        creds_parser['CREDENTIALS']['USERNAME'] = username
    return username, creds_parser


def download_requested_items(links_series, num_requested):
    """
    :param links_series: Pandas series of just the links
    :param num_requested: How many links requested
    """

    # links_series.iteritems() returns a zip object of (index, link). This
    #  is casted to a list, so we can used list slicing.
    for index, row in list(links_series.iteritems())[:num_requested]:
        webbrowser.open(row)


def check_legal_input(user_input, input_type):
    """
    :param user_input: Self explanatory
    :param input_type: Either 'lang' for language, 'semester' etc
    :return: The user input is returned as is
    """
    legal_dict = {
        'lang': ['he', 'en'],
        'semester': [str(num) for num in range(1, 4)],
        'urls': ['y', 'n']
    }
    if user_input not in legal_dict[input_type]:
        exit('Illegal input!')
    return user_input


def main():
    try:
        f = Figlet()
        welcome_message = f.renderText('scroodle')
        print(welcome_message + "\nIf you wish to"
                                " exit the program, hit Ctrl+c")

        creds_parser = configparser.ConfigParser()
        first_time_flag = False

        # If the file is empty, it is the first use!
        if creds_parser.read('my_creds.ini') == []:
            first_time_flag = True
            creds_parser['PREFERENCES'] = {}
            creds_parser['PREFERENCES']['LANGUAGE'] = check_legal_input(
                input('What is your preferred language? he\\en: '), 'lang')
            creds_parser['PREFERENCES']['URLS'] = check_legal_input(
                input('Do you want to display a full URL address for each '
                      'item? y\\n: '), 'urls')

            # creds_parser['PREFERENCES']['CURRENT_SEMESTER'] = check_legal_input(
            #     input('What is the current semester? 1\\2\\3: '), 'semester')
            # There is only one semester in 2019 at the moment. Will be changed
            # by second semester.
            creds_parser['PREFERENCES']['CURRENT_SEMESTER'] = 1
            print('Preferred language and current semester'
                  ' are saved in my_creds.ini.')
            username, creds_parser = ask_for_username(creds_parser=creds_parser)

        # If 'CREDENTIALS' section is not in file, then the user asked
        #  the program to not save his username last time
        elif 'CREDENTIALS' not in creds_parser:
            username, creds_parser = ask_for_username(creds_parser=creds_parser)

        # Get username, either from file or input
        else:
            username = creds_parser['CREDENTIALS']['USERNAME']

        global CURRENT_SEMESTER
        global PREFERRED_LANG
        global PREFERRED_DISPLAY_FULL_URLS
        CURRENT_SEMESTER = creds_parser['PREFERENCES']['CURRENT_SEMESTER']
        PREFERRED_LANG = creds_parser['PREFERENCES']['LANGUAGE']
        PREFERRED_DISPLAY_FULL_URLS = creds_parser['PREFERENCES']['URLS']

        # Get user's password
        user_password = getpass.getpass('Password for {}: '.format(username))

        print('Working!')

        # If the username wasn't in file, suggest it
        # if first_time_flag:
        with open('my_creds.ini', 'w') as creds_file:
            creds_parser.write(creds_file)

        df = pd.DataFrame()
        browser = RoboBrowser(parser='html.parser')
        init_connection(browser=browser, username=username,
                        password=user_password)
        course_codes = get_courses_codes(browser=browser)
        courses_dict = dict()

        # Each course has its own unique code
        for code in course_codes:
            courses_dict['{}'.format(get_course_name(browser, code))] = code

        # For each such course, we add its new information to the dataframe
        for course in courses_dict:
            df = add_course_new_info(browser, df, course, courses_dict)

        # Sorting the dataframe by date
        df['Time'] = pd.to_datetime(df['Time']).apply(
            lambda date_index: date_index.strftime('%d/%m/%Y'))
        df['Time'] = pd.to_datetime(df['Time'])
        df.sort_values(by='Time', ascending=False, inplace=True)

        # Reordering the dataframe
        new_col_order = ['Time', 'Course Name', 'Text', 'Activity',
                         'Action', 'View']
        df = df[new_col_order]
        df.set_index(['Time'], inplace=True)
        if PREFERRED_DISPLAY_FULL_URLS == 'y':
            df.drop(['View'], axis=1, inplace=True)
        print(tabulate(df, headers='keys', tablefmt='psql'))

        if input('Should we view the latest updates online? y\\n: ') == 'y':

            # Has to be casted to integer, to be parsed
            # in download_requested_items as slicing index
            num_requested = int(input('How many to view? '
                                      '(from the newest) 1\\2\\3... :\n'
                                      'Note that some will be downloaded!'))
            download_requested_items(links_series=df['View'],
                                     num_requested=num_requested)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
