# """
# This is a boilerplate pipeline 'tagging'
# generated using Kedro 0.18.3
# """

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



# def search_word(text:list(),m_word:str,m_index:int,window:10):

import numpy as np

def predict(data:pd.DataFrame,config:dict):
    def get_labels(text):
        tokens=ancora_tokenizer(text,return_tensors='pt')
        words=ancora_tokenizer.convert_ids_to_tokens(ancora_tokenizer(text)["input_ids"])
        logits=ancora_model(**tokens).logits
        out=[]
        for i,logit in enumerate(logits[0]):
            predicted_class_id = logit.argmax().item()
            label=ancora_model.config.id2label[predicted_class_id]
            out.append({"word":words[i],"label":label})
        return out

    ancora_tokenizer,ancora_model=pipe_conll()
    data=data.sample(frac=0.00001, replace=True, random_state=1)
    out=[]
    for id,row in tqdm(data.iterrows()):
            text=re.sub(" +"," ",row["text"])
            paragraphs=text.split("\n")
            for paragraph in paragraphs:
                if len(paragraph.split(" "))>200:
                    short_paragraphs=[" ".join(paragraph.split()[i:i+200]) for i in range(0, len(paragraph.split()), 200)]
                    for short_paragraph in short_paragraphs:
                        out.extend(get_labels(short_paragraph))
                else:
                    out.extend(get_labels(paragraph))
                    
    return pd.DataFrame().from_records(out)

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

def join_entities(conll,capitel,ancora)->pd.DataFrame:
    all_df=pd.concat([conll,capitel,ancora])
    all_df = all_df.reset_index(drop=True)
    return all_df

from statistics import mean
def fix_entities(entities:pd.DataFrame)->pd.DataFrame:
    entities=entities[["entity_group","score","word","model","start","end"]]
    entities=entities[entities["word"]!="\""]
    entities=entities[entities["word"]!="."]

    new_entities=[]
    buffer=pd.Series([])
    for index,entity in tqdm(entities.iterrows()):
        if not buffer.empty:
            if buffer.end == entity.start:
                if not entity.word[0].isupper():
                    if buffer.score<entity.score:
                        buffer.entity_group=entity.entity_group

                    buffer.score=mean([buffer.score,entity.score])
                    buffer.word+=entity.word
                    buffer.end=entity.end
                else:
                    new_entities.append(buffer)
                    buffer=entity
            elif buffer.end+1 == entity.start:
                if buffer.score<entity.score:
                    buffer.entity_group=entity.entity_group

                buffer.score=mean([buffer.score,entity.score])
                if entity.word.startswith(" "):
                    buffer.word+=entity.word
                else:
                    buffer.word+=" "+entity.word
                buffer.end=entity.end
            else:
                new_entities.append(buffer)
                buffer=entity
        else:
            buffer=entity
    new_entities.append(buffer)
    # entities=entities[entities["score"]>0.5]
    return pd.DataFrame.from_records(new_entities)

import spacy
def format_sentences_to_BIO(sentences:pd.DataFrame)->pd.DataFrame:
    out=[]
    nlp = spacy.load("es_core_news_sm")
    nlp.max_length = 1200000
    for _, item in tqdm(sentences.iterrows(),desc="Procesing "+str(len(sentences))+" sentences."):
        text=str(item["text"])
        print(len(text))
        if len(text)>=300000:
            print("Error."+str(len(text)))
        else:
            words=nlp(text)
            entry={"name":item["name"],"section":item["section"],"pdf":item["pdf"]}
            for word in words:
                entry["word"]=word
                out.append(entry)

    return pd.DataFrame.from_records(out)

def tag_sentences(entities:pd.DataFrame,sentences:pd.DataFrame)->pd.DataFrame:
    print(sentences)
    return sentences