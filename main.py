import requests
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser as rb
import my_creds

preferred_lang = 'en'  # Your preferred language

def init_connection():
    browser = rb()
    browser.open('https://my.idc.ac.il/')
    login_form = browser.get_form(id='auth_form')
    login_form['username'].value = my_creds.USERNAME
    login_form['password'].value = my_creds.PASSWORD
    browser.submit_form(login_form)

    semester_dict = {'Semester 1': '16', 'Semester 2': '95', 'Semester 3': '134'}
    current_semester = 'Semester 2'

    browser.open('http://moodle.idc.ac.il/2018/my/index.php?lang={}'.format(preferred_lang))
    semester_form = browser.get_forms()[1]
    semester_form['coc-category'].value = semester_dict['{}'.format(current_semester)]
    all_courses_links = [BeautifulSoup(str(div_class)).a for div_class in
                         browser.select(".coc-category-{}".format(semester_dict[current_semester]))]

# all_courses_links = [link.find_all('a')
#                      for link in browser.select(".coc-category-{}".format(semester_dict[current_semester]))]

    all_courses_links = [url.get('href') for url in
                         [link.find('a') for link in browser.select(".coc-category-{}".format(
                         semester_dict[current_semester]))]]

    all_courses_codes = [code.split('=')[1] for code in all_courses_links]
    print(all_courses_codes)

init_connection()