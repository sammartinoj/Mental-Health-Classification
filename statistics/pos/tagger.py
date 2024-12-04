#!/usr/bin/env python3

import spacy
import pandas as pd
import os
import subprocess

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Installing en_core_web_sm.")
    subprocess.run(["python3", "-m", "spacy", "download", "en_core_web_sm"], check=True)

input = os.path.expandvars("$HOME/text_tools_project/data/mini-csvs")
output = os.path.expandvars("$HOME/text_tools_project/data/tagged-csvs")
os.makedirs(output, exist_ok=True)

for file_name in os.listdir(input):
    file_path= os.path.join(input, file_name)
    basename = file_name.replace(".csv", "")
    output_path= os.path.join(output, f"{basename}-pos.csv")

    df = pd.read_csv(file_path, header=None)

    df.columns = ["id", "statement", "label"]

    results = []

    for idx, text in df["statement"].items():
        doc = nlp(text)
        for token in doc:
            results.append({
                "row_id": idx,
                "text": text,
                "token": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_
            })

    tagged_df = pd.DataFrame(results)
    tagged_df.to_csv(output_path, index=False)
    print(f"Finished {file_name} : {output_path}")
