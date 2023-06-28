import cv2
import numpy as np
import pandas as pd
from functions import detect_answers, find_the_answer_datasheet, find_the_question, evaluation, presentation

path = 'C:/Users/Hassan/Desktop/Projects/ResponseLetter/image0000013A.tif'
path_to_key = 'C:/Users/Hassan/Desktop/Projects/ResponseLetter/key.png'
path_to_key_csv = 'C:/Users/Hassan/Desktop/Projects/ResponseLetter/key.csv'

# --------------Generate_key--------------

# Load the image
image = cv2.imread(path_to_key)

# Crop 400 pixels from the top of the image
image = image[400:, :]

# Convert the image from BGR to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range of green color in HSV
lower_green = np.array([40, 40, 40])
upper_green = np.array([70, 255, 255])

# Create a mask for the green color
mask = cv2.inRange(hsv, lower_green, upper_green)

# Find the contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create an empty list to store the correct answers
correct_answers = []

# Define the minimum area for a contour to be considered a fully green cell
min_area = 500

# Iterate over each contour
for contour in reversed(contours):
    
    x, y, w, h = cv2.boundingRect(contour)
    cx = x + w // 2
    cy = y + h // 2
    
    col = (cx - 50) // 100
    row = (cy - 50) // 100

    # Check if the area of the contour is above the minimum area
    if cv2.contourArea(contour) >= min_area:

        # Store the row and column indices in the correct_answers list
        correct_answers.append({
            'row': row,
            'col': col
        })
    else: 
        correct_answers.append({
            'row': row,
            'col': 0, 
        }) 
        

# Create a DataFrame from the correct_answers list
df = pd.DataFrame(correct_answers)
df.index = df.index + 1

# Define a custom function to compute the value of the new column
def find_the_answer(row):
    if 1 <= row['col'] <= 3:
        return 1
    elif 5 <= row['col'] <= 7:
        return 2
    elif 9 <= row['col'] <= 11:
        return 3
    elif 13 <= row['col'] <= 16:
        return 4
    else:
        return row['col']

df['correct'] = df.apply(find_the_answer, axis=1)

# Save the DataFrame to a CSV file
df.to_csv(path_to_key_csv, index=True, index_label='question')

# Print a message to indicate that the data has been saved
print('The Key has been saved to the "key.csv" file.')



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