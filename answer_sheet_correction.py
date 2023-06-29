import cv2
import numpy as np
import pandas as pd
from functions import generate_key, detect_answers, find_the_answer_datasheet, find_the_question, evaluation, presentation

path = 'images/image0000013A.tif'
path_to_key = 'images/key.png'
path_to_key_csv = 'images/key.csv'

# --------------Generate_key--------------

generate_key(path_to_key, path_to_key_csv)


#-------------- Add Answer to DataSheet ------------- 
path_to_answer_sheet = detect_answers(path)

df = pd.read_csv(path_to_answer_sheet)
print(df)
df['answer'] = 0     
for item in range(len(df)): 
    df['answer'][item] = find_the_answer_datasheet(df['x2'][item]) 

df.to_csv(path_to_answer_sheet, index=False)


#----------------- Detect Questions ----------------- 
df = pd.read_csv(path_to_answer_sheet)

df['question'] = 0
for item in range(len(df)): 
    df['question'][item] = find_the_question(df['x2'][item], df['y2'][item]) 
    
print(df)
df.to_csv(path_to_answer_sheet, index=False)

#----------------- Evaluation -----------------
key_df = pd.read_csv(path_to_key_csv)

evaluation(key_df, df)

#----------------- Presentation  -----------------

presentation(df, path)