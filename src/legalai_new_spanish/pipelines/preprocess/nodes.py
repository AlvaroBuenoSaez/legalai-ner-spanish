"""
This is a boilerplate pipeline 'preprocess'
generated using Kedro 0.18.3
"""
import pandas as pd
import os
from .BS.Sentence import Sentence

def process_tc(file_path:str)-> pd.DataFrame:
    out={}
    #set absolute paths
    project_path=os.sep.join(__file__.split(os.sep)[0:-5])
    tc_path=os.path.join(project_path,"data",file_path)
    html_files=os.listdir(tc_path)

    # process all xml files
    for html in html_files[0:1]:
        out[html]={}
        with open(os.path.join(tc_path,html)) as html_file:
            content=html_file.read()
            sentence=Sentence(content)
            out[html]=sentence.__dict__
    
    return out
