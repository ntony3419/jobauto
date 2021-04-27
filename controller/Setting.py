
import configparser
from shutil import which

class Setting(object):

    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
    def load_setting(self):
        settings={}
        try:
            self.config.read('setting.conf')
        except :
            print("read setting file Error")

        settings["HOME_URL"] = self.config["DEFAULT"]["HOME_URL"]
        settings["WP_USER_NAME"]=self.config["DEFAULT"]["WP_USER_NAME"]
        settings["WP_PASSWORD"]=self.config["DEFAULT"]["WP_PASSWORD"]

        settings["DRIVER_EXECUTABLE"] = which(self.config["DEFAULT"]["DRIVER_EXECUTABLE"])

        settings["CHROME_PROFILE"]=self.config["DEFAULT"]["CHROME_PROFILE"]
        settings["USER_AGENT"] = self.config["DEFAULT"]["USER_AGENT"]
        settings["HEADLESS"] = self.config["DEFAULT"]["HEADLESS"]


        return settings
