__author__ = 'Yaniv Ranen'

from selenium import webdriver
from time import sleep
import os

class Attenix_Api(object):
    def __init__(self,
                 general_schedule_option_id=None, #you need to have this for your company
                 time_constants={'Weekday': {'start_hour': '9',
                                             'end_hour': '18'},
                                 'Holiday eve': {'start_hour': '9',
                                                 'end_hour': '15'}},
                 user_credentials=[],
                 chrome_home=os.getenv("HOME") + "/Documents/chromedriver"):
        self.general_schedule_option_id = general_schedule_option_id
        self.time_constants = time_constants
        self.user_credentials = user_credentials
        self.chrome_home = chrome_home

    def login_to_attenix(self, driver, credentials):
        elem = driver.find_element_by_class_name('COMBO_SMALL_login')
        elem.send_keys(credentials['user'])
        form_elem = driver.find_element_by_css_selector('form[name="form1"]')
        elem = driver.find_element_by_css_selector('input[name=password]')
        elem.send_keys(credentials['password'])
        driver.find_element_by_css_selector('input[type="submit"]').click()
        return driver

    def number_of_month_days(self, driver):
        # a bit yucky, I know...
        number_of_month_days = 31
        for rownum in range(31, 27, -1):
            try:
                found_element = driver.find_element_by_css_selector('tr[row_no="' + str(rownum) + '"]')
                if found_element:
                    number_of_month_days = rownum
                    break
            except:
                pass
        return number_of_month_days

    def update_hours(self):
        driver = webdriver.Chrome(self.chrome_home)

        for credentials in self.user_credentials:
            print 'Setting the hours for user %s'%(credentials['user'])
            driver.get('https://asp.attenix.co.il')
            self.login_to_attenix(driver, credentials)
            driver.find_element_by_css_selector('div[id=el2]').click()
            driver.find_element_by_css_selector('select#assignments option[value="' + self.general_schedule_option_id +
                                                '"]').click()
            number_of_month_days = self.number_of_month_days(driver)
            self.update_attenix_rows(driver, number_of_month_days)
            driver.find_element_by_id('save_btn').click()
            driver.find_element_by_css_selector('div[id=el6]').click()

        driver.close()

    def update_attenix_rows(self, driver, number_of_month_days):
        for rownum in range(number_of_month_days):
            row_elem = driver.find_element_by_css_selector('tr[row_no="' + str(rownum + 1) + '"]')
            ''' get only weekdays + holiday eve '''
            try:
                row_title = row_elem.find_element_by_css_selector(
                    'td[title="Weekday"],td[title="Holiday eve"]').get_attribute('title')
            except:
                row_title = "OffWorkDay"

            if not self.time_constants.get(row_title):
                # Vacation, no need to update anything
                continue
            assignment_cell = row_elem.find_element_by_css_selector('input[valname="jid_' + str(rownum + 1) + '"]')
            if assignment_cell.get_attribute('value') == '':
                assignment_cell.click()
                row_elem.find_element_by_css_selector('input[fieldname="time_start_HH"]'
                                                      ).send_keys(self.time_constants[row_title]['start_hour'])
                row_elem.find_element_by_css_selector('input[fieldname="time_start_MM"]').send_keys('0')
                row_elem.find_element_by_css_selector('input[fieldname="time_end_HH"]'
                                                      ).send_keys(self.time_constants[row_title]['end_hour'])
                row_elem.find_element_by_css_selector('input[fieldname="time_end_MM"]').send_keys('0')

if __name__ == "__main__":
    a = Attenix_Api(general_schedule_option_id='1111', user_credentials=[{'user':'bla.bla', 'password':'blabla', 'user_display_name':'164'}])
    a.update_hours()
