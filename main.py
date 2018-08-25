import pandas as pd
from robobrowser import RoboBrowser
import my_creds

preferred_lang = 'en'  # 'en' or 'he'
current_semester = 'Semester 1'

def init_connection():
    browser.open('https://my.idc.ac.il/')
    login_form = browser.get_form(id='auth_form')
    login_form['username'].value = my_creds.USERNAME
    login_form['password'].value = my_creds.PASSWORD
    browser.submit_form(login_form)

    semester_dict = {'Semester 1': '16', 'Semester 2': '95', 'Semester 3': '134'}

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


def add_course_new_info(df, course_name, num_last_items=5):

    browser.open('http://moodle.idc.ac.il/2018/blocks/idc_news/full_list.php?courseid={}'.format(
        courses_dict[course_name]
    ))
    course_info = pd.read_html(str(browser.find('table')))[0].head(num_last_items)
    course_info['Course name'] = course_name
    course_info['View'] = [item.get('href') for item in browser.find('table').find_all('a')][:num_last_items]
    # print(browser.find('table').find_all('a')[0].get('href'))
    if len(df.index) == 0:  # If the dataframe is empty, initialize it
        df = course_info
    else:
        df = df.append(course_info, ignore_index=True)
    return df


df = pd.DataFrame()

browser = RoboBrowser()
codes = init_connection()

courses_dict = dict()
for code in codes:
    courses_dict['{}'.format(get_course_name(code))] = code
# print(courses_dict)

for course in courses_dict:
    df = add_course_new_info(df, course)
df.sort_values(by=['Time'], ascending=False, inplace=True)  # TODO is wrong!
print(df)