from legalai_new_spanish.pipelines.tagging.nodes import infer_ancora,infer_capitel,infer_conll
import pandas as pd
import os
path="../data/02_intermediate/tc_sentences_text.csv"

if os.path.isfile(path):
    conll=infer_conll(pd.read_csv(path),{"frac":1})
    conll.to_csv("../data/09_server/tc_conll.csv")
    ancora=infer_ancora(pd.read_csv(path),{"frac":1})
    ancora.to_csv("../data/09_server/tc_ancora.csv")
    capitel=infer_capitel(pd.read_csv(path),{"frac":1})
    capitel.to_csv("../data/09_server/tc_capitel.csv")
else:
    print("Error: no existe el archivo.")
