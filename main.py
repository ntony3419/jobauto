import os
import random
import gui.MainWindow as mw
import model.WordpressPost as wordpress_post
import model.WordPress as wordpress
import controller.FileIO as fio
import tkinter as tk
import controller.Controller as controller
import controller.Setting as setting
from controller.FacebookController import FacebookController


class main_class():
    def __init__(self):
        super().__init__()
        self.settings = setting.Setting().load_setting()
        self.wordpress_default = setting.Setting().load_wordpress_default()
        self.controller = controller.Controller(self.settings)
        self.fb_controller = FacebookController(self.settings)


        #self.wordpress_default.display()

    def main(self):
        program_stop = False
        while program_stop is False:
            self.mode_menu()
            mode_input = int(input("choose mode: "))
            if mode_input == 1:
                r_mode_menu = False
                while r_mode_menu is False:
                    self.debug_menu()
                    debug_input = int(input("choose 1 item: "))
                    if debug_input == 1:  # import the posts from file
                        posts_list =[]
                        file_io = fio.FileIO()
                        try:
                            file_io.read_job_file_to_wordpress(posts_list, r"C:\Users\nguye\Documents\github\python\jobauto_2\Singapura Test Pass Quang.xlsx")
                        except Exception:
                            print("read file error, maybe the file is not exist")


                        #create the posts from list of posts
                        self.controller.create_wordpress_post(posts_list, self.settings, self.wordpress_default)

                    if debug_input == 2:
                        '''Post to facebook group'''

                        # prepare the post to use by scrape post from job site
                        #url = #"https://singapurajobs.com/lastest-jobs"
                        url = "https://www.singapurajobs.com/latest-jobs/"
                        scraped_job_file_location = self.controller.scrape_job(url)
                        content_list = {}
                        file_io = fio.FileIO()
                        try:
                            content_list=file_io.read_job_file_to_dict(scraped_job_file_location)
                        except Exception:
                            print("read file error, maybe the file is not exist")
                        '''generate list of joined group'''
                        group_file = f"{os.path.dirname(os.path.abspath(__file__))}\{'group_list.csv'}"
                        groups_list = self.fb_controller.facebook_group_list(group_file,
                                                               self.settings["GROUP_TO_SHARE"])
                        '''share job on group'''
                        group_index_shared = []  # store group index that is already shared
                        content_index_shared = []  # store item that is already shared
                        count = 0
                        while count < self.settings["GROUP_TO_SHARE"]:
                            index_group_to_share = random.randint(0, len(groups_list) - 1)  # index of group to share post
                            content_index = random.randint(0, len(content_list) - 1)  # index of content will be shared

                            ''' create post content from the dictionary of content from content list'''
                            company = content_list[content_index]["company"]
                            title = content_list[content_index]["title"]
                            location = content_list[content_index]["location"]
                            url = content_list[content_index]["url"]
                            content = content_list[content_index]["detail"]
                            post_content = f"new jobs today: \n{content}\ndetail at : {url}"

                            if index_group_to_share not in group_index_shared and content_index not in content_index_shared:
                                self.fb_controller.share_to_group(group_url=groups_list[index_group_to_share], post_content=post_content)
                                group_index_shared.append(index_group_to_share)  # add this group index to shared group
                                content_index_shared.append(content_index)  # add this content index to shared content
                                count += 1
                                print(f"The amount of group shared : {count}")

                        # group_count=0
                        # while group_count<self.settings["GROUP_TO_SHARE"]:
                        #     index_group_to_share = random.randint(0,
                        #                                           len(groups_list) - 1)  # index of group to share post
                        #     content_index = random.randint(0, len(content_list) - 1)  # index of content will be shared
                        #
                        #     ''' create post content from the dictionary of content from content list'''
                        #     company = content_list[content_index]["company"]
                        #     title = content_list[content_index]["title"]
                        #     location = content_list[content_index]["location"]
                        #     url = content_list[content_index]["url"]
                        #     content = content_list[content_index]["content"]
                        #     group_index_shared=[]
                        #     post_content = f"Chia sẻ việc làm cho anh chị em nào cần tìm việc làm hôm nay: \n{content}\nxem chi tiết công việc : {url}"
                        #
                        #     if index_group_to_share not in group_index_shared and content_index not in content_index_shared:
                        #         self.fb_controller.share_to_group(group_url=groups_list[index_group_to_share],
                        #                             post_content=post_content)
                        #         group_index_shared.append(index_group_to_share)  # add this group index to shared group
                        #         content_index_shared.append(content_index)  # add this content index to shared content
                        #         count += 1
                        #         print(f"The amount of group shared : {count}")
                        #     group_count+=1



                    if debug_input == 3:

                        posts_list = []
                        file_io = fio.FileIO()
                        scraped_job_file_location = r"C:\Users\quang nguyen\PycharmProjects\python\jobauto\jobs_from_singapurajob.xls"
                        try:
                            file_io.read_job_file_to_dict(posts_list, scraped_job_file_location)
                        except Exception:
                            print("read file error, maybe the file is not exist")


                    if debug_input == 9:
                        r_mode_menu = True
                    if debug_input == 0:
                        r_mode_menu = True
                        program_stop = True
            if mode_input == 2:
                pass
            if mode_input == 0:
                program_stop = True

        # main_window = mw.MainWindow() #init the gui
        # main_window.create_main_window()



    def mode_menu(self):
        print("1. debug mode")
        print("2. auto mode")
        print("0. exit")

    def debug_menu(self):
        print("1. Create wordpress draft from file")
        print("2. Post to facebook group")
        print("3. ")
        print("4. ")
        print("5. ")
        print("9. ")
        print("0. exit")

    def database_menu(self):
        print("Choose a task to perform ")
        print("\t1. Display database Decreasing by Date ")
        print("\t2. ")
        print("\t")
        print("\t")
        print("\t")
        print("\t")
        print("\t9. Previous menu")
        print("\t0. Exit")



if __name__ == "__main__":
    main_class = main_class()
    main_class.main()

