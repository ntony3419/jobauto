

import model.ChromeBrowser as chrome
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class Controller(object):
    def __init__(self):
        super().__init__()

    def create_wordpress_post(self, posts_list, settings, wordpress_default):
        browser = chrome.ChromeBrowser(settings).browser()
        # open url
        browser.get(settings["HOME_URL"])
        # login if there is a sign in button
        login_btn_exist = browser.find_element_by_class_name("submit").is_displayed()
        if login_btn_exist is True:
            # ask for username and password or use from setting file
            if (settings["WP_USER_NAME"].lower() == "null") | (settings["WP_PASSWORD"].lower() == "null"):
                username_text = input("Enter username: ")
                pass_text = input("Enter password: ")
            else:
                username_text = settings["WP_USER_NAME"]
                pass_text = settings["WP_PASSWORD"]

            # paste to login fields
            if (username_text is not None) & (pass_text is not None):
                self.send_text(browser, 1, 10, None, "(//*[@id='user_login'])[2]", username_text)
                self.send_text(browser, 1, 10, None, "//*[@id='login_password']", pass_text)
                self.click_btn(browser, 10, 1, None, "//*[@id='loginform']/p[5]/input[1]")

        # open the wordpress admin page
        browser.get("https://www.singapurajobs.com/wp-admin/")
        ''' go through each wordpress post and create draft post'''
        for post in posts_list:
            self.add_post_data_to_wordpress(post, browser, wordpress_default)
        # all the drafts are created
        #browser.close() #close chrome Tab
        browser.quit() #close chrome Window

    def add_post_data_to_wordpress(self, post, browser, wordpress_default):
        # create the new post
        browser.get("https://www.singapurajobs.com/wp-admin/post-new.php?post_type=job_listing")
        ''' set the status'''
        self.set_status(post,browser)
        ''' add publish date data'''
        self.set_publish_data(post, browser)
        ''' add job title '''
        self.send_text(browser, 10, 1, None, "//input[@id='title']", post.get_post_title())  # minute
        '''select post type (Jobs or Posts)'''
        self.set_post_type(post,browser)
        ''' add job detail '''
        self.set_post_detail(post, browser)
        ''' set company '''
        self.set_job_company(post, browser)
        ''' select category'''
        self.set_category(post, browser, wordpress_default)
        ''' set location '''
        self.set_location(post, browser)
        ''' set feature image - no need'''

        # TODO: modify this part to add feature image ( sending image failed)
        ''' self.click_btn(browser, 10, 1, None, "//a[contains(@title, 'Set featured image')]") 
            select_image = browser.find_element_by_xpath("//a[@id='__wp-uploader-id-4']") #select image button
            select_image.send_keys(r"") 
        '''
        ''' set author '''
        self.set_author(post,browser,wordpress_default)
        ''' set job_type'''
        self.set_job_type(post,browser,wordpress_default)
        ''' set salary '''
        self.set_salary(post,browser,wordpress_default)


        '''Final step click publish button '''
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//input[contains(@id, 'publish') and contains(@type,'submit')]")).perform()
        self.click_btn(browser, 10, 1, None, "//input[contains(@id, 'publish') and contains(@type,'submit')]")  # click
        sleep(5)  # wait for the post to be added to database

    def send_text(self, driver, wait_time, frequence, list_error_to_ignored, input_xpath, post):
        default_exception_to_ignore = [ElementNotSelectableException, ElementNotInteractableException,
                                       ElementNotVisibleException, NoSuchElementException]
        if list_error_to_ignored is None:
            list_error_to_ignored = default_exception_to_ignore
        try:
            WebDriverWait(driver, wait_time, poll_frequency=frequence, ignored_exceptions=list_error_to_ignored) \
                .until(EC.presence_of_element_located((By.XPATH, input_xpath))) \
                .send_keys(post)
        # //*[@id=’mount_0_0‘]/div/div[1]/div/div[4
        except Exception:
            print(f'error in send_text function {traceback.format_exc()}')

    def click_btn(self, driver, wait_time, frequence, list_error_to_ignored, input_xpath):
        default_exception_to_ignore = [ElementNotSelectableException, ElementNotInteractableException,
                                       ElementNotVisibleException, NoSuchElementException]
        if list_error_to_ignored is None:
            list_error_to_ignored = default_exception_to_ignore
        try:
            clickable_btn = WebDriverWait(driver, wait_time, poll_frequency=frequence,
                                          ignored_exceptions=list_error_to_ignored) \
                .until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            clickable_btn.click()
        except Exception:
            print(f'error in clickable_btn function {traceback.format_exc()}')


    def set_publish_data(self, post, browser):
        self.click_btn(browser, 10, 1, None, "//div/a[contains(@href, '#edit_timestamp')][1]")  # click edit button
        # select the month
        self.click_btn(browser, 10, 1, None,
                       f"//select[@id='mm']/option[{post.get_publish_date().month}]")  # select month  from list
        # add day
        # click into the day box, delete old value
        self.click_btn(browser, 10, 1, None, "//input[@id='jj']")  # select month  from list
        # delete all old value,
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()  # perform ctrl A
        self.send_text(browser, 10, 1, None, "//input[@id='jj']", post.get_publish_date().day)  # new value

        # add year
        # click into the year box, delete old value
        self.click_btn(browser, 10, 1, None, "//input[@id='aa']")  # select month  from list
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform()  # perform ctrl A
        self.send_text(browser, 10, 1, None, "//input[@id='aa']", post.get_publish_date().year)
        # add time
        # click into the year box, delete old value
        self.click_btn(browser, 10, 1, None, "//input[@id='hh']")  # select month  from list
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL).perform()  # perform ctrl A
        self.send_text(browser, 10, 1, None, "//input[@id='hh']", "09")  # hour
        # minute
        self.click_btn(browser, 10, 1, None, "//input[@id='mn']")  # select month  from list
        ActionChains(browser).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL).perform()  # perform ctrl A
        self.send_text(browser, 10, 1, None, "//input[@id='mn']", "00")  # minute
        # click ok
        self.click_btn(browser, 10, 1, None, "//p/a[contains(@href,'#edit_timestamp')][1]")  # click ok1 button

    def set_post_type(self, post,browser):
        if post.get_post_type() is None:
            self.click_btn(browser, 10, 1, None, "//div/a[@class='edit-post-type hide-if-no-js']")  # click edit button
            self.click_btn(browser, 10, 1, None, "//select[@id='pts_post_type']/option[4]")  # select post type
            # click ok button
            self.click_btn(browser, 10, 1, None,
                           "//div/a[contains(@class, 'save-post-type hide-if-no-js button')][1]")  # click ok button

    def set_post_detail(self, post, browser):
        # switch to text content tab in job detail box
        self.click_btn(browser, 10, 1, None, "//button[@id='content-html']")  # click the text button
        self.click_btn(browser, 10, 1, None, "//textarea[@id='content']")  # click the detail text box
        ActionChains(browser).send_keys(post.get_post_detail()).perform()  # send the job detail

    def set_location(self, post, browser):
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//input[@id='geolocation-address']")).perform()
        self.click_btn(browser, 10, 1, None, "//input[@id='geolocation-address']")  # click the job location input
        # ActionChains(browser).send_keys(post.get_location()).perform()  # send the job detail
        self.send_text(browser, 10, 1, None, "//input[@id='geolocation-address']", post.get_location())
        self.click_btn(browser, 10, 1, None, "//input[@id='geolocation-load']")  # click find
        # sleep(3) # wait 3 second for location to be located

    def set_job_company(self, post, browser):
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//input[@name='_Company']")).perform()
        self.click_btn(browser, 10, 1, None, "//input[@name='_Company']")  # click the job location input
        #self.send_text(browser, 10, 1, None, "//input[@name='_Company']", post.get_company())
        if post.get_company() is not None:
            ActionChains(browser).send_keys(post.get_company()).perform()  # send the job detail

    def set_author(self,post,browser,wordpress_default):
        # TODO: modify this part to set the author correctly
        # get author from post and compare with wordpres preset author and return index to tick
        index = 1 #default author
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//select[@id='post_author_override']")).perform()
        if post.get_author() is None:

            self.click_btn(browser, 10, 1, None, f"(//select[@id='post_author_override']/option)[{index}]")  # click the tick box
        else:
            self.click_btn(browser, 10, 1, None,
                           f"(//select[@id='post_author_override']/option)[{index}]")  # click the tick box


    def set_category(self,post,browser,wordpress_default):
        # TODO: modify this part to correctly set category
        # get the category from post and compare with the wordpress category and return index to tick new jobs
        index = 1
        self.click_btn(browser, 10, 1, None, f"(//ul[@id='job_catchecklist']//input)[{index}]")  # click the tick box

    def set_salary(self,post,browser,wordpress_default):
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//ul[@id='job_salarychecklist']")).perform()
        # get the salary from post and compare with the salary set up in wordpress_default and return index to tick
        salary_index = 4 #default value index
        # TODO: modify this part to correctly set salary
        self.click_btn(browser, 10, 1, None,
                           f"(//ul[@id='job_salarychecklist']/li/label/input)[{salary_index}]")  # click the tick box

    def set_job_type(self,post,browser,wordpress_default):

        # get the job type from post and compare with the preset wordpress and return corect index to tick
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("(//ul[@id='job_typechecklist'])")).perform()
        index = 1
        #TODO: find the index of job type from wordpress_default and post.get job type
        self.click_btn(browser, 10, 1, None,
                           f"(//ul[@id='job_typechecklist']/li/label/input)[{index}]")  # click the tick box

    def set_status(self,post, broser):
        if post.get_status() is None:
            pass #no need to do any thing here yet