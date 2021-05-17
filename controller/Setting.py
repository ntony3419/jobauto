import configparser
from shutil import which
import os
import model.WordPress as wordpress
import re


class Setting(object):

    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.wp_default_conf = configparser.ConfigParser()

    def load_setting(self):
        settings = {}
        try:
            config_file_path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
            self.config.read(os.path.join(config_file_path, 'setting.conf'))

        except:
            print("read setting file Error")

        settings["HOME_URL"] = self.config["DEFAULT"]["HOME_URL"]
        settings["WP_USER_NAME"] = self.config["DEFAULT"]["WP_USER_NAME"]
        settings["WP_PASSWORD"] = self.config["DEFAULT"]["WP_PASSWORD"]

        broswer_driver_path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-2])
        settings["DRIVER_EXECUTABLE"] = os.path.join(broswer_driver_path, self.config["GOOGLE_CHROME"]["DRIVER_EXECUTABLE"])
        settings["CHROME_PROFILE_PATH"] = self.config["GOOGLE_CHROME"]["CHROME_PROFILE_PATH"]
        settings["CHROME_PROFILE"] = self.config["GOOGLE_CHROME"]["CHROME_PROFILE"]
        if self.config["GOOGLE_CHROME"]["USER_AGENT"].lower == 'none':
            settings["USER_AGENT"] =  (self.config["GOOGLE_CHROME"]["USER_AGENT"]).replace("'", "")
        else:
            settings["USER_AGENT"] = None
        settings["HEADLESS"] = self.config["GOOGLE_CHROME"]["HEADLESS"]
        settings["GROUP_TO_SHARE"] = self.config["FACEBOOK"]["GROUP_TO_SHARE"]
        return settings

    def load_wordpress_default(self):
        wordpress_default=wordpress.WordPress()
        try:
            config_file_path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
            self.wp_default_conf.read(os.path.join(config_file_path, 'wordpress_default.conf'))
        except:
            print("read setting file Error")


        for section_name in self.wp_default_conf.sections():
            if section_name == "AUTHORS":
                for key, value in self.wp_default_conf.items(section_name):
                    wordpress_default.add_to_author_dict(key,value.lower())
            if section_name == "JOB_TYPE":
                for key, value in self.wp_default_conf.items(section_name):
                    wordpress_default.add_to_job_type_dict(key, value.lower())
            if section_name == "CATEGORY":
                for key, value in self.wp_default_conf.items(section_name):
                    #split and trim the value into list
                    value = re.sub("\([a-zA-Z]\)","", value)
                    value = value.replace("(","") # remove parenthesis ( inside string
                    value = value.replace(")", "")# remove parenthesis ) inside string
                    value = value.split("|")
                    value = [x.lower().strip(' ') for x in value] #remove spces front and back and convert to lower case
                    value = [x.lower().strip("()") for x in value] #remove parenthesis front and back if exist
                    wordpress_default.add_to_category_dict(key, value)
            if section_name == "SALARY":
                for key, value in self.wp_default_conf.items(section_name):
                    new_val_array =[]
                    if (int(key) < 7 or (int(key) >25 and int(key) !=28)) : # number less than 7 and large 25 but not 28
                        new_val_array.append(value)
                    elif int(key) == 28:
                        value = value.replace(">$", "")
                        new_val_array.append(int(value))
                    else:
                        value = "-".join(re.findall("[0-9]+", value))
                        value = value.split("-")
                        value = [int(float(x)) for x in value] #convert string to integer if possble
                        new_val_array = value
                        ''' convert to array'''
                    wordpress_default.add_to_salary_dict(key, new_val_array)
        return wordpress_default