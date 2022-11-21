"""
This is a boilerplate pipeline 'analysis'
generated using Kedro 0.18.3
"""

import pandas as pd
def print_data(data:dict,relevant_data:pd.DataFrame)->pd.DataFrame:
    out=[]
    for file in data:
        row=dict()
        info=data[file]
        row["file"]=file
        name=info["name"]
        info_in_name=name.split(" ")
        name=info_in_name[4]
        date=info_in_name[5].split("/")[1]
        num_sections=len(info["sections"])
        length=len(" ".join([str(info["sections"][key]) for key in info["sections"]]))
        out.append({
            "file":file,
            "name":name,
            "date":date,
            "num_sections":num_sections,
            "length":length
        })
        
    df=pd.DataFrame.from_records(out)
    print(df["date"].value_counts())
    print(df["num_sections"].value_counts())
    return df