import pandas as pd


class FileIO(object):
    def __init__(self):
        super().__init__()

    def read_file(self, file_name):
        posts_dict = {}
        df = pd.read_excel(file_name)
        ''' convert each row into 1 single dictionary'''
        posts_dict=df.to_dict("index")

        return posts_dict