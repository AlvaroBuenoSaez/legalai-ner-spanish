import pandas as pd
import os
PATH="../data/02_intermediate/tc_sentences_text.csv"

import os,re
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

from transformers import pipeline,  XLMRobertaForTokenClassification, XLMRobertaTokenizerFast,XLMRobertaConfig
from transformers import pipeline,  RobertaForTokenClassification, RobertaTokenizerFast

capitel_labels=['B-OTH', 'I-OTH', 'E-OTH', 'S-ORG', 'S-OTH', 'B-PER', 'E-PER', 'B-ORG', 'E-ORG', 
'S-LOC', 'S-PER', 'B-LOC', 'E-LOC', 'I-PER', 'I-ORG', 'I-LOC', 'O']
ancora_labels=[ 'B-DATE', 'B-LOC', 'B-MISC', 'B-NUM', 'B-ORG', 'B-PER', 'I-DATE',
'I-LOC', 'I-MISC', 'I-NUM', 'I-ORG', 'I-PER', 'O']
conll_labels=[ "O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC",]


conll_path="/home/abueno/workspaces/workspace-thesis/legalai-ner-spanish/data/06_models/alvaro-models-ner-timex/xlm-roberta-large-conll2002_ner/conll_ner_8_0.1_0.00003_10-21-22_17-58"
ancora_path="/home/abueno/workspaces/workspace-thesis/legalai-ner-spanish/data/06_models/alvaro-models-ner-timex/ixabertesv2-ancora_ner/ancora_ner_8_0.1_0.00005_10-24-22_20-19"
capitel_path="/home/abueno/workspaces/workspace-thesis/legalai-ner-spanish/data/06_models/alvaro-models-ner-timex/xlm-roberta-large-capitel_ner/capitel_ner_8_0.1_0.00001_10-22-22_11-55"

aggregation_strategy="simple"
frac=0.0001
def pipe_capitel():
    model =  XLMRobertaForTokenClassification.from_pretrained(capitel_path,ignore_mismatched_sizes=True)
    tokenizer = XLMRobertaTokenizerFast.from_pretrained(capitel_path,add_prefix_space=True)
    pipe = pipeline(task="ner",
                    model=model,
                    tokenizer=tokenizer,aggregation_strategy=aggregation_strategy)
    return pipe

def pipe_ancora():
    model =  RobertaForTokenClassification.from_pretrained(ancora_path,ignore_mismatched_sizes=True)
    tokenizer = RobertaTokenizerFast.from_pretrained(ancora_path,)
    pipe = pipeline(task="ner",
                    model=model,
                    tokenizer=tokenizer, aggregation_strategy="max")
    return pipe

def pipe_conll():
    model =  XLMRobertaForTokenClassification.from_pretrained(conll_path,ignore_mismatched_sizes=True)
    tokenizer = XLMRobertaTokenizerFast.from_pretrained(conll_path,add_prefix_space=True)
    pipe = pipeline(task="ner",
                    model=model,
                    tokenizer=tokenizer, aggregation_strategy=aggregation_strategy)

    return pipe

def process_data(data,pipe,model_name):
    out=[]
    texts={}
    for index,row in tqdm(data.iterrows()):
        if row.pdf not in texts:
            texts[row.pdf]=[str(row.text)]
        else:
            texts[row.pdf].append(str(row.text).strip("\n"))
    
    for key in tqdm(texts):
        text=str("\n".join(texts[key]))
        if text.strip("\n").strip(" ")!="":
            try:
                entities=pipe(text)
            except Exception as e:
                print(e)
                print(text)
                entities=[]

            # for entity in entities:
            #     entity["is_subword"]=False

            # entities=pipe.aggregate_words(entities,"max")
            for entity in entities:
                # if entity not in out:
                    entity["model"]=model_name
                    out.append(entity)
    return out

def infer_ancora(data:pd.DataFrame,config:dict):
    frac=config["frac"] if config and "frac" in config else 0.0001
    print(frac)
    data=data.sample(frac=frac, replace=True)
    ancora=pipe_ancora()
    out=process_data(data,ancora,"ancora")
    return pd.DataFrame.from_records(out)

def infer_capitel(data:pd.DataFrame,config:dict):
    frac=config["frac"] if config and "frac" in config else 0.0001

    data=data.sample(frac=frac, replace=True)
    capitel=pipe_capitel()
    out=process_data(data,capitel,"capitel")
    return pd.DataFrame.from_records(out)

def infer_conll(data:pd.DataFrame,config:dict):
    frac=config["frac"] if config and "frac" in config else 0.0001
    data=data.sample(frac=frac, replace=True)
    conll=pipe_conll()
    out=process_data(data,conll,"conll")
    return pd.DataFrame.from_records(out)


if os.path.isfile(PATH):
    conll=infer_conll(pd.read_csv(PATH),{"frac":1})
    conll.to_csv("../data/09_server/tc_conll.csv")
    ancora=infer_ancora(pd.read_csv(PATH),{"frac":1})
    ancora.to_csv("../data/09_server/tc_ancora.csv")
    capitel=infer_capitel(pd.read_csv(PATH),{"frac":1})
    capitel.to_csv("../data/09_server/tc_capitel.csv")
else:
    print("Error: no existe el archivo.")
