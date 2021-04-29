import pandas as pd
from model.WordpressPost import WordpressPost

class FileIO(object):
    def __init__(self):
        super().__init__()



    def read_file(self,posts_list, file_name):
        posts_dict = {}
        df = pd.read_excel(file_name)
        ''' convert each row into 1 single dictionary'''
        posts_dict=df.to_dict("index")
        '''turn posts information in posts_dict into list of wordpress posts '''
        for item in posts_dict:
            #for keys, values in posts_dict[item].items():  # iterate through each collected item from excel file and add to new post
            post = WordpressPost(status=None, visibility=None, publish_date=posts_dict[item]["Posted Date"], post_type=None,
                               category=None, featured_image=None, post_title=posts_dict[item]["JOB TITLE"],post_detail=posts_dict[item]["Job Details"],
                                 author=posts_dict[item]["SEARCHED BY"],salary=None,job_type=None,location=posts_dict[item]["JOB LOCATION"], company=posts_dict[item]["COMPANY NAME"])
            posts_list.append(post)