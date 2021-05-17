import os
import xlwt
from xlwt import Workbook
import re
import pandas
import model.ChromeBrowser as chrome
import traceback
from datetime import date,datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class Controller(object):
    def __init__(self, setting):
        super().__init__()
        self.settings = setting

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

        '''Final step click publish button or save draft'''
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//input[contains(@id, 'publish') and contains(@type,'submit')]")).perform()
        print("psot get satus {}".format(post.get_status()))

        if post.get_status() == "draft":
            self.click_btn(browser, 10, 1, None,
                           "//input[@id='save-post']")  # click
            sleep(5)  # wait for the post to be added to database
        elif post.get_status()== "publish":
            self.click_btn(browser, 10, 1, None, "//input[contains(@id, 'publish') and contains(@type,'submit')]")  # click
            sleep(5)  # wait for the post to be added to database
        else: # not sure which to select then just set the post as draft
            self.click_btn(browser, 10, 1, None,
                           "//input[@id='save-post']")  # click
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
            #print(f'error in clickable_btn function {traceback.format_exc()}')
            print("something wrong with click button function but if noreal issue then just ignore this message/error")


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

        # get author from post and compare with wordpres preset author and return index to tick
        index = 1 #default author
        for key, value in wordpress_default.get_author_dict().items():
            if post.get_author().lower() in value:
                index = key

        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//select[@id='post_author_override']")).perform()
        self.click_btn(browser, 10, 1, None,
                           f"(//select[@id='post_author_override']/option)[{index}]")  # click the tick box


    def set_category(self,post,browser,wordpress_default):

        # get the category from post and compare with the wordpress category and return index to tick new jobs
        index = 1
        for key, value in wordpress_default.get_category_dict().items():
            if post.get_category().lower() in value:
                index = key
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("(//ul[@id='job_catchecklist']//input)")).perform()
        self.click_btn(browser, 10, 1, None, f"(//ul[@id='job_catchecklist']//input)[{index}]")  # click the tick box

    def set_salary(self,post,browser,wordpress_default):
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("//ul[@id='job_salarychecklist']")).perform()
        # get the salary from post and compare with the salary set up in wordpress_default and return index to tick
        salary_index = 4 #default value index

        try:
            for key, value in wordpress_default.get_salary_dict().items(): #value is default setting of salary in WP
                if (int(key) < 7 or ( int(key) > 25) and int(key) !=28):
                    if post.get_salary() in value:
                        salary_index = key
                elif int(key) == 28:
                    if (int(post.get_salary())+1) >= value[0]:
                        salary_index = key
                else:
                    if (int(post.get_salary())+1) >= value[0] and (int(post.get_salary()))+1 < value[1]:
                        salary_index = key

        except:
            print("salary has issue. using default value 'disclosed'")
            #print("{}".format(traceback.format_exc()))
        self.click_btn(browser, 10, 1, None,
                           f"(//ul[@id='job_salarychecklist']/li/label/input)[{salary_index}]")  # click the tick box

    def set_job_type(self,post,browser,wordpress_default):

        # get the job type from post and compare with the preset wordpress and return corect index to tick
        ActionChains(browser).move_to_element(
            browser.find_element_by_xpath("(//ul[@id='job_typechecklist'])")).perform()
        index = 1
        for key, value in wordpress_default.get_job_type_dict().items():
            if post.get_job_type() in value:
                index = key
        self.click_btn(browser, 10, 1, None,
                           f"(//ul[@id='job_typechecklist']/li/label/input)[{index}]")  # click the tick box

    def set_status(self,post, broser):
        if post.get_status() is None:
            pass #no need to do any thing here yet

    def scrape_job(self, url):
        scraped_job_file_location =None
        browser = chrome.ChromeBrowser(self.settings).browser()
        stop = False
        wb = Workbook()
        sheet1=wb.add_sheet("sheet 1")
        row = 0
        col = 0

        sheet1.write(row, col, "title")
        sheet1.write(row, col + 1, "company")
        sheet1.write(row, col + 2, "location")
        sheet1.write(row, col + 3, "detail")
        row+=1
        total_post=0
        while stop is False:
            count = 0
            # open url
            browser.get(url)
            # next page url
            next_page = browser.find_element_by_xpath("""//*/div[@id="pagination"]/a[contains(text(),"Next")]""").get_attribute("href")
            # all post urls on page
            post_url_elements = browser.find_elements_by_xpath("//*/dl/dd[2]/h4/a")
            post_urls = []
            for url_element in post_url_elements:
                post_urls.append(url_element.get_attribute("href"))
            #scrape one post at a time and save to excel file

            while count < len(post_urls) and stop is False:
                browser.get(post_urls[count])
                '''collect the date and use it to determine when to stop'''
                post_date = browser.find_element_by_xpath('''//*/span[@class="job-posted"]''').text #format 14 May
                year = int((browser.find_element_by_xpath('''//*/span[@class="year"]''').text).strip())
                #convert to date datatype
                month = re.sub("[0-9]+","",post_date).strip()
                month = int(datetime.strptime(month,'%b').strftime('%m'))
                #test =re.findall("^[0-9]+", post_date)
                day = int(re.findall("^[0-9]+", post_date)[0].strip())
                post_date = date(year,month,day)
                current_date = date.today()

                if (current_date - post_date).days != 0:
                    stop = True
                if stop is False:

                    '''scrape the post that is today'''
                    title = browser.find_element_by_xpath('''//*/h4[@class="title"]''').text.strip()
                    company =browser.find_element_by_xpath('''//*/span[@class="job-author"]''').text.strip()
                    location =browser.find_element_by_xpath('''//*/span[@class="jobs-place"]''').text.strip()
                    detail =browser.find_element_by_xpath('''//*/div[@class="jobdesc"]''').text.strip()
                    ''' write to excel file using pandas'''
                    sheet1.write(row, col,title)
                    sheet1.write(row, col + 1, company)
                    sheet1.write(row, col + 2, location)
                    sheet1.write(row, col + 3, detail)
                    # df = pandas.DataFrame({"title": title, "company":company,"location":location, "detail":detail }, columns=["title","company","location", "details"])
                    # file_path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-2])
                    # df.to_excel(os.path.join(file_path, "jobs_from_singapurajob.xlsx"), index=False, header=True)
                    count += 1
                    total_post+=1
                    row = row+1

            url=next_page #go to next job page
        print(f"amount of job today {date.today()} are {total_post}")
        wb.save("jobs_from_singapurajob.xls")
        browser.close()
        scraped_job_file_location_path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-2])
        scraped_job_file_location = f'''{scraped_job_file_location_path}\{"jobs_from_singapurajob.xls"}'''
        return scraped_job_file_location