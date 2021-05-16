import pandas as pd
from model.WordpressPost import WordpressPost
import re
class FileIO(object):
    def __init__(self):
        super().__init__()

    def read_job_file_to_dict(self):
        pass

    def read_job_file_to_wordpress(self,posts_list, file_name):

        df = pd.read_excel(file_name)
        ''' convert each row into 1 single dictionary'''
        posts_dict=df.to_dict("index")
        '''turn posts information in posts_dict into list of wordpress posts '''
        for item in posts_dict:
            job_location = posts_dict[item]["JOB LOCATION"]
            if posts_dict[item]["JOB LOCATION"] is not None:
                if bool(re.match("singapore" ,posts_dict[item]["JOB LOCATION"], re.IGNORECASE)) is False:
                    job_location = "{},{}".format(posts_dict[item]["JOB LOCATION"],"Singapore")
            #for keys, values in posts_dict[item].items():  # iterate through each collected item from excel file and add to new post
            post = WordpressPost(status=posts_dict[item]["STATUS"], visibility=None, publish_date=posts_dict[item]["Posted Date"],
                               category=posts_dict[item]["CATEGORY"], featured_image=None, post_title=posts_dict[item]["JOB TITLE"],post_detail=posts_dict[item]["Job Details"],
                                 author=posts_dict[item]["SEARCHED BY"],salary=posts_dict[item]["SALARY"],job_type=posts_dict[item]["JOB TYPE"],location=job_location, company=posts_dict[item]["COMPANY NAME"])
            posts_list.append(post)