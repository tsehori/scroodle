import pandas as pd
from robobrowser import RoboBrowser
import my_creds

preferred_lang = 'en'  # Your preferred language


def init_connection():
    browser.open('https://my.idc.ac.il/')
    login_form = browser.get_form(id='auth_form')
    login_form['username'].value = my_creds.USERNAME
    login_form['password'].value = my_creds.PASSWORD
    browser.submit_form(login_form)

    semester_dict = {'Semester 1': '16', 'Semester 2': '95', 'Semester 3': '134'}
    current_semester = 'Semester 1'

    browser.open('http://moodle.idc.ac.il/2018/my/index.php?lang={}'.format(preferred_lang))
    semester_form = browser.get_forms()[1]
    semester_form['coc-category'].value = semester_dict['{}'.format(current_semester)]
    # all_courses_links = [BeautifulSoup(str(div_class)).a for div_class in
    #                      browser.select(".coc-category-{}".format(semester_dict[current_semester]))]
    # all_courses_links = [link.find_all('a')
    #                       for link in browser.select(".coc-category-{}".
    #                       format(semester_dict[current_semester]))]

    all_courses_links = [url.get('href') for url in
                         [link.find('a') for link in browser.select(".coc-category-{}".format(
                         semester_dict[current_semester]))]]

    return [code.split('=')[1] for code in all_courses_links]


def get_course_name(code):
    browser.open('http://moodle.idc.ac.il/2018/course/view.php?id={}'.format(code))
    return browser.select('.page-header-headings')[0].h1.string


def add_course_new_info(df):
    pass


browser = RoboBrowser()
df = pd.DataFrame(index=['Time'], columns=['Course', 'Text', 'Activity', 'Action'])
codes = init_connection()
courses_dict = dict()
for code in codes:
    courses_dict['{}'.format(get_course_name(code))] = code

for course in courses_dict:
    add_course_new_info(df)