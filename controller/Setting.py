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

        broswer_driver_path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])

        settings["DRIVER_EXECUTABLE"] = os.path.join(broswer_driver_path, self.config["DEFAULT"]["DRIVER_EXECUTABLE"])

        settings["CHROME_PROFILE"] = self.config["DEFAULT"]["CHROME_PROFILE"]
        settings["USER_AGENT"] = self.config["DEFAULT"]["USER_AGENT"]
        settings["HEADLESS"] = self.config["DEFAULT"]["HEADLESS"]

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
                    wordpress_default.add_to_author_dict(key,value)
            if section_name == "JOB_TYPE":
                for key, value in self.wp_default_conf.items(section_name):
                    wordpress_default.add_to_job_type_dict(key, value)
            if section_name == "CATEGORY":
                for key, value in self.wp_default_conf.items(section_name):
                    #split and trim the value into list
                    print("test _ {}_ value short {} _ regex {} _ value full {}".format(re.sub("\([a-zA-Z]\)","", value),value[-3:], re.match("r'\([^)]*\)'", value[-3:]), value))
                    value = re.sub("\([a-zA-Z]\)","", value)
                    value = value.replace("(","") # remove parenthesis ( inside string
                    value = value.replace(")", "")# remove parenthesis ) inside string
                    value = value.split("|")
                    value = [x.strip(' ') for x in value] #remove spces front and back
                    value = [x.strip("()") for x in value] #remove parenthesis front and back if exist
                    wordpress_default.add_to_category_dict(key, value)
            if section_name == "SALARY":
                for key, value in self.wp_default_conf.items(section_name):
                    if bool(re.match("\$[0-9]+", value)):
                        value = "-".join(re.findall("\$[0-9]+", value))
                    wordpress_default.add_to_salary_dict(key, value)
        return wordpress_default