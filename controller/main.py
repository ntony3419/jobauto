import gui.MainWindow as mw
import model.WordpressPost as wordpress_post
import model.WordPress as wordpress
import controller.FileIO as fio
import tkinter as tk
import controller.Controller as controller
import controller.Setting as setting


class main_class():
    def __init__(self):
        super().__init__()
        self.controller = controller.Controller()
        self.settings = setting.Setting().load_setting()
        self.wordpress_default = setting.Setting().load_wordpress_default()
        self.wordpress_default.display()

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
                        file_io.read_file(posts_list, r"C:\Users\nguye\Documents\github\python\resources\Singapura Test Pass Quang.xlsx")
                        # display list of posts for checking
                        for post in posts_list:
                            print(post.display())

                        #create the posts from list of posts
                        self.controller.create_wordpress_post(posts_list, self.settings, self.wordpress_default)

                    if debug_input == 2:  # open url and login
                        pass



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
        print("1. import job from file and display imported data")
        print("2. open the url and log in")
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

