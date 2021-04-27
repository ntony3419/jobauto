
import model.ChromeBrowser as chrome
import selenium
import traceback
from selenium import webdriver
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

    def create_wordpress_post(self, posts_list, settings):
        browser = chrome.ChromeBrowser(settings).browser()
        #open url
        browser.get(settings["HOME_URL"])
        #login if there is a sign in button
        login_btn_exist = browser.find_element_by_class_name("submit").is_displayed()
        if login_btn_exist is True:
            # ask for username and password or use from setting file
            username_text = None
            pass_text= None
            if (settings["WP_USER_NAME"].lower() == "null") | (settings["WP_PASSWORD"].lower() == "null"):
                username_text = input("Enter username: ")
                pass_text = input ("Enter password: ")
            else:
                username_text=settings["WP_USER_NAME"]
                pass_text=settings["WP_PASSWORD"]

            # paste to login fields
            if (username_text!=None) & (pass_text != None):
                self.send_text(browser,1,10,None,"(//*[@id='user_login'])[2]",username_text )
                self.send_text(browser, 1, 10, None, "//*[@id='login_password']", pass_text)
                self.click_btn(browser, 10, 1, None, "//*[@id='loginform']/p[5]/input[1]")

        # open the wordpress admin page
        browser.get("https://www.singapurajobs.com/wp-admin/")

        #post
        for item in posts_list:
            #create the new post
            browser.get("https://www.singapurajobs.com/wp-admin/post-new.php")
            for keys,values in posts_list[item].items(): #iterate through each collected item from excel file and add to new post
                split_date =[]
                if keys == "Posted Date":
                    #split_date = values.split("-")
                    #set the publish date
                    self.click_btn(browser, 10, 1, None, "//div/a[contains(@href, '#edit_timestamp')][1]") #click edit button
                    #select the month
                    self.click_btn(browser, 10, 1, None,
                                   f"//select[@id='mm']/option[{values.month}]")  # select month  from list
                    # add day
                    self.send_text(browser, 10, 1, None, "//input[@id='jj']", values.day)
                    # add year
                    self.send_text(browser, 10, 1, None, "//input[@id='aa']", values.year)
                    # add time
                    self.send_text(browser, 10, 1, None, "//input[@id='hh']", "09")  # hour
                    self.send_text(browser, 10, 1, None, "//input[@id='mn']", "00")  # minute
                    #click ok
                    self.click_btn(browser, 10, 1, None,"//p/a[contains(@href,'#edit_timestamp')][1]")  # click edit button

                    # self.click_btn(browser, 10, 1, None,f"//select[@id='mm']/option[{split_date[1]}]" ) #select month  from list
                    # # add day
                    # self.send_text(browser, 10,1,None,"//input[@id='jj']", split_date[2])
                    # #add year
                    # self.send_text(browser, 10, 1, None, "//input[@id='aa']", split_date[0])
                    # #add time
                    # self.send_text(browser, 10, 1, None, "//input[@id='hh']", "09") #hour
                    # self.send_text(browser, 10, 1, None, "//input[@id='mn']", "00") #minute

                #add post title
                if keys == "JOB TITLE":
                    self.send_text(browser, 10, 1, None, "//input[@name='post_title']", values)  # minute

                #select post type
                self.click_btn(browser, 10, 1, None,"//div/a[@class='edit-post-type hide-if-no-js']")  # click edit button
                self.click_btn(browser, 10, 1, None,"//select[@id='pts_post_type']/option[4]")  # select post type
                #click ok button
                self.click_btn(browser, 10, 1, None,"//div/a[contains(@class, 'save-post-type hide-if-no-js button')][1]")  # click edit button


        #test input posts_list
        for item in posts_list:
            for keys, values in posts_list[item].items():
                print("key : {}".format(keys))
                print("value: {}".format(values))
        sleep(60)
        browser.close() #finish the session

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
        except:
            print(f'error in send_text function {traceback.format_exc()}')

    def click_btn(self, driver, wait_time, frequence, list_error_to_ignored, input_xpath):
        clickable_btn = None
        default_exception_to_ignore = [ElementNotSelectableException, ElementNotInteractableException,
                                       ElementNotVisibleException, NoSuchElementException]
        if list_error_to_ignored is None:
            list_error_to_ignored = default_exception_to_ignore
        try:
            clickable_btn = WebDriverWait(driver, wait_time, poll_frequency=frequence,
                                          ignored_exceptions=list_error_to_ignored) \
                .until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            clickable_btn.click()
        except:
            print(f'error in clickable_btn function {traceback.format_exc()}')
        # send post data to the input field

