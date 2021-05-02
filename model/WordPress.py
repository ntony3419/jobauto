


class WordPress(object):

    def __init__(self):
        self.__list_of_post = []
        self.__author_dict={}
        self.__category_dict={}
        self.__job_type_dict={}
        self.__salary_dict={}

    def login(self, url):
        pass

    def add_post(self, post):
        self.__list_of_post.append(post)

    def get_post_list(self):
        return self.__list_of_post
    def get_author_dict(self):
        return self.__author_dict
    def get_category_dict(self):
        return self.__category_dict
    def get_job_type_dict(self):
        return self.__job_type_dict
    def get_salary_dict(self):
        return self.__salary_dict


    def set_post_list(self, list_of_post):
        self.__list_of_post = list_of_post
    def set_author_dict(self, author_dict):
        self.__author_dict =author_dict
    def set_category_dict(self, category_dict):
        self.__category_dict =category_dict
    def set_job_type_dict(self, job_type_dict):
        self.__job_type_dict =job_type_dict
    def set_salary_dict(self, salary_dict ):
        self.__salary_dict =salary_dict

    def add_to_author_dict(self, key , author_value):
        self.__author_dict[key]=author_value
    def add_to_salary_dict(self, key, salary):
        self.__salary_dict[key]=salary
    def add_to_job_type_dict(self, key, job_type):
        self.__job_type_dict[key] = job_type
    def add_to_category_dict(self, key, category_list):
        self.__category_dict[key] = category_list

    def display(self):
        print("AUTHOR")
        for key,value in self.__author_dict.items():
            print("{} : {}".format(key,value))
        print("Salary")
        for key, value in self.__salary_dict.items():
            print("{} : {}".format(key, value))
        print("JOB_TYPE")
        for key, value in self.__job_type_dict.items():
            print("{} : {}".format(key, value))
        print("CATEGORY")
        for key, value in self.__category_dict.items():
            print("{} : {}".format(key, value))
