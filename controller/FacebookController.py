import traceback
import os
import re
import random
from time import sleep
import csv
from model.ChromeBrowser import ChromeBrowser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
class FacebookController(object):

    def __init__(self, setting):
        super().__init__()
        self.setting = setting
        self.sca = ChromeBrowser(self.setting);

    ''' name: share_to_group
        Excert: wrapper method to share to group function
        import: none
        export: none    
    '''
    def share_to_group_wraper(self):# controller
        print("Post to multiple group")
        amount_of_group_to_share = self.setting["GROUP_TO_SHARE"]
        file_name = f"{os.path.dirname(os.path.abspath(__file__))}\{'facebook_group.csv'}"
        '''generate list of joined group'''
        groups_list = self.facebook_group_list(file_name,
                                               amount_of_group_to_share)  # verify the join state of each faceboko group
        '''generate list of post will be shared'''
        file_name = f"{os.path.dirname(os.path.abspath(__file__))}\{'today_job.csv'}"
        content_list = self.content_to_share_list(file_name)  # generate a list of content to be shared
        group_index_shared = []  # store group index that is already shared
        content_index_shared = []  # store item that is already shared
        count=0
        while count < amount_of_group_to_share:
            index_group_to_share = random.randint(0, len(groups_list) - 1)  # index of group to share post
            content_index = random.randint(0, len(content_list) - 1)  # index of content will be shared

            ''' create post content from the dictionary of content from content list'''
            company = content_list[content_index]["company"]
            title = content_list[content_index]["title"]
            location = content_list[content_index]["location"]
            url = content_list[content_index]["url"]
            content = content_list[content_index]["content"]
            post_content = f"Chia sẻ việc làm cho anh chị em nào cần tìm việc làm hôm nay: \n{content}\nxem chi tiết công việc : {url}"

            if index_group_to_share not in group_index_shared and content_index not in content_index_shared:
                self.share_to_group(group_url=groups_list[index_group_to_share], post_content=post_content)
                group_index_shared.append(index_group_to_share)  # add this group index to shared group
                content_index_shared.append(content_index)  # add this content index to shared content
                count += 1
                print(f"The amount of group shared : {count}")

    ''' name: facebook_group_list
            excert : generate facebook group list to share base on the limit to share randomly from list of groups
            import: file_name
            export: group_list
        '''

    def facebook_group_list(self, file_name, amount_to_share):
        joined_group = []
        init_group_list = []
        file_fpt = open(file_name, "r", encoding="utf-8", newline="")
        csv_reader = csv.reader(file_fpt, delimiter=",")
        # add all url to a list before filter out
        for row in csv_reader:
            init_group_list.append(row[0])

        # filter amount of group to share (joined group)
        join_count = 0
        while join_count < amount_to_share:
            joined = False
            rand_index = random.randint(0, len(init_group_list) - 1)  # generate a random index number
            # open browser and check joined status

            if init_group_list[rand_index] not in joined_group:  # if the selected url is not added in joined_group
                browser = self.sca.browser(self.setting)
                browser.get(init_group_list[rand_index])
                # check for the invite_button - if there is invite button then group is joined
                invite_btn_xpath = """(//*[contains(@role,"button")]/div//span[contains(text(),"Invite")])[2]"""

                try:
                    joined = self.check_presence_of_element(browser, 15, 1, None, invite_btn_xpath)
                except:
                    print(f"error: {traceback.format_exc()}")
                # add joined group into the group list
                if joined is True:
                    joined_group.append(init_group_list[rand_index])
                    join_count += 1

                sleep(2)
                browser.close()

        return joined_group

    def content_to_share_list(self, data_file_csv):
        content_list = []
        file_ptr = open(data_file_csv, 'r', newline="", encoding='utf-8')
        csv_reader = csv.reader(file_ptr, delimiter=',')

        for row in csv_reader:
            one_job = {"title": None, "company": None, "location": None, "url": None}
            if (row[1]) != "title":
                one_job["title"] = re.findall("(^.+)\(", row[1])[0].strip()
                one_job["company"] = re.findall("\(.+\)", row[1])[0].strip()
                one_job["company"] = re.sub("\(|\)", "", one_job["company"])
                one_job["location"] = re.findall(".+–(.+)$", row[1])[0].strip()
                one_job["url"] = row[2]
                one_job["content"] = row[4]
                content_list.append(one_job)
        return content_list

    def check_presence_of_element(self, driver, wait_time, frequence, list_error_to_ignored, input_xpath):
        # posting xpath #//*/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/form/div/div[1]/div/div[2]/div[3]/div[5]
        presence = False
        element = None
        try:
            element = WebDriverWait(driver, wait_time, poll_frequency=frequence,
                                    ignored_exceptions=list_error_to_ignored) \
                .until(EC.presence_of_element_located((By.XPATH, input_xpath)))
        except:
            pass
        if element is not None:
            presence = True

        return presence

    ''' Function name: share_to_group
           Description: create a post on a group page in dicussion section
           Import: group_url, post_content
           EXPORT: None
       '''

    def share_to_group(self, group_url, post_content):
        browser = self.sca.browser(self.setting)
        browser.get(group_url)
        create_post_btn_xpath = '''//*[contains(text(),"Create a public post")] | //*[contains(text(),"Start Discussion")] |//*/span[contains(text(),"What's on your mind")]'''
        # '''//*[contains(text(),"Create a public post")] | //*[contains(text(),"Start Discussion")]'''
        # check if the create_post_btn for discussion exist. if not open the discuss and seell tab
        create_post_btn = None
        try:
            create_post_btn = self.clickable_btn(browser, 10, 2, None, create_post_btn_xpath)
            create_post_btn.click()
        except:
            pass
        if create_post_btn is None:
            group_url = f'''{group_url}/{"buy_sell_discussion"}'''
            browser.get(group_url)
            try:
                create_post_btn = self.clickable_btn(browser, 10, 2, None, create_post_btn_xpath)
                create_post_btn.click()
            except:
                pass

        # text field to create post
        text_field_xpath = '''//*/div[contains(@role, "presentation")]//div[contains(@role, "textbox")]//div/span'''
        # post button //*[@id="mount_0_0"]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div[3]/div[2]/div/div
        post_btn_xpath = '''//*/div[contains(@role,"button")]/div/div/div/span/span[contains(text(),"Post")]'''

        try:
            self.send_text(browser, 10, 2, None, text_field_xpath, post_content)
            post_btn = self.clickable_btn(browser, 30, 2, None, post_btn_xpath)
            sleep(5)
            post_btn.click()
        except:
            pass
        sleep(random.randint(7, 15))  # wait a bit for the post to update
        browser.close()

    ''' this function will click on the input XPATH element'''

    def clickable_btn(self, driver, wait_time, frequence, list_error_to_ignored, input_xpath):
        clickable_btn = None
        default_exception_to_ignore = [ElementNotSelectableException, ElementNotInteractableException,
                                       ElementNotVisibleException, NoSuchElementException]
        if list_error_to_ignored is None:
            list_error_to_ignored = default_exception_to_ignore
        try:
            clickable_btn = WebDriverWait(driver, wait_time, poll_frequency=frequence,
                                          ignored_exceptions=list_error_to_ignored) \
                .until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        except:
            pass
        # send post data to the input field
        return clickable_btn