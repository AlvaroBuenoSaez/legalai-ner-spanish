"""
This is a boilerplate pipeline 'preprocess'
generated using Kedro 0.18.3
"""
from email.quoprimime import quote
from unittest import result
import pandas as pd
import os
from .BS.Sentence import Sentence
from tqdm import tqdm

def process_tc(file_path:str)-> pd.DataFrame:
    out={}
    reports={}
    results={}
    #set absolute paths
    project_path=os.sep.join(__file__.split(os.sep)[0:-5])
    tc_path=os.path.join(project_path,"data",file_path)
    html_files=os.listdir(tc_path)

    # process all xml files
    for html in tqdm(html_files):
        out[html]={}
        
        with open(os.path.join(tc_path,html)) as html_file:
            content=html_file.read()
            sentence=Sentence(html,content)
            out[html]=sentence.__dict__
            reports[html]=sentence.report()

    return out,reports

def get_results(reports:dict)->dict:
    results={}
    parameters=reports[list(reports.keys())[0]].keys()
    results["num_sentences"]=len(reports.keys())
    for p in parameters:
        results[p]=len([reports[pdf][p] for pdf in reports if p in reports[pdf] if reports[pdf][p]])
        results[p+"(%)"]=(results[p]/results["num_sentences"])*100
    
    for p in parameters:
        if "%" not in p and results[p+"(%)"]!=100.0:
            results["NO_"+p+"_files"]=[pdf for pdf in reports if p in reports[pdf] if not reports[pdf][p]][0:10]
    return results


def extract_relevant_data(sentences:dict)->dict:

    fields=["info","quotes","concepts"]
    out={}
    for pdf in tqdm(sentences.keys()):
        content=sentences[pdf]
        for f in fields:
            if f in content:
                level_1=content[f]
                if type(level_1)==dict:
                    for k in level_1.keys():
                        key=f+"."+k
                        level_2=level_1[k]
                        if type(level_2)==str:
                            if key not in out:
                                out[key]=set()
                            out[key].add(level_2)
                elif type(level_1)==list:
                    if f not in out:
                        out[f]=set(level_1) 
                    else:
                        out[f].update(level_1)

    keys=list(out.keys())
    for key in keys:
        out[key]=list(out[key])
        out["num_"+key]=len(out[key])

    all_magistrados=set()
    all_magistrados=set([magistrado.strip().capitalize() for magistrados in out["info.Magistrados"] for magistrado in magistrados.split(",")])
    all_magistrados=set([magistrado.strip().capitalize() if magistrado.startswith("Do") else "Don "+ magistrado for magistrados in all_magistrados for magistrado in magistrados.split(" y don ")])
    all_magistrados=set([magistrado.strip().capitalize() if magistrado.startswith("Do") else "Doña "+ magistrado for magistrados in all_magistrados for magistrado in magistrados.split(" y doña ")])
    out["info.Magistrados"]=list(all_magistrados)



    return out