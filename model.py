import csv
import cv2
import numpy as np
import pandas as pd
from functions import generate_key, detect_answers, find_the_answer_datasheet, find_the_question, evaluation, presentation
from functions import add_answers_to_datasheet, detect_questions_in_datasheet, presentation, add_checked_to_datasheet
import os

class ClassScore:
    def __init__(self, answer_sheet_path, answer_key_path):
        self.answer_sheet_path = answer_sheet_path
        self.answer_key_path = answer_key_path
    
    def score(self):
        # Calculate the score and return a float value between 0 and 100
        key_df = generate_key(self.answer_key_path)

        answer_sheet_df = detect_answers(self.answer_sheet_path)
        answer_sheet_df = add_answers_to_datasheet(answer_sheet_df)
        answer_sheet_df = detect_questions_in_datasheet(answer_sheet_df)
        answer_sheet_df = add_checked_to_datasheet(key_df, answer_sheet_df)
        
        score = evaluation(answer_sheet_df)
        return score 
        
    
    def representation(self):
        # Visual representation of correct and incorrect answers based on input
        key_df = generate_key(self.answer_key_path)

        answer_sheet_df = detect_answers(self.answer_sheet_path)
        answer_sheet_df = add_answers_to_datasheet(answer_sheet_df)
        answer_sheet_df = detect_questions_in_datasheet(answer_sheet_df)
        answer_sheet_df = add_checked_to_datasheet(key_df, answer_sheet_df)
        presentation(answer_sheet_df, self.answer_sheet_path)
        
        pass
    
    def save_status(self, output_file):
        key_df = generate_key(self.answer_key_path)

        answer_sheet_df = detect_answers(self.answer_sheet_path)
        answer_sheet_df = add_answers_to_datasheet(answer_sheet_df)
        answer_sheet_df = detect_questions_in_datasheet(answer_sheet_df)
        answer_sheet_df = add_checked_to_datasheet(key_df, answer_sheet_df)

        answer_sheet_df = answer_sheet_df.drop(['x', 'y', 'x2', 'y2'], axis=1)
        answer_sheet_df = answer_sheet_df.sort_values('question')

        df = pd.DataFrame()
        df['question'] = range(1,166)
        df['checked'] = "-"

        merged_df = df.merge(answer_sheet_df, on='question', how='left')
        df['checked'] = merged_df['checked_y']
        df['checked'] = df['checked'].fillna('-')

        df.to_csv(output_file, index=False)
        pass 
    
    @staticmethod
    def save_allstatus(answer_sheet_path, answer_key_path, output_file):
        key_df = generate_key(answer_key_path)

        answer_sheet_df = detect_answers(answer_sheet_path)
        answer_sheet_df = add_answers_to_datasheet(answer_sheet_df)
        answer_sheet_df = detect_questions_in_datasheet(answer_sheet_df)
        answer_sheet_df = add_checked_to_datasheet(key_df, answer_sheet_df)

        answer_sheet_df = answer_sheet_df.drop(['x', 'y', 'x2', 'y2'], axis=1)
        answer_sheet_df = answer_sheet_df.sort_values('question')

        df = pd.DataFrame()
        df['question'] = range(1,166)
        df['checked'] = "-"

        merged_df = df.merge(answer_sheet_df, on='question', how='left')
        df['checked'] = merged_df['checked_y']
        df['checked'] = df['checked'].fillna('-')

        df['2'] = os.path.basename(answer_sheet_path)
        df.insert(0, 'file.name', df['2'])
        df = df.drop('2', axis=1)

        df.to_csv(output_file, index=False)
                
        pass 
        
        
    
    @staticmethod
    def save_all(answer_sheets_folder, key_path, output_file):
        # Read all answer sheets and keys, calculate scores, and save them in a CSV file
        

        # Calculate the score and return a float value between 0 and 100
        key_df = generate_key(answer_key_path)

        answer_sheet_df = detect_answers(answer_sheet_path)
        answer_sheet_df = add_answers_to_datasheet(answer_sheet_df)
        answer_sheet_df = detect_questions_in_datasheet(answer_sheet_df)
        answer_sheet_df = add_checked_to_datasheet(key_df, answer_sheet_df)
        
        score = evaluation(answer_sheet_df)



        pass