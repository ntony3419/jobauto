

class WordpressPost(object):

    #instance attribute
    def __init__(self, status, visibility, publish_date, post_type, category, featured_image, post_title,post_detail, author,salary,job_type,location,company):
        super().__init__()
        self.__status = status #can edit later but default is None
        self.__visibility = visibility
        self.__publish_date = publish_date
        self.__post_type = post_type #can edit later but default is Job
        self.__category = category
        self.__featured_image = featured_image
        self.__post_title = post_title
        self.__post_detail = post_detail
        self.__author = author
        self.__salary = salary
        self.__job_type = job_type
        self.__location = location
        self.__company = company

    def get_status(self):
        return self.__status
    def get_visibility(self):
        return self.__visibility
    def get_publish_date(self):
        return self.__publish_date
    def get_post_type(self):
        return self.__post_type
    def get_category(self):
        return self.__category
    def get_featured_image(self):
        return  self.__featured_image
    def get_post_title(self):
        return self.__post_title
    def get_post_detail(self):
        return self.__post_detail
    def get_author(self):
        return self.__author
    def get_salary(self):
        return self.__salary
    def get_job_type(self):
        return self.__job_type
    def get_location(self):
        return self.__location
    def get_company(self):
        return self.__company


    #mutators
    def set_status(self, status ):
        self.__status = status
    def set_visibility(self, visibility):
        self.__visibility = visibility
    def set_publish_date(self, publish_date):
        self.__publish_date = publish_date
    def set_post_type(self, post_type):
        self.__post_type = post_type
    def set_category(self , category):
        self.__category= category
    def set_featured_image(self, featured_image):
         self.__featured_image = featured_image
    def set_post_title(self, post_title):
        self.__post_title = post_title
    def set_post_detail(self, post_detail):
        self.__post_detail = post_detail
    def set_author(self, author):
        self.__author = author
    def set_salary(self, salary):
        self.__salary = salary
    def set_job_type(self, job_type):
        self.__job_type = job_type
    def set_location(self, location):
        self.__location = location
    def set_company(self, company):
        self.__company=company

    def display(self):
        return "{}\t{}".format(self.__publish_date , self.__post_title)




